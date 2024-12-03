import os
import sys
import time
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QProgressBar, QMessageBox, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Constants
TOOL_NAME = "BitBury"
TAGLINE = "Bury the bits or bring them back!"
SECTOR_SIZE = 512

# File Signatures
FILE_SIGNATURES = {
    'jpeg': {'header': b'\xFF\xD8\xFF', 'footer': b'\xFF\xD9'},
    'png': {'header': b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A', 'footer': b'\x49\x45\x4E\x44\xAE\x42\x60\x82'},
    'pdf': {'header': b'\x25\x50\x44\x46', 'footer': b'\x0A\x25\x25\x45\x4F\x46'},
    'zip': {'header': b'\x50\x4B\x03\x04'},
    'docx': {'header': b'\x50\x4B\x03\x04', 'footer': b'\x50\x4B\x05\x06'},  # Matches DOCX footers
    'mp4': {'header': b'\x00\x00\x00\x18\x66\x74\x79\x70', 'footer': None},  # No fixed footer
    'txt': {'header': None, 'footer': None},  # Plain text files don't have headers or footers
}

class FileRecoveryWorker(QThread):
    progress = pyqtSignal(int)
    message = pyqtSignal(str)

    def __init__(self, disk_path, output_folder, file_type=None):
        super().__init__()
        self.disk_path = disk_path
        self.output_folder = output_folder
        self.file_type = file_type

    def run(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        file_counter = 0
        inside_file = False
        current_file_data = b""
        file_type = None

        self.message.emit(f"Starting recovery from {self.disk_path}...")
        with open(self.disk_path, "rb") as disk:
            while True:
                sector = disk.read(SECTOR_SIZE)
                if not sector:
                    break

                # Check for file headers
                if not inside_file:
                    for ftype, sig in FILE_SIGNATURES.items():
                        if self.file_type and self.file_type != ftype:
                            continue
                        if sig['header'] and sector.startswith(sig['header']):
                            self.message.emit(f"Found {ftype.upper()} file header.")
                            current_file_data = sector
                            inside_file = True
                            file_type = ftype
                            break

                # Continue reading file content
                elif inside_file:
                    current_file_data += sector
                    if file_type in FILE_SIGNATURES and 'footer' in FILE_SIGNATURES[file_type]:
                        if FILE_SIGNATURES[file_type]['footer'] and FILE_SIGNATURES[file_type]['footer'] in sector:
                            footer_index = sector.index(FILE_SIGNATURES[file_type]['footer']) + len(FILE_SIGNATURES[file_type]['footer'])
                            current_file_data = current_file_data[:footer_index]
                            inside_file = False

                            file_name = os.path.join(self.output_folder, f"recovered_{file_counter}.{file_type}")
                            with open(file_name, "wb") as recovered_file:
                                recovered_file.write(current_file_data)
                            self.message.emit(f"Recovered file saved as {file_name}")
                            file_counter += 1
                            current_file_data = b""
                            file_type = None

            self.message.emit(f"Recovery completed. {file_counter} files recovered.")

class DiskWipeWorker(QThread):
    progress = pyqtSignal(int)
    message = pyqtSignal(str)

    def __init__(self, disk_path, mode="zeros", passes=1):
        super().__init__()
        self.disk_path = disk_path
        self.mode = mode
        self.passes = passes

    def run(self):
        try:
            for p in range(self.passes):
                self.message.emit(f"Pass {p + 1} of {self.passes} starting...")
                with open(self.disk_path, "wb") as disk:
                    count = 0
                    while True:
                        data = os.urandom(SECTOR_SIZE) if self.mode == "random" else b'\x00' * SECTOR_SIZE
                        try:
                            disk.write(data)
                            count += 1
                            if count % 1000 == 0:
                                self.progress.emit(count * SECTOR_SIZE)
                        except Exception as e:
                            break
                self.message.emit(f"Pass {p + 1} completed.")
            self.message.emit("Disk wipe completed.")
        except PermissionError:
            self.message.emit("Permission denied. Run as administrator/root.")
        except Exception as e:
            self.message.emit(f"Error: {e}")

class BitBuryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{TOOL_NAME} - {TAGLINE}")
        self.setGeometry(100, 100, 600, 400)
        self.initUI()

    def initUI(self):
        # Layouts
        layout = QVBoxLayout()

        self.label = QLabel("Welcome to BitBury!")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.progressBar = QProgressBar()
        layout.addWidget(self.progressBar)

        # Disk path
        disk_layout = QHBoxLayout()
        self.diskInput = QLineEdit()
        self.diskInput.setPlaceholderText("Enter disk path (e.g., /dev/sdb, \\.\PhysicalDrive1)")
        disk_layout.addWidget(self.diskInput)
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browseDisk)
        disk_layout.addWidget(browse_button)
        layout.addLayout(disk_layout)

        # Action buttons
        wipe_button = QPushButton("Wipe Disk")
        wipe_button.clicked.connect(self.wipeDisk)
        layout.addWidget(wipe_button)

        recover_button = QPushButton("Recover Files")
        recover_button.clicked.connect(self.recoverFiles)
        layout.addWidget(recover_button)

        # Output widget
        self.output = QLabel("")
        self.output.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output)

        # Main widget
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def browseDisk(self):
        options = QFileDialog.Options()
        path, _ = QFileDialog.getOpenFileName(self, "Select Disk", "", options=options)
        if path:
            self.diskInput.setText(path)

    def wipeDisk(self):
        disk_path = self.diskInput.text()
        if not disk_path:
            self.showError("Please specify a disk path.")
            return
        # Start wiping
        self.output.setText("Starting disk wipe...")
        self.progressBar.setValue(0)

    def recoverFiles(self):
        disk_path = self.diskInput.text()
        if not disk_path:
            self.showError("Please specify a disk path.")
            return
        # Start recovery
        self.output.setText("Starting file recovery...")
        self.progressBar.setValue(0)

    def showError(self, message):
        QMessageBox.critical(self, "Error", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitBuryApp()
    window.show()
    sys.exit(app.exec_())
