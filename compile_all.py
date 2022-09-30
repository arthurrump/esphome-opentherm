import os
import sys

status = 0
results = {}

for file in os.listdir():
    if os.path.isfile(file) and file.endswith(".yaml"):
        print(f"------- Compiling {file} -------")
        res = os.system(f"esphome compile {file}")
        print(f"------- Finished compiling {file} with status {res} -------")
        status += res
        results[file] = res

print("======= Results =======")
for file, res in results.items():
    print(f"{'✅' if res == 0 else '❌'} {file}")
    if res != 0:
        print(f"  Status: {res}")
print("=======================")

if status != 0:
    sys.exit(1)
