import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_UNIT_OF_MEASUREMENT

from . import schema, validate, input
from . import cg_write_read_input_defines
from . import CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

OpenthermNumber = opentherm_ns.class_("OpenthermNumber", number.Number, cg.Component, input.OpenthermInput)

async def new_openthermnumber(config, *args, min_value, max_value, step = None):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await cg.register_component(var, config)
    await number.register_number(var, config, min_value = min_value, max_value = max_value, step = step)
    return var

def get_entity_validation_schema(entity: schema.InputSchema) -> cv.Schema:
    return number.NUMBER_SCHEMA \
        .extend({
            cv.GenerateID(): cv.declare_id(OpenthermNumber),
            cv.Optional(CONF_UNIT_OF_MEASUREMENT, entity["unit_of_measurement"]): cv.string_strict
        }) \
        .extend(input.input_schema(entity)) \
        .extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.INPUTS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    cg.add_define("OPENTHERM_USE_NUMBER")
    
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

    # cg_write_required_messages(hub, input_required_messages(keys))    
    cg_write_component_defines("NUMBER", keys)
    cg_write_read_input_defines(keys, "number")
