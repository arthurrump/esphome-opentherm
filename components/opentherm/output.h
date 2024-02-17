#pragma once

#include "esphome/components/output/float_output.h"
#include "input.h"

namespace esphome {
namespace opentherm {

class OpenthermOutput : public output::FloatOutput, public Component, public OpenthermInput {
protected:
    bool has_state_ = false;
    const char* id = nullptr;

    float min_value, max_value;

public:
    float state;

    void set_id(const char* id) { this->id = id; }

    void write_state(float state) override {
        this->state = state < 0.003 && this->zero_means_zero_ ? 0.0 : clamp(state * (max_value - min_value) + min_value, min_value, max_value);
        this->has_state_ = true;
        ESP_LOGD("opentherm.output", "Output set to %.2f", this->state);
    };

    bool has_state() { return this->has_state_; };

    void set_min_value(float min_value) override { this->min_value = min_value; }
    void set_max_value(float max_value) override { this->max_value = max_value; }

    float get_min_value() { return this->min_value; }
    float get_max_value() { return this->max_value; }
};

} // namespace opentherm
} // namespace esphome
