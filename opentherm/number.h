#pragma once

#include "esphome/components/number/number.h"

namespace esphome {
namespace opentherm {

// Just a simple number, which stores the number
class OpenthermNumber : public number::Number, public Component {
protected:
    void control(float value) override {
        this->publish_state(value);
    }
};

} // namespace opentherm
} // namespace esphome
