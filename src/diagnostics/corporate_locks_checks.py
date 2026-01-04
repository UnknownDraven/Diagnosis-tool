from utils.command_executor import run_command

def check_work_account():
    out, err, r = run_command(
        'reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AAD\\Storage"'
    )
    if r == 0 and out:
        return {
            "name": "Work/School Account",
            "status": "FAIL",
            "message": "Work/School account present",
            "severity": "DEAL_BREAKER",
            "confidence": "high",
            "details": {}
        }
    else:
        return {
            "name": "Work/School Account",
            "status": "PASS",
            "message": "None detected",
            "confidence": "medium",
            "details": {}
        }

def check_bitlocker():
    out, err, r = run_command("manage-bde -status")
    if "Protection On" in out:
        return {
            "name": "BitLocker",
            "status": "FAIL",
            "message": "BitLocker enabled (recovery key required)",
            "severity": "DEAL_BREAKER",
            "confidence": "high",
            "details": {}
        }
    else:
        return {
            "name": "BitLocker",
            "status": "PASS",
            "message": "BitLocker off",
            "confidence": "high",
            "details": {}
        }

def check_proxy_vpn():
    out, err, r = run_command(
        'reg query "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable'
    )
    if "0x1" in out:
        return {
            "name": "Proxy/VPN",
            "status": "WARN",
            "message": "Proxy configured",
            "severity": "NEGOTIATE",
            "confidence": "medium",
            "details": {}
        }
    else:
        return {
            "name": "Proxy/VPN",
            "status": "PASS",
            "message": "No forced proxy",
            "confidence": "medium",
            "details": {}
        }
    
def perform_corporate_locks_checks(executor):
    results = []
    results.append(check_work_account())
    results.append(check_bitlocker())
    results.append(check_proxy_vpn())
    return results