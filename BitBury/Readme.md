# BitBury

**Bury the bits or bring them back!**

BitBury is a Python-based data recovery and wiping tool designed to help you securely erase data from storage drives or recover specific file types (JPEG, PNG, PDF, ZIP) from formatted or partially damaged disks. Ideal for data recovery specialists, developers, or anyone in need of a reliable way to either rescue or permanently erase data.

## Features
- **Data Recovery**: Recovers JPEG, PNG, PDF, and ZIP files from formatted disks or SD cards.
- **Data Wiping**: Securely wipes a disk with zeros or random data, effectively making data recovery impossible.
- **Progress Tracking**: Displays progress during data wiping to keep users informed.
- **Interactive Command-Line Interface**: Provides clear prompts and feedback for easy navigation.
- **File-by-File Recovery Reporting**: Shows detailed information about each file recovered.

## Prerequisites
- **Python 3.6 or later**
- Administrator/root permissions are required for accessing and modifying disk devices.

> **⚠ WARNING:** Running BitBury with data wiping mode will *permanently erase* all data on the selected drive. Make sure you select the correct drive and understand the implications before proceeding.

## Installation
1. Download the project files as a zip or clone the repository in another way.
2. Extract the contents to a directory of your choice.
3. Ensure Python 3.6+ is installed on your system.

## Usage

Run BitBury from the command line:

```bash
python bitbury.py
```

You will be prompted to select an action:
1. **Wipe the Disk**: Choose this to securely overwrite data on the selected drive.
   - **Wipe Modes**: Choose to overwrite with `zeros` or `random` data for added security.
2. **Recover Files**: Select this to attempt recovery of specific file types (JPEG, PNG, PDF, ZIP) from the disk.
   - **Output Folder**: Specify an output folder where recovered files will be saved.

### Example Usage

1. **Recovering Files**:
   ```bash
   python bitbury.py
   ```
   - Enter disk path (e.g., `/dev/sdb` on Linux, `\\.\PhysicalDrive1` on Windows).
   - Choose the recovery option.
   - Specify an output folder, or use the default (`recovered_files`).

2. **Wiping a Disk**:
   ```bash
   python bitbury.py
   ```
   - Enter disk path.
   - Choose the wipe option and confirm by typing `YES`.
   - Select the wipe mode (`zeros` for standard, `random` for more secure erasure).

## Example Disk Paths
- **Linux**: `/dev/sdb`, `/dev/sdc1`, etc.
- **Windows**: `\\.\PhysicalDrive1`, `\\.\PhysicalDrive2`, etc.

> **Note**: Ensure you have the necessary privileges to access the disk. On Linux, this typically requires `sudo` privileges.

## File Structure
- **bitbury.py**: Main script for running BitBury.
- **README.md**: Documentation and usage information.
- **recovered_files**: Default folder for storing recovered files.

## Requirements
BitBury is designed to run on Python 3.6+ and does not require any external libraries.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer
BitBury is provided as-is without any warranty. Use this tool at your own risk, especially the wiping function. Ensure backups and double-check the target disk path before proceeding with wiping operations.

## Contributing
Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with a description of the changes.

---

Enjoy using **BitBury – Bury the bits or bring them back!**
