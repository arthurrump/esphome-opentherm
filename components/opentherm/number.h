#pragma once

#include "esphome/components/number/number.h"
#include "input.h"

namespace esphome {
namespace opentherm {

// Just a simple number, which stores the number
class OpenthermNumber : public number::Number, public Component, public OpenthermInput {
protected:
    void control(float value) override {
        this->publish_state(value);
    }

public:
    void set_min_value(float min_value) override { this->traits.set_min_value(min_value); }
    void set_max_value(float max_value) override { this->traits.set_max_value(max_value); }
};

} // namespace opentherm
} // namespace esphome
