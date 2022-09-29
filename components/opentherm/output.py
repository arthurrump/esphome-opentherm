from typing import Any, Dict

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_ID

from . import schema, validate, input, generate, CONF_OPENTHERM_ID, OpenthermHub, opentherm_ns

DEPENDENCIES = [ "opentherm" ]
COMPONENT_TYPE = "output"

OpenthermOutput = opentherm_ns.class_("OpenthermOutput", output.FloatOutput, cg.Component, input.OpenthermInput)

async def new_openthermoutput(config: Dict[str, Any]) -> cg.Pvariable:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await output.register_output(var, config)
    cg.add(getattr(var, "set_id")(cg.RawExpression(f'"{id}"')))
    # TODO set other input properties
    return var

def get_entity_validation_schema(entity: schema.InputSchema) -> cv.Schema:
    return output.FLOAT_OUTPUT_SCHEMA \
        .extend({ cv.GenerateID(): cv.declare_id(OpenthermOutput) }) \
        .extend(input.input_schema(entity)) \
        .extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = \
    cv.Schema({ cv.GenerateID(CONF_OPENTHERM_ID): cv.use_id(OpenthermHub) }) \
        .extend(validate.create_validation_schema(schema.INPUTS, get_entity_validation_schema)) \
        .extend(cv.COMPONENT_SCHEMA)

async def to_code(config: Dict[str, Any]) -> None:
    await generate.component_to_code(
        COMPONENT_TYPE, 
        schema.INPUTS,
        OpenthermOutput, 
        lambda _, conf: new_openthermoutput(conf), 
        config
    )
