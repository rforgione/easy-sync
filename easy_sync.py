#!/usr/bin/env python

import json
import argparse
import subprocess

parser = argparse.ArgumentParser(description="Create a loop that listens for changes " +
                                             "and syncs them to a remote directory.")

parser.add_argument("--config", dest="config", nargs="?", default="./sync.json",
                    help="Location of the JSON config file.")
parser.add_argument("--fswatch", dest="fswatch_loc",
                    help="Location of system fswatch.")
parser.add_argument("--rsync", dest="rsync_loc",
                    help="Location of system rsync.")

args = parser.parse_args()

FSWATCH = args.fswatch_loc if args.fswatch_loc else "fswatch"
RSYNC = args.rsync_loc if args.rsync_loc else "rsync"
CONFIG = args.config

if CONFIG:
    with open(CONFIG) as f:
        config = json.loads(f.read())
        f.close()

sync_location = "".join([config["username"], "@", config["remote_host"], ":", config["remote_dir"]])

fswatch_cmd = "%s -1 %s" % (FSWATCH, config["local_dir"])
rsync_cmd = ("{} -aziP ".format(RSYNC) +
             "--exclude=\".git/\" " +
             "--exclude=\"*.csv\" " +
             "--exclude=\"*.tsv\" " +
             "--exclude=\"*.npy\" " +
             "--exclude=\"*.jar\" " +
             "{}/ {}/".format(config["local_dir"], sync_location))


# Arguments:
#   config: dict, contains the sync configuration dict
#
# Description: aligns the current branch of the local repository and the remote
#   repository
def align_remote_branch(config):
    remote_branch = run_shell_cmd("ssh {} git -C {} rev-parse --abbrev-ref HEAD".format(config["remote_host"],
                                                                                        config["remote_dir"]))

    current_branch = run_shell_cmd("git -C {} rev-parse --abbrev-ref HEAD".format(config["local_dir"]))

    if current_branch != remote_branch:
        cmd_prefix = "ssh {} git -C {} ".format(config["remote_host"], config["remote_dir"])

        print "Cleaning remote branch..."

        # reset the remote branch
        run_shell_cmd(cmd_prefix+"reset --hard")

        # download remote branch data
        run_shell_cmd(cmd_prefix+"fetch origin {}".format(current_branch))

        # checkout remote branch
        run_shell_cmd(cmd_prefix+"checkout -f {}".format(current_branch))

        # checkout remote branch
        run_shell_cmd(cmd_prefix+"clean -fd")

        # pull with rebase from github
        run_shell_cmd(cmd_prefix+"pull --rebase origin {}".format(current_branch))


# Arguments:
#   cmd: string, the shell command you want to run
#   return_code: bool, whether or not you want to return
#     the command's return code. If False, will return the
#     output of the command.
# Returns:
#   if return_code is True, returns the return code. Otherwise
#   returns the output from the command.
#
def run_shell_cmd(cmd, return_code=False):
    if return_code:
        return subprocess.call(cmd, shell=True)
    else:
        return subprocess.check_output(cmd, shell=True).strip()


# Arguments:
#   config: dict, contains the sync configuration contained
#     in sync.json
#
# Description:
#   Creates the main listening loop. Checks to make sure the branch is initially
#   aligned and then calls itself recursively for subsequent syncs.
def listen_for_changes(config, align_branches=False):
    # align local branch with remote to make sure we're editing the same
    # branch on both
    if align_branches:
        print "Aligning branches..."
        align_remote_branch(config)

    print "Running initial sync..."
    run_shell_cmd(rsync_cmd)

    print "Listening for changes..."
    while True:
        run_shell_cmd(" ".join([fswatch_cmd, "| xargs -0 -I {} ", rsync_cmd]), return_code=True)

listen_for_changes(config, align_branches=True)
