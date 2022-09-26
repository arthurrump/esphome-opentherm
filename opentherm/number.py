import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID

from . import cv_inputs_schema, input_required_messages
from . import CONF_OPENTHERM_ID, OpenthermHub, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub),
}).extend(cv_inputs_schema(lambda _: number.NUMBER_SCHEMA)).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == number.Number:
            so = await number.new_number(conf, min_value = 0, max_value = 100)
            cg.add(getattr(hub, f"set_{key}_number")(so))
            keys.append(key)

    cg_write_required_messages(hub, input_required_messages(keys))    
    cg_write_component_defines("NUMBER", keys)
