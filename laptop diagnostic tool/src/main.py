from constants import STATUS_PASS, STATUS_WARN, STATUS_FAIL
from diagnostics.bios_checks import perform_bios_checks
from diagnostics.hardware_checks import perform_hardware_checks
from diagnostics.storage_checks import perform_storage_checks
from diagnostics.corporate_locks_checks import perform_corporate_locks_checks
from diagnostics.windows_checks import perform_windows_checks
from utils.command_executor import CommandExecutor, clear_command_cache
from summary import summarize_results

def main():
    executor = CommandExecutor()

    # Perform diagnostic checks
    bios_results = perform_bios_checks(executor)
    hardware_results = perform_hardware_checks(executor)
    storage_results = perform_storage_checks(executor)
    corporate_locks_results = perform_corporate_locks_checks(executor)
    windows_results = perform_windows_checks(executor)

    # Combine results
    all_results = (
        bios_results + hardware_results + storage_results +
        corporate_locks_results + windows_results
    )

    # Summarize results
    score, verdict = summarize_results(all_results)

    # Output results
    print(f"SCORE: {score}/100")
    print(f"VERDICT: {verdict}")

    # Clear command cache after diagnostics
    clear_command_cache()

if __name__ == "__main__":
    main()