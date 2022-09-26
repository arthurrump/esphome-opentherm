#include "hub.h"

namespace esphome {
namespace opentherm {

static const char *TAG = "opentherm";

int16_t get_s16(unsigned long response) {
    return (int16_t) (response & 0xffff);
}

int8_t get_high_s8(unsigned long response) {
    return (int8_t) (response & 0xff);
}

int8_t get_low_s8(unsigned long response) {
    return (int8_t) ((response >> 8) & 0xff);
}

void OpenthermHub::set_output_max_setpoint(float max_setpoint) {
#define OPENTHERM_SET_OUTPUT_MAX_SETPOINT(output) \
    if (this->output ## _output != nullptr && this->output ## _output->auto_max_power) { \
        output ## _output->set_max_power(max_setpoint / 100.); \
    }
    OPENTHERM_OUTPUT_LIST(OPENTHERM_SET_OUTPUT_MAX_SETPOINT, )
}

unsigned int OpenthermHub::build_request(byte request_id) {
    switch (request_id) {
        case OpenThermMessageID::Status:
            ESP_LOGD(TAG, "Building Status request");
            return ot->buildSetBoilerStatusRequest(this->ch_enable, this->dhw_enable, this->cooling_enable, this->otc_active, this->ch2_active);
        #ifdef OPENTHERM_READ_INPUT_t_set
        case OpenThermMessageID::TSet: {
            float target_temp = OPENTHERM_READ_INPUT_t_set;
            ESP_LOGD(TAG, "Building request to set target temperature at %.1f", target_temp);
            unsigned int data = ot->temperatureToData(target_temp);
            return ot->buildRequest(OpenThermMessageType::WRITE_DATA, (OpenThermMessageID)request_id, data);
        }
        #endif
        #ifdef OPENTHERM_READ_INPUT_t_set_ch2
        case OpenThermMessageID::TsetCH2: {
            float target_temp = OPENTHERM_READ_INPUT_t_set_ch2;
            ESP_LOGD(TAG, "Building request to set target temperature at %.1f", target_temp);
            unsigned int data = ot->temperatureToData(target_temp);
            return ot->buildRequest(OpenThermMessageType::WRITE_DATA, (OpenThermMessageID)request_id, data);
        }
        #endif
        case OpenThermMessageID::RelModLevel:
        case OpenThermMessageID::CHPressure:
        case OpenThermMessageID::DHWFlowRate:
        case OpenThermMessageID::Tboiler:
        case OpenThermMessageID::Tdhw:
        case OpenThermMessageID::Toutside:
        case OpenThermMessageID::Tret:
        case OpenThermMessageID::Tstorage:
        case OpenThermMessageID::Tcollector:
        case OpenThermMessageID::TflowCH2:
        case OpenThermMessageID::Tdhw2:
        case OpenThermMessageID::Texhaust:
        case OpenThermMessageID::BurnerStarts:
        case OpenThermMessageID::CHPumpStarts:
        case OpenThermMessageID::DHWPumpValveStarts:
        case OpenThermMessageID::DHWBurnerStarts:
        case OpenThermMessageID::BurnerOperationHours:
        case OpenThermMessageID::CHPumpOperationHours:
        case OpenThermMessageID::DHWPumpValveOperationHours:
        case OpenThermMessageID::DHWBurnerOperationHours:
        case OpenThermMessageID::TdhwSetUBTdhwSetLB:
        case OpenThermMessageID::MaxTSetUBMaxTSetLB:
        case OpenThermMessageID::TdhwSet:
        case OpenThermMessageID::MaxTSet:
        case OpenThermMessageID::SConfigSMemberIDcode:
        case OpenThermMessageID::RBPflags:
            ESP_LOGD(TAG, "Building simple read request with id %d", request_id);
            return ot->buildRequest(OpenThermMessageType::READ_DATA, (OpenThermMessageID)request_id, 0);
    }
    ESP_LOGE(TAG, "Tried to create a request with unknown id %d", request_id);
    return 0;
}

OpenthermHub::OpenthermHub(void(*handle_interrupt_callback)(void), void(*process_response_callback)(unsigned long, OpenThermResponseStatus)) 
    : Component(), handle_interrupt_callback(handle_interrupt_callback), process_response_callback(process_response_callback) {
}

void IRAM_ATTR OpenthermHub::handle_interrupt() {
    this->ot->handleInterrupt();
}

#define OPENTHERM_PUBLISH_SENSOR(name, state) \
    if (this->name ## _sensor != nullptr) { \
        this->name ## _sensor->publish_state(state); \
    }

#define OPENTHERM_PUBLISH_BINARY_SENSOR(name, state) \
    if (this->name ## _binary_sensor != nullptr) { \
        this->name ## _binary_sensor->publish_state(state); \
    }

void OpenthermHub::process_response(unsigned long response, OpenThermResponseStatus status) {
    if (!ot->isValidResponse(response)) {
        ESP_LOGW(
            TAG, 
            "Received invalid OpenTherm response: %s, status=%s", 
            String(response, HEX).c_str(),
            String(ot->getLastResponseStatus()).c_str()
        );
        return;
    }

    byte id = (response >> 16 & 0xFF);

    ESP_LOGD(TAG, "Received OpenTherm response with id %d: %s", id, String(response, HEX).c_str());

    switch (id) {
        case OpenThermMessageID::Status:
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_fault_indication
            OPENTHERM_PUBLISH_BINARY_SENSOR(fault_indication, ot->isFault(response))
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_ch_active
            OPENTHERM_PUBLISH_BINARY_SENSOR(ch_active, ot->isCentralHeatingActive(response))
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_dhw_active
            OPENTHERM_PUBLISH_BINARY_SENSOR(dhw_active, ot->isHotWaterActive(response))
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_flame_on
            OPENTHERM_PUBLISH_BINARY_SENSOR(flame_on, ot->isFlameOn(response))
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_cooling_active
            OPENTHERM_PUBLISH_BINARY_SENSOR(cooling_active, ot->isCoolingActive(response))
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_ch2_active
            OPENTHERM_PUBLISH_BINARY_SENSOR(ch2_active, response & 0x20)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_diagnostic_indication
            OPENTHERM_PUBLISH_BINARY_SENSOR(diagnostic_indication, ot->isDiagnostic(response))
            #endif
            break;
        case OpenThermMessageID::TSet:
        case OpenThermMessageID::TsetCH2:
            ESP_LOGD(TAG, "Response temperature: %.1f", ot->getFloat(response));
            break;
        #ifdef OPENTHERM_HAS_SENSOR_rel_mod_level
        case OpenThermMessageID::RelModLevel:
            OPENTHERM_PUBLISH_SENSOR(rel_mod_level, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_ch_pressure
        case OpenThermMessageID::CHPressure:
            OPENTHERM_PUBLISH_SENSOR(ch_pressure, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_dhw_flow_rate
        case OpenThermMessageID::DHWFlowRate:
            OPENTHERM_PUBLISH_SENSOR(dhw_flow_rate, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_boiler
        case OpenThermMessageID::Tboiler:
            OPENTHERM_PUBLISH_SENSOR(t_boiler, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_dhw
        case OpenThermMessageID::Tdhw:
            OPENTHERM_PUBLISH_SENSOR(t_dhw, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_outside
        case OpenThermMessageID::Toutside:
            OPENTHERM_PUBLISH_SENSOR(t_outside, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_ret
        case OpenThermMessageID::Tret:
            OPENTHERM_PUBLISH_SENSOR(t_ret, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_storage
        case OpenThermMessageID::Tstorage:
            OPENTHERM_PUBLISH_SENSOR(t_storage, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_collector
        case OpenThermMessageID::Tcollector:
            OPENTHERM_PUBLISH_SENSOR(t_collector, get_s16(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_flow_ch2
        case OpenThermMessageID::TflowCH2:
            OPENTHERM_PUBLISH_SENSOR(t_flow_ch2, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_dhw2
        case OpenThermMessageID::Tdhw2:
            OPENTHERM_PUBLISH_SENSOR(t_dhw2, ot->getFloat(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_t_exhaust
        case OpenThermMessageID::Texhaust:
            OPENTHERM_PUBLISH_SENSOR(t_exhaust, get_s16(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_burner_starts
        case OpenThermMessageID::BurnerStarts:
            OPENTHERM_PUBLISH_SENSOR(burner_starts, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_ch_pump_starts
        case OpenThermMessageID::CHPumpStarts:
            OPENTHERM_PUBLISH_SENSOR(ch_pump_starts, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_dhw_pump_valve_starts
        case OpenThermMessageID::DHWPumpValveStarts:
            OPENTHERM_PUBLISH_SENSOR(dhw_pump_valve_starts, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_dhw_burner_starts
        case OpenThermMessageID::DHWBurnerStarts:
            OPENTHERM_PUBLISH_SENSOR(dhw_burner_starts, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_burner_operation_hours
        case OpenThermMessageID::BurnerOperationHours:
            OPENTHERM_PUBLISH_SENSOR(burner_operation_hours, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_ch_pump_operation_hours
        case OpenThermMessageID::CHPumpOperationHours:
            OPENTHERM_PUBLISH_SENSOR(ch_pump_operation_hours, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_dhw_pump_valve_operation_hours
        case OpenThermMessageID::DHWPumpValveOperationHours:
            OPENTHERM_PUBLISH_SENSOR(dhw_pump_valve_operation_hours, ot->getUInt(response))
            break;
        #endif
        #ifdef OPENTHERM_HAS_SENSOR_dhw_burner_operation_hours
        case OpenThermMessageID::DHWBurnerOperationHours:
            OPENTHERM_PUBLISH_SENSOR(dhw_burner_operation_hours, ot->getUInt(response))
            break;
        #endif
        case OpenThermMessageID::TdhwSetUBTdhwSetLB:
            #ifdef OPENTHERM_HAS_SENSOR_t_dhw_set_ub
            OPENTHERM_PUBLISH_SENSOR(t_dhw_set_ub, get_high_s8(response))
            #endif
            #ifdef OPENTHERM_HAS_SENSOR_t_dhw_set_lb
            OPENTHERM_PUBLISH_SENSOR(t_dhw_set_lb, get_low_s8(response))
            #endif
            break;
        case OpenThermMessageID::MaxTSetUBMaxTSetLB:
            #ifdef OPENTHERM_HAS_SENSOR_max_t_set_ub
            OPENTHERM_PUBLISH_SENSOR(max_t_set_ub, get_high_s8(response))
            #endif
            #ifdef OPENTHERM_HAS_SENSOR_max_t_set_lb
            OPENTHERM_PUBLISH_SENSOR(max_t_set_lb, get_low_s8(response))
            #endif
            break;
        #ifdef OPENTHERM_HAS_SENSOR_t_dhw_set
        case OpenThermMessageID::TdhwSet:
            OPENTHERM_PUBLISH_SENSOR(t_dhw_set, ot->getFloat(response))
            break;
        #endif
        case OpenThermMessageID::MaxTSet:
            #ifdef OPENTHERM_HAS_SENSOR_max_t_set
            OPENTHERM_PUBLISH_SENSOR(max_t_set, ot->getFloat(response))
            #endif
            this->set_output_max_setpoint(ot->getFloat(response));
            break;
        case OpenThermMessageID::SConfigSMemberIDcode:
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_dhw_present
            OPENTHERM_PUBLISH_BINARY_SENSOR(dhw_present, response & 0x1)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_control_type_on_off
            OPENTHERM_PUBLISH_BINARY_SENSOR(control_type_on_off, response & 0x2)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_cooling_supported
            OPENTHERM_PUBLISH_BINARY_SENSOR(cooling_supported, response & 0x4)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_dhw_storage_tank
            OPENTHERM_PUBLISH_BINARY_SENSOR(dhw_storage_tank, response & 0x8)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_master_pump_control_allowed
            OPENTHERM_PUBLISH_BINARY_SENSOR(master_pump_control_allowed, response & 0x10)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_ch2_present
            OPENTHERM_PUBLISH_BINARY_SENSOR(ch2_present, response & 0x20)
            #endif
            break;
        case OpenThermMessageID::RBPflags:
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_dhw_setpoint_transfer_enabled
            OPENTHERM_PUBLISH_BINARY_SENSOR(dhw_setpoint_transfer_enabled, response & 0x1)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_max_ch_setpoint_transfer_enabled
            OPENTHERM_PUBLISH_BINARY_SENSOR(max_ch_setpoint_transfer_enabled, response & 0x2)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_dhw_setpoint_rw
            OPENTHERM_PUBLISH_BINARY_SENSOR(dhw_setpoint_rw, (response >> 8) & 0x1)
            #endif
            #ifdef OPENTHERM_HAS_BINARY_SENSOR_max_ch_setpoint_rw
            OPENTHERM_PUBLISH_BINARY_SENSOR(max_ch_setpoint_rw, (response >> 8) & 0x2)
            #endif
            break;
        default:
            ESP_LOGW(TAG, "This response was not expected.");
            break;
    }
}

void OpenthermHub::setup() {
    ESP_LOGD(TAG, "Setting up OpenTherm component");
    this->ot = new OpenTherm(this->in_pin, this->out_pin, false);
    this->ot->begin(this->handle_interrupt_callback, this->process_response_callback);

    // Ensure that there is at least one request, as we are required to
    // communicate at least once every second. Sending the status request is
    // good practice anyway.
    this->add_repeating_request(OpenThermMessageID::Status);

    this->current_request_iterator = this->initial_requests.begin();
}

void OpenthermHub::on_shutdown() {
    this->ot->end();
}

void OpenthermHub::loop() {
    if (this->ot->isReady()) {
        if (this->initializing && this->current_request_iterator == this->initial_requests.end()) {
            this->initializing = false;
            this->current_request_iterator = this->repeating_requests.begin();
        } else if (this->current_request_iterator == this->repeating_requests.end()) {
            this->current_request_iterator = this->repeating_requests.begin();
        }

        unsigned int request = this->build_request(*this->current_request_iterator);
        this->ot->sendRequestAync(request);
        ESP_LOGD(TAG, "Sent OpenTherm request: %s", String(request, HEX).c_str());
        this->current_request_iterator++;
        
        this->ot->process();
    }
}

#define ID(x) x
#define SHOW2(x) #x
#define SHOW(x) SHOW2(x)

void OpenthermHub::dump_config() {
    ESP_LOGCONFIG(TAG, "OpenTherm:");
    ESP_LOGCONFIG(TAG, "  In: GPIO%d", this->in_pin);
    ESP_LOGCONFIG(TAG, "  Out: GPIO%d", this->out_pin);
    ESP_LOGCONFIG(TAG, "  Sensors: %s", SHOW(OPENTHERM_SENSOR_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Binary sensors: %s", SHOW(OPENTHERM_BINARY_SENSOR_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Switches: %s", SHOW(OPENTHERM_SWITCH_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Input sensors: %s", SHOW(OPENTHERM_INPUT_SENSOR_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Outputs: %s", SHOW(OPENTHERM_OUTPUT_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Numbers: %s", SHOW(OPENTHERM_NUMBER_LIST(ID, )));
    ESP_LOGCONFIG(TAG, "  Initial requests:");
    for (auto type : this->initial_requests) {
        ESP_LOGCONFIG(TAG, "  - %d", type);
    }
    ESP_LOGCONFIG(TAG, "  Repeating requests:");
    for (auto type : this->repeating_requests) {
        ESP_LOGCONFIG(TAG, "  - %d", type);
    }
}

}  // namespace opentherm
}  // namespace esphome
