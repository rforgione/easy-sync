import json
import os
import subprocess
import argparse

parser = argparse.ArgumentParser(description="Install easy-sync script.")

parser.add_argument("--config", dest="config", help="Location of the JSON config file.")
parser.add_argument("--fswatch", dest="fswatch_loc", help="Location of system fswatch.")
parser.add_argument("--rsync", dest="rsync_loc", help="Location of system rsync.")
parser.add_argument("--xargs", dest="xargs_loc", help="Location of system xargs.")

args = parser.parse_args()

FSWATCH = args.fswatch_loc if args.fswatch_loc else "fswatch"
RSYNC = args.rsync_loc if args.rsync_loc else "rsync"
XARGS = args.xargs_loc if args.xargs_loc else "xargs"
CONFIG = args.config

with open(CONFIG) as f:
    config = json.loads(f.read())
    f.close()

sync_location = "".join([config["username"],"@",config["remote_host"],":",config["remote_dir"]])

fswatch_cmd = "%s -o %s" % (FSWATCH, config["local_dir"])
xargs_cmd = "%s -n1 -I {}" % XARGS
rsync_cmd = "%s -azP --exclude=*.csv,*.tsv '%s/' '%s'" % (RSYNC, config["local_dir"], sync_location)
full_cmd = " ".join([fswatch_cmd, "|", xargs_cmd, rsync_cmd])

# run rsync once for an initial sync, and then begin listening for changes
subprocess.call(rsync_cmd, shell=True)
subprocess.call(full_cmd, shell=True)
