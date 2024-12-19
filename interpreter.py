import struct
import yaml
import sys

# Структура памяти УВМ
memory = [0] * 20000  # Предположим, что у нас есть 1024 ячейки памяти

def execute_instruction(binary_code, pc):
    # Чтение первой части команды
    try:
        A, B, C = struct.unpack("<BHI", binary_code[pc:pc+7])  # Загрузка команд
    except:
        A, B, C = struct.unpack("<BHIH", binary_code[pc:pc+9])
    if A == 195:  # LOAD_CONST
        memory[B] = C
        print("1!")
    elif A == 83:  # LOAD_MEM
        print("2!")
        memory[B] = memory[C]  # Загружаем значение из памяти по индексу C в ячейку B
    elif A == 53:  # WRITE_MEM
        print("3!")
        D = struct.unpack("<H", binary_code[pc+7:pc+9])[0]  # Смещение для записи
        memory[B + C] = memory[D]  # Записываем значение в память
        return pc + 2

    return pc + 7  # Переходим к следующей инструкции (12 байт)

# Интерпретатор
def interpret(input_binary, output_result):
    with open(input_binary, "rb") as bin_file:
        binary_code = bin_file.read()

    pc = 0  # Программный счетчик
    log = {'memory': {}}  # Лог для сохранения результата

    while pc < len(binary_code):
        pc = execute_instruction(binary_code, pc)

    # Сохраняем результат в файл
    for i, value in enumerate(memory):
        if value != 0:  # Записываем только те ячейки, которые имеют значения
            log['memory'][i] = value
            print(value)

    # Сохраняем результаты в формате YAML
    with open(output_result, "w") as result_file:
        yaml.dump(log, result_file, default_flow_style=False)

if __name__ == "__main__":
    input_binary = sys.argv[1]  # Путь к бинарному файлу
    output_result = sys.argv[2]  # Путь к результату
    interpret(input_binary, output_result)
