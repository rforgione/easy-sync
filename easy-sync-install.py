from __future__ import print_function
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Install easy-sync script.")
parser.add_argument("--config", dest="config", help="Location of the JSON config file.")

args = parser.parse_args()

BASEDIR = subprocess.check_output("echo $(git rev-parse --show-toplevel)", shell=True).strip()
USERNAME = subprocess.check_output("echo $USER", shell=True).strip()
PYTHON_INSTALL_LOCATION = subprocess.check_output("which python", shell=True).strip()
HOME = subprocess.check_output("echo $HOME", shell=True).strip()

PYTHON_SCRIPT_LOCATION = BASEDIR + "/remote_sync.py"

base_str = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
	<dict>
		<key>Label</key>
		<string>remote-sync</string>
		<key>Program</key>
        <string>%s</string>
		<string>%s</string>
        <string>%s</string>
		<key>RunAtLoad</key>
		<true/>
	</dict>
</plist>
""" % (PYTHON_INSTALL_LOCATION, PYTHON_SCRIPT_LOCATION, args.config)

with open(subprocess.check_output("echo $HOME", shell=True).strip() + "/Library/LaunchAgents/org.%s.remotesync.plist" % USERNAME, "w+") as f:
    print(base_str, file=f)
    f.close()
