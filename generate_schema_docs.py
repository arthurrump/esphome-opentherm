from typing import Dict

import re

import components.opentherm.schema as schema

LINESEP = "\n"
MD_LINEBREAK = "\n"

README = "README.md"

BEGIN_PATTERN = re.compile(r"<!-- BEGIN schema_docs:(\w+) -->")
END_PATTERN = re.compile(r"<!-- END schema_docs:(\w+) -->")

def begins_section(line: str) -> str | None:
    match = BEGIN_PATTERN.match(line)
    if match:
        return match.group(1)
    return None

def ends_section(line: str) -> bool:
    match = END_PATTERN.match(line)
    return match != None

def replace_docs(sections: Dict[str, str]) -> None:
    with open(README, "r") as f:
        lines = f.readlines()
    with open(README, "w", encoding = "utf-8") as f:
        in_section = False
        for line in lines:
            section = begins_section(line)
            if section:
                in_section = True
                f.write(line)
                f.write(sections[section])
                continue
            if ends_section(line):
                in_section = False
            if not in_section:
                f.write(line)

sections = {
    "input": LINESEP.join([
        f"- `{key}`: {sch['description']} ({sch['unit_of_measurement']})"
        + MD_LINEBREAK + f"  Default `min_value`: {sch['range'][0]}"
        + MD_LINEBREAK + f"  Default `max_value`: {sch['range'][1]}"
        + (MD_LINEBREAK + f"  Supports `auto_min_value`" if "auto_min_value" in sch else "")
        + (MD_LINEBREAK + f"  Supports `auto_max_value`" if "auto_max_value" in sch else "")
        for key, sch in schema.INPUTS.items()
    ]) + LINESEP,
    "switch": LINESEP.join([
        f"- `{key}`: {sch['description']}"
        + MD_LINEBREAK + f"  Defaults to *{sch['default_mode'].endswith('on')}*"
        for key, sch in schema.SWITCHES.items()
    ]) + LINESEP,
    "binary_sensor": LINESEP.join([
        f"- `{key}`: {sch['description']}"
        for key, sch in schema.BINARY_SENSORS.items()
    ]) + LINESEP,
    "sensor": LINESEP.join([
        f"- `{key}`: {sch['description']}" 
        + (f" ({sch['unit_of_measurement']})" if "unit_of_measurement" in sch else "")
        for key, sch in schema.SENSORS.items()
    ]) + LINESEP,
}

replace_docs(sections)
