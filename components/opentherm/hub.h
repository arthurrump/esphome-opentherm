#pragma once

#include "esphome/core/component.h"
#include "esphome/core/log.h"

#include "OpenTherm.h"

#if defined(OPENTHERM_USE_INPUT_SENSOR) || defined(OPENTHERM_USE_SENSOR)
#include "esphome/components/sensor/sensor.h"
#endif //OPENTHERM_USE_INUPT_SENSOR || OPENTHERM_USE_SENSOR

#ifdef OPENTHERM_USE_BINARY_SENSOR
#include "esphome/components/binary_sensor/binary_sensor.h"
#endif //OPENTHERM_USE_BINARY_SENSOR

#ifdef OPENTHERM_USE_SWITCH
#include "switch.h"
#endif //OPENTHERM_USE_SWITCH

#ifdef OPENTHERM_USE_NUMBER
#include "number.h"
#endif //OPENTHERM_USE_NUMBER

#ifdef OPENTHERM_USE_OUTPUT
#include "output.h"
#endif //OPENTHERM_USE_OUTPUT

#include <unordered_map>
#include <unordered_set>

namespace esphome {
namespace opentherm {

// OpenTherm component for ESPHome
class OpenthermHub : public Component {
protected:
    // Communication pins for the OpenTherm interface
    int in_pin, out_pin;
    // The OpenTherm interface from @ihormelnyk's library
    OpenTherm* ot;

    #define OPENTHERM_DECLARE_SENSOR(s) sensor::Sensor* s ## _sensor;
    #ifndef OPENTHERM_SENSOR_LIST
    #define OPENTHERM_SENSOR_LIST(F, sep)
    #endif
    OPENTHERM_SENSOR_LIST(OPENTHERM_DECLARE_SENSOR, )

    #define OPENTHERM_DECLARE_BINARY_SENSOR(s) binary_sensor::BinarySensor* s ## _binary_sensor;
    #ifndef OPENTHERM_BINARY_SENSOR_LIST
    #define OPENTHERM_BINARY_SENSOR_LIST(F, sep)
    #endif
    OPENTHERM_BINARY_SENSOR_LIST(OPENTHERM_DECLARE_BINARY_SENSOR, )

    #define OPENTHERM_DECLARE_SWITCH(s) switch_::Switch* s ## _switch;
    #ifndef OPENTHERM_SWITCH_LIST
    #define OPENTHERM_SWITCH_LIST(F, sep)
    #endif
    OPENTHERM_SWITCH_LIST(OPENTHERM_DECLARE_SWITCH, )

    #define OPENTHERM_DECLARE_INPUT_SENSOR(s) sensor::Sensor* s ## _input_sensor;
    #ifndef OPENTHERM_INPUT_SENSOR_LIST
    #define OPENTHERM_INPUT_SENSOR_LIST(F, sep)
    #endif
    OPENTHERM_INPUT_SENSOR_LIST(OPENTHERM_DECLARE_INPUT_SENSOR, )

    #define OPENTHERM_DECLARE_OUTPUT(s) OpenthermOutput* s ## _output;
    #ifndef OPENTHERM_OUTPUT_LIST
    #define OPENTHERM_OUTPUT_LIST(F, sep)
    #endif
    OPENTHERM_OUTPUT_LIST(OPENTHERM_DECLARE_OUTPUT, )

    #define OPENTHERM_DECLARE_NUMBER(s) number::Number* s ## _number;
    #ifndef OPENTHERM_NUMBER_LIST
    #define OPENTHERM_NUMBER_LIST(F, sep)
    #endif
    OPENTHERM_NUMBER_LIST(OPENTHERM_DECLARE_NUMBER, )

    // The set of initial requests to make on starting communication with the boiler
    std::unordered_set<byte> initial_requests;
    // and the repeating requests which are made repeatedly to update various sensors
    std::unordered_set<byte> repeating_requests;
    // Indicates if we are still working on the initial requests or not
    bool initializing = true;
    // Index for the current request in one of the _requests sets.
    std::unordered_set<byte>::const_iterator current_request_iterator;

    // This method returns the current setpoint, or 0.0 is no setpoint is set
    // If more than one input is configured, the first one takes precedence
    float get_t_set_input(byte request_id);

    // void set_output_max_setpoint(float max_setpoint);

    // Create OpenTherm messages based on the message id
    unsigned int build_request(byte request_id);

    // Callbacks to pass to OpenTherm interface for globally defined interrupts
    void(*handle_interrupt_callback)();
	void(*process_response_callback)(unsigned long, OpenThermResponseStatus);

public:
    // Constructor with references to the global interrupt handlers
    OpenthermHub(void(*handle_interrupt_callback)(void), void(*process_response_callback)(unsigned long, OpenThermResponseStatus));

    // Interrupt handler, which notifies the OpenTherm interface of an interrupt
    void IRAM_ATTR handle_interrupt();

    // Handle responses from the OpenTherm interface
    void process_response(unsigned long response, OpenThermResponseStatus status);

    // Setters for the input and output OpenTherm interface pins
    void set_in_pin(int in_pin) { this->in_pin = in_pin; }
    void set_out_pin(int out_pin) { this->out_pin = out_pin; }

    #define OPENTHERM_SET_SENSOR(s) void set_ ## s ## _sensor(sensor::Sensor* sensor) { this->s ## _sensor = sensor; }
    OPENTHERM_SENSOR_LIST(OPENTHERM_SET_SENSOR, )

    #define OPENTHERM_SET_BINARY_SENSOR(s) void set_ ## s ## _binary_sensor(binary_sensor::BinarySensor* binary_sensor) { this->s ## _binary_sensor = binary_sensor; }
    OPENTHERM_BINARY_SENSOR_LIST(OPENTHERM_SET_BINARY_SENSOR, )

    #define OPENTHERM_SET_SWITCH(s) void set_ ## s ## _switch(switch_::Switch* sw) { this->s ## _switch = sw; }
    OPENTHERM_SWITCH_LIST(OPENTHERM_SET_SWITCH, )

    #define OPENTHERM_SET_INPUT_SENSOR(s) void set_ ## s ## _input_sensor(sensor::Sensor* sensor) { this->s ## _input_sensor = sensor; }
    OPENTHERM_INPUT_SENSOR_LIST(OPENTHERM_SET_INPUT_SENSOR, )

    #define OPENTHERM_SET_OUTPUT(s) void set_ ## s ## _output(OpenthermOutput* output) { this->s ## _output = output; }
    OPENTHERM_OUTPUT_LIST(OPENTHERM_SET_OUTPUT, )

    #define OPENTHERM_SET_NUMBER(s) void set_ ## s ## _number(number::Number* number) { this->s ## _number = number; }
    OPENTHERM_NUMBER_LIST(OPENTHERM_SET_NUMBER, )

    // Add a request to the set of initial requests
    void add_initial_request(byte request) { this->initial_requests.insert(request); }
    // Add a request to the set of repeating requests. Note that a large number of repeating
    // requests will slow down communication with the boiler. Each request may take up to 1 second,
    // so with all sensors enabled, it may take about half a minute before a change in setpoint
    // will be processed.
    void add_repeating_request(byte request) { this->repeating_requests.insert(request); }

    // There are five status variables, which can either be set as a simple variable,
    // or using a switch. ch_enable and dhw_enable default to true, the others to false.
    bool ch_enable = true, dhw_enable = true, cooling_enable, otc_active, ch2_active;

    // Setters for the status variables
    void set_ch_enable(bool ch_enable) { this->ch_enable = ch_enable; }
    void set_dhw_enable(bool dhw_enable) { this->dhw_enable = dhw_enable; }
    void set_cooling_enable(bool cooling_enable) { this->cooling_enable = cooling_enable; }
    void set_otc_active(bool otc_active) { this->otc_active = otc_active; }
    void set_ch2_active(bool ch2_active) { this->ch2_active = ch2_active; }
    
    float get_setup_priority() const override{
        return setup_priority::HARDWARE;
    }

    void setup() override;
    void on_shutdown() override;
    void loop() override;
    void dump_config() override;
};

} // namespace opentherm
} // namespace esphome
