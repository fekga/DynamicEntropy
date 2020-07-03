import os
import subprocess
label = subprocess.check_output(["git", "describe","--tags","--abbrev=0"]).strip().decode("utf-8")

with open('core/app_version.py','w') as f:
    f.write(f'version_label = "{str(label)}"')

os.system('python3 -m brython --modules')
os.system('python3 -m http.server')
