import tkinter as tk
from tkinter import ttk
import threading
import platform
import psutil
import time
from tkinter import messagebox

root = tk.Tk()
root.configure(bg='#111111')
root.title("System Monitor")
root.geometry("800x600")
root.resizable(True, True)

# Создаем Notebook (вкладки)
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Первая вкладка - системная информация
sysinfo_frame = tk.Frame(notebook, bg='#111111')
notebook.add(sysinfo_frame, text="System Info")

# Вторая вкладка - процессы
process_frame = tk.Frame(notebook, bg='#111111')
notebook.add(process_frame, text="Processes")

# Стили
bigger_font = ("Helvetica", 16, "bold")
smaller_font = ("Helvetica", 13, "bold")
table_font = ("Helvetica", 10)


# ========== Вкладка System Info ==========
def monitoring():
    while True:
        # CPU информация
        cpu_arch = platform.architecture()
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu_name_label.config(
            text=f"CPU architecture: {cpu_arch[0]} {cpu_arch[1]}")
        cpu_percent_label.config(text=f"CPU usage: {cpu_percent}%")
        cpu_count_label.config(text=f"Cores count: {cpu_count}")
        cpu_freq_label.config(
            text=f"CPU freq: {int(cpu_freq.current)}Mhz\nMinimum: {cpu_freq.min}Mhz Maximum: {cpu_freq.max}Mhz")

        # Память
        memory_info = psutil.virtual_memory()
        memory_total_label.config(
            text=f"Total memory: {int(memory_info.total / 1024 ** 2)}mb")
        memory_available_label.config(
            text=f"Available memory: {int(memory_info.available / 1024 ** 2)}mb")
        memory_used_label.config(
            text=f"Memory used: {int(memory_info.used / 1024 ** 2)}mb")
        memory_used_percent.config(text=f"Memory used: {memory_info.percent}%")

        time.sleep(1)


def start_infinite_loop():
    thread = threading.Thread(target=monitoring)
    thread.daemon = True
    thread.start()


# Элементы на вкладке System Info
cpu_section_label = tk.Label(
    sysinfo_frame, text="\nCPU:", font=bigger_font, fg="#FFFFFF", bg='#111111')
cpu_name_label = tk.Label(sysinfo_frame, text="\nCPU name:",
                          font=smaller_font, fg="#FFFFFF", bg='#111111')
cpu_percent_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')
cpu_count_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')
cpu_freq_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')

memory_section_label = tk.Label(
    sysinfo_frame, text="\nRAM:", font=bigger_font, fg="#FFFFFF", bg='#111111')
memory_total_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')
memory_available_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')
memory_used_label = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')
memory_used_percent = tk.Label(
    sysinfo_frame, text="", font=smaller_font, fg="#FFFFFF", bg='#111111')

os = platform.platform()
username = platform.node()
python_version = platform.python_version()

system_section_label = tk.Label(
    sysinfo_frame, text="\nSysInfo:", font=bigger_font, fg="#FFFFFF", bg='#111111')
platform_label = tk.Label(
    sysinfo_frame, text=f"{os}", font=smaller_font, fg="#FFFFFF", bg='#111111')
username_label = tk.Label(
    sysinfo_frame, text=f"{username}", font=smaller_font, fg="#FFFFFF", bg='#111111')
python_version_label = tk.Label(
    sysinfo_frame, text=f"{python_version}", font=smaller_font, fg="#FFFFFF", bg='#111111')

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


# ========== Вкладка Processes ==========
class ProcessManager:
    def __init__(self, frame):
        self.frame = frame
        self.auto_refresh_active = True  # Флаг автоматического обновления
        self.setup_ui()
        self.update_process_list()
        self.start_auto_refresh()

    def setup_ui(self):
        # Панель инструментов
        toolbar = tk.Frame(self.frame, bg='#222222')
        toolbar.pack(fill='x', padx=5, pady=5)

        # Кнопка обновления
        refresh_btn = tk.Button(
            toolbar, text="Refresh", command=self.update_process_list,
            bg='#333333', fg='white', relief='flat')
        refresh_btn.pack(side='left', padx=5)

        # Кнопка завершения процесса
        self.kill_btn = tk.Button(
            toolbar, text="End Process", command=self.kill_selected_process,
            bg='#ff3333', fg='white', relief='flat', state='disabled')
        self.kill_btn.pack(side='left', padx=5)

        # Кнопка остановки/возобновления автообновления
        self.toggle_refresh_btn = tk.Button(
            toolbar, text="Pause Auto-Refresh", command=self.toggle_auto_refresh,
            bg='#555555', fg='white', relief='flat')
        self.toggle_refresh_btn.pack(side='left', padx=5)

        # Поиск
        search_frame = tk.Frame(toolbar, bg='#222222')
        search_frame.pack(side='right', padx=5)
        tk.Label(search_frame, text="Search:", bg='#222222', fg='white').pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.filter_processes)

        # Таблица процессов
        columns = ('pid', 'name', 'status', 'cpu', 'memory')
        self.tree = ttk.Treeview(
            self.frame, columns=columns, show='headings', selectmode='browse')

        # Настройка колонок
        self.tree.heading('pid', text='PID', anchor='w', command=lambda: self.sort_column('pid', False))
        self.tree.heading('name', text='Name', anchor='w', command=lambda: self.sort_column('name', False))
        self.tree.heading('status', text='Status', anchor='w', command=lambda: self.sort_column('status', False))
        self.tree.heading('cpu', text='CPU%', anchor='w', command=lambda: self.sort_column('cpu', True))
        self.tree.heading('memory', text='Memory%', anchor='w', command=lambda: self.sort_column('memory', True))

        self.tree.column('pid', width=80, stretch=False)
        self.tree.column('name', width=200)
        self.tree.column('status', width=100, stretch=False)
        self.tree.column('cpu', width=80, stretch=False)
        self.tree.column('memory', width=80, stretch=False)

        # Скроллбар
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        # Привязка события выбора
        self.tree.bind('<<TreeviewSelect>>', self.on_process_select)

        # Начальная сортировка по CPU
        self.sort_column('cpu', True)

    def start_auto_refresh(self):
        self.auto_refresh_active = True
        self.toggle_refresh_btn.config(text="Pause Auto-Refresh")
        self.auto_refresh()

    def stop_auto_refresh(self):
        self.auto_refresh_active = False
        self.toggle_refresh_btn.config(text="Resume Auto-Refresh")

    def toggle_auto_refresh(self):
        if self.auto_refresh_active:
            self.stop_auto_refresh()
        else:
            self.start_auto_refresh()

    def auto_refresh(self):
        if self.auto_refresh_active:
            self.update_process_list()
            self.frame.after(1000, self.auto_refresh)

    def update_process_list(self):
        # Получаем список процессов
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            try:
                # Нормализуем CPU% (делим на количество ядер)
                cpu_cores = psutil.cpu_count()
                cpu_percent = proc.info['cpu_percent'] / cpu_cores if cpu_cores else proc.info['cpu_percent']

                processes.append((
                    proc.info['pid'],
                    proc.info['name'],
                    proc.info['status'],
                    f"{cpu_percent:.1f}",
                    f"{proc.info['memory_percent']:.1f}"
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        # Обновляем таблицу
        for child in self.tree.get_children():
            self.tree.delete(child)

        for proc in processes:
            self.tree.insert('', 'end', values=proc)

        # Применяем текущую сортировку
        self.apply_sort()

        # Применяем фильтр, если есть поисковый запрос
        if self.search_entry.get():
            self.filter_processes()

    def sort_column(self, col, is_numeric):
        # Получаем текущую сортировку
        current_sort = getattr(self, 'sort_column_data', None)

        if current_sort and current_sort['column'] == col:
            # Если уже сортируется по этой колонке, меняем направление
            self.sort_column_data = {
                'column': col,
                'reverse': not current_sort['reverse'],
                'is_numeric': is_numeric
            }
        else:
            # Иначе сортируем по новой колонке
            self.sort_column_data = {
                'column': col,
                'reverse': False,
                'is_numeric': is_numeric
            }

        self.apply_sort()

    def apply_sort(self):
        if hasattr(self, 'sort_column_data'):
            col = self.sort_column_data['column']
            reverse = self.sort_column_data['reverse']
            is_numeric = self.sort_column_data['is_numeric']

            # Получаем все элементы
            items = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

            # Сортируем
            if is_numeric:
                # Для числовых значений
                items.sort(key=lambda x: float(x[0].replace('%', '')), reverse=reverse)
            else:
                # Для текстовых значений
                items.sort(key=lambda x: x[0].lower(), reverse=reverse)

            # Перемещаем элементы в отсортированном порядке
            for index, (val, child) in enumerate(items):
                self.tree.move(child, '', index)

    def filter_processes(self, event=None):
        search_term = self.search_entry.get().lower()

        for child in self.tree.get_children():
            values = self.tree.item(child)['values']
            if search_term in values[1].lower():  # Ищем по имени процесса
                self.tree.item(child, tags=('match',))
                self.tree.detach(child)
                self.tree.attach(child, '', '0')  # Перемещаем в начало
            else:
                self.tree.detach(child)
                self.tree.attach(child, '', 'end')  # Перемещаем в конец

    def on_process_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.kill_btn.config(state='normal')
        else:
            self.kill_btn.config(state='disabled')

    def kill_selected_process(self):
        selected = self.tree.selection()
        if not selected:
            return

        pid = int(self.tree.item(selected[0])['values'][0])
        name = self.tree.item(selected[0])['values'][1]

        try:
            process = psutil.Process(pid)
            response = messagebox.askyesno(
                "Confirm End Process",
                f"Are you sure you want to end the process '{name}' (PID: {pid})?")

            if response:
                process.terminate()
                self.update_process_list()
                messagebox.showinfo(
                    "Success",
                    f"Process '{name}' (PID: {pid}) has been terminated.")
        except psutil.NoSuchProcess:
            messagebox.showerror(
                "Error",
                f"Process with PID {pid} no longer exists.")
            self.update_process_list()
        except psutil.AccessDenied:
            messagebox.showerror(
                "Error",
                f"Access denied. Cannot terminate process '{name}' (PID: {pid}).")
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to terminate process: {str(e)}")


# Создаем менеджер процессов
process_manager = ProcessManager(process_frame)

# Запускаем мониторинг
root.after(100, start_infinite_loop)
root.mainloop()