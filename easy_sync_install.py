from shutil import copyfile
import subprocess
from utilities import run_shell_cmd

copyfile("easy_sync.py", "~/bin/easy_sync.py")
subprocess.call("chmod +x ~/bin/easy_sync.py", shell=True)
