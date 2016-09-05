from __future__ import print_function
import subprocess
import argparse
from utilities import run_shell_cmd

parser = argparse.ArgumentParser(description="Install easy-sync script.")
parser.add_argument("--config", dest="config", help="Location of the JSON config file.")
parser.add_argument("--debug", dest="debug", action="store_const", const=True, default=False)

args = parser.parse_args()

BASEDIR = run_shell_cmd("echo $(git rev-parse --show-toplevel)")
USERNAME = run_shell_cmd("echo $USER")
HOME = run_shell_cmd("echo $HOME")

FSWATCH_FULL = subprocess.check_output("which fswatch", shell=True).strip()
RSYNC_FULL = subprocess.check_output("which rsync", shell=True).strip()
XARGS_FULL = subprocess.check_output("which xargs", shell=True).strip()

PYTHON_INSTALL_LOCATION = subprocess.check_output("which python", shell=True).strip()
PYTHON_SCRIPT_LOCATION = BASEDIR + "/easy_sync.py"

PLIST_NAME = "org.%s.easysync" % USERNAME
PLIST_LOC = subprocess.check_output("echo $HOME", shell=True).strip() +\
	"/Library/LaunchAgents/%s.plist" % PLIST_NAME

base_str = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>%s</string>
		<key>ProgramArguments</key>
			<array>
		        <string>%s</string>
				<string>%s</string>
		        <string>%s</string>
		        <string>%s</string>
		        <string>%s</string>
				<string>%s</string>
		        <string>%s</string>
				<string>%s</string>
		        <string>%s</string>
				<string>%s</string>
			</array>
		<key>RunAtLoad</key>
		<true/>
		<key>KeepAlive</key>
		<true/>
		<key>StandardErrorPath</key>
		<string>/tmp/easysync.err</string>
		<key>StandardOutPath</key>
		<string>/tmp/easysync.out</string>
	</dict>
</plist>
""" % (PLIST_NAME,
	   PYTHON_INSTALL_LOCATION,
	   PYTHON_SCRIPT_LOCATION,
	   "--config",
	   args.config,
	   "--fswatch",
	   FSWATCH_FULL,
	   "--rsync",
	   RSYNC_FULL,
	   "--xargs",
	   XARGS_FULL)

if args.debug:
	print("Would have written: %s" % base_str)
else:
	with open(PLIST_LOC, "w+") as f:
	    print(base_str, file=f)
	    f.close()