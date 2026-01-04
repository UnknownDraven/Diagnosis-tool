import re

def check_cpu(command_executor):
    out, err, r = command_executor.run(
        "wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors /format:list"
    )
    if r != 0 or not out:
        return {
            "name": "CPU",
            "status": "FAIL",
            "message": f"CPU detection failed: {err}",
            "severity": "DEAL_BREAKER",
            "confidence": "low"
        }
    info = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    return {
        "name": "CPU",
        "status": "PASS",
        "message": info.get("Name", "Unknown"),
        "details": info,
        "severity": "INFO",
        "confidence": "high"
    }

def check_ram(command_executor):
    out, err, r = command_executor.run(
        "wmic ComputerSystem get TotalPhysicalMemory /format:list"
    )
    if r != 0:
        return {
            "name": "RAM",
            "status": "FAIL",
            "message": f"RAM detection failed: {err}",
            "severity": "DEAL_BREAKER"
        }
    m = re.search(r"=(\d+)", out)
    gb = round(int(m.group(1)) / (1024**3), 2) if m else 0
    return {
        "name": "RAM",
        "status": "PASS",
        "message": f"{gb} GB installed",
        "severity": "INFO",
        "confidence": "high"
    }

def check_gpu(command_executor):
    out, _, r = command_executor.run(
        "wmic path win32_VideoController get Name /format:list"
    )
    gpus = [l.split("=", 1)[1] for l in out.splitlines() if "=" in l]
    if gpus:
        return {
            "name": "GPU",
            "status": "PASS",
            "message": ", ".join(gpus),
            "severity": "INFO",
            "confidence": "high"
        }
    else:
        return {
            "name": "GPU",
            "status": "FAIL",
            "message": "No GPU detected",
            "severity": "DEAL_BREAKER"
        }
"""
def stress_cpu(command_executor, seconds=30):
    import psutil
    import threading
    import time

    def load():
        end = time.time() + seconds
        while time.time() < end:
            sum(i*i for i in range(10000))

    threads = []
    for _ in range(psutil.cpu_count()):
        t = threading.Thread(target=load)
        t.start()
        threads.append(t)

    max_temp = 0
    for _ in range(seconds // 2):
        time.sleep(2)
        temps = psutil.sensors_temperatures()
        for entries in temps.values():
            for e in entries:
                max_temp = max(max_temp, e.current or 0)

    for t in threads:
        t.join()

    if max_temp > 95:
        return {
            "name": "CPU Stress",
            "status": "FAIL",
            "message": f"Overheating ({max_temp}°C)",
            "severity": "DEAL_BREAKER"
        }
    else:
        return {
            "name": "CPU Stress",
            "status": "PASS",
            "message": f"Max temp {max_temp}°C",
            "severity": "INFO"
        }

"""

def stress_cpu(command_executor, seconds=30):
    import psutil
    import threading
    import time
    from utils.cpu_temperature import get_cpu_temperatures

    def load():
        end = time.time() + seconds
        while time.time() < end:
            sum(i * i for i in range(10000))

    threads = []
    for _ in range(psutil.cpu_count(logical=True)):
        t = threading.Thread(target=load)
        t.start()
        threads.append(t)

    max_temp = None

    for _ in range(seconds // 2):
        time.sleep(2)

        temps = get_cpu_temperatures()
        if temps:
            current_max = max(temps)
            max_temp = current_max if max_temp is None else max(max_temp, current_max)

    for t in threads:
        t.join()

    if max_temp is None:
        return {
            "name": "CPU Stress",
            "status": "PASS",
            "message": "Stress completed (temperature not exposed by firmware)",
            "severity": "INFO"
        }

    if max_temp > 95:
        return {
            "name": "CPU Stress",
            "status": "FAIL",
            "message": f"Overheating ({max_temp:.1f}°C)",
            "severity": "DEAL_BREAKER"
        }

    return {
        "name": "CPU Stress",
        "status": "PASS",
        "message": f"Max temp {max_temp:.1f}°C",
        "severity": "INFO"
    }

def perform_hardware_checks(executor):
    results = []
    results.append(check_cpu(executor))
    results.append(check_ram(executor))
    results.append(check_gpu(executor))
    results.append(stress_cpu(executor))
    return results