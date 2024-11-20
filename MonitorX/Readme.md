# MonitorX: Advanced Task Manager

MonitorX is a powerful task manager and system monitoring tool built with Python. It allows users to manage processes, monitor system resources in real-time, and set up alerts for CPU and memory usage. The tool provides a sleek and interactive GUI built with `Tkinter` and visualizations using `Matplotlib`.

## Features

- **Real-Time Monitoring**: Displays real-time graphs for CPU, memory, disk, and network usage.
- **Process Management**:
  - View and search processes by name.
  - Kill selected processes.
  - Set process priorities (Low, Normal, High).
  - View detailed process information.
- **User Alerts**: Get notified when CPU or memory usage exceeds user-defined thresholds.
- **Customizable Settings**: Adjust refresh rate, CPU, and memory alert thresholds.
- **Interactive Interface**: A tabbed UI for easy navigation and intuitive controls.

## Requirements

- Python 3.x
- `psutil` (for system monitoring)
- `tkinter` (for the GUI)
- `matplotlib` (for graphing)

To install the required packages, run the following:

```bash
pip install psutil matplotlib
```

## Installation

1. Download or copy the **MonitorX** source code from the repository.
2. Navigate into the project folder:
   ```bash
   cd path/to/MonitorX
   ```

3. Install the required dependencies (if not already installed):

   ```bash
   pip install psutil matplotlib
   ```

4. Run the application:

   ```bash
   python monitorx.py
   ```

## How to Use

1. **Task Manager Tab**:
   - View and search for processes by name.
   - Kill a process by selecting it and pressing the "Kill Process" button.
   - Set process priority (Low, Normal, or High).
   - Double-click on a process to view detailed information such as memory usage, CPU usage, and more.

2. **Resource Monitor Tab**:
   - View real-time graphs displaying CPU usage, memory usage, disk usage, and network statistics.
   - The graphs update every few seconds.

3. **Settings Tab**:
   - Change the refresh rate (in seconds) for updating system stats.
   - Set CPU and memory usage alert thresholds.
   - Click "Update Settings" to save changes.

## Alerts

- MonitorX will show a warning message if CPU or memory usage exceeds the thresholds set in the **Settings** tab. This helps keep your system from being overwhelmed by high resource usage.

## Contributing

If you'd like to contribute to **MonitorX**, feel free to submit issues or create pull requests. Any contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**MonitorX** is developed by [Mahmudur Rahman Shibly](https://github.com/mrshibly).
