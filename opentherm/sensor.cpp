#include "sensor.h"

namespace esphome {
namespace opentherm {

static const char *TAG = "opentherm.sensor";

std::string OpenthermSensor::unit_of_measurement() {
    switch (this->type) {
        case OpenthermSensorType::rel_mod_level:
            return "%";
        case OpenthermSensorType::ch_pressure:
            return "bar";
        case OpenthermSensorType::dhw_flow_rate:
            return "l/min";
        case OpenthermSensorType::t_boiler:
        case OpenthermSensorType::t_dhw:
        case OpenthermSensorType::t_outside:
        case OpenthermSensorType::t_ret:
        case OpenthermSensorType::t_storage:
        case OpenthermSensorType::t_collector:
        case OpenthermSensorType::t_flow_ch2:
        case OpenthermSensorType::t_dhw2:
        case OpenthermSensorType::t_exhaust:
            return "°C";
        case OpenthermSensorType::burner_starts:
        case OpenthermSensorType::ch_pump_starts:
        case OpenthermSensorType::dhw_pump_valve_starts:
        case OpenthermSensorType::dhw_burner_starts:
        case OpenthermSensorType::burner_operation_hours:
        case OpenthermSensorType::ch_pump_operation_hours:
        case OpenthermSensorType::dhw_pump_valve_operation_hours:
        case OpenthermSensorType::dhw_burner_operation_hours:
            return "";
        case OpenthermSensorType::t_dhw_set_ub:
        case OpenthermSensorType::t_dhw_set_lb:
        case OpenthermSensorType::max_t_set_ub:
        case OpenthermSensorType::max_t_set_lb:
        case OpenthermSensorType::t_dhw_set:
        case OpenthermSensorType::max_t_set:
            return "°C";
    }
    return "";
}

int8_t OpenthermSensor::accuracy_decimals() {
    switch (this->type) {
        case OpenthermSensorType::rel_mod_level:
        case OpenthermSensorType::ch_pressure:
        case OpenthermSensorType::dhw_flow_rate:
        case OpenthermSensorType::t_boiler:
        case OpenthermSensorType::t_dhw:
        case OpenthermSensorType::t_outside:
        case OpenthermSensorType::t_ret:
        case OpenthermSensorType::t_storage:
            return 2;
        case OpenthermSensorType::t_collector:
            return 0;
        case OpenthermSensorType::t_flow_ch2:
        case OpenthermSensorType::t_dhw2:
            return 2;
        case OpenthermSensorType::t_exhaust:
            return 0;
        case OpenthermSensorType::burner_starts:
        case OpenthermSensorType::ch_pump_starts:
        case OpenthermSensorType::dhw_pump_valve_starts:
        case OpenthermSensorType::dhw_burner_starts:
        case OpenthermSensorType::burner_operation_hours:
        case OpenthermSensorType::ch_pump_operation_hours:
        case OpenthermSensorType::dhw_pump_valve_operation_hours:
        case OpenthermSensorType::dhw_burner_operation_hours:
            return 0;
        case OpenthermSensorType::t_dhw_set_ub:
        case OpenthermSensorType::t_dhw_set_lb:
        case OpenthermSensorType::max_t_set_ub:
        case OpenthermSensorType::max_t_set_lb:
            return 0;
        case OpenthermSensorType::t_dhw_set:
        case OpenthermSensorType::max_t_set:
            return 2;
    }
    return 2;
}

std::string OpenthermSensor::device_class() {
    switch (this->type) {
        case OpenthermSensorType::rel_mod_level:
            return "";
        case OpenthermSensorType::ch_pressure:
            return "pressure";
        case OpenthermSensorType::dhw_flow_rate:
            return "";
        case OpenthermSensorType::t_boiler:
        case OpenthermSensorType::t_dhw:
        case OpenthermSensorType::t_outside:
        case OpenthermSensorType::t_ret:
        case OpenthermSensorType::t_storage:
        case OpenthermSensorType::t_collector:
        case OpenthermSensorType::t_flow_ch2:
        case OpenthermSensorType::t_dhw2:
        case OpenthermSensorType::t_exhaust:
            return "temperature";
        case OpenthermSensorType::burner_starts:
        case OpenthermSensorType::ch_pump_starts:
        case OpenthermSensorType::dhw_pump_valve_starts:
        case OpenthermSensorType::dhw_burner_starts:
        case OpenthermSensorType::burner_operation_hours:
        case OpenthermSensorType::ch_pump_operation_hours:
        case OpenthermSensorType::dhw_pump_valve_operation_hours:
        case OpenthermSensorType::dhw_burner_operation_hours:
            return "";
        case OpenthermSensorType::t_dhw_set_ub:
        case OpenthermSensorType::t_dhw_set_lb:
        case OpenthermSensorType::max_t_set_ub:
        case OpenthermSensorType::max_t_set_lb:
        case OpenthermSensorType::t_dhw_set:
        case OpenthermSensorType::max_t_set:
            return "temperature";
    }
    return "";
}

sensor::StateClass OpenthermSensor::state_class() {
    switch (this->type) {
        case OpenthermSensorType::rel_mod_level:
        case OpenthermSensorType::ch_pressure:
        case OpenthermSensorType::dhw_flow_rate:
        case OpenthermSensorType::t_boiler:
        case OpenthermSensorType::t_dhw:
        case OpenthermSensorType::t_outside:
        case OpenthermSensorType::t_ret:
        case OpenthermSensorType::t_storage:
        case OpenthermSensorType::t_collector:
        case OpenthermSensorType::t_flow_ch2:
        case OpenthermSensorType::t_dhw2:
        case OpenthermSensorType::t_exhaust:
            return sensor::STATE_CLASS_MEASUREMENT;
        case OpenthermSensorType::burner_starts:
        case OpenthermSensorType::ch_pump_starts:
        case OpenthermSensorType::dhw_pump_valve_starts:
        case OpenthermSensorType::dhw_burner_starts:
        case OpenthermSensorType::burner_operation_hours:
        case OpenthermSensorType::ch_pump_operation_hours:
        case OpenthermSensorType::dhw_pump_valve_operation_hours:
        case OpenthermSensorType::dhw_burner_operation_hours:
            return sensor::STATE_CLASS_TOTAL_INCREASING;
        case OpenthermSensorType::t_dhw_set_ub:
        case OpenthermSensorType::t_dhw_set_lb:
        case OpenthermSensorType::max_t_set_ub:
        case OpenthermSensorType::max_t_set_lb:
        case OpenthermSensorType::t_dhw_set:
        case OpenthermSensorType::max_t_set:
            return sensor::STATE_CLASS_MEASUREMENT;
    }
    return sensor::STATE_CLASS_NONE;
}

}  // namespace opentherm
}  // namespace esphome
