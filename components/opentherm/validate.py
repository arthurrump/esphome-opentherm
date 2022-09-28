from typing import Callable

import esphome.config_validation as cv

from . import schema as schema

def create_validation_schema(entities: schema.Schema[schema.T], get_entity_validation_schema: Callable[[schema.T], cv.Schema]) -> cv.Schema:
    schema = {}
    for key, entity in entities.items():
        schema[cv.Optional(key)] = get_entity_validation_schema(entity)
    return cv.Schema(schema)
