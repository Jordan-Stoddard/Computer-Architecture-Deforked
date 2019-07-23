"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR):
        pass

    def load(self):
        """Load a program into memory."""

        # address = 0

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        if len(sys.argv) != 2:
            print(f'usage: {sys.argv[0]} <filename>')
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                address = 0
                for line in f:
                    num = line.split('#', 1)[0]
                    if num.strip() == '':
                        continue
                    
                    self.ram[address] = int(num, 2)
                    address += 1
                    
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found.')

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        running = True
        
        while running:
            IR = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            num_operands = (IR & 0b11000000) >> 6
            dist_to_move_pc = num_operands + 1
            if IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += dist_to_move_pc
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += dist_to_move_pc
            elif IR == MUL:
                self.alu('MUL', operand_a, operand_b)
                self.pc += dist_to_move_pc
            elif IR == HLT:
                running = False
                sys.exit(1)


"""
program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]
"""
