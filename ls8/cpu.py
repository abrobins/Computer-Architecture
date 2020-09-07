"""CPU functionality."""

import sys


HLT = 0b00000001
MUL = 0b10100010
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def HLT(self):
        self.running = False
        self.pc += 1

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

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

        try:
            with open(file_name) as file:
                for line in file:
                    split_file = line.split("#")[0]
                    comm = split_file.strip()
                    if comm == "":
                        continue
                    instruction = int(comm, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if ir == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif ir == PRN:
                reg_info = self.ram_read(self.pc + 1)
                print(self.reg[reg_info])
                self.pc += 2
            elif ir == MUL:
                self.alu(ir, operand_a, operand_b)
                self.pc += 3
            elif ir == HLT:
                running = False
            else:
                print("Unknown instruction")
