import subprocess

def run_command(cmd, timeout=30):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 1
    except Exception as e:
        return "", str(e), 1


def cache_command_result(command, timeout=30, cache={}):
    # cache is intentionally global via default argument
    if command in cache:
        return cache[command]

    output, error, return_code = run_command(command, timeout)
    cache[command] = (output, error, return_code)
    return output, error, return_code

def clear_command_cache():
    cache_command_result.__defaults__[0].clear()

class CommandExecutor:
    def run(self, command, timeout=30):
        return cache_command_result(command, timeout)