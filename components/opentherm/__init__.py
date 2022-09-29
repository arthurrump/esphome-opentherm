import esphome.codegen as cg
import esphome.cpp_generator as cpp
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID

from . import schema, validate, generate

MULTI_CONF = True

CONF_OPENTHERM_ID = "opentherm_id"

opentherm_ns = cg.esphome_ns.namespace("esphome::opentherm")
OpenthermHub = opentherm_ns.class_("OpenthermHub", cg.Component)

INPUT_SENSOR = "input_sensor"

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(OpenthermHub),
        cv.Optional("in_pin", 4): cv.int_,
        cv.Optional("out_pin", 5): cv.int_,
        cv.Optional("ch_enable", True): cv.boolean,
        cv.Optional("dhw_enable", True): cv.boolean,
        cv.Optional("cooling_enable", False): cv.boolean,
        cv.Optional("otc_active", False): cv.boolean,
        cv.Optional("ch2_active", False): cv.boolean,
    }).extend(validate.create_validation_schema(schema.INPUTS, (lambda _: cv.use_id(sensor.Sensor))))
      .extend(cv.COMPONENT_SCHEMA),
    cv.only_with_arduino,
)

async def to_code(config):
    id = str(config[CONF_ID])
    # Define two global callbacks to process responses on interrupt
    cg.add_global(cpp.RawStatement("void IRAM_ATTR " + id + "_handle_interrupt() { " + id + "->handle_interrupt(); }"))
    cg.add_global(cpp.RawStatement("void " + id + "_process_response(unsigned long response, OpenThermResponseStatus status) { " + id + "->process_response(response, status); }"))
    # Create the hub, passing the two callbacks
    var = cg.new_Pvariable(config[CONF_ID], cpp.RawExpression(id + "_handle_interrupt"), cpp.RawExpression(id + "_process_response"))
    await cg.register_component(var, config)

    input_sensors = []
    for key, value in config.items():
        if key != CONF_ID:
            if key in schema.INPUTS:
                sensor = await cg.get_variable(value)
                cg.add(getattr(var, f"set_{key}_input_sensor")(sensor))
                input_sensors.append(key)
            else:
                cg.add(getattr(var, f"set_{key}")(value))

    if len(input_sensors) > 0:
        generate.define_has_component(INPUT_SENSOR, input_sensors)
        generate.define_message_handler(INPUT_SENSOR, input_sensors, schema.INPUTS)
        generate.add_messages(var, input_sensors, schema.INPUTS)

    cg.add_library("ihormelnyk/OpenTherm Library", "1.1.3")
