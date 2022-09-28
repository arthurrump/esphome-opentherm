import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

from . import schema, validate
from . import CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

OpenthermSwitch = opentherm_ns.class_("OpenthermSwitch", switch.Switch, cg.Component)

async def new_ot_switch(config, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    return var

CONF_MODE = "mode"

def get_entity_validation_schema(entity: schema.SwitchSchema) -> cv.Schema:
    return switch.SWITCH_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(OpenthermSwitch),
        cv.Optional(CONF_MODE, entity["default_mode"]): 
            cv.enum({
                "restore_default_on": cg.RawExpression("opentherm::OpenthermSwitchMode::OPENTHERM_SWITCH_RESTORE_DEFAULT_ON"), 
                "restore_default_off": cg.RawExpression("opentherm::OpenthermSwitchMode::OPENTHERM_SWITCH_RESTORE_DEFAULT_OFF"),
                "start_on": cg.RawExpression("opentherm::OpenthermSwitchMode::OPENTHERM_SWITCH_START_ON"),
                "start_off": cg.RawExpression("opentherm::OpenthermSwitchMode::OPENTHERM_SWITCH_START_OFF")
            })
    }).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.OPENTHERM_SWITCHES, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

def required_messages(keys):
    messages = set()
    for key in keys:
        match key:
            case "ch_enable" | "dhw_enable" | "cooling_enable" | "otc_active" | "ch2_active":
                messages.add((True, "Status"))
    return messages

async def to_code(config):
    cg.add_define("OPENTHERM_USE_SWITCH")

    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == OpenthermSwitch:
            sw = await new_ot_switch(conf, cg.RawExpression(f"&{config[CONF_OPENTHERM_ID]}->{key}"))
            cg.add(getattr(sw, "set_mode")(conf[CONF_MODE]))
            cg.add(getattr(hub, f"set_{key}_switch")(sw))
            keys.append(key)

    cg_write_required_messages(hub, required_messages(keys))    
    cg_write_component_defines("SWITCH", keys)
