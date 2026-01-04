def check_owner(command_executor):
    out, _, r = command_executor.run(
        'reg query "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion" /v RegisteredOwner'
    )
    owner = out.lower()
    if any(k in owner for k in ["corp", "ltd", "inc", "enterprise"]):
        return {
            "name": "System Owner",
            "status": "WARN",
            "message": "Corporate owner detected",
            "severity": "NEGOTIATE",
            "confidence": "medium"
        }
    else:
        return {
            "name": "System Owner",
            "status": "PASS",
            "message": "Personal ownership",
            "confidence": "medium"
        }

def check_activation(command_executor):
    out, _, r = command_executor.run(
        'wmic path SoftwareLicensingService get OA3xOriginalProductKey'
    )
    if r == 0 and out.strip():
        return {
            "name": "Windows Activation",
            "status": "PASS",
            "message": "Windows is activated",
            "confidence": "high"
        }
    else:
        return {
            "name": "Windows Activation",
            "status": "FAIL",
            "message": "Windows is not activated",
            "severity": "DEAL_BREAKER",
            "confidence": "high"
        }

def check_device_manager(command_executor):
    out, _, r = command_executor.run(
        'devcon status *'
    )
    if r == 0 and "error" not in out.lower():
        return {
            "name": "Device Manager Status",
            "status": "PASS",
            "message": "All devices are functioning properly",
            "confidence": "high"
        }
    else:
        return {
            "name": "Device Manager Status",
            "status": "FAIL",
            "message": "Some devices have issues",
            "severity": "DEAL_BREAKER",
            "confidence": "high"
        }
    
def perform_windows_checks(executor):
    results = []
    results.append(check_owner(executor))
    results.append(check_activation(executor))
    results.append(check_device_manager(executor))
    return results