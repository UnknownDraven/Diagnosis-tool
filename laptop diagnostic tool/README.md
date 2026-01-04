# Laptop Diagnostic Tool

## Overview
The Used Laptop Diagnostic Tool is a comprehensive utility designed to assess the condition of used laptops before purchase. It performs a series of diagnostic checks to evaluate hardware, software, and security features, providing potential buyers with a detailed report on the laptop's status.

## Features
- **BIOS Checks**: Verifies BIOS vendor, version, serial number, TPM presence, and secure boot status.
- **Hardware Checks**: Assesses CPU, RAM, and GPU specifications, including stress testing for CPU overheating.
- **Storage Checks**: Enumerates physical disks, classifies storage types, checks partition schemes, and evaluates SMART status.
- **Corporate Locks Checks**: Detects Azure AD join status, BitLocker encryption, and presence of work/school accounts.
- **Windows Checks**: Evaluates system ownership, activation status, and device manager status.

## Project Structure
```
used-laptop-diagnostic-tool
├── src
│   ├── main.py
│   ├── constants.py
│   ├── models
│   │   └── result.py
│   ├── utils
│   │   └── command_executor.py
│   ├── diagnostics
│   │   ├── __init__.py
│   │   ├── bios_checks.py
│   │   ├── hardware_checks.py
│   │   ├── storage_checks.py
│   │   ├── corporate_locks_checks.py
│   │   └── windows_checks.py
│   └── summary.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/used-laptop-diagnostic-tool.git
   ```
2. Navigate to the project directory:
   ```
   cd used-laptop-diagnostic-tool
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the diagnostic tool, execute the following command:
```
python src/main.py
```
You can use the `--quick` option to skip stress tests and the `--json-only` option to output results in JSON format only.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
