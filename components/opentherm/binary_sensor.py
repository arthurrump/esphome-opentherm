from typing import Any, Dict

import esphome.config_validation as cv
from esphome.components import binary_sensor

from . import schema, validate, generate, CONF_OPENTHERM_ID, OpenthermHub

DEPENDENCIES = [ "opentherm" ]
COMPONENT_TYPE = "binary_sensor"

def get_entity_validation_schema(entity: schema.BinarySensorSchema) -> cv.Schema:
    return binary_sensor.binary_sensor_schema(
        device_class = entity["device_class"] if "device_class" in entity else binary_sensor._UNDEF,
        icon = entity["icon"] if "icon" in entity else binary_sensor._UNDEF
    )

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.BINARY_SENSORS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config: Dict[str, Any]) -> None:
    await generate.generic_to_code(
        COMPONENT_TYPE, 
        binary_sensor.BinarySensor, 
        lambda _, conf: binary_sensor.new_binary_sensor(conf), 
        config
    )
