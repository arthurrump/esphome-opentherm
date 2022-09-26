import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import (
    CONF_ID,
    DEVICE_CLASS_COLD,
    DEVICE_CLASS_HEAT,
    DEVICE_CLASS_PROBLEM
)
from . import CONF_OPENTHERM_ID, OpenthermHub

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

async def to_code(config):
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == binary_sensor.BinarySensor:
            sens = await binary_sensor.new_binary_sensor(conf)
            cg.add(getattr(hub, "register_binary_sensor")(cg.RawExpression(f"opentherm::OpenthermBinarySensorType::{key}"), sens))
