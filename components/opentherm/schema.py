# This file contains a schema for all supported sensors, binary sensors and
# inputs of the OpenTherm component.

from typing import Dict, Generic, Tuple, TypeVar, TypedDict
from typing_extensions import NotRequired

from esphome.const import (
    UNIT_CELSIUS,
    UNIT_PERCENT,
    DEVICE_CLASS_COLD,
    DEVICE_CLASS_HEAT,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_PROBLEM,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

T = TypeVar("T")
class Schema(Generic[T], Dict[str, T]):
    pass

class EntitySchema(TypedDict):
    # Description of the item, based on the OpenTherm spec
    description: str
    # OpenTherm message id used to read or write the value
    message: str
    # Whether the value should be read or write repeatedly (True) or only during
    # the initialization phase (False)
    keep_updated: bool
    # Instructions on how to interpret the data in the message
    #   - flag8_[hb|lb]_[0-7]: data is a byte of single bit flags, 
    #                          this flag is set in the high (hb) or low byte (lb),
    #                          at position 0 to 7
    #   - u8_[hb|lb]: data is an unsigned 8-bit integer, 
    #                 in the high (hb) or low byte (lb)
    #   - f8.8: data is a signed fixed point value with 
    #           1 sign bit, 7 integer bits, 8 fractional bits
    #   - u16: data is an unsigned 16-bit integer
    #   - s16: data is a signed 16-bit integer
    message_data: str

class SensorSchema(EntitySchema):
    unit_of_measurement: NotRequired[str]
    accuracy_decimals: int
    icon: NotRequired[str]
    state_class: str

OPENTHERM_SENSORS: Schema[SensorSchema] = {
    "rel_mod_level": {
        "description": "Relative modulation level",
        "unit_of_measurement": UNIT_PERCENT,
        "accuracy_decimals": 2,
        "icon": "mdi:percent",
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "RelModLevel",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "ch_pressure": {
        "description": "Water pressure in CH circuit",
        "unit_of_measurement": "bar",
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_PRESSURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "CHPressure",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "dhw_flow_rate": {
        "description": "Water flow rate in DHW circuit",
        "unit_of_measurement": "l/min",
        "accuracy_decimals": 2,
        "icon": "mdi:waves-arrow-right",
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "DHWFlowRate",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_boiler": {
        "description": "Boiler water temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tboiler",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_dhw": {
        "description": "DHW temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tdhw",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_outside": {
        "description": "Outside temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Toutside",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_ret": {
        "description": "Return water temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tret",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_storage": {
        "description": "Solar storage temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tstorage",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_collector": {
        "description": "Solar collector temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tcollector",
        "keep_updated": True,
        "message_data": "s16",
    },
    "t_flow_ch2": {
        "description": "Flow water temperature CH2 circuit",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "TflowCH2",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_dhw2": {
        "description": "Domestic hot water temperature 2",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Tdhw2",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "t_exhaust": {
        "description": "Boiler exhaust temperature",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "Texhaust",
        "keep_updated": True,
        "message_data": "s16",
    },
    "burner_starts": {
        "description": "Number of starts burner",
        "accuracy_decimals": 0,
        "icon": "mdi:gas-burner",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "BurnerStarts",
        "keep_updated": True,
        "message_data": "u16",
    },
    "ch_pump_starts": {
        "description": "Number of starts CH pump",
        "accuracy_decimals": 0,
        "icon": "mdi:pump",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "CHPumpStarts",
        "keep_updated": True,
        "message_data": "u16",
    },
    "dhw_pump_valve_starts": {
        "description": "Number of starts DHW pump/valve",
        "accuracy_decimals": 0,
        "icon": "mdi:water-pump",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "DHWPumpValveStarts",
        "keep_updated": True,
        "message_data": "u16",
    },
    "dhw_burner_starts": {
        "description": "Number of starts burner during DHW mode",
        "accuracy_decimals": 0,
        "icon": "mdi:gas-burner",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "DHWBurnerStarts",
        "keep_updated": True,
        "message_data": "u16",
    },
    "burner_operation_hours": {
        "description": "Number of hours that burner is in operation",
        "accuracy_decimals": 0,
        "icon": "mdi:clock-outline",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "BurnerOperationHours",
        "keep_updated": True,
        "message_data": "u16",
    },
    "ch_pump_operation_hours": {
        "description": "Number of hours that CH pump has been running",
        "accuracy_decimals": 0,
        "icon": "mdi:clock-outline",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "CHPumpOperationHours",
        "keep_updated": True,
        "message_data": "u16",
    },
    "dhw_pump_valve_operation_hours": {
        "description": "Number of hours that DHW pump has been running or DHW valve has been opened",
        "accuracy_decimals": 0,
        "icon": "mdi:clock-outline",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "DHWPumpValveOperationHours",
        "keep_updated": True,
        "message_data": "u16",
    },
    "dhw_burner_operation_hours": {
        "description": "Number of hours that burner is in operation during DHW mode",
        "accuracy_decimals": 0,
        "icon": "mdi:clock-outline",
        "state_class": STATE_CLASS_TOTAL_INCREASING,
        "message": "DHWBurnerOperationHours",
        "keep_updated": True,
        "message_data": "u16",
    },
    "t_dhw_set_ub": {
        "description": "Upper bound for adjustement of DHW setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "TdhwSetUBTdhwSetLB",
        "keep_updated": False,
        "message_data": "s8_hb",
    },
    "t_dhw_set_lb": {
        "description": "Lower bound for adjustement of DHW setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "TdhwSetUBTdhwSetLB",
        "keep_updated": False,
        "message_data": "s8_lb",
    },
    "max_t_set_ub": {
        "description": "Upper bound for adjustement of max CH setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "MaxTSetUBMaxTSetLB",
        "keep_updated": False,
        "message_data": "s8_hb",
    },
    "max_t_set_lb": {
        "description": "Lower bound for adjustement of max CH setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 0,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "MaxTSetUBMaxTSetLB",
        "keep_updated": False,
        "message_data": "s8_lb",
    },
    "t_dhw_set": {
        "description": "Domestic hot water temperature setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "TdhwSet",
        "keep_updated": True,
        "message_data": "f8.8",
    },
    "max_t_set": {
        "description": "Maximum allowable CH water setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "accuracy_decimals": 2,
        "device_class": DEVICE_CLASS_TEMPERATURE,
        "state_class": STATE_CLASS_MEASUREMENT,
        "message": "MaxTSet",
        "keep_updated": True,
        "message_data": "f8.8",
    },
}

class BinarySensorSchema(EntitySchema):
    device_class: NotRequired[str]

OPENTHERM_BINARY_SENSORS: Schema = {
    "fault_indication": {
        "description": "Status: Fault indication",
        "device_class": DEVICE_CLASS_PROBLEM,
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_0",
    },
    "ch_active": {
        "description": "Status: Central Heating active",
        "device_class": DEVICE_CLASS_HEAT,
        "icon": "mdi:radiator",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_1",
    },
    "dhw_active": {
        "description": "Status: Domestic Hot Water active",
        "device_class": DEVICE_CLASS_HEAT,
        "icon": "mdi:faucet",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_2",
    },
    "flame_on": {
        "description": "Status: Flame on",
        "device_class": DEVICE_CLASS_HEAT,
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_3",
    },
    "cooling_active": {
        "description": "Status: Cooling active",
        "device_class": DEVICE_CLASS_COLD,
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_4",
    },
    "ch2_active": {
        "description": "Status: Central Heating 2 active",
        "device_class": DEVICE_CLASS_HEAT,
        "icon": "mdi:radiator",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_5",
    },
    "diagnostic_indication": {
        "description": "Status: Diagnostic event",
        "device_class": DEVICE_CLASS_PROBLEM,
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_lb_6",
    },
    "dhw_present": {
        "description": "Configuration: DHW present",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_0",
    },
    "control_type_on_off": {
        "description": "Configuration: Control type is on/off",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_1",
    },
    "cooling_supported": {
        "description": "Configuration: Cooling supported",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_2",
    },
    "dhw_storage_tank": {
        "description": "Configuration: DHW storage tank",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_3",
    },
    "master_pump_control_allowed": {
        "description": "Configuration: Master pump control allowed",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_4",
    },
    "ch2_present": {
        "description": "Configuration: CH2 present",
        "message": "SConfigSMemberIDcode",
        "keep_updated": False,
        "message_data": "flag8_hb_5",
    },
    "dhw_setpoint_transfer_enabled": {
        "description": "Remote boiler parameters: DHW setpoint transfer enabled",
        "message": "RBPflags",
        "keep_updated": False,
        "message_data": "flag8_hb_0",
    },
    "max_ch_setpoint_transfer_enabled": {
        "description": "Remote boiler parameters: CH maximum setpoint transfer enabled",
        "message": "RBPflags",
        "keep_updated": False,
        "message_data": "flag8_hb_1",
    },
    "dhw_setpoint_rw": {
        "description": "Remote boiler parameters: DHW setpoint read/write",
        "message": "RBPflags",
        "keep_updated": False,
        "message_data": "flag8_lb_0",
    },
    "max_ch_setpoint_rw": {
        "description": "Remote boiler parameters: CH maximum setpoint read/write",
        "message": "RBPflags",
        "keep_updated": False,
        "message_data": "flag8_lb_1",
    },
}

class SwitchSchema(EntitySchema):
    default_mode: str

OPENTHERM_SWITCHES: Schema[SwitchSchema] = {
    "ch_enable": {
        "description": "Central Heating enabled",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_hb_0",
        "default_mode": "restore_default_on"
    },
    "dhw_enable": {
        "description": "Domestic Hot Water enabled",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_hb_1",
        "default_mode": "restore_default_on"
    },
    "cooling_enable": {
        "description": "Cooling enabled",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_hb_2",
        "default_mode": "restore_default_off"
    },
    "otc_active": {
        "description": "Outside temperature compensation active",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_hb_3",
        "default_mode": "restore_default_off"
    },
    "ch2_active": {
        "description": "Central Heating 2 active",
        "message": "Status",
        "keep_updated": True,
        "message_data": "flag8_hb_4",
        "default_mode": "restore_default_off"
    },
}

class AutoConfigure(TypedDict):
    message: str
    message_data: str

class InputSchema(EntitySchema):
    unit_of_measurement: str
    range: Tuple[int, int]
    auto_max_value: NotRequired[AutoConfigure]
    auto_min_value: NotRequired[AutoConfigure]

OPENTHERM_INPUTS: Schema[InputSchema] = {
    "t_set": {
        "description": "Control setpoint: temperature setpoint for the boiler's supply water",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "TSet",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (0, 100),
        "auto_max_value": { "message": "MaxTSet", "message_data": "f8.8" },
    },
    "t_set_ch2": {
        "description": "Control setpoint 2: temperature setpoint for the boiler's supply water on the second heating circuit",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "TsetCH2",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (0, 100),
        "auto_max_value": { "message": "MaxTSet", "message_data": "f8.8" },
    },
    "cooling_control": {
        "description": "Cooling control signal",
        "unit_of_measurement": UNIT_PERCENT,
        "message": "CoolingControl",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (0, 100),
    },
    "t_dhw_set": {
        "description": "Domestic hot water temperature setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "TdhwSet",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (0, 127),
        "auto_min_value": { "message": "TdhwSetUBTdhwSetLB", "message_data": "s8_lb" },
        "auto_max_value": { "message": "TdhwSetUBTdhwSetLB", "message_data": "s8_hb" },
    },
    "max_t_set": {
        "description": "Maximum allowable CH water setpoint",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "MaxTSet",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (0, 127),
        "auto_min_value": { "message": "MaxTSetUBMaxTSetLB", "message_data": "s8_lb" },
        "auto_max_value": { "message": "MaxTSetUBMaxTSetLB", "message_data": "s8_hb" },
    },
    "t_room_set": {
        "description": "Current room temperature setpoint (informational)",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "TrSet",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (-40, 127),
    },
    "t_room_set_ch2": {
        "description": "Current room temperature setpoint on CH2 (informational)",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "TrSetCH2",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (-40, 127),
    },
    "t_room": {
        "description": "Current sensed room temperature (informational)",
        "unit_of_measurement": UNIT_CELSIUS,
        "message": "Tr",
        "keep_updated": True,
        "message_data": "f8.8",
        "range": (-40, 127),
    },
}
