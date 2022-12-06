#!/usr/bin/env python

import os
import sys
import json
import subprocess

# Optional name of distro for packages to build.
dist_name = None
# Optional package name to build.
package_name = None

if len(sys.argv) > 2:
    dist_name = sys.argv[1]
    package_name = sys.argv[2]
elif len(sys.argv) > 1:
    dist_name = sys.argv[1]

base_dir = os.path.join(os.path.dirname(__file__), "..")
manifest = json.load(open(os.path.join(base_dir, "tools.json"), "r"))
tools = []

if dist_name:
    tools = manifest[dist_name]

    if package_name:
        tools = [next(tool for tool in tools if tool["name"] == package_name)]
else:
    # If no arguments are provided, print the build matrix.
    result = []

    for dist in manifest:
        tools = manifest[dist]

        for tool in tools:
            name = tool['name']
            packages = tool['packages']
            entrypoint = tool['entrypoint']
            result.append({'tool': name, 'dist': dist, 'packages': packages, 'entrypoint': entrypoint})

    print(json.dumps(result))

    sys.exit(0)

for tool in tools:
    name = tool["name"]
    packages = " ".join(tool['packages'])
    entrypoint = tool['entrypoint']
    dockerfile = f"{dist_name}.Dockerfile"

    cmd = [
        "docker",
        "build",
        ".",
        "--file",
        dockerfile,
        "--build-arg",
        f"packages={packages}",
        "--build-arg",
        f"entrypoint={entrypoint}",
        "--tag",
        f"ghcr.io/rwx-labs/{name}:latest",
    ]

    subprocess.run(cmd, stdout=subprocess.PIPE)
