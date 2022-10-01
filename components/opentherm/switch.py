from typing import Any, Dict

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ID

from . import const, schema, validate, generate

DEPENDENCIES = [ const.OPENTHERM ]
COMPONENT_TYPE = const.SWITCH

OpenthermSwitch = generate.opentherm_ns.class_("OpenthermSwitch", switch.Switch, cg.Component)

CONF_MODE = "mode"

async def new_openthermswitch(config: Dict[str, Any]) -> cg.Pvariable:
    var = cg.new_Pvariable(config[CONF_ID])
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

CONFIG_SCHEMA = validate.create_component_schema(schema.SWITCHES, get_entity_validation_schema)

async def to_code(config: Dict[str, Any]) -> None:
    keys = await generate.component_to_code(
        COMPONENT_TYPE, 
        schema.SWITCHES,
        OpenthermSwitch, 
        generate.create_only_conf(new_openthermswitch), 
        config
    )
    generate.define_readers(COMPONENT_TYPE, keys)
