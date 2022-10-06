import sys
from release import CHANGELOG_FILE, VERSION_HEADER_PATTERN

if __name__ == "__main__":
    version = sys.argv[1]
    in_version = False

    with open(CHANGELOG_FILE, "r", encoding = "utf-8") as f:
        for line in f.readlines():
            if in_version:
                if line.startswith("##"):
                    break
                print(line, end = None)
            if line.startswith("##"):
                match = VERSION_HEADER_PATTERN.match(line)
                in_version = match and ("v" + match.group(1)) == version
