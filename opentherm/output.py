import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_ID

from . import cg_write_read_input_defines, cv_inputs_schema, input_required_messages
from . import CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

SetpointOutput = opentherm_ns.class_("SetpointOutput", output.FloatOutput, cg.Component)

async def new_setpointoutput(config, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await cg.register_component(var, config)
    await output.register_output(var, config)
    return var

CONF_auto_max_power = "auto_max_power"

def setpointoutput_schema():
    return output.FLOAT_OUTPUT_SCHEMA.extend({
        cv.GenerateID(): cv.declare_id(SetpointOutput),
        cv.Optional(CONF_auto_max_power): cv.boolean,
    }).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub),
}).extend(cv_inputs_schema(lambda _: setpointoutput_schema())).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == SetpointOutput:
            so = await new_setpointoutput(conf)
            if CONF_auto_max_power in conf:
                cg.add(getattr(so, "set_auto_max_power")(conf[CONF_auto_max_power]))
            cg.add(getattr(hub, f"set_{key}_output")(so))
            keys.append(key)

    cg_write_required_messages(hub, input_required_messages(keys))    
    cg_write_component_defines("OUTPUT", keys)
    cg_write_read_input_defines(keys, "output")
