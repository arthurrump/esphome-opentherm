from typing import Any, Dict

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

from . import schema, validate, generate, CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns

DEPENDENCIES = [ "opentherm" ]
COMPONENT_TYPE = "switch"

OpenthermSwitch = opentherm_ns.class_("OpenthermSwitch", switch.Switch, cg.Component)

CONF_MODE = "mode"

async def new_openthermswitch(key: str, config: Dict[str, Any]) -> cg.Pvariable:
    var = cg.new_Pvariable(config[CONF_ID], cg.RawExpression(f"&{config[CONF_OPENTHERM_ID]}->{key}"))
    await cg.register_component(var, config)
    await switch.register_switch(var, config)
    cg.add(getattr(var, "set_mode")(config[CONF_MODE]))
    return var

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
        .extend(validate.create_validation_schema(schema.SWITCHES, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config: Dict[str, Any]) -> None:
    await generate.generic_to_code(
        COMPONENT_TYPE, 
        OpenthermSwitch, 
        new_openthermswitch, 
        config
    )
