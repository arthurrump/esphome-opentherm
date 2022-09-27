import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_UNIT_OF_MEASUREMENT
from components.opentherm.input import input_schema

from components.opentherm.schema import OPENTHERM_INPUTS, InputSchema
from components.opentherm.validate import create_validation_schema

from . import cg_write_read_input_defines, cv_inputs_schema, input_required_messages
from . import CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

OpenthermNumber = opentherm_ns.class_("OpenthermNumber", number.Number, cg.Component)

async def new_openthermnumber(config, *args, min_value, max_value, step = None):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await cg.register_component(var, config)
    await number.register_number(var, config, min_value = min_value, max_value = max_value, step = step)
    return var

def get_entity_validation_schema(entity: InputSchema) -> cv.Schema:
    return number.NUMBER_SCHEMA \
        .extend({
            cv.GenerateID(): cv.declare_id(OpenthermNumber),
            cv.Optional(CONF_UNIT_OF_MEASUREMENT, entity["unit_of_measurement"]): cv.string_strict
        }) \
        .extend(input_schema(entity)) \
        .extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(create_validation_schema(OPENTHERM_INPUTS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == number.Number:
            so = await new_openthermnumber(conf, min_value=0, max_value=100)
            cg.add(getattr(hub, f"set_{key}_number")(so))
            keys.append(key)

    cg_write_required_messages(hub, input_required_messages(keys))    
    cg_write_component_defines("NUMBER", keys)
    cg_write_read_input_defines(keys, "number")
