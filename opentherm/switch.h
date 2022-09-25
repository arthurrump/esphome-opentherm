#pragma once

#include "esphome/core/component.h"
#include "esphome/components/switch/switch.h"

namespace esphome {
namespace opentherm {

enum class OpenthermSwitchType {
    ch_enable,
    dhw_enable,
    cooling_enable,
    otc_active,
    ch2_active,
};

class OpenthermSwitch : public switch_::Switch, public Component {
public:
    OpenthermSwitchType type;
    OpenthermSwitch(OpenthermSwitchType type) : type(type) {}
};

} // namespace opentherm
} // namespace esphome
