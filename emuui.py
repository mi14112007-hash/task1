import tkinter as tk
from tkinter import scrolledtext
from emu import act
import os
import socket

def process_command(event=None):
    a = input_entry.get()
    input_entry.delete(0, tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, f"vfs@ {a} \n")
    output = act(a)
    output_text.insert(tk.END, f"{output}\n")
    output_text.config(state=tk.DISABLED)
    output_text.see(tk.END)

# Получаем реальные данные ОС для заголовка
username = os.getlogin()
hostname = socket.gethostname()
window_title = f"Эмулятор - [{username}@{hostname}]"

root = tk.Tk()
root.title(window_title)
root.geometry("1200x400")

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(main_frame, height=20, width=70)
output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
output_text.config(state=tk.DISABLED)

input_frame = tk.Frame(main_frame)
input_frame.pack(fill=tk.X)

prompt_label = tk.Label(input_frame, text="vfs@", font=("Courier", 10))
prompt_label.pack(side=tk.LEFT)

input_entry = tk.Entry(input_frame, font=("Courier", 10))
input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
input_entry.bind('<Return>', process_command)

enter_button = tk.Button(input_frame, text="Enter", command=process_command)
enter_button.pack(side=tk.RIGHT)

input_entry.focus()
root.mainloop()