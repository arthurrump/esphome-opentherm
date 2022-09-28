import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_ID

from . import schema, validate, input
from . import cg_write_read_input_defines
from . import CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

OpenthermOutput = opentherm_ns.class_("OpenthermOutput", output.FloatOutput, cg.Component, input.OpenthermInput)

async def new_setpointoutput(config, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await cg.register_component(var, config)
    await output.register_output(var, config)
    return var

def get_entity_validation_schema(entity: schema.InputSchema) -> cv.Schema:
    return output.FLOAT_OUTPUT_SCHEMA \
        .extend({ cv.GenerateID(): cv.declare_id(OpenthermOutput) }) \
        .extend(input.input_schema(entity)) \
        .extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.OPENTHERM_INPUTS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    cg.add_define("OPENTHERM_USE_OUTPUT")

    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == OpenthermOutput:
            so = await new_setpointoutput(conf)
            cg.add(getattr(so, "set_id")(cg.RawExpression(f'"{id}"')))
            # if CONF_auto_max_value in conf:
            #     cg.add(getattr(so, "set_auto_max_power")(conf[CONF_auto_max_value]))
            cg.add(getattr(hub, f"set_{key}_output")(so))
            keys.append(key)

    # cg_write_required_messages(hub, input_required_messages(keys))    
    cg_write_component_defines("OUTPUT", keys)
    cg_write_read_input_defines(keys, "output")
