#pragma once

#include "esphome/components/output/float_output.h"

namespace esphome {
namespace opentherm {

// Output component for the relative setpoint
class RelativeSetpoint : public output::FloatOutput, public Component {
protected:
    bool has_state_ = false;

public:
    float state;

    void write_state(float state) override { 
        this->state = state;
        this->has_state_ = true;
    };

    bool has_state() { return this->has_state_; };
    float get_state() { return this->state; };
};

} // namespace opentherm
} // namespace esphome
