from shutil import copyfile
from utilities import run_shell_cmd

copyfile("easy_sync.py", "~/bin/easy_sync.py")
copyfile("utilities.py", "~/bin/utilities.py")

run_shell_cmd("chmod +x ~/bin/easy_sync.py")
run_shell_cmd("chmod +x ~/bin/utilities.py")
