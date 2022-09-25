#pragma once

#include "esphome/core/component.h"
#include "esphome/components/binary_sensor/binary_sensor.h"

namespace esphome {
namespace opentherm {

enum class OpenthermBinarySensorType {
    // Class 1: Control and status information
    // Message 0 (Status) slave status flags
    fault_indication,
    ch_active,
    dhw_active,
    flame_on,
    cooling_active,
    ch2_active,
    diagnostic_indication,

    // Class 2: Configuration information
    // Message 3 (SConfigSMemberIDcode) slave configuration flags
    dhw_present,
    control_type_on_off, // 0 = modulating, 1 = on/off
    cooling_supported,
    dhw_storage_tank, // 0 = instantaneous or not-specified, 1 = storage tank
    master_pump_control_allowed,
    ch2_present,

    // Class 5: Pre-defined remote boiler parameters
    // Message 6 (RBPflags) remote boiler parameter transfer-enable & read/write flags
    dhw_setpoint_transfer_enabled,
    max_ch_setpoint_transfer_enabled,
    dhw_setpoint_rw,
    max_ch_setpoint_rw,
};

class OpenthermBinarySensor : public binary_sensor::BinarySensor, public Component {
public:
    OpenthermBinarySensorType type;
    OpenthermBinarySensor(OpenthermBinarySensorType type) : type(type) {}

    std::string device_class() override;
};

} // namespace opentherm
} // namespace esphome