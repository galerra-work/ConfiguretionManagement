import struct
import yaml
import sys

def assemble_instruction(command, args):
    print(command, args)
    if command == "LOAD_CONST":
        # Пример для LOAD_CONST A B C
        assert len(args) == 3, "LOAD_CONST requires 3 arguments"
        A, B, C = args
        return struct.pack("<BHI", A, B, C)  # Пакуем в байты
    
    elif command == "LOAD_MEM":
        print("Я в load_mem")
        # Пример для LOAD_MEM A B C
        assert len(args) == 3, "LOAD_MEM requires 3 arguments"
        A, B, C = args
        return struct.pack("<BHI", A, B, C)

    elif command == "WRITE_MEM":
        # Пример для WRITE_MEM A B C D
        assert len(args) == 4, "WRITE_MEM requires 4 arguments"
        A, B, C, D = args
        return struct.pack("<BHIH", A, B, C, D)
    
    else:
        raise ValueError(f"Unknown command: {command}")

# Ассемблер
def assemble(input_file, output_binary, output_log):
    with open(input_file, "r") as infile:
        lines = infile.readlines()

    binary_code = bytearray()  # Массив для бинарного кода
    log = {}  # Лог для YAML

    for line in lines:
        # Разбиваем команду на части
        parts = line.strip().split()
        command = parts[0]
        args = list(map(int, parts[1:]))

        # Ассемблируем команду
        binary = assemble_instruction(command, args)
        binary_code.extend(binary)

        # Записываем в лог
        log[f"{command} {' '.join(map(str, args))}"] = list(binary)

    # Сохраняем бинарный файл
    with open(output_binary, "wb") as bin_file:
        bin_file.write(binary_code)

    # Сохраняем лог в формате YAML
    with open(output_log, "w") as log_file:
        yaml.dump(log, log_file, default_flow_style=False)

if __name__ == "__main__":
    input_file = sys.argv[1]  # Путь к входному файлу
    output_binary = sys.argv[2]  # Путь к бинарному файлу
    output_log = sys.argv[3]  # Путь к файлу лога
    assemble(input_file, output_binary, output_log)
