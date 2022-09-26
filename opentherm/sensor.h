#pragma once

namespace esphome {
namespace opentherm {

enum class OpenthermSensorType {
    // Class 4: Sensor and informational data
    // Message 17 (RelModLevel) relative modulation level (%)
    rel_mod_level,
    // Message 18 (CHPressure) water pressure in CH circuit (bar)
    ch_pressure,
    // Message 19 (DHWFlowRate) water flow rate in DHW circuit (l/min)
    dhw_flow_rate,
    // Message 25 (Tboiler) boiler water temperature (°C)
    t_boiler,
    // Message 26 (Tdhw) DHW temperature (°C)
    t_dhw,
    // Message 27 (Toutside) outside temperature (°C)
    t_outside,
    // Message 28 (Tret) return water temperature (°C)
    t_ret,
    // Message 29 (Tstorage) solar storage temperature (°C)
    t_storage,
    // Message 30 (Tcollector) solar collector temperature (°C)
    t_collector,
    // Message 31 (TflowCH2) flow water temperature CH2 circuit (°C)
    t_flow_ch2,
    // Message 32 (Tdhw2) domestic hot water temperature 2 (°C)
    t_dhw2,
    // Message 33 (Texhaust) boiler exhaust temperature (°C)
    t_exhaust,
    // Message 116 (BurnerStarts) number of starts burner
    burner_starts,
    // Message 117 (CHPumpStarts) number of starts CH pump
    ch_pump_starts,
    // Message 118 (DHWPumpValveStarts) number of starts DHW pump/valve
    dhw_pump_valve_starts,
    // Message 119 (DHWBurnerStarts) number of starts burner during DHW mode
    dhw_burner_starts,
    // Message 120 (BurnerOperationHours) number of hours that burner is in operation (i.e. flame on)
    burner_operation_hours,
    // Message 121 (CHPumpOperationHours) number of hours that CH pump has been running
    ch_pump_operation_hours,
    // Message 122 (DHWPumpValveOperationHours) number of hours that DHW pump has been running or DHW valve has been opened
    dhw_pump_valve_operation_hours,
    // Message 123 (DHWBurnerOperationHours) number of hours that burner is in operation during DHW mode
    dhw_burner_operation_hours,

    // Class 5: Pre-defined remote boiler parameters
    // Message 48 (TdhwSetUBTdhwSetLB) upper and lower bound for adjustement of DHW setpoint (°C)
    t_dhw_set_ub,
    t_dhw_set_lb,
    // Message 49 (MaxTSetUBMaxTSetLB) upper and lower bound for adjustement of max CH setpoint (°C)
    max_t_set_ub,
    max_t_set_lb,
    // Message 56 (TdhwSet) domestic hot water temperature setpoint (°C)
    t_dhw_set,
    // Message 57 (MaxTSet) maximum allowable CH water setpoint (°C)
    max_t_set,
};

} // namespace opentherm
} // namespace esphome
