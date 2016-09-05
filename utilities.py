import subprocess

def run_shell_cmd(cmd, return_code=False):
    if return_code:
        return subprocess.call(cmd, shell=True)
    else:
        return subprocess.check_output(cmd, shell=True).strip()
