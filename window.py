import tkinter as tk
import threading
import platform
import psutil
import time

root = tk.Tk()

root.configure(bg='#111111')

root.title("Name")
root.geometry("400x500")
root.resizable(False, False)

custom_font1 = ("Helvetica", 16, "bold")
custom_font2 = ("Helvetica", 13, "bold")


def monitoring():
    while True:
        cpu_arch = platform.architecture()
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_name_label.config(
            text=f"CPU architecture: {cpu_arch[0]} {cpu_arch[1]}")
        cpu_percent_label.config(text=f"CPU usage: {cpu_percent}%")
        cpu_count_label.config(text=f"Cores count: {cpu_count}")
        cpu_freq_label.config(
            text=f"CPU freq: {int(cpu_freq[0])}Mhz\nMinimum: {cpu_freq[1]}Mhz Maximum: {cpu_freq[2]}Mhz")

        memory_info = psutil.virtual_memory()
        memory_total_label.config(
            text=f"Total memory: {int(memory_info.total / 1024**2)}mb")
        memory_available_label.config(
            text=f"Available memory: {int(memory_info.available / 1024**2)}mb")
        memory_used_label.config(
            text=f"Memory used: {int(memory_info.used / 1024**2)}mb")
        memory_used_percent.config(text=f"Memory used: {memory_info.percent}%")

        time.sleep(1)


def start_infinite_loop():
    thread = threading.Thread(target=monitoring)
    thread.daemon = True
    thread.start()


cpu_section_label = tk.Label(
    root, text="\nCPU:", font=custom_font1, fg="#FFFFFF", bg='#111111')
cpu_name_label = tk.Label(root, text="\nCPU name:",
                          font=custom_font2, fg="#FFFFFF", bg='#111111')
cpu_percent_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')
cpu_count_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')
cpu_freq_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')

memory_section_label = tk.Label(
    root, text="\nRAM:", font=custom_font1, fg="#FFFFFF", bg='#111111')
memory_total_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')
memory_available_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')
memory_used_label = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')
memory_used_percent = tk.Label(
    root, text="", font=custom_font2, fg="#FFFFFF", bg='#111111')

os = platform.platform()
username = platform.node()
python_version = platform.python_version()

system_section_label = tk.Label(
    root, text="\nSysInfo:", font=custom_font1, fg="#FFFFFF", bg='#111111')
platform_label = tk.Label(
    root, text=f"{os}", font=custom_font2, fg="#FFFFFF", bg='#111111')
username_label = tk.Label(
    root, text=f"{username}", font=custom_font2, fg="#FFFFFF", bg='#111111')
python_version_label = tk.Label(
    root, text=f"{python_version}", font=custom_font2, fg="#FFFFFF", bg='#111111')

cpu_section_label.pack()
cpu_name_label.pack()
cpu_percent_label.pack()
cpu_count_label.pack()
cpu_freq_label.pack()

memory_section_label.pack()
memory_total_label.pack()
memory_available_label.pack()
memory_used_label.pack()
memory_used_percent.pack()

system_section_label.pack()
platform_label.pack()
username_label.pack()
python_version_label.pack()

root.after(100, start_infinite_loop)

root.mainloop()
