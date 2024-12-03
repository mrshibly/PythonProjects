# OptiFlow

**OptiFlow** is a powerful Process Analyzer and Optimizer designed to visualize and manage system processes in real-time. With an intuitive GUI, advanced filtering, and real-time resource monitoring, OptiFlow helps you optimize your system's performance effortlessly.

---

## 🚀 Features

- **Process Monitoring:**
  - View real-time data for processes (CPU %, memory usage, status, etc.).
  - Sort and filter processes dynamically.

- **Process Control:**
  - Terminate processes with a single click.
  - Adjust process priorities for better resource allocation.

- **Resource Visualization:**
  - Live graphs for CPU and memory usage.
  - Real-time dependency mapping using a Graphviz-rendered process tree.

- **High Resource Alerts:**
  - Highlight high CPU usage processes in red.
  - Enable filters for specific use cases (e.g., show only high CPU usage processes).

- **Dynamic Dependency Graph:**
  - Visualize parent-child relationships between processes.

- **Cross-Platform:**
  - Works seamlessly on Windows, macOS, and Linux.

---

## 🛠️ Installation

### Prerequisites
1. **Python 3.8+** installed on your system. [Download Python](https://www.python.org/downloads/)
2. Install the required Python packages:
   ```bash
   pip install psutil PyQt5 matplotlib graphviz PyQtWebEngine
   ```
3. **Graphviz** must be installed on your system:
   - **Windows**: [Download Graphviz](https://graphviz.gitlab.io/_pages/Download/Download_windows.html)
   - **Linux (Debian/Ubuntu)**:
     ```bash
     sudo apt install graphviz
     ```
   - **macOS**:
     ```bash
     brew install graphviz
     ```

---

## 🖥️ Usage

1. Clone or download this repository.
2. Run the `OptiFlow.py` file:
   ```bash
   python OptiFlow.py
   ```
3. Explore the tabs for:
   - **Process Manager**: View and manage system processes.
   - **Resource Monitoring**: Visualize real-time CPU and memory usage.
   - **Process Dependencies**: View the process dependency tree.

---

## 🎨 Screenshots

### Process Manager
*Real-time process information with sorting, filtering, and controls.*

### Resource Monitoring
*Live CPU and memory graphs for resource tracking.*

### Dependency Visualization
*Visualize parent-child relationships in your system processes.*

---

## ⚠️ Disclaimer

**OptiFlow** provides control over system processes. Terminating or modifying critical processes may cause system instability. Use with caution.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 📧 Contact

For questions or feedback, please open an issue or reach out via email.

---

Enjoy using **OptiFlow**! 🌟
