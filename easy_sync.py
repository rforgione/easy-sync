import json
import os
import subprocess
from sys import argv

with open(argv[1]) as f:
    config = json.loads(f.read())
    f.close()

sync_location = "".join([config["username"],"@",config["remote_host"],":",config["remote_dir"]])

fswatch_cmd = "fswatch -o %s" % config["local_dir"]
xargs_cmd = "xargs -n1 -I {}"
rsync_cmd = "rsync -azP --exclude=*.csv,*.tsv '%s/' '%s'" % (config["local_dir"], sync_location)
full_cmd = " ".join([fswatch_cmd, "|", xargs_cmd, rsync_cmd])

# run rsync ones for an initial sync, and then begin listening for changes
subprocess.call(rsync_cmd, shell=True)
subprocess.call(full_cmd, shell=True)
