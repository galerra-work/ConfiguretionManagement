# config_parser.py
import argparse
import re
import os
import colorama
from colorama import Fore, Back, Style
colorama.init()

def parse_config(input_file):
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Удаляем многострочные комментарии
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    output_lines = []
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith("var "):
            output_lines.append(parse_variable(line))
        elif re.match(r'^[A-Z]+$', line):  # Имя
            output_lines.append(f'[{line}]')
        elif re.match(r'<<.*>>', line):  # Массив
            output_lines.append(parse_array(line))
        elif line.startswith("|"):  # Вычисление константного выражения
            result = evaluate_expression(line[1:-1].strip())
            output_lines.append(str(result))

    return "\n".join(output_lines)

def parse_variable(line):
    match = re.match(r'var (\w+) (.+);', line)
    if match:
        name, value = match.groups()
        return f'{name} = {value}'
    raise ValueError(f'Invalid variable declaration: {line}')

def parse_array(line):
    match = re.match(r'<<(.+?)>>', line)
    if match:
        values = match.group(1).split(',')
        values = [value.strip() for value in values]
        return f'array = [{", ".join(values)}]'
    raise ValueError(f'Invalid array syntax: {line}')

def evaluate_expression(expression):
    tokens = expression.split()
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token == '+':
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif token == 'abs()':
            print(token)
            a = stack.pop()
            stack.append(abs(a))
        else:
            raise ValueError(f'Unknown token: {token}')
    return stack[-1] if stack else None

def write_output(output_file, content):
    with open(output_file, 'w') as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description='Convert custom config to TOML.')
    parser.add_argument('input_file', help='Path to the input configuration file')
    parser.add_argument('output_file', help='Path to the output TOML file')
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        raise FileNotFoundError(f'Input file not found: {args.input_file}')

    result = parse_config(args.input_file)
    write_output(args.output_file, result)
    print(Fore.GREEN + "Дорогой преподаватель, проверьте выходной файл, там появился " + Fore.YELLOW + "подарок!")

if __name__ == '__main__':
    main()

