from typing import Any, Awaitable, Callable, Dict, List, Set, Tuple, TypeVar

import esphome.codegen as cg
from esphome.const import CONF_ID

from . import const, schema

opentherm_ns = cg.esphome_ns.namespace("esphome::opentherm")
OpenthermHub = opentherm_ns.class_("OpenthermHub", cg.Component)

def define_has_component(component_type: str, keys: List[str]) -> None:
    cg.add_define(
        f"OPENTHERM_{component_type.upper()}_LIST(F, sep)", 
        cg.RawExpression(" sep ".join(map(lambda key: f"F({key}_{component_type.lower()})", keys)))
    )
    for key in keys:
        cg.add_define(f"OPENTHERM_HAS_{component_type.upper()}_{key}")

TSchema = TypeVar("TSchema", bound=schema.EntitySchema)

def define_message_handler(component_type: str, keys: List[str], schema_: schema.Schema[TSchema]) -> None:
    
    # The macros defined here should be able to generate things like this:
    # // Parsing a message and publishing to sensors
    # case OpenthermMessageID::Message:
    #     // Can have multiple sensors here, for example for a Status message with multiple flags
    #     this->thing_binary_sensor->publish_state(parse_flag8_lb_0(response));
    #     this->other_binary_sensor->publish_state(parse_flag8_lb_1(response));
    #     break;
    # // Building a message for a write request
    # case OpenthermMessageID::Message: {
    #     unsigned int data = write_message_data(some_input_sensor->state); // Where input_sensor can also be a number/output/switch
    #     return ot->buildRequest(OpenthermMessageType::WriteData, OpenthermMessageID::Message, data);
    # }

    # There doesn't seem to be a way to combine the handlers for different components, so we'll
    # have to call them seperately in C++.

    messages: Dict[str, List[Tuple[str, str]]] = {}
    for key in keys:
        msg = schema_[key]["message"]
        if msg != "Status": # Status is special, and will be handled separately
            if msg not in messages:
                messages[msg] = []
            messages[msg].append((key, schema_[key]["message_data"]))

    cg.add_define(
        f"OPENTHERM_{component_type.upper()}_MESSAGE_HANDLERS(MESSAGE, ENTITY, entity_sep, postscript, msg_sep)",
        " msg_sep ".join([ 
            f"MESSAGE({msg}) "
            + " entity_sep ".join([ f"ENTITY({key}_{component_type.lower()}, {msg_data})" for key, msg_data in keys ])
            + " postscript"
            for msg, keys in messages.items()
        ])
    )

def add_messages(hub: cg.MockObj, keys: List[str], schema_: schema.Schema[TSchema]):
    messages: Set[Tuple[str, bool]] = set()
    for key in keys:
        messages.add((schema_[key]["message"], schema_[key]["keep_updated"]))
    for msg, keep_updated in messages:
        msg_expr = cg.RawExpression(f"OpenThermMessageID::{msg}")
        if keep_updated:
            cg.add(hub.add_repeating_message(msg_expr))
        else:
            cg.add(hub.add_initial_message(msg_expr))

Create = Callable[[Dict[str, Any], str, cg.MockObj], Awaitable[cg.Pvariable]]

def create_only_conf(create: Callable[[Dict[str, Any]], Awaitable[cg.Pvariable]]) -> Create:
    return lambda conf, _key, _hub: create(conf)

async def component_to_code(component_type: str, schema_: schema.Schema[TSchema], type: cg.MockObjClass, create: Create, config: Dict[str, Any]) -> None:
    cg.add_define(f"OPENTHERM_USE_{component_type.upper()}")

    hub = await cg.get_variable(config[const.CONF_OPENTHERM_ID])

    keys: List[str] = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == type:
            entity = await create(conf, key, hub)
            cg.add(getattr(hub, f"set_{key}_{component_type.lower()}")(entity))
            keys.append(key)

    define_has_component(component_type, keys)
    define_message_handler(component_type, keys, schema_)
    add_messages(hub, keys, schema_)
