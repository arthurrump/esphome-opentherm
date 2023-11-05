from typing import Iterator, List, Optional, Tuple

from datetime import date
import os
import re

CHANGELOG_FILE = "CHANGELOG.md"
CHANGELOG_HEADER = "# Changelog"
VERSION_NEXT_HEADER = "## vNext"
VERSION_HEADER_PATTERN = re.compile(r"## v(\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2})")
VERSION_PATTERN = re.compile(r"(\d+)\.(\d+)\.(\d+)")

def read_changelog() -> List[str]:
    with open(CHANGELOG_FILE, "r", encoding = "utf-8") as f:
        return f.readlines()

def get_current_version(changelog: List[str]) -> Optional[str]:
    for line in changelog:
        match = VERSION_HEADER_PATTERN.match(line)
        if match:
            return match.group(1)
    return None

def get_next_changelog(changelog: List[str]) -> Iterator[str]:
    in_vNext = False
    for line in changelog:
        if in_vNext:
            if line.startswith("##"):
                break
            yield line
        if line.startswith(VERSION_NEXT_HEADER):
            in_vNext = True

def parse_version(version: str) -> Tuple[int, int, int]:
    match = VERSION_PATTERN.match(version)
    if match and len(match.groups()) == 3:
        return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
    raise ValueError(f"Invalid version number: {version}")

def update_changelog(changelog: List[str], next_version: str) -> None:
    with open(CHANGELOG_FILE, "w", encoding = "utf-8") as f:
        for line in changelog:
            f.write(line)
            if line.startswith(VERSION_NEXT_HEADER):
                f.write("\n")
                f.write(f"## v{next_version} - {date.today().strftime('%Y-%m-%d')}\n")

if __name__ == "__main__":
    changelog = read_changelog()
    current_version = get_current_version(changelog)

    if current_version:
        print(f"Current version is v{current_version}")
    else:
        print("No current version found...")

    print("Changelog for the next version:")
    for line in get_next_changelog(changelog):
        print("  " + line)

    next_version = input("Enter the version number for the new release: ")
    major, minor, patch = parse_version(next_version)

    update_changelog(changelog, next_version)

    os.system('git add CHANGELOG.md')
    os.system(f'git commit -m "Release v{next_version}"')
    os.system(f'git tag -a v{next_version} -m "v{next_version}"')
    os.system(f'git branch -f v{major}.{minor}')
    if major != 0:
        os.system(f'git branch -f v{major}')

    if input("Please verify the changes. Push to origin? (y/n) ").lower() in [ "y", "yes" ]:
        os.system('git push origin')
        os.system(f'git push origin v{next_version}')
        os.system(f'git push origin v{major}.{minor}')
        if major != 0:
            os.system(f'git push origin v{major}')
