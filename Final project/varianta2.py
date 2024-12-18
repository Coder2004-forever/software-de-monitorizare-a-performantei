import tkinter as tk
from tkinter import ttk
import psutil
import time
import pynvml
from pynvml import *
import threading
from tkinter import messagebox

# Initialize NVML for GPU monitoring
NVML_AVAILABLE = False
try:
    nvmlInit()
    NVML_AVAILABLE = True
except Exception as e:
    print(f"GPU monitoring not available: {e}")


# Function to update system stats
def update_system_stats():
    while True:
        # CPU Usage
        cpu_usage = psutil.cpu_percent()
        cpu_freq = psutil.cpu_freq().current
        cpu_threads = psutil.cpu_count(logical=True)

        # Memory Usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        memory_total = memory.total / (1024 * 1024)  # Convert to MB
        memory_free = memory.available / (1024 * 1024)  # Convert to MB

        # Disk Usage
        disk = psutil.disk_usage('/') #root directory
        disk_usage = disk.percent
        disk_total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
        disk_free = disk.free / (1024 * 1024 * 1024)  # Convert to GB

        # Network Usage
        net_io = psutil.net_io_counters()
        data_sent = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        data_received = net_io.bytes_recv / (1024 * 1024)  # Convert to MB

        # GPU Metrics (if available)
        if NVML_AVAILABLE:
            try:
                handle = nvmlDeviceGetHandleByIndex(0)  # Asigură-te că GPU-ul există la indexul 0
                gpu_temp = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
                gpu_util = nvmlDeviceGetUtilizationRates(handle).gpu
                gpu_mem_info = nvmlDeviceGetMemoryInfo(handle)
                gpu_memory_used = gpu_mem_info.used / (1024 * 1024)  # Convert to MB
                gpu_memory_total = gpu_mem_info.total / (1024 * 1024)  # Convert to MB
            except pynvml.NVMLError as e:
                print(f"Error accessing GPU: {e}")
                gpu_temp = gpu_util = gpu_memory_used = gpu_memory_total = "N/A"
        else:
            gpu_temp = gpu_util = gpu_memory_used = gpu_memory_total = "N/A"



        # Actualizarea interfeței grafice cu cele mai recente date
        cpu_label_value.config(text=f"{cpu_usage}%")
        cpu_freq_label_value.config(text=f"{cpu_freq:.2f} MHz")
        cpu_threads_label_value.config(text=f"{cpu_threads}")
        memory_label_value.config(text=f"{memory_usage}%")
        memory_total_label_value.config(text=f"{memory_total:.2f} MB")
        memory_free_label_value.config(text=f"{memory_free:.2f} MB")
        disk_label_value.config(text=f"{disk_usage}%")
        disk_total_label_value.config(text=f"{disk_total:.2f} GB")
        disk_free_label_value.config(text=f"{disk_free:.2f} GB")
        net_sent_label_value.config(text=f"{data_sent:.2f} MB")
        net_recv_label_value.config(text=f"{data_received:.2f} MB")

        # Verifică dacă valorile pentru GPU sunt valabile (nu sunt șiruri de caractere)
        if NVML_AVAILABLE and isinstance(gpu_memory_used, (int, float)) and isinstance(gpu_memory_total, (int, float)):
            gpu_mem_label_value.config(text=f"{gpu_memory_used:.2f} MB / {gpu_memory_total:.2f} MB")
        else:
            gpu_mem_label_value.config(text="N/A")

        # Verifică dacă GPU-ul este disponibil și formatează corespunzător temperatura și utilizarea
        if NVML_AVAILABLE and isinstance(gpu_temp, (int, float)):
            gpu_temp_label_value.config(text=f"{gpu_temp}°C")
        else:
            gpu_temp_label_value.config(text="N/A")

        if NVML_AVAILABLE and isinstance(gpu_util, (int, float)):
            gpu_util_label_value.config(text=f"{gpu_util}%")
        else:
            gpu_util_label_value.config(text="N/A")

        time.sleep(1)


# Initialize the GUI
root = tk.Tk()
root.title("System Monitor")
root.geometry("600x600")
root.configure(bg="#2c3e50")

# Define styles
style = ttk.Style()
style.theme_use("clam")

# Custom colors for the interface
style.configure("TLabel", font=("Helvetica", 12, "bold"), foreground="#FFFFFF")
style.configure("TButton", font=("Helvetica", 12, "bold"), background="#4CAF50", foreground="#FFFFFF", padding=10)
style.configure("TProgressbar", thickness=20, troughcolor="#2c3e50", background="#3498db")

# CPU Metrics Frame
cpu_frame = ttk.Frame(root, padding=10, style="TFrame")
cpu_frame.pack(fill=tk.X, pady=5)

tk.Label(cpu_frame, text="CPU Usage:", font=("Helvetica", 14), anchor="w", background="#3498db").pack(side=tk.LEFT)
cpu_label_value = tk.Label(cpu_frame, text="0%", font=("Helvetica", 12), anchor="e", background="#3498db",
                           foreground="#FFFFFF")
cpu_label_value.pack(side=tk.RIGHT)
cpu_bar = ttk.Progressbar(cpu_frame, orient="horizontal", mode="determinate", maximum=100)
cpu_bar.pack(fill=tk.X, pady=5)

tk.Label(cpu_frame, text="Frequency:", font=("Helvetica", 14), anchor="w", background="#3498db").pack(side=tk.LEFT)
cpu_freq_label_value = tk.Label(cpu_frame, text="0.00 MHz", font=("Helvetica", 12), anchor="e", background="#3498db",
                                foreground="#FFFFFF")
cpu_freq_label_value.pack(side=tk.RIGHT)

tk.Label(cpu_frame, text="Threads:", font=("Helvetica", 14), anchor="w", background="#3498db").pack(side=tk.LEFT)
cpu_threads_label_value = tk.Label(cpu_frame, text="0", font=("Helvetica", 12), anchor="e", background="#3498db",
                                   foreground="#FFFFFF")
cpu_threads_label_value.pack(side=tk.RIGHT)

# Memory Metrics Frame
memory_frame = ttk.Frame(root, padding=10, style="TFrame")
memory_frame.pack(fill=tk.X, pady=5)

tk.Label(memory_frame, text="Memory Usage:", font=("Helvetica", 14), anchor="w", background="#E74C3C").pack(
    side=tk.LEFT)
memory_label_value = tk.Label(memory_frame, text="0%", font=("Helvetica", 12), anchor="e", background="#E74C3C",
                              foreground="#FFFFFF")
memory_label_value.pack(side=tk.RIGHT)
memory_bar = ttk.Progressbar(memory_frame, orient="horizontal", mode="determinate", maximum=100)
memory_bar.pack(fill=tk.X, pady=5)

tk.Label(memory_frame, text="Total Memory:", font=("Helvetica", 14), anchor="w", background="#E74C3C").pack(
    side=tk.LEFT)
memory_total_label_value = tk.Label(memory_frame, text="0 MB", font=("Helvetica", 12), anchor="e", background="#E74C3C",
                                    foreground="#FFFFFF")
memory_total_label_value.pack(side=tk.RIGHT)

tk.Label(memory_frame, text="Available Memory:", font=("Helvetica", 14), anchor="w", background="#E74C3C").pack(
    side=tk.LEFT)
memory_free_label_value = tk.Label(memory_frame, text="0 MB", font=("Helvetica", 12), anchor="e", background="#E74C3C",
                                   foreground="#FFFFFF")
memory_free_label_value.pack(side=tk.RIGHT)

# Disk Metrics Frame
disk_frame = ttk.Frame(root, padding=10, style="TFrame")
disk_frame.pack(fill=tk.X, pady=5)

tk.Label(disk_frame, text="Disk Usage:", font=("Helvetica", 14), anchor="w", background="#F39C12").pack(side=tk.LEFT)
disk_label_value = tk.Label(disk_frame, text="0%", font=("Helvetica", 12), anchor="e", background="#F39C12",
                            foreground="#FFFFFF")
disk_label_value.pack(side=tk.RIGHT)
disk_bar = ttk.Progressbar(disk_frame, orient="horizontal", mode="determinate", maximum=100)
disk_bar.pack(fill=tk.X, pady=5)

tk.Label(disk_frame, text="Total Disk:", font=("Helvetica", 14), anchor="w", background="#F39C12").pack(side=tk.LEFT)
disk_total_label_value = tk.Label(disk_frame, text="0 GB", font=("Helvetica", 12), anchor="e", background="#F39C12",
                                  foreground="#FFFFFF")
disk_total_label_value.pack(side=tk.RIGHT)

tk.Label(disk_frame, text="Free Disk:", font=("Helvetica", 14), anchor="w", background="#F39C12").pack(side=tk.LEFT)
disk_free_label_value = tk.Label(disk_frame, text="0 GB", font=("Helvetica", 12), anchor="e", background="#F39C12",
                                 foreground="#FFFFFF")
disk_free_label_value.pack(side=tk.RIGHT)

# Network Metrics Frame
network_frame = ttk.Frame(root, padding=10, style="TFrame")
network_frame.pack(fill=tk.X, pady=5)

tk.Label(network_frame, text="Data Sent:", font=("Helvetica", 14), anchor="w", background="#8E44AD").pack(side=tk.LEFT)
net_sent_label_value = tk.Label(network_frame, text="0 MB", font=("Helvetica", 12), anchor="e", background="#8E44AD",
                                foreground="#FFFFFF")
net_sent_label_value.pack(side=tk.RIGHT)

tk.Label(network_frame, text="Data Received:", font=("Helvetica", 14), anchor="w", background="#8E44AD").pack(
    side=tk.LEFT)
net_recv_label_value = tk.Label(network_frame, text="0 MB", font=("Helvetica", 12), anchor="e", background="#8E44AD",
                                foreground="#FFFFFF")
net_recv_label_value.pack(side=tk.RIGHT)

# GPU Metrics Frame (if available)
if NVML_AVAILABLE:
    gpu_frame = ttk.Frame(root, padding=10, style="TFrame")
    gpu_frame.pack(fill=tk.X, pady=5)

    tk.Label(gpu_frame, text="GPU Temp:", font=("Helvetica", 14), anchor="w", background="#1ABC9C").pack(side=tk.LEFT)
    gpu_temp_label_value = tk.Label(gpu_frame, text="N/A", font=("Helvetica", 12), anchor="e", background="#1ABC9C",
                                    foreground="#FFFFFF")
    gpu_temp_label_value.pack(side=tk.RIGHT)

    tk.Label(gpu_frame, text="GPU Utilization:", font=("Helvetica", 14), anchor="w", background="#1ABC9C").pack(
        side=tk.LEFT)
    gpu_util_label_value = tk.Label(gpu_frame, text="N/A", font=("Helvetica", 12), anchor="e", background="#1ABC9C",
                                    foreground="#FFFFFF")
    gpu_util_label_value.pack(side=tk.RIGHT)

    tk.Label(gpu_frame, text="GPU Memory:", font=("Helvetica", 14), anchor="w", background="#1ABC9C").pack(side=tk.LEFT)
    gpu_mem_label_value = tk.Label(gpu_frame, text="N/A", font=("Helvetica", 12), anchor="e", background="#1ABC9C",
                                   foreground="#FFFFFF")
    gpu_mem_label_value.pack(side=tk.RIGHT)

# Motherboard Metrics Frame
mobo_frame = ttk.Frame(root, padding=10)
mobo_frame.pack(fill=tk.X)

tk.Label(mobo_frame, text="Motherboard Temps:", font=("Helvetica", 12, "bold"), anchor="w", background="#7FFFD4").pack(
    side=tk.LEFT)
mobo_temp_label_value = tk.Label(mobo_frame, text="N/A", font=("Helvetica", 12), anchor="e", background="#7FFFD4")
mobo_temp_label_value.pack(side=tk.RIGHT)

tk.Label(mobo_frame, text="Voltage:", font=("Helvetica", 12, "bold"), anchor="w", background="#7FFFD4").pack(
    side=tk.LEFT)
mobo_voltage_label_value = tk.Label(mobo_frame, text="N/A", font=("Helvetica", 12), anchor="e", background="#7FFFD4")
mobo_voltage_label_value.pack(side=tk.RIGHT)

# Power Metrics Frame
power_frame = ttk.Frame(root, padding=10)
power_frame.pack(fill=tk.X)

tk.Label(power_frame, text="Power Consumption:", font=("Helvetica", 12, "bold"), anchor="w").pack(side=tk.LEFT)
power_consumption_label_value = tk.Label(power_frame, text="N/A", font=("Helvetica", 12), anchor="e")
power_consumption_label_value.pack(side=tk.RIGHT)

tk.Label(power_frame, text="Battery Status:", font=("Helvetica", 12, "bold"), anchor="w").pack(side=tk.LEFT)
battery_status_label_value = tk.Label(power_frame, text="N/A", font=("Helvetica", 12), anchor="e")
battery_status_label_value.pack(side=tk.RIGHT)


# Simulator Button Functionality
def open_simulator():
    simulator_window = tk.Toplevel(root)
    simulator_window.title("Simulator")
    tk.Label(simulator_window, text="Simulator Values", font=("Helvetica", 14, "bold")).pack(pady=10)
    entries = {}
    metrics = [
        ("GPU Temp", "30-100"),
        ("GPU Utilization", "0-100"),
        ("GPU Memory", "0-16"),
        ("Motherboard Temp", "30-100"),
        ("Voltage", "0.8-1.5"),
        ("Power Consumption", "0-1200"),
        ("Battery Status", "0-100"),
    ]
    for metric, range_ in metrics:
        frame = ttk.Frame(simulator_window, padding=5)
        frame.pack(fill=tk.X)
        tk.Label(frame, text=f"{metric} ({range_}):", font=("Helvetica", 12), anchor="w").pack(side=tk.LEFT)
        entry = ttk.Entry(frame)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        entries[metric] = entry

    def simulate():
        try:
            # Validate and update main labels with simulated values
            for metric, range_ in metrics:
                value = entries[metric].get().strip()  # Strip whitespace from input
                if not value:  # Check if the entry is empty
                    tk.messagebox.showwarning("Warning", f"{metric} is empty!")
                    return
                try:
                    value = float(value)  # Attempt to convert input to a float
                except ValueError:
                    tk.messagebox.showwarning("Warning", f"{metric} must be a valid number!")
                    return
                min_val, max_val = map(float, range_.split('-'))
                if value < min_val:
                    tk.messagebox.showwarning("Warning", f"{metric} is too low! Minimum is {min_val}.")
                    return
                if value > max_val:
                    tk.messagebox.showwarning(
                        "Warning",
                        f"{metric} is too high! Maximum is {max_val}.\nIt is recommended to shut down the system to prevent damage."
                    )
                    return
            # Specific condition for Battery Status
            battery_value = float(entries["Battery Status"].get().strip())
            if battery_value < 15:
                messagebox.showwarning(
                    "Battery Low",
                    "Battery level is below 15%. Please plug in your charger to avoid system shutdown."
                )
            # Update labels with the simulated values
            gpu_temp_label_value.config(text=entries["GPU Temp"].get())
            gpu_util_label_value.config(text=entries["GPU Utilization"].get())
            gpu_mem_label_value.config(text=entries["GPU Memory"].get())
            mobo_temp_label_value.config(text=entries["Motherboard Temp"].get())
            mobo_voltage_label_value.config(text=entries["Voltage"].get())
            power_consumption_label_value.config(text=entries["Power Consumption"].get())
            battery_status_label_value.config(text=entries["Battery Status"].get())
        except Exception as e:
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    simulate_button = ttk.Button(simulator_window, text="Simulate", command=simulate)
    simulate_button.pack(pady=10)


# Add Simulator Button
simulator_button = ttk.Button(root, text="Simulator", command=open_simulator)
simulator_button.pack(pady=10)

# Start the update loop in a separate thread
thread = threading.Thread(target=update_system_stats, daemon=True)
thread.start()

# Run the GUI
root.mainloop()