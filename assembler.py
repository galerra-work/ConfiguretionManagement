import sys
import yaml

OPCODES = {
    'LOADCONST': 195,
    'OR': 74
}

def assemble_line(line):
    parts = line.strip().split()
    mnemonic = parts[0]
    args = dict(arg.split('=') for arg in parts[1:])
    A = OPCODES[mnemonic]
    B = int(args.get('B', 0))
    C = int(args.get('C', 0))
    D = int(args.get('D', 0))
    if mnemonic == 'LOADCONST':
        instr_bits = (A & 0xFF)
        instr_bits |= (B & ((1 << 27)-1)) << 8
        instr_bits |= (C & ((1 << 26)-1)) << 35
        return instr_bits.to_bytes(12, 'little'), {'A': A, 'B': B, 'C': C}
    elif mnemonic == 'OR':
        instr_bits = (A & 0xFF)
        instr_bits |= (B & ((1 << 27)-1)) << 8
        instr_bits |= (C & ((1 << 27)-1)) << 35
        instr_bits |= (D & ((1 << 27)-1)) << 62
        return instr_bits.to_bytes(12, 'little'), {'A': A, 'B': B, 'C': C, 'D': D}
    return (b'\x00' * 12), {}

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 assembler.py <input.asm> <output.bin> <log.yaml>")
        sys.exit(1)
    asm_file = sys.argv[1]
    bin_file = sys.argv[2]
    log_file = sys.argv[3]
    instructions = []
    with open(asm_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instr_bytes, info = assemble_line(line)
                instructions.append((instr_bytes, info))
    with open(bin_file, 'wb') as f:
        for instr_bytes, _ in instructions:
            f.write(instr_bytes)
    log_data = [info for _, info in instructions]
    with open(log_file, 'w') as f:
        yaml.dump(log_data, f)

if __name__ == '__main__':
    main()

