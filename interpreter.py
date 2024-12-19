import sys
import yaml

MEMORY_SIZE = 1000

def decode_instruction(instr_bytes):
    instr_bits = int.from_bytes(instr_bytes, 'little')
    A = instr_bits & 0xFF
    if A == 195:
        B = (instr_bits >> 8) & ((1 << 27) - 1)
        C = (instr_bits >> 35) & ((1 << 26) - 1)
        D = 0
    elif A == 74:
        B = (instr_bits >> 8) & ((1 << 27) - 1)
        C = (instr_bits >> 35) & ((1 << 27) - 1)
        D = (instr_bits >> 62) & ((1 << 27) - 1)
    else:
        B, C, D = 0, 0, 0
    return A, B, C, D

def execute_instruction(A, B, C, D, memory):
    if A == 195:
        if B < len(memory):
            memory[B] = C
    elif A == 74:
        if B < len(memory) and C < len(memory) and D < len(memory):
            memory[B] = memory[C] | memory[D]

def save_memory_to_yaml(memory, start, end, output_file):
    result = {addr: memory[addr] for addr in range(start, end)}
    with open(output_file, 'w') as f:
        yaml.dump(result, f)

def main():
    if len(sys.argv) < 5:
        print("Usage: python3 interpreter.py <input.bin> <start_addr> <end_addr> <output.yaml>")
        sys.exit(1)
    bin_file = sys.argv[1]
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    output_file = sys.argv[4]
    memory = [0] * MEMORY_SIZE
    with open(bin_file, 'rb') as f:
        program = f.read()
    for i in range(0, len(program), 12):
        instr_bytes = program[i:i+12]
        A, B, C, D = decode_instruction(instr_bytes)
        execute_instruction(A, B, C, D, memory)
    save_memory_to_yaml(memory, start, end, output_file)

if __name__ == '__main__':
    main()

