import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from emu2 import act, execute_script
import os
import socket
import sys

class ConsoleEmulator:
    def __init__(self, root, vfs_path="", script_path=""):
        self.root = root
        self.vfs_path = vfs_path
        self.script_path = script_path
        
        # Получаем реальные данные ОС для заголовка
        username = os.getlogin()
        hostname = socket.gethostname()
        window_title = f"Эмулятор - [{username}@{hostname}]"
        
        self.root.title(window_title)
        self.root.geometry("1200x400")
        
        self.setup_ui()
        
        # Автоматически выполняем стартовый скрипт если указан
        if self.script_path and os.path.exists(self.script_path):
            self.execute_startup_script()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выполнить скрипт", command=self.run_script_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)

        # Область вывода
        self.output_text = scrolledtext.ScrolledText(self.main_frame, height=20, width=70)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.output_text.config(state=tk.DISABLED)

        # Панель ввода
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X)

        self.prompt_label = tk.Label(self.input_frame, text="vfs@", font=("Courier", 10))
        self.prompt_label.pack(side=tk.LEFT)

        self.input_entry = tk.Entry(self.input_frame, font=("Courier", 10))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind('<Return>', self.process_command)

        self.enter_button = tk.Button(self.input_frame, text="Enter", command=self.process_command)
        self.enter_button.pack(side=tk.RIGHT)

        self.input_entry.focus()

    def print_output(self, text):
        """Вывод текста в область вывода"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"{text}\n")
        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def process_command(self, event=None):
        """Обработка команды из интерфейса"""
        a = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        
        self.print_output(f"vfs@ {a}")
        output = act(a)
        self.print_output(output)

    def execute_startup_script(self):
        """Выполнение стартового скрипта"""
        try:
            self.print_output(f"=== Выполнение стартового скрипта: {self.script_path} ===")
            success = execute_script(self.script_path, self.print_output)
            if success:
                self.print_output("=== Стартовый скрипт выполнен успешно ===")
            else:
                self.print_output("=== Ошибка выполнения стартового скрипта ===")
        except Exception as e:
            self.print_output(f"Ошибка при выполнении скрипта: {str(e)}")

    def run_script_dialog(self):
        """Диалог выбора скрипта"""
        filename = filedialog.askopenfilename(
            title="Выберите скрипт для выполнения",
            filetypes=[("Все файлы", "*.*"), ("Python файлы", "*.py"), ("Текстовые файлы", "*.txt")]
        )
        if filename:
            try:
                self.print_output(f"=== Выполнение скрипта: {filename} ===")
                success = execute_script(filename, self.print_output)
                if success:
                    self.print_output("=== Скрипт выполнен успешно ===")
                else:
                    self.print_output("=== Ошибка выполнения скрипта ===")
            except Exception as e:
                self.print_output(f"Ошибка при выполнении скрипта: {str(e)}")

def parse_arguments():
    """Парсинг аргументов командной строки"""
    args = sys.argv[1:]
    vfs_path = ""
    script_path = ""
    config_path = ""
    
    i = 0
    while i < len(args):
        if args[i] == "--vfs" and i + 1 < len(args):
            vfs_path = args[i + 1]
            i += 1
        elif args[i] == "--script" and i + 1 < len(args):
            script_path = args[i + 1]
            i += 1
        elif args[i] == "--config" and i + 1 < len(args):
            config_path = args[i + 1]
            i += 1
        i += 1
    
    return vfs_path, script_path, config_path

if __name__ == "__main__":
    vfs_path, script_path, config_path = parse_arguments()
    
    root = tk.Tk()
    app = ConsoleEmulator(root, vfs_path, script_path)
    root.mainloop()