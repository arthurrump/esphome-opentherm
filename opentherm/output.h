#pragma once

#include "esphome/components/output/float_output.h"

namespace esphome {
namespace opentherm {

// FloatOutput component for TSet and TSetCH2 setpoint temperatures. By default
// this ranges from temperature 0-100 degrees Celsius (the control setpoint
// range supported in the OpenTherm protocol) for inputs 0.0-1.0, but this can
// be changed by setting min_power and max_power to the desired minimum and
// maximum temperatures.
class SetpointOutput : public output::FloatOutput, public Component {
protected:
    bool has_state_ = false;

public:
    float state;
    bool auto_max_power = false;

    void write_state(float state) override { 
        this->state = state * 100;
        this->has_state_ = true;
    };

    bool has_state() { return this->has_state_; };
    float get_state() { return this->state; };

    // Use auto_max_power to automatically set the maximum power for this
    // component to the maximum allowable setpoint temperature reported by the
    // boiler.
    void set_auto_max_power(bool auto_max_power) { this->auto_max_power = auto_max_power; };
};

} // namespace opentherm
} // namespace esphome
