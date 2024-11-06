import os
import time

# Tool Details
TOOL_NAME = "BitBury"
TAGLINE = "Bury the bits or bring them back!"

# Define file signatures for common file types
FILE_SIGNATURES = {
    'jpeg': {'header': b'\xFF\xD8\xFF', 'footer': b'\xFF\xD9'},
    'png': {'header': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 'footer': b'\x49\x45\x4E\x44\xAE\x42\x60\x82'},
    'pdf': {'header': b'\x25\x50\x44\x46', 'footer': b'\x0A\x25\x25\x45\x4F\x46'},
    'zip': {'header': b'\x50\x4B\x03\x04'},
}

SECTOR_SIZE = 512  # Common sector size

def wipe_disk(disk_path, mode="zeros"):
    """Wipes the disk with either zeros or random data based on user choice."""
    print(f"\nStarting data wiping on {disk_path} in '{mode}' mode...")
    try:
        with open(disk_path, "wb") as disk:
            count = 0
            while True:
                if mode == "zeros":
                    data = b'\x00' * SECTOR_SIZE
                elif mode == "random":
                    data = os.urandom(SECTOR_SIZE)
                else:
                    print("Invalid wipe mode selected.")
                    return
                disk.write(data)
                count += 1
                if count % 1000 == 0:
                    print(f"Wiping... {count * SECTOR_SIZE / (1024 * 1024):.2f} MB processed", end='\r')
    except PermissionError:
        print("Permission denied. Please run as administrator or root.")
    except Exception as e:
        print(f"An error occurred during wiping: {e}")
    print("\nData wiping completed successfully.")

def find_files(disk_path, output_folder="recovered_files"):
    """Scans the disk for files with specified headers and footers to recover them."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"\n{TOOL_NAME} - Starting recovery from {disk_path}...")

    with open(disk_path, "rb") as disk:
        file_counter = 0
        inside_file = False
        current_file_data = b""
        file_type = None
        while True:
            sector = disk.read(SECTOR_SIZE)
            if not sector:
                break

            # Check for file headers
            if not inside_file:
                for ftype, sig in FILE_SIGNATURES.items():
                    if sector.startswith(sig['header']):
                        print(f"Found {ftype.upper()} file header at sector {disk.tell() // SECTOR_SIZE}")
                        current_file_data = sector
                        inside_file = True
                        file_type = ftype
                        break

            # Continue reading file content
            elif inside_file:
                current_file_data += sector
                if file_type in FILE_SIGNATURES and 'footer' in FILE_SIGNATURES[file_type]:
                    if FILE_SIGNATURES[file_type]['footer'] in sector:
                        footer_index = sector.index(FILE_SIGNATURES[file_type]['footer']) + len(FILE_SIGNATURES[file_type]['footer'])
                        current_file_data = current_file_data[:footer_index]
                        inside_file = False

                        file_name = os.path.join(output_folder, f"recovered_{file_counter}.{file_type}")
                        with open(file_name, "wb") as recovered_file:
                            recovered_file.write(current_file_data)
                        print(f"Recovered file saved as {file_name}")
                        file_counter += 1
                        current_file_data = b""
                        file_type = None

            # Special case for ZIP files without footer
            if inside_file and file_type == 'zip':
                if len(current_file_data) > 5000000:  # Arbitrary 5 MB limit
                    file_name = os.path.join(output_folder, f"recovered_{file_counter}.zip")
                    with open(file_name, "wb") as recovered_file:
                        recovered_file.write(current_file_data)
                    print(f"Recovered ZIP-based file saved as {file_name}")
                    file_counter += 1
                    current_file_data = b""
                    inside_file = False
                    file_type = None

        print(f"\n{file_counter} files recovered and saved in '{output_folder}' folder.")

def main():
    print(f"\nWelcome to {TOOL_NAME} - {TAGLINE}")
    print("This tool can securely wipe data or attempt to recover JPEG, PNG, PDF, and ZIP files from a formatted drive.")
    print("Ensure you have root/administrator privileges and close other applications using the drive.")
    
    disk_path = input("Enter the path to the disk (e.g., /dev/sdb on Linux, \\\\.\\PhysicalDrive1 on Windows): ")
    if not os.path.exists(disk_path):
        print("Disk path does not exist or cannot be accessed. Please try again.")
        return

    # Prompt for action: Wipe or Recover
    action_choice = input("Do you want to (1) Wipe the disk or (2) Recover files? Enter 1 or 2: ").strip()
    if action_choice == '1':
        confirm_wipe = input("WARNING: Wiping will permanently erase all data! Type 'YES' to confirm: ")
        if confirm_wipe == 'YES':
            wipe_mode = input("Choose wipe mode ('zeros' for zeros, 'random' for random data): ").strip().lower()
            wipe_disk(disk_path, mode=wipe_mode)
            print("Wipe completed. Exiting program.")
        else:
            print("Wipe operation canceled.")
    elif action_choice == '2':
        output_folder = input("Enter the output folder to save recovered files (default is 'recovered_files'): ") or "recovered_files"
        find_files(disk_path, output_folder)
        print("\nData recovery process completed.")
    else:
        print("Invalid option. Exiting program.")

if __name__ == "__main__":
    main()
