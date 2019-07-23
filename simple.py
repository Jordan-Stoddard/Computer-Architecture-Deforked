import sys

PRINT_BEEJ = 1
HALT = 2
PRINT_NUM = 3
SAVE_REGISTER = 4
PRINT_REGISTER = 5

memory = [0] * 128 # 128 bits of memory

registers = [0] * 8  # 8 registers

pc = 0  # Program Counter -- Pointer to currently-executing instruction

running = True

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} filename")
    sys.exit(1)
try:
    with open(sys.argv[1]) as f:
        address = 0
        for line in f:
            num = line.split('#', 1)[0]
            if num.strip() == '': # ignore comment-only line
                continue

            memory[address] = int(num)
            address += 1

except FileNotFoundError:
    print(f"{sys.argv[0]}: {sys.argv[1]} not found")
    sys.exit(2)

while running:
    command = memory[pc]

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1

    elif command == HALT:
        running = False
        pc += 1

    elif command == SAVE_REGISTER:
        value = memory[pc+1]
        regnum = memory[pc+2]
        registers[regnum] = value
        pc += 3

    elif command == PRINT_REGISTER:
        regnum = memory[pc+1]
        print(registers[regnum])
        pc += 2

    elif command == PRINT_NUM:
        operand = memory[pc + 1]
        print(operand)
        pc += 2

    else:
        print(f'unknown instruction {command}')
        sys.exit(1)
