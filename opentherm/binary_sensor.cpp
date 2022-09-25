#include "binary_sensor.h"

namespace esphome {
namespace opentherm {

static const char *TAG = "opentherm.binary_sensor";

std::string OpenthermBinarySensor::device_class() {
    switch (this->type) {
        case OpenthermBinarySensorType::fault_indication:
        case OpenthermBinarySensorType::diagnostic_indication:
            return "problem";
        case OpenthermBinarySensorType::ch_active:
        case OpenthermBinarySensorType::dhw_active:
        case OpenthermBinarySensorType::flame_on:
            return "heat";
        case OpenthermBinarySensorType::cooling_active:
            return "cold";
        case OpenthermBinarySensorType::ch2_active:
            return "heat";
        case OpenthermBinarySensorType::dhw_present:
        case OpenthermBinarySensorType::control_type_on_off:
        case OpenthermBinarySensorType::cooling_supported:
        case OpenthermBinarySensorType::dhw_storage_tank:
        case OpenthermBinarySensorType::master_pump_control_allowed:
        case OpenthermBinarySensorType::ch2_present:
        case OpenthermBinarySensorType::dhw_setpoint_transfer_enabled:
        case OpenthermBinarySensorType::max_ch_setpoint_transfer_enabled:
        case OpenthermBinarySensorType::dhw_setpoint_rw:
        case OpenthermBinarySensorType::max_ch_setpoint_rw:
            return "";
    }
    return "";
}

}  // namespace opentherm
}  // namespace esphome
