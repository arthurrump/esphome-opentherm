import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_COLD,
    DEVICE_CLASS_HEAT,
    DEVICE_CLASS_PROBLEM
)
from . import CONF_OPENTHERM_ID, OpenthermHub, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ 'opentherm' ]

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub),
    cv.Optional("fault_indication"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM
    ),
    cv.Optional("ch_active"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_HEAT,
        icon="mdi:radiator"
    ),
    cv.Optional("dhw_active"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_HEAT,
        icon="mdi:faucet"
    ),
    cv.Optional("flame_on"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_HEAT
    ),
    cv.Optional("cooling_active"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_COLD
    ),
    cv.Optional("ch2_active"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_HEAT,
        icon="mdi:radiator"
    ),
    cv.Optional("diagnostic_indication"): binary_sensor.binary_sensor_schema(
        device_class=DEVICE_CLASS_PROBLEM
    ),
    cv.Optional("dhw_present"): binary_sensor.binary_sensor_schema(),
    cv.Optional("control_type_on_off"): binary_sensor.binary_sensor_schema(),
    cv.Optional("cooling_supported"): binary_sensor.binary_sensor_schema(),
    cv.Optional("dhw_storage_tank"): binary_sensor.binary_sensor_schema(),
    cv.Optional("master_pump_control_allowed"): binary_sensor.binary_sensor_schema(),
    cv.Optional("ch2_present"): binary_sensor.binary_sensor_schema(),
    cv.Optional("dhw_setpoint_transfer_enabled"): binary_sensor.binary_sensor_schema(),
    cv.Optional("max_ch_setpoint_transfer_enabled"): binary_sensor.binary_sensor_schema(),
    cv.Optional("dhw_setpoint_rw"): binary_sensor.binary_sensor_schema(),
    cv.Optional("max_ch_setpoint_rw"): binary_sensor.binary_sensor_schema(),
}).extend(cv.COMPONENT_SCHEMA)

def required_messages(sensor_keys):
    messages = set()
    for key in sensor_keys:
        match key:
            case "fault_indication" | "ch_active" | "dhw_active" | "flame_on" | "cooling_active" | "ch2_active" | "diagnostic_indication":
                messages.add((True, "Status"))
            case "dhw_present" | "control_type_on_off" | "cooling_supported" | "dhw_storage_tank" | "master_pump_control_allowed" | "ch2_present":
                messages.add((False, "SConfigSMemberIDcode"))
            case "dhw_setpoint_transfer_enabled" | "max_ch_setpoint_transfer_enabled" | "dhw_setpoint_rw" | "max_ch_setpoint_rw":
                messages.add((False, "RBPflags"))
    return messages

async def to_code(config):
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    sensor_keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == binary_sensor.BinarySensor:
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(getattr(hub, f"set_{key}_binary_sensor")(sens))
            sensor_keys.append(key)

    cg_write_required_messages(hub, required_messages(sensor_keys))
    cg_write_component_defines("BINARY_SENSOR", sensor_keys)
