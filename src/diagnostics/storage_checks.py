from utils.command_executor import run_command
import json
import re

def check_storage():
    out, err, r = run_command(
        'powershell -command "Get-PhysicalDisk | '
        'Select FriendlyName,MediaType,BusType | ConvertTo-Json"'
    )
    if r == 0 and out:
        disks = json.loads(out)
        disks = disks if isinstance(disks, list) else [disks]

        desc = [f"{d['MediaType']} ({d['BusType']})" for d in disks]

        severity = "INFO"
        status = "PASS"

        if any("HDD" in d["MediaType"] for d in disks):
            status = "WARN"
            severity = "NEGOTIATE"

        if len(disks) > 1:
            status = "WARN"
            severity = "NEGOTIATE"

        return {
            "name": "Storage",
            "status": status,
            "message": ", ".join(desc),
            "details": disks,
            "severity": severity,
            "confidence": "high"
        }

    # WMIC fallback
    out, _, _ = run_command("wmic diskdrive get Model,MediaType /format:list")
    return {
        "name": "Storage",
        "status": "WARN",
        "message": "Storage detected (limited detail)",
        "details": {},
        "severity": "INFO",
        "confidence": "low"
    }

def check_partition_scheme():
    out, _, r = run_command(
        'powershell -command "Get-Disk | '
        'Select PartitionStyle | ConvertTo-Json"'
    )
    if r == 0 and out:
        schemes = {d["PartitionStyle"] for d in json.loads(out)}
        if "MBR" in schemes:
            return {
                "name": "Partition Scheme",
                "status": "WARN",
                "message": "MBR detected",
                "details": {},
                "severity": "NEGOTIATE",
                "confidence": "high"
            }
        else:
            return {
                "name": "Partition Scheme",
                "status": "PASS",
                "message": "GPT",
                "details": {},
                "severity": "INFO",
                "confidence": "high"
            }

def check_smart():
    out, _, r = run_command("wmic diskdrive get Status /format:list")
    if "Pred Fail" in out:
        return {
            "name": "SMART",
            "status": "FAIL",
            "message": "SMART predicts failure",
            "details": {},
            "severity": "DEAL_BREAKER",
            "confidence": "high"
        }
    else:
        return {
            "name": "SMART",
            "status": "PASS",
            "message": "No SMART failure reported",
            "details": {},
            "severity": "INFO",
            "confidence": "low"
        }
    
def perform_storage_checks(command_executor):
    results = []
    results.append(check_storage())
    results.append(check_partition_scheme())
    results.append(check_smart())
    return results