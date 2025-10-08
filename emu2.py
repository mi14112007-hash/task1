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
    if not input_string.strip():
        return "", []
    
    # Сначала раскрываем переменные окружения
    expanded_input = expand_environment_variables(input_string)
    
    # Затем разбиваем на команду и аргументы
    parts = expanded_input.split()
    if not parts:
        return "", []
    
    command = parts[0]
    args = parts[1:]
    
    return command, args

def execute_script(script_path, output_callback=None):
    """Выполнение скрипта с командами эмулятора"""
    try:
        if not os.path.exists(script_path):
            if output_callback:
                output_callback(f"Ошибка: файл скрипта не найден: {script_path}")
            return False
        
        with open(script_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        error_occurred = False
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Пропускаем пустые строки
            if not line:
                continue
                
            # Показываем ввод в выводе
            if output_callback:
                output_callback(f"vfs@ {line}")
            
            # Выполняем команду
            result = act(line)
            
            # Показываем результат
            if output_callback:
                output_callback(result)
            
            # Проверяем на ошибку (останавливаемся при первой ошибке)
            if "command not found" in result or "Ошибка" in result:
                error_occurred = True
                if output_callback:
                    output_callback(f"Ошибка в строке {line_num}: {line}")
                break
        
        return not error_occurred
        
    except Exception as e:
        if output_callback:
            output_callback(f"Ошибка выполнения скрипта: {str(e)}")
        return False

def act(a):
    if a.strip() == "exit":
        exit()
    
    if len(a.strip()) == 0:
        return ""
    
    command, args = parse_command(a)
    
    if command == "ls":
        try:
            if not args:
                # ls без аргументов - показываем текущую директорию
                files = os.listdir('.')
                return "\n".join(files) if files else "Директория пуста"
            else:
                # ls с аргументами - эмулируем поведение
                target_path = args[0] if args else "."
                if os.path.exists(target_path):
                    files = os.listdir(target_path)
                    return f"Содержимое {target_path}:\n" + "\n".join(files) if files else "Директория пуста"
                else:
                    return f"Ошибка: путь не существует: {target_path}"
        except Exception as e:
            return f"Ошибка ls: {str(e)}"
    
    elif command == "cd":
        try:
            if args:
                target_dir = args[0]
                os.chdir(target_dir)  # Меняем реальную директорию
                return f"Переход в директорию: {os.getcwd()}"
            else:
                # Если cd без аргументов - переходим в домашнюю директорию
                home_dir = os.getenv('HOME')
                if home_dir:
                    os.chdir(home_dir)
                    return f"Переход в домашнюю директорию: {os.getcwd()}"
                else:
                    return "Ошибка: домашняя директория не найдена"
        except Exception as e:
            return f"Ошибка cd: {str(e)}"
    
    elif command == "echo":
        return ' '.join(args) if args else ""
    
    elif command == "pwd":
        return f"Текущая директория: {os.getcwd()}"
    
    elif command == "whoami":
        return f"Текущий пользователь: {os.getlogin()}"
    
    elif command == "date":
        from datetime import datetime
        return f"Текущая дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    else:
        return f"{command}: command not found"

if __name__ == "__main__":
    # Консольная версия (для тестирования)
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
        # Выполняем стартовый скрипт если указан
        if os.path.exists(script_path):
            def console_output(text):
                print(text)
            execute_script(script_path, console_output)

    while True:
        a = input(f'{prompt}> ')
        print(act(a))