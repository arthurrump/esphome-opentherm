import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_ID
from . import OpenthermHub, CONF_HUB_ID

DEPENDENCIES = [ 'opentherm' ]

binary_sensor_ns = cg.esphome_ns.namespace('binary_sensor')
