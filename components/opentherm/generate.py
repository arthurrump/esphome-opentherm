from typing import Any, Awaitable, Callable, Dict, List
import esphome.codegen as cg
from esphome.const import CONF_ID

from . import CONF_OPENTHERM_ID

def define_has_component(component_type: str, keys: List[str]) -> None:
    cg.add_define(
        f"OPENTHERM_{component_type.upper()}_LIST(F, sep)", 
        cg.RawExpression(" sep ".join(map(lambda key: f"F({key})", keys)))
    )
    for key in keys:
        cg.add_define(f"OPENTHERM_HAS_{component_type.upper()}_{key}")

async def generic_to_code(component_type: str, type: cg.MockObjClass, create: Callable[[str, Dict[str, Any]], Awaitable[cg.Pvariable]], config: Dict[str, Any]) -> None:
    cg.add_define(f"OPENTHERM_USE_{component_type.upper()}")
    
    hub = await cg.get_variable(config[CONF_OPENTHERM_ID])

    keys = []
    for key, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == type:
            entity = await create(key, conf)
            cg.add(getattr(hub, f"set_{key}_{component_type.lower()}")(entity))
            keys.append(key)

    define_has_component(component_type, keys)
    # TODO Generate defines for messages
