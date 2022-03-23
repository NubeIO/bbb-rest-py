import subprocess


def command(cmd, _input=""):
    rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=_input.encode("utf-8"))
    assert rst.returncode == 0, rst.stderr.decode("utf-8")
    try:
        return rst.stdout.decode("utf-8")
    except ValueError:
        return "Error"


def execute_command(cmd, cwd=None) -> bool:
    """Run command line"""
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, cwd=cwd)
    except subprocess.CalledProcessError:
        return False
    return True
