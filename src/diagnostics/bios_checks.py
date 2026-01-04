def check_bios_info(command_executor):
    out, err, r = command_executor.run(
        "wmic bios get Manufacturer,SMBIOSBIOSVersion,SerialNumber /format:list"
    )
    if r != 0 or not out:
        return {
            "name": "BIOS Info",
            "status": "WARN",
            "message": "BIOS info unreadable",
            "confidence": "low"
        }

    info = dict(l.split("=", 1) for l in out.splitlines() if "=" in l)
    serial = info.get("SerialNumber", "").lower()

    if serial and serial not in ["", "default", "to be filled by o.e.m."]:
        return {
            "name": "BIOS Serial",
            "status": "PASS",
            "message": f"Serial: {serial}",
            "details": info,
            "confidence": "high"
        }
    else:
        return {
            "name": "BIOS Serial",
            "status": "WARN",
            "message": "Serial missing/generic",
            "details": info,
            "confidence": "high"
        }

def check_tpm(command_executor):
    out, _, r = command_executor.run(
        "wmic /namespace:\\\\root\\cimv2\\security\\microsofttpm "
        "path win32_tpm get IsEnabled_InitialValue /format:list"
    )
    if r == 0 and "TRUE" in out.upper():
        return {
            "name": "TPM",
            "status": "PASS",
            "message": "TPM present",
            "confidence": "high"
        }
    else:
        return {
            "name": "TPM",
            "status": "WARN",
            "message": "TPM missing/disabled",
            "severity": "INFO",
            "confidence": "medium"
        }

def check_secure_boot(command_executor):
    out, _, r = command_executor.run(
        'powershell -command "Confirm-SecureBootUEFI"', timeout=10
    )
    if r == 0:
        return {
            "name": "Secure Boot",
            "status": "PASS" if "True" in out else "WARN",
            "message": f"Secure Boot = {out.strip()}",
            "confidence": "high"
        }
    else:
        return {
            "name": "Secure Boot",
            "status": "WARN",
            "message": "Unable to determine (Legacy BIOS?)",
            "confidence": "low"
        }

def check_boot_mode(command_executor):
    out, _, _ = command_executor.run("bcdedit | findstr /i path")
    if "efi" in out.lower():
        return {
            "name": "Boot Mode",
            "status": "PASS",
            "message": "UEFI",
            "confidence": "high"
        }
    else:
        return {
            "name": "Boot Mode",
            "status": "WARN",
            "message": "Legacy BIOS",
            "confidence": "medium"
        }

def perform_bios_checks(executor):
    results = []
    results.append(check_bios_info(executor))
    results.append(check_tpm(executor))
    results.append(check_secure_boot(executor))
    results.append(check_boot_mode(executor))
    return results