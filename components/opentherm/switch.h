#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"

namespace esphome {
namespace opentherm {

enum OpenthermSwitchMode {
    OPENTHERM_SWITCH_RESTORE_DEFAULT_ON,
    OPENTHERM_SWITCH_RESTORE_DEFAULT_OFF,
    OPENTHERM_SWITCH_START_ON,
    OPENTHERM_SWITCH_START_OFF
};

class OpenthermSwitch : public switch_::Switch, public Component {
protected:
    OpenthermSwitchMode mode;

    void write_state(bool state) override;

public:
    void set_mode(OpenthermSwitchMode mode) { this->mode = mode; }

    void setup() override;
};

} // namespace opentherm
} // namespace esphome
