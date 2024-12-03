import sys
import psutil
import threading
import time
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QPushButton, QHBoxLayout, QWidget, QLabel, QInputDialog, QMessageBox,
    QTabWidget, QCheckBox, QLineEdit, QSlider, QFormLayout
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime


class ProcessAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Process Analyzer and Optimizer")
        self.setGeometry(100, 100, 1200, 800)

        self.cpu_threshold = 50  # Default CPU usage threshold
        self.initUI()

    def initUI(self):
        # Main Layout with Tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Process Management Tab
        self.process_tab = QWidget()
        self.process_tab_layout = QVBoxLayout(self.process_tab)

        # Search Bar
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search process by name...")
        self.search_bar.textChanged.connect(self.update_table)
        search_layout.addWidget(self.search_bar)
        self.process_tab_layout.addLayout(search_layout)

        # Process Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Memory (MB)", "Status", "Parent PID"])
        self.process_tab_layout.addWidget(self.table)

        # Buttons and CPU Threshold Slider
        controls_layout = QHBoxLayout()
        self.terminate_btn = QPushButton("Terminate Process")
        self.terminate_btn.clicked.connect(self.terminate_process)
        self.change_priority_btn = QPushButton("Change Priority")
        self.change_priority_btn.clicked.connect(self.change_priority)
        self.filter_high_cpu = QCheckBox("Filter High CPU Usage")
        self.filter_high_cpu.stateChanged.connect(self.update_table)

        # CPU Threshold Slider
        self.cpu_threshold_slider = QSlider(Qt.Horizontal)
        self.cpu_threshold_slider.setRange(10, 100)
        self.cpu_threshold_slider.setValue(self.cpu_threshold)
        self.cpu_threshold_slider.setTickInterval(10)
        self.cpu_threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.cpu_threshold_slider.valueChanged.connect(self.update_cpu_threshold)

        slider_layout = QFormLayout()
        slider_layout.addRow("CPU Threshold (%)", self.cpu_threshold_slider)

        controls_layout.addWidget(self.terminate_btn)
        controls_layout.addWidget(self.change_priority_btn)
        controls_layout.addWidget(self.filter_high_cpu)
        controls_layout.addLayout(slider_layout)
        self.process_tab_layout.addLayout(controls_layout)

        self.tabs.addTab(self.process_tab, "Process Manager")

        # Graphs Tab
        self.graph_tab = QWidget()
        graph_layout = QVBoxLayout(self.graph_tab)

        self.cpu_graph = LiveGraph(self, "CPU Usage (%)")
        self.memory_graph = LiveGraph(self, "Memory Usage (%)", psutil.virtual_memory)
        graph_layout.addWidget(self.cpu_graph)
        graph_layout.addWidget(self.memory_graph)

        self.tabs.addTab(self.graph_tab, "Resource Monitoring")

        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_table)
        self.timer.start(2000)  # Refresh every 2 seconds

        self.update_table()

    def update_cpu_threshold(self, value):
        self.cpu_threshold = value
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)  # Clear the table
        search_query = self.search_bar.text().lower()
        filter_high_cpu = self.filter_high_cpu.isChecked()
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_info', 'status', 'ppid']):
            try:
                if filter_high_cpu and proc.info['cpu_percent'] < self.cpu_threshold:
                    continue
                if search_query and search_query not in proc.info['name'].lower():
                    continue
                row = [
                    str(proc.info['pid']),
                    proc.info['name'],
                    f"{proc.info['cpu_percent']:.1f}",
                    f"{proc.info['memory_info'].rss / (1024 * 1024):.2f}",
                    proc.info['status'],
                    str(proc.info['ppid'])
                ]
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                for col, data in enumerate(row):
                    item = QTableWidgetItem(data)
                    if col == 2 and float(data) > 80.0:  # Highlight high CPU usage
                        item.setBackground(QColor(255, 100, 100))
                    self.table.setItem(row_position, col, item)
            except psutil.NoSuchProcess:
                continue

    def terminate_process(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No process selected!")
            return
        pid = int(self.table.item(row, 0).text())
        try:
            psutil.Process(pid).terminate()
            QMessageBox.information(self, "Success", f"Process {pid} terminated.")
            self.update_table()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to terminate process: {e}")

    def change_priority(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "No process selected!")
            return
        pid = int(self.table.item(row, 0).text())
        priority, ok = QInputDialog.getInt(self, "Change Priority", "Enter new priority (0-19):")
        if not ok:
            return
        try:
            psutil.Process(pid).nice(priority)
            QMessageBox.information(self, "Success", f"Priority of process {pid} changed to {priority}.")
            self.update_table()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to change priority: {e}")


class LiveGraph(FigureCanvas):
    def __init__(self, parent, title, stat_func=psutil.cpu_percent):
        fig = Figure(figsize=(5, 3))
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.setParent(parent)
        self.title = title
        self.stat_func = stat_func
        self.data = []
        self.timestamps = []
        self.start_graph()

    def start_graph(self):
        self.ax.set_title(self.title)
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel("Usage (%)")
        self.ax.set_xlabel("Time (s)")

        self.line, = self.ax.plot([], [], 'r-')
        self.update_graph()

    def update_graph(self):
        def run():
            while True:
                value = self.stat_func()
                if isinstance(value, psutil._common.svmem):  # Handle memory usage
                    value = value.percent
                self.data.append(value)
                self.data = self.data[-50:]

                self.timestamps.append(datetime.now().strftime("%H:%M:%S"))
                self.timestamps = self.timestamps[-50:]

                self.line.set_data(range(len(self.data)), self.data)
                self.ax.set_xticks(range(len(self.timestamps)))
                self.ax.set_xticklabels(self.timestamps, rotation=45, fontsize=8)
                self.ax.set_xlim(0, max(len(self.data), 50))
                self.draw()
                time.sleep(1)

        thread = threading.Thread(target=run, daemon=True)
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Dark theme
    window = ProcessAnalyzer()
    window.show()
    sys.exit(app.exec_())
