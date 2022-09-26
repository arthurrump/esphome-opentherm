import esphome.codegen as cg
import esphome.cpp_generator as cpp
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID

AUTO_LOAD = [ 'binary_sensor', 'sensor', 'switch', 'number', 'output' ]
MULTI_CONF = True

CONF_INPUT_t_set = "t_set"
CONF_INPUT_t_set_ch2 = "t_set_ch2"

input_keys = [
    CONF_INPUT_t_set,
    CONF_INPUT_t_set_ch2,
]

def is_input_key(key):
    return key in input_keys

def input_required_messages(input_keys):
    messages = set()
    if CONF_INPUT_t_set in input_keys:
        messages.add((True, "TSet"))
    if CONF_INPUT_t_set_ch2 in input_keys:
        messages.add((True, "TsetCH2"))
    return messages

def cv_inputs_schema(get_validator):
    schema = {}
    for key in input_keys:
        schema[cv.Optional(key)] = get_validator(key)
    return cv.Schema(schema)

def cg_write_read_input_defines(keys, sensor_type):
    for key in keys:
        cg.add_define("OPENTHERM_READ_INPUT_" + key, cg.RawExpression(f"this->{key}_{sensor_type}->state"))

CONF_OPENTHERM_ID = "opentherm_id"

opentherm_ns = cg.esphome_ns.namespace("esphome::opentherm")
OpenthermHub = opentherm_ns.class_("OpenthermHub", cg.Component)

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
    }).extend(cv_inputs_schema(lambda _: cv.use_id(sensor.Sensor)))
      .extend(cv.COMPONENT_SCHEMA),
    cv.only_with_arduino,
)

def cg_write_component_defines(component, keys):
    cg.add_define(
        f"OPENTHERM_{component}_LIST(F, sep)", 
        cg.RawExpression(" sep ".join(map(lambda key: f"F({key})", keys)))
    )
    for key in keys:
        cg.add_define(f"OPENTHERM_HAS_{component}_{key}")

def cg_write_required_messages(hub, messages):
    for (repeat, message) in messages:
        add = "add_repeating_request" if repeat else "add_initial_request"
        cg.add(getattr(hub, add)(cg.RawExpression(f"OpenThermMessageID::{message}")))

async def to_code(config):
    id = str(config[CONF_ID])
    var = cg.new_Pvariable(config[CONF_ID], cpp.RawExpression(id + "_handle_interrupt"), cpp.RawExpression(id + "_process_response"))
    cg.add_global(cpp.RawStatement("void IRAM_ATTR " + id + "_handle_interrupt() { " + id + "->handle_interrupt(); }"))
    cg.add_global(cpp.RawStatement("void " + id + "_process_response(unsigned long response, OpenThermResponseStatus status) { " + id + "->process_response(response, status); }"))
    await cg.register_component(var, config)

    for key, value in config.items():
        if key != CONF_ID:
            if is_input_key(key):
                sensor = await cg.get_variable(value)
                cg.add(getattr(var, f"set_{key}_input_sensor")(sensor))
            else:
                cg.add(getattr(var, f"set_{key}")(value))

    input_sensors = list(filter(is_input_key, config.keys()))
    if len(input_sensors) > 0:
        cg_write_component_defines("INPUT_SENSOR", input_sensors)
        cg_write_required_messages(var, input_required_messages(input_sensors))
        cg_write_read_input_defines(input_sensors, "input_sensor")

    cg.add_library("ihormelnyk/OpenTherm Library", "1.1.3")
