import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
import time

# Global settings
refresh_rate = 2  # Refresh rate in seconds
cpu_alert_threshold = 80  # CPU usage alert threshold in percentage
memory_alert_threshold = 80  # Memory usage alert threshold in percentage

# Function to update the task list
def update_task_list():
    search_query = search_var.get().lower()
    for row in task_tree.get_children():
        task_tree.delete(row)

    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            name = process.info['name'].lower()
            if search_query in name:
                task_tree.insert('', 'end', values=(
                    process.info['pid'],
                    process.info['name'],
                    process.info['cpu_percent'],
                    process.info['memory_info'].rss / (1024 * 1024)  # Convert to MB
                ))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    root.after(refresh_rate * 1000, update_task_list)  # Update at the specified refresh rate

# Function to kill a selected process
def kill_process():
    try:
        selected_item = task_tree.selection()[0]
        pid = int(task_tree.item(selected_item, 'values')[0])
        process = psutil.Process(pid)
        process.terminate()
        update_task_list()
        error_label.config(text="Process terminated successfully", fg="green")
    except Exception as e:
        error_label.config(text=f"Error: {e}", fg="red")

# Function to show detailed process information
def show_process_details(event):
    try:
        selected_item = task_tree.selection()[0]
        pid = int(task_tree.item(selected_item, 'values')[0])
        process = psutil.Process(pid)
        details = (
            f"Name: {process.name()}\n"
            f"PID: {process.pid}\n"
            f"Status: {process.status()}\n"
            f"Threads: {process.num_threads()}\n"
            f"Memory (RSS): {process.memory_info().rss / (1024 * 1024):.2f} MB\n"
            f"Memory (VMS): {process.memory_info().vms / (1024 * 1024):.2f} MB\n"
            f"CPU Usage: {process.cpu_percent()}%\n"
            f"Open Files: {process.open_files()}"
        )
        messagebox.showinfo("Process Details", details)
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve details: {e}")

# Function to set process priority
def set_priority(priority_level):
    try:
        selected_item = task_tree.selection()[0]
        pid = int(task_tree.item(selected_item, 'values')[0])
        process = psutil.Process(pid)
        process.nice(priority_level)
        error_label.config(text=f"Priority set to {priority_level} for PID {pid}", fg="green")
    except Exception as e:
        error_label.config(text=f"Error: {e}", fg="red")

# Function to refresh resource usage graphs
def update_graphs():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    net_info = psutil.net_io_counters()

    # Update the graphs
    cpu_usage_bar[0].set_height(cpu_percent)
    memory_usage_bar[0].set_height(memory_info.percent)
    disk_usage_bar[0].set_height(disk_info.percent)
    net_sent_bar[0].set_height(net_info.bytes_sent / (1024 * 1024))  # Convert to MB
    net_recv_bar[0].set_height(net_info.bytes_recv / (1024 * 1024))  # Convert to MB
    canvas.draw()

    # Check for high resource usage and send alerts
    if cpu_percent > cpu_alert_threshold:
        messagebox.showwarning("High CPU Usage", f"CPU usage is at {cpu_percent}%!")
    if memory_info.percent > memory_alert_threshold:
        messagebox.showwarning("High Memory Usage", f"Memory usage is at {memory_info.percent}%!")

    root.after(refresh_rate * 1000, update_graphs)  # Update at the specified refresh rate

# Function to update settings
def update_settings():
    global refresh_rate, cpu_alert_threshold, memory_alert_threshold
    try:
        refresh_rate = int(refresh_rate_entry.get())
        cpu_alert_threshold = int(cpu_alert_entry.get())
        memory_alert_threshold = int(memory_alert_entry.get())
        settings_label.config(text="Settings updated successfully", fg="green")
    except ValueError:
        settings_label.config(text="Invalid input. Please enter integers.", fg="red")

# Set up the main window
root = tk.Tk()
root.title("MonitorX: Advanced Task Manager")
root.geometry("1000x800")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Task Manager Tab
task_manager_frame = ttk.Frame(notebook)
notebook.add(task_manager_frame, text="Task Manager")

# Search Bar
search_var = tk.StringVar()
search_entry = ttk.Entry(task_manager_frame, textvariable=search_var)
search_entry.pack(pady=5)
search_entry.bind("<KeyRelease>", lambda event: update_task_list())

# Treeview for processes
columns = ("PID", "Name", "CPU %", "Memory (MB)")
task_tree = ttk.Treeview(task_manager_frame, columns=columns, show='headings')
for col in columns:
    task_tree.heading(col, text=col)
    task_tree.column(col, width=200)
task_tree.pack(fill='both', expand=True)
task_tree.bind("<Double-1>", show_process_details)

# Buttons for process management
button_frame = ttk.Frame(task_manager_frame)
button_frame.pack(pady=5)
kill_button = tk.Button(button_frame, text="Kill Process", command=kill_process)
kill_button.pack(side='left', padx=5)
set_priority_low = tk.Button(button_frame, text="Set Low Priority", command=lambda: set_priority(psutil.IDLE_PRIORITY_CLASS))
set_priority_low.pack(side='left', padx=5)
set_priority_normal = tk.Button(button_frame, text="Set Normal Priority", command=lambda: set_priority(psutil.NORMAL_PRIORITY_CLASS))
set_priority_normal.pack(side='left', padx=5)
set_priority_high = tk.Button(button_frame, text="Set High Priority", command=lambda: set_priority(psutil.HIGH_PRIORITY_CLASS))
set_priority_high.pack(side='left', padx=5)

# Error Label
error_label = tk.Label(task_manager_frame, text="", fg="red")
error_label.pack()

# Resource Monitor Tab
resource_frame = ttk.Frame(notebook)
notebook.add(resource_frame, text="Resource Monitor")

# Resource Usage Graphs
fig, axes = plt.subplots(4, figsize=(6, 8))
fig.tight_layout()

# CPU Usage Graph
axes[0].set_title("CPU Usage (%)")
cpu_usage_bar = axes[0].bar(["CPU"], [0], color='skyblue')
axes[0].set_ylim(0, 100)

# Memory Usage Graph
axes[1].set_title("Memory Usage (%)")
memory_usage_bar = axes[1].bar(["Memory"], [0], color='lightgreen')
axes[1].set_ylim(0, 100)

# Disk Usage Graph
axes[2].set_title("Disk Usage (%)")
disk_usage_bar = axes[2].bar(["Disk"], [0], color='lightcoral')
axes[2].set_ylim(0, 100)

# Network Usage Graph
axes[3].set_title("Network Usage (MB)")
net_sent_bar = axes[3].bar(["Sent"], [0], color='orange')
net_recv_bar = axes[3].bar(["Received"], [0], color='purple')
axes[3].set_ylim(0, 100)

# Embed the graphs in tkinter
canvas = FigureCanvasTkAgg(fig, master=resource_frame)
canvas.get_tk_widget().pack()

# Settings Tab
settings_frame = ttk.Frame(notebook)
notebook.add(settings_frame, text="Settings")

# Settings for refresh rate and alerts
tk.Label(settings_frame, text="Refresh Rate (seconds):").pack(pady=5)
refresh_rate_entry = tk.Entry(settings_frame)
refresh_rate_entry.insert(0, str(refresh_rate))
refresh_rate_entry.pack()

tk.Label(settings_frame, text="CPU Alert Threshold (%):").pack(pady=5)
cpu_alert_entry = tk.Entry(settings_frame)
cpu_alert_entry.insert(0, str(cpu_alert_threshold))
cpu_alert_entry.pack()

tk.Label(settings_frame, text="Memory Alert Threshold (%):").pack(pady=5)
memory_alert_entry = tk.Entry(settings_frame)
memory_alert_entry.insert(0, str(memory_alert_threshold))
memory_alert_entry.pack()

update_button = tk.Button(settings_frame, text="Update Settings", command=update_settings)
update_button.pack(pady=5)

settings_label = tk.Label(settings_frame, text="", fg="green")
settings_label.pack()

# Start updating the task list and graphs
update_task_list()
update_graphs()

# Run the main loop
root.mainloop()
