"""CPU functionality."""
import sys

PRN = 0b01000111
LDI = 0b10000010
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.branchtable = {}
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[ADD] = self.handle_ADD
        self.SP = 7
        # sets the stack pointer register's value to be 244 AKA 0xF4
        self.stack_pointer = self.reg[self.SP] = 244

# A function that takes in the current instruction and runs them in O(1) against our branchtable, 
# based on what the current instruction is.
    def handle_operations(self, IR, operand_a, operand_b, distance):
        if IR == LDI:
            self.branchtable[IR](operand_a, operand_b, distance)
        elif IR == PRN:
            self.branchtable[IR](operand_a, distance)
        elif IR == MUL:
            self.branchtable[IR](operand_a, operand_b, distance)
        elif IR == PUSH:
            self.branchtable[IR](operand_a, distance)
        elif IR == POP:
            self.branchtable[IR](operand_a, distance)
        elif IR == CALL:
            self.branchtable[IR](operand_a)
        elif IR == RET: 
            self.branchtable[IR]()
        elif IR == ADD:
            self.branchtable[IR](operand_a, operand_b, distance)
        elif IR == HLT:
            self.branchtable[IR]()

    # A helper function that performs ADD per the ls8 spec.
    def handle_ADD(self, operand_a, operand_b, distance):
        self.alu('ADD', operand_a, operand_b)
        self.pc += distance

    # A helper function that performs RET per the ls8 spec.
    def handle_RET(self):
        self.pc = self.ram[self.stack_pointer]
        self.stack_pointer -= 1

    # A helper function that performs CALL per the ls8 spec.
    def handle_CALL(self, operand_a):
        return_address = self.pc + 2
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = return_address
        self.pc = self.reg[operand_a]

    # A helper function that performs POP per the ls8 spec.
    def handle_POP(self, operand_a, distance):
        self.reg[operand_a] = self.ram[self.stack_pointer]
        self.stack_pointer += 1
        self.pc += distance

    # A helper function that performs PUSH per the ls8 spec.
    def handle_PUSH(self, operand_a, distance):
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = self.reg[operand_a]
        self.pc += distance

    # A helper function that performs MUL per the ls8 spec.
    def handle_MUL(self, operand_a, operand_b, distance):
        self.alu('MUL', operand_a, operand_b)
        self.pc += distance

    # A helper function that performs HLT per the ls8 spec.
    def handle_HLT(self):
        running = False
        return sys.exit(1)

    # A helper function that performs PRN per the ls8 spec.
    def handle_PRN(self, operand_a, distance):
        print(self.reg[operand_a])
        self.pc += distance

    # A helper function that performs LDI per the ls8 spec.
    def handle_LDI(self, operand_a, operand_b, distance):
        self.reg[operand_a] = operand_b
        self.pc += distance

    # Gets the current ram value of the current MAR.
    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR):
        pass

    def load(self):
        """Load a program into memory."""

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
            sys.exit(2)

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
        running = True
        # print(0b00011000)
        while running:
            # Gets the current instruction from RAM
            IR = self.ram[self.pc]
            # Sets the first operand from ram (operand is a like a variable)
            operand_a = self.ram_read(self.pc + 1)
            # sets the second operand from ram (operand is like a variable)
            operand_b = self.ram_read(self.pc + 2)
            # gets the number of operands by using bitwise-AND to parse our instruction.
            num_operands = (IR & 0b11000000) >> 6
            # gets the number of operations that the pc will need to be incremented.
            dist_to_move_pc = num_operands + 1
            # A function that takes in the current instruction and runs them in O(1) against our branchtable, 
            # based on what the current instruction is.
            self.handle_operations(IR, operand_a, operand_b, dist_to_move_pc)
