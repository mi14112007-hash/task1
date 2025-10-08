import sys
import os
import re

def expand_environment_variables(text):
    """Раскрывает переменные окружения в формате $VARIABLE"""
    def replace_var(match):
        var_name = match.group(1)
        return os.getenv(var_name, '')
    
    return re.sub(r'\$(\w+)', replace_var, text)

def parse_command(input_string):
    """Парсер с поддержкой раскрытия переменных окружения"""
    # Сначала раскрываем переменные окружения
    expanded_input = expand_environment_variables(input_string)
    
    # Затем разбиваем на команду и аргументы
    parts = expanded_input.split()
    if not parts:
        return "", []
    
    command = parts[0]
    args = parts[1:]
    
    return command, args

def act(a):
    if a == "exit":
        exit()
    
    if len(a) == 0:
        return ""
    
    command, args = parse_command(a)
    
    # Обработка команд
    if command == "ls":
        return f"ls: {' '.join(args)}" if args else "ls"
    elif command == "cd":
        return f"cd: {' '.join(args)}" if args else "cd"
    elif command == "echo":
        # ВАЖНО: команда echo просто возвращает свои аргументы
        return ' '.join(args) if args else ""
    else:
        return f"{command}: command not found"

if __name__ == "__main__":
    args = sys.argv

    if len(args) > 1:
        path = args[1]
    else:
        path = ""
    
    if len(args) > 2:
        prompt = args[2]
    else:
        prompt = "vfs"
    
    if len(args) > 3:
        script_path = args[3]
    else:
        script_path = ""

    while True:
        a = input(f'{prompt}> ')
        print(act(a))