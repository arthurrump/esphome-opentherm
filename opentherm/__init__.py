import esphome.codegen as cg
import esphome.cpp_generator as cpp
import esphome.config_validation as cv
from esphome.const import CONF_ID

AUTO_LOAD = [ 'binary_sensor', 'sensor', 'switch', 'number', 'output' ]
MULTI_CONF = True

CONF_HUB_ID = "opentherm"
CONF_OPENTHERM_ID = "opentherm_id"

opentherm_ns = cg.esphome_ns.namespace("esphome::opentherm")
OpenthermHub = opentherm_ns.class_("OpenthermHub", cg.Component)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(OpenthermHub)
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    id = str(config[CONF_ID])
    var = cg.new_Pvariable(config[CONF_ID], cpp.RawExpression(id + "_handle_interrupt"), cpp.RawExpression(id + "_process_response"))
    cg.add_global(cpp.RawStatement("void IRAM_ATTR " + id + "_handle_interrupt() { " + id + "->handle_interrupt(); }"))
    cg.add_global(cpp.RawStatement("void " + id + "_process_response(unsigned long response, OpenThermResponseStatus status) { " + id + "->process_response(response, status); }"))
    await cg.register_component(var, config)

    cg.add_library("ihormelnyk/OpenTherm Library", "1.1.3")
