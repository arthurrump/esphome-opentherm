// ESPHome OpenTherm component with support for a few sensors

#pragma once

#include "esphome.h"
#include "OpenTherm.h"

class OpenThermComponent;

// Global singletons for the OpenTherm manager and ESPHome component
OpenTherm* ot;
OpenThermComponent* otComponent;

// Declaration of interrupt handlers to handle OpenTherm responses
void IRAM_ATTR handleInterrupt();
void processResponse(unsigned long response, OpenThermResponseStatus status);

//  FloatOutput that simply stores its state and makes it available through a getter
class StoredFloatOutput : public FloatOutput {
protected:
    float state;
    const char* name;
    void write_state(float state) override { 
        ESP_LOGD("StoredFloatOutput", "Set %s state to %.2f", this->name, state);
        this->state = state;
    }
public:
    StoredFloatOutput (const char* name, float state = 0) : state(state) {}
    float get_state() { 
        return this->state; 
    }
};

// OpenTherm component for ESPHome
class OpenThermComponent : public Component {
private:
    const char* TAG = "opentherm";

protected:
    static const byte requestsCount = 5;
    const uint8_t requests[requestsCount] = {
        // Get current status: flame, CH/DHW activity etc.
        OpenThermMessageID::Status,
        // Set boiler flow temperature setpoint
        OpenThermMessageID::TSet,
        // Get boiler flow temperature
        OpenThermMessageID::Tboiler,
        // Get boiler return flow temperature
        OpenThermMessageID::Tret,
        // Get boiler relative modulation level
        OpenThermMessageID::RelModLevel,
    };

    const int inPin, outPin;
    const bool enableHeating, enableHotWater, enableCooling;

    byte currentRequestIndex;

public:
    StoredFloatOutput* flowTempSetpointOutput = new StoredFloatOutput("flowTempSetpoint");
    Sensor* flowTempSensor = new Sensor();
    Sensor* returnTempSensor = new Sensor();
    Sensor* relModLevelSensor = new Sensor();
    BinarySensor* isFlameOnSensor = new BinarySensor();
    BinarySensor* isCentralHeatingActiveSensor = new BinarySensor();
    BinarySensor* isHotWaterActiveSensor = new BinarySensor();
    BinarySensor* isCoolingActiveSensor = new BinarySensor();
    BinarySensor* hasFaultSensor = new BinarySensor();
    BinarySensor* hasDiagnosticSensor = new BinarySensor();

    OpenThermComponent(int inPin, int outPin, bool enableHeating = true, bool enableHotWater = true, bool enableCooling = false): Component(),
      inPin(inPin), outPin(outPin),
      enableHeating(enableHeating), enableHotWater(enableHotWater), enableCooling(enableCooling),
      currentRequestIndex(0)
    {
        ESP_LOGD(TAG, "Creating OpenTherm component");
        if (otComponent != NULL) {
            ESP_LOGE(TAG, "Only one OpenThermComponent can be created");
            return;
        }
        ot = new OpenTherm(inPin, outPin, false);
        otComponent = this;
    }

protected:
    unsigned int buildRequest(byte requestIndex) {
        byte id = requests[requestIndex];
        switch (id) {
            case OpenThermMessageID::Status:
                ESP_LOGD(TAG, "Building Status request with enableHeating=%d, enableHotWater=%d, enableCooling=%d", enableHeating, enableHotWater, enableCooling);
                return ot->buildSetBoilerStatusRequest(enableHeating, enableHotWater, enableCooling);
            case OpenThermMessageID::TSet:
                ESP_LOGD(TAG, "Building TSet request to set target temperature at %.1f", flowTempSetpointOutput->get_state());
                return ot->buildSetBoilerTemperatureRequest(flowTempSetpointOutput->get_state());
            case OpenThermMessageID::Tboiler:
                ESP_LOGD(TAG, "Building Tboiler request to request boiler flow temperature");
                return ot->buildRequest(OpenThermMessageType::READ, OpenThermMessageID::Tboiler, 0);
            case OpenThermMessageID::Tret:
                ESP_LOGD(TAG, "Building Tret request to request boiler return flow temperature");
                return ot->buildRequest(OpenThermMessageType::READ, OpenThermMessageID::Tret, 0);
            case OpenThermMessageID::RelModLevel:
                ESP_LOGD(TAG, "Building RelModLevel request to request boiler relative modulation level");
                return ot->buildRequest(OpenThermMessageType::READ, OpenThermMessageID::RelModLevel, 0);
        }
        return 0;
    }

public:
    void processResponse(unsigned long response, OpenThermResponseStatus status) {
        if (!ot->isValidResponse(response)) {
            ESP_LOGW(
                TAG, 
                "Received invalid OpenTherm response: %s, status=%s", 
                String(response, HEX).c_str(),
                String(ot->getLastResponseStatus()).c_str()
            );
            return;
        }

        float res;
        byte id = (response >> 16 & 0xFF);
        switch (id) {
            // Response to a status request
            case OpenThermMessageID::Status:
                ESP_LOGD(TAG, "Received OpenTherm Status response: %s", String(response, HEX).c_str());
                isFlameOnSensor->publish_state(ot->isFlameOn(response));
                isCentralHeatingActiveSensor->publish_state(ot->isCentralHeatingActive(response));
                isHotWaterActiveSensor->publish_state(ot->isHotWaterActive(response));
                isCoolingActiveSensor->publish_state(ot->isCoolingActive(response));
                hasFaultSensor->publish_state(ot->isFault(response));
                hasDiagnosticSensor->publish_state(ot->isDiagnostic(response));
                break;
            // Response to the request to set the boiler flow temperature
            case OpenThermMessageID::TSet:
                ESP_LOGD(TAG, "Received OpenTherm TSet response: %s", String(response, HEX).c_str());
                res = (response & 0xFFFF) / 256.0;
                ESP_LOGD(TAG, "TSet response temperature: %.1f", res);
                break;
            // Response to a request for the actual current flow temperature
            case OpenThermMessageID::Tboiler:
                ESP_LOGD(TAG, "Received OpenTherm Tboiler response: %s", String(response, HEX).c_str());
                res = (response & 0xFFFF) / 256.0;
                ESP_LOGD(TAG, "Tboiler response temperature: %.1f", res);
                flowTempSensor->publish_state(res);
                break;
            // Response to a request for the current return flow temperature
            case OpenThermMessageID::Tret:
                ESP_LOGD(TAG, "Received OpenTherm Tret response: %s", String(response, HEX).c_str());
                res = (response & 0xFFFF) / 256.0;
                ESP_LOGD(TAG, "Tret response temperature: %.1f", res);
                returnTempSensor->publish_state(res);
                break;
            // Response to a request for the relative modulation level
            case OpenThermMessageID::RelModLevel:
                ESP_LOGD(TAG, "Received OpenTherm RelModLevel response: %s", String(response, HEX).c_str());
                res = (response & 0xFFFF) / 256.0;
                ESP_LOGD(TAG, "RelModLevel response level: %.1f%%", res);
                relModLevelSensor->publish_state(res);
                break;
            default:
                ESP_LOGW(TAG, "Received unexpected response with id %d: %s", id, String(response, HEX).c_str());
                break;
        }
    }

    float get_setup_priority() const override{
        return setup_priority::HARDWARE;
    }

    void setup() override{
        ESP_LOGD(TAG, "Setting up OpenTherm component");
        ot->begin(handleInterrupt);
    }

    void on_shutdown() override {
        ot->end();
        ot = NULL;
        otComponent = NULL;
    }

    void loop() override {
        if (ot->isReady()) {
            unsigned int request = buildRequest(currentRequestIndex);
            ot->sendRequestAync(request);
            ESP_LOGD(TAG, "Sent request %s over OpenTherm", String(request, HEX).c_str());
            currentRequestIndex = currentRequestIndex + 1 % requestsCount;
            ot->process();
        }
    }

    void dump_config() override {
        ESP_LOGCONFIG(TAG, "OpenTherm:");
        ESP_LOGCONFIG(TAG, "  In pin: GPIO%d", inPin);
        ESP_LOGCONFIG(TAG, "  Out pin: GPIO%d", outPin);
        ESP_LOGCONFIG(TAG, "  Enable heating: %s", enableHeating ? "YES" : "NO");
        ESP_LOGCONFIG(TAG, "  Enable hot water: %s", enableHotWater ? "YES" : "NO");
        ESP_LOGCONFIG(TAG, "  Enable cooling: %s", enableCooling ? "YES" : "NO");
    }
};

// Implementation of interrupt handlers
void IRAM_ATTR handleInterrupt() {
    if (ot != NULL) {
        ot->handleInterrupt();
    }
}

void processResponse(unsigned long response, OpenThermResponseStatus status) {
    if (otComponent != NULL) {
        otComponent->processResponse(response, status);
    }
}
