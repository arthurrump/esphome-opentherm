import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID

from . import schema, validate
from . import CONF_OPENTHERM_ID, OpenthermHub, cg_write_component_defines, cg_write_required_messages

DEPENDENCIES = [ "opentherm" ]

def get_entity_validation_schema(entity: schema.SensorSchema) -> cv.Schema:
    return sensor.sensor_schema(
        unit_of_measurement = entity["unit_of_measurement"] if "unit_of_measurement" in entity else sensor._UNDEF,
        accuracy_decimals = entity["accuracy_decimals"],
        device_class=entity["device_class"] if "device_class" in entity else sensor._UNDEF,
        icon = entity["icon"] if "icon" in entity else sensor._UNDEF,
        state_class = entity["state_class"]
    )

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.SENSORS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

def required_messages(sensor_keys):
    messages = set()
    for key in sensor_keys:
        match key:
            case "rel_mod_level":
                messages.add((True, "RelModLevel"))
            case "ch_pressure":
                messages.add((True, "CHPressure"))
            case "dhw_flow_rate":
                messages.add((True, "DHWFlowRate"))
            case "t_boiler":
                messages.add((True, "Tboiler"))
            case "t_dhw":
                messages.add((True, "Tdhw"))
            case "t_outside":
                messages.add((True, "Toutside"))
            case "t_ret":
                messages.add((True, "Tret"))
            case "t_storage":
                messages.add((True, "Tstorage"))
            case "t_collector":
                messages.add((True, "Tcollector"))
            case "t_flow_ch2":
                messages.add((True, "TflowCH2"))
            case "t_dhw2":
                messages.add((True, "Tdhw2"))
            case "t_exhaust":
                messages.add((True, "Texhaust"))
            case "burner_starts":
                messages.add((True, "BurnerStarts"))
            case "ch_pump_starts":
                messages.add((True, "CHPumpStarts"))
            case "dhw_pump_valve_starts":
                messages.add((True, "DHWPumpValveStarts"))
            case "dhw_burner_starts":
                messages.add((True, "DHWBurnerStarts"))
            case "burner_operation_hours":
                messages.add((True, "BurnerOperationHours"))
            case "ch_pump_operation_hours":
                messages.add((True, "CHPumpOperationHours"))
            case "dhw_pump_valve_operation_hours":
                messages.add((True, "DHWPumpValveOperationHours"))
            case "dhw_burner_operation_hours":
                messages.add((True, "DHWBurnerOperationHours"))
            case "t_dhw_set_ub" |"t_dhw_set_lb":
                messages.add((False, "TdhwSetUBTdhwSetLB"))
            case "max_t_set_ub" | "max_t_set_lb":
                messages.add((False, "MaxTSetUBMaxTSetLB"))
            case "t_dhw_set":
                messages.add((True, "TdhwSet"))
            case "max_t_set":
                messages.add((True, "MaxTSet"))
    return messages

async def to_code(config):
    cg.add_define("OPENTHERM_USE_SENSOR")
    
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    sensor_keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == sensor.Sensor:
            sens = await sensor.new_sensor(conf)
            cg.add(getattr(hub, f"set_{key}_sensor")(sens))
            sensor_keys.append(key)

    cg_write_required_messages(hub, required_messages(sensor_keys))    
    cg_write_component_defines("SENSOR", sensor_keys)
