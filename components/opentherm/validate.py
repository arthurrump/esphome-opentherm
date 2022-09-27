from typing import Callable

import esphome.config_validation as cv

from schema import T, Schema

def create_validation_schema(entities: Schema[T], get_entity_validation_schema: Callable[[T], cv.Schema]) -> cv.Schema:
    schema = {}
    for key, entity in entities.items():
        schema[cv.Optional(key)] = get_entity_validation_schema(entity)
    return cv.Schema(schema)
