


# Reference doco - http://www.obelisk.me.uk/65C02/reference.html

# Reference CPU from Javrix - https://raw.githubusercontent.com/OneLoneCoder/olcNES/master/Part%232%20-%20CPU/olc6502.cpp
# 65C02 Data Sheet - https://eater.net/datasheets/w65c02s.pdf

# MicroChess - http://retro.hansotten.nl/6502-sbc/lee-davison-web-site/microchess/

# nestest
# https://wiki.nesdev.com/w/index.php/Emulator_tests
# http://nickmass.com/images/nestest.nes        # start execution at $C000
# doco - https://www.qmtpro.com/~nes/misc/nestest.txt

class cpu65c02:
    def __init__(self,bus):
        self.A = 0x00         # A register of 8 bits
        self.X = 0x00         # X register of 8 bits
        self.Y = 0x00         # Y register of 8 bits
        self.PC = 0x0000       # Program Counter of 16 bits
        self.SP = 0xFF         # Stack Pointer
        self.OPCODE = 0x00    # the current opcode we're running
        self.P = {
                    "N" : False,        # NEGATIVE
                    "V" : False,        # OVERFLOW
                    "5" : True,        # NOT IN USE
                    "B" : True,        # BREAK
                    "D" : False,        # DECIMAL
                    "I" : True,        # IRQB disable
                    "Z" : False,        # ZERO
                    "C" : False         # CARRY
        }
         

        

        self.bus = bus

        self.RW = False

        # == all the opcodes are here.  they are grouped as an array
        # -- opcode, instruction, addressing, cycles
        OPCODElibrary = [
            [ 0x00 , 'BRK' , 'STA' , 7  ],
            [ 0x01 , 'ORA' , 'IZX' , 6  ],
            [ 0x04 , 'TSB' , 'ZP0' , 3  ],
            [ 0x05 , 'ORA' , 'ZP0' , 3  ],
            [ 0x06 , 'ASL' , 'ZP0' , 5  ],
            [ 0x07 , 'RMB' , 'ZP0' , 5  ],
            [ 0x08 , 'PHP' , 'STA' , 3  ],
            [ 0x09 , 'ORA' , 'IMM' , 2  ],
            [ 0x0A , 'ASL' , 'ACC' , 2  ],
            [ 0x0C , 'TSB' , 'ABS' , 4  ],
            [ 0x0D , 'ORA' , 'ABS' , 4  ],
            [ 0x0E , 'ASL' , 'ABS' , 6  ],
            [ 0x0F , 'BBR' , 'REL' , 6  ],
            [ 0x10 , 'BPL' , 'REL' , 2  ],
            [ 0x11 , 'ORA' , 'IZY' , 5  ],
            [ 0x12 , 'ORA' , 'ZPI' , 2  ],
            [ 0x14 , 'TRB' , 'ZP0' , 4  ],
            [ 0x15 , 'ORA' , 'ZPX' , 4  ],
            [ 0x16 , 'ASL' , 'ZPX' , 6  ],
            [ 0x17 , 'RMB' , 'ZP0' , 6  ],
            [ 0x18 , 'CLC' , 'IMP' , 2  ],
            [ 0x19 , 'ORA' , 'ABY' , 4  ],
            [ 0x1A , 'INC' , 'ACC' , 2  ],
            [ 0x1C , 'TRB' , 'ABS' , 4  ],
            [ 0x1D , 'ORA' , 'ABX' , 4  ],
            [ 0x1E , 'ASL' , 'ABX' , 7  ],
            [ 0x1F , 'BBR' , 'REL' , 7  ],
            [ 0x20 , 'JSR' , 'ABS' , 6  ],
            [ 0x21 , 'AND' , 'IZX' , 6  ],
            [ 0x24 , 'BIT' , 'ZP0' , 3  ],
            [ 0x25 , 'AND' , 'ZP0' , 3  ],
            [ 0x26 , 'ROL' , 'ZP0' , 5  ],
            [ 0x27 , 'RMB' , 'ZP0' , 5  ],
            [ 0x28 , 'PLP' , 'STA' , 4  ],
            [ 0x29 , 'AND' , 'IMM' , 2  ],
            [ 0x2A , 'ROL' , 'ACC' , 2  ],
            [ 0x2C , 'BIT' , 'ABS' , 4  ],
            [ 0x2D , 'AND' , 'ABS' , 4  ],
            [ 0x2E , 'ROL' , 'ABS' , 6  ],
            [ 0x2F , 'BBR' , 'REL' , 6  ],
            [ 0x30 , 'BMI' , 'REL' , 2  ],
            [ 0x31 , 'AND' , 'IZY' , 5  ],
            [ 0x32 , 'AND' , 'ZPI' , 2  ],
            [ 0x34 , 'BIT' , 'ZPX' , 4  ],
            [ 0x35 , 'AND' , 'ZPX' , 4  ],
            [ 0x36 , 'ROL' , 'ZPX' , 6  ],
            [ 0x37 , 'RMB' , 'ZP0' , 6  ],
            [ 0x38 , 'SEC' , 'IMP' , 2  ],
            [ 0x39 , 'AND' , 'ABY' , 4  ],
            [ 0x3A , 'DEC' , 'ACC' , 2  ],
            [ 0x3C , 'BIT' , 'ABX' , 4  ],
            [ 0x3D , 'AND' , 'ABX' , 4  ],
            [ 0x3E , 'ROL' , 'ABX' , 7  ],
            [ 0x3F , 'BBR' , 'REL' , 7  ],
            [ 0x40 , 'RTI' , 'STA' , 6  ],
            [ 0x41 , 'EOR' , 'IZX' , 6  ],
            [ 0x45 , 'EOR' , 'ZP0' , 3  ],
            [ 0x46 , 'LSR' , 'ZP0' , 5  ],
            [ 0x47 , 'RMB' , 'ZP0' , 5  ],
            [ 0x48 , 'PHA' , 'STA' , 3  ],
            [ 0x49 , 'EOR' , 'IMM' , 2  ],
            [ 0x4A , 'LSR' , 'ACC' , 2  ],
            [ 0x4C , 'JMP' , 'ABS' , 3  ],
            [ 0x4D , 'EOR' , 'ABS' , 4  ],
            [ 0x4E , 'LSR' , 'ABS' , 6  ],
            [ 0x4F , 'BBR' , 'REL' , 6  ],
            [ 0x50 , 'BVC' , 'REL' , 2  ],
            [ 0x51 , 'EOR' , 'IZY' , 5  ],
            [ 0x52 , 'EOR' , 'ZPI' , 2  ],
            [ 0x55 , 'EOR' , 'ZPX' , 4  ],
            [ 0x56 , 'LSR' , 'ZPX' , 6  ],
            [ 0x57 , 'RMB' , 'ZP0' , 6  ],
            [ 0x58 , 'CLI' , 'IMP' , 2  ],
            [ 0x59 , 'EOR' , 'ABY' , 4  ],
            [ 0x5A , 'PHY' , 'STA' , 2  ],
            [ 0x5D , 'EOR' , 'ABX' , 4  ],
            [ 0x5E , 'LSR' , 'ABX' , 7  ],
            [ 0x5F , 'BBR' , 'REL' , 7  ],
            [ 0x60 , 'RTS' , 'STA' , 6  ],
            [ 0x61 , 'ADC' , 'IZX' , 6  ],
            [ 0x64 , 'STZ' , 'ZP0' , 3  ],
            [ 0x65 , 'ADC' , 'ZP0' , 3  ],
            [ 0x66 , 'ROR' , 'ZP0' , 5  ],
            [ 0x67 , 'RMB' , 'ZP0' , 5  ],
            [ 0x68 , 'PLA' , 'STA' , 4  ],
            [ 0x69 , 'ADC' , 'IMM' , 2  ],
            [ 0x6A , 'ROR' , 'ACC' , 2  ],
            [ 0x6C , 'JMP' , 'IND' , 5  ],
            [ 0x6D , 'ADC' , 'ABS' , 4  ],
            [ 0x6E , 'ROR' , 'ABS' , 6  ],
            [ 0x6F , 'BBR' , 'REL' , 6  ],
            [ 0x70 , 'BVS' , 'REL' , 2  ],
            [ 0x71 , 'ADC' , 'IZY' , 5  ],
            [ 0x72 , 'ADC' , 'ZPI' , 2  ],
            [ 0x74 , 'STZ' , 'ZPX' , 4  ],
            [ 0x75 , 'ADC' , 'ZPX' , 4  ],
            [ 0x76 , 'ROR' , 'ZPX' , 6  ],
            [ 0x77 , 'RMB' , 'ZP0' , 6  ],
            [ 0x78 , 'SEI' , 'IMP' , 2  ],
            [ 0x79 , 'ADC' , 'ABY' , 4  ],
            [ 0x7A , 'PLY' , 'STA' , 2  ],
            [ 0x7C , 'JMP' , 'IAX' , 4  ],
            [ 0x7D , 'ADC' , 'ABX' , 4  ],
            [ 0x7E , 'ROR' , 'ABX' , 7  ],
            [ 0x7F , 'BBR' , 'REL' , 7  ],
            [ 0x80 , 'BRA' , 'REL' , 2  ],
            [ 0x81 , 'STA' , 'IZX' , 6  ],
            [ 0x84 , 'STY' , 'ZP0' , 3  ],
            [ 0x85 , 'STA' , 'ZP0' , 3  ],
            [ 0x86 , 'STX' , 'ZP0' , 3  ],
            [ 0x87 , 'SMB' , 'ZP0' , 3  ],
            [ 0x88 , 'DEY' , 'IMP' , 2  ],
            [ 0x89 , 'BIT' , 'IMM' , 2  ],
            [ 0x8A , 'TXA' , 'IMP' , 2  ],
            [ 0x8C , 'STY' , 'ABS' , 4  ],
            [ 0x8D , 'STA' , 'ABS' , 4  ],
            [ 0x8E , 'STX' , 'ABS' , 4  ],
            [ 0x8F , 'BBS' , 'REL' , 4  ],
            [ 0x90 , 'BCC' , 'REL' , 2  ],
            [ 0x91 , 'STA' , 'IZY' , 6  ],
            [ 0x92 , 'STA' , 'ZPI' , 2  ],
            [ 0x94 , 'STY' , 'ZPX' , 4  ],
            [ 0x95 , 'STA' , 'ZPX' , 4  ],
            [ 0x96 , 'STX' , 'ZPY' , 4  ],
            [ 0x97 , 'SMB' , 'ZP0' , 4  ],
            [ 0x98 , 'TYA' , 'IMP' , 2  ],
            [ 0x99 , 'STA' , 'ABY' , 5  ],
            [ 0x9A , 'TXS' , 'IMP' , 2  ],
            [ 0x9C , 'STZ' , 'ABS' , 5  ],
            [ 0x9D , 'STA' , 'ABX' , 5  ],
            [ 0x9E , 'STZ' , 'ABX' , 5  ],
            [ 0x9F , 'BBS' , 'REL' , 5  ],
            [ 0xA0 , 'LDY' , 'IMM' , 2  ],
            [ 0xA1 , 'LDA' , 'IZX' , 6  ],
            [ 0xA2 , 'LDX' , 'IMM' , 2  ],
            [ 0xA4 , 'LDY' , 'ZP0' , 3  ],
            [ 0xA5 , 'LDA' , 'ZP0' , 3  ],
            [ 0xA6 , 'LDX' , 'ZP0' , 3  ],
            [ 0xA7 , 'SMB' , 'ZP0' , 3  ],
            [ 0xA8 , 'TAY' , 'IMP' , 2  ],
            [ 0xA9 , 'LDA' , 'IMM' , 2  ],
            [ 0xAA , 'TAX' , 'IMP' , 2  ],
            [ 0xAC , 'LDY' , 'ABS' , 4  ],
            [ 0xAD , 'LDA' , 'ABS' , 4  ],
            [ 0xAE , 'LDX' , 'ABS' , 4  ],
            [ 0xAF , 'BBS' , 'REL' , 4  ],
            [ 0xB0 , 'BCS' , 'REL' , 2  ],
            [ 0xB1 , 'LDA' , 'IZY' , 5  ],
            [ 0xB2 , 'LDA' , 'ZPI' , 2  ],
            [ 0xB4 , 'LDY' , 'ZPX' , 4  ],
            [ 0xB5 , 'LDA' , 'ZPX' , 4  ],
            [ 0xB6 , 'LDX' , 'ZPY' , 4  ],
            [ 0xB7 , 'SMB' , 'ZP0' , 4  ],
            [ 0xB8 , 'CLV' , 'IMP' , 2  ],
            [ 0xB9 , 'LDA' , 'ABY' , 4  ],
            [ 0xBA , 'TSX' , 'IMP' , 2  ],
            [ 0xBC , 'LDY' , 'ABX' , 4  ],
            [ 0xBD , 'LDA' , 'ABX' , 4  ],
            [ 0xBE , 'LDX' , 'ABY' , 4  ],
            [ 0xBF , 'BBS' , 'REL' , 4  ],
            [ 0xC0 , 'CPY' , 'IMM' , 2  ],
            [ 0xC1 , 'CMP' , 'IZX' , 6  ],
            [ 0xC4 , 'CPY' , 'ZP0' , 3  ],
            [ 0xC5 , 'CMP' , 'ZP0' , 3  ],
            [ 0xC6 , 'DEC' , 'ZP0' , 5  ],
            [ 0xC7 , 'SMB' , 'ZP0' , 5  ],
            [ 0xC8 , 'INY' , 'IMP' , 2  ],
            [ 0xC9 , 'CMP' , 'IMM' , 2  ],
            [ 0xCA , 'DEX' , 'IMP' , 2  ],
            [ 0xCB , 'WAI' , 'IMP' , 2  ],
            [ 0xCC , 'CPY' , 'ABS' , 4  ],
            [ 0xCD , 'CMP' , 'ABS' , 4  ],
            [ 0xCE , 'DEC' , 'ABS' , 6  ],
            [ 0xCF , 'BBS' , 'REL' , 6  ],
            [ 0xD0 , 'BNE' , 'REL' , 2  ],
            [ 0xD1 , 'CMP' , 'IZY' , 5  ],
            [ 0xD2 , 'CMP' , 'ZPI' , 2  ],
            [ 0xD5 , 'CMP' , 'ZPX' , 4  ],
            [ 0xD6 , 'DEC' , 'ZPX' , 6  ],
            [ 0xD7 , 'SMB' , 'ZP0' , 6  ],
            [ 0xD8 , 'CLD' , 'IMP' , 2  ],
            [ 0xD9 , 'CMP' , 'ABY' , 4  ],
            [ 0xDA , 'PHX' , 'IMP' , 2  ],
            [ 0xDB , 'STP' , 'IMP' , 3  ],
            [ 0xDD , 'CMP' , 'ABX' , 4  ],
            [ 0xDE , 'DEC' , 'ABX' , 7  ],
            [ 0xDF , 'BBS' , 'REL' , 7  ],
            [ 0xE0 , 'CPX' , 'IMM' , 2  ],
            [ 0xE1 , 'SBC' , 'IZX' , 6  ],
            [ 0xE4 , 'CPX' , 'ZP0' , 3  ],
            [ 0xE5 , 'SBC' , 'ZP0' , 3  ],
            [ 0xE6 , 'INC' , 'ZP0' , 5  ],
            [ 0xE7 , 'SMB' , 'ZP0' , 5  ],
            [ 0xE8 , 'INX' , 'IMP' , 2  ],
            [ 0xE9 , 'SBC' , 'IMM' , 2  ],
            [ 0xEA , 'NOP' , 'IMP' , 2  ],
            [ 0xEC , 'CPX' , 'ABS' , 4  ],
            [ 0xED , 'SBC' , 'ABS' , 4  ],
            [ 0xEE , 'INC' , 'ABS' , 6  ],
            [ 0xEF , 'BBS' , 'REL' , 6  ],
            [ 0xF0 , 'BEQ' , 'REL' , 2  ],
            [ 0xF1 , 'SBC' , 'IZY' , 5  ],
            [ 0xF2 , 'SBC' , 'ZPI' , 2  ],
            [ 0xF5 , 'SBC' , 'ZPX' , 4  ],
            [ 0xF6 , 'INC' , 'ZPX' , 6  ],
            [ 0xF7 , 'SMB' , 'ZP0' , 6  ],
            [ 0xF8 , 'SED' , 'IMP' , 2  ],
            [ 0xF9 , 'SBC' , 'ABY' , 4  ],
            [ 0xFA , 'PLX' , 'STA' , 2  ],
            [ 0xFD , 'SBC' , 'ABX' , 4  ],
            [ 0xFE , 'INC' , 'ABX' , 7  ],
            [ 0xFF , 'BBS' , 'REL' , 7  ],

        ]
        

        # -- flatten the dictionary out to speed up execution
        self.OPCx = {}

        
        self.OPC = {}
        for a in OPCODElibrary:
            O = a[0]    # OpCode
            I = a[1]    # Instruction
            A = a[2]    # Addressing
            C = a[3]    # Cycles

            self.OPC[O] = {
                'I' : I,
                'A' : A,
                'C' : C,
            }


        self.ENABLE = True

        self.debug = ''

    def cpudump(self):
        print(
            'PC = 0x%04X ; ' % self.PC + 
            'OP = 0x%02X ; ' % self.OPCODE +
            'SP = 0x%02X ; ' % self.SP +
            'A = 0x%02X ; ' % self.A +
            'X = 0x%02X ; ' % self.X +
            'Y = 0x%02X ;' % self.Y + 
            ' P = '
                + ('N' if self.P['N'] else 'n')
                + ('V' if self.P['V'] else 'v')
                + ('B' if self.P['B'] else 'b')
                + ('D' if self.P['D'] else 'd')
                + ('I' if self.P['I'] else 'i')
                + ('Z' if self.P['Z'] else 'z')
                + ('C' if self.P['C'] else 'c') + ' ; ' )

    def RESET(self):
        self.PC = (self.bus.read(0xFFFD) << 8) + self.bus.read(0xFFFC)
        self.P['5'] = True
        self.P['B'] = True
        self.P['D'] = False
        self.P['I'] = False
        self.SP = 0xFF

    def pushStack(self,value):
        self.bus.write(0x0100 + self.SP,value)
        self.SP -= 1
    
    def popStack(self):
        self.SP += 1
        return self.bus.read(0x0100 + self.SP)

    def IRQ(self,B = None):

        
        if self.P['I'] == True:
            return

        # == push the Program counter to the stack
        self.pushStack(((self.PC )>> 8) & 0x00FF)
        self.pushStack((self.PC ) & 0x00FF)

        # == push the P register to the stack
        _p =  (0b10000000 if self.P['N'] else 0)  + (0b01000000 if self.P['V'] else 0) + (0b00100000 if self.P['5'] else 0) + (0b00010000 if self.P['B'] else 0) + (0b00001000 if self.P['D'] else 0) + (0b00000100 if self.P['I'] else 0) + (0b00000010 if self.P['Z'] else 0) + (0b00000001 if self.P['C'] else 0)
        self.pushStack(_p & 0xFF)

        self.PC = (self.bus.read(0xFFFF) << 8) + self.bus.read(0xFFFE)

        self.P['I'] = True

        # == used by the BRK instruction
        if B != None:
            self.P['B'] = B

    def CLOCK(self):
        # == read the memory at the program counter
        self.OPCODE = self.bus.read(self.PC) & 0xFF

        # --------------- Find the opcode in our library
        if self.OPCODE not in self.OPC:
            print('ERROR : Opcode 0X%02X' % self.OPCODE + ' not in the library' )
            exit(1)
        else:
            q = self.OPC[self.OPCODE]

            # -- grab the addressing
            # _bytes contains how many bytes to be read for the instruction
            # _data contains the data added with the opcode
            # _addr contains the calculated adress (if any)
            # _value contains the value at that memory location
            _bytes = 0

            if q['A'] == 'ABS':     # 4.1 Absolute a
                _bytes = 3
                _data =  ((self.bus.read(self.PC+2) << 8) + self.bus.read(self.PC+1)) & 0xFFFF
                _addr = _data
                _value = self.bus.read(_addr)

            if q['A'] == 'IAX':     # 4.2 Absolute Indexed Indirect (a,x)
                _bytes = 3
                _d =  ((self.bus.read(self.PC+2) << 8) + self.bus.read(self.PC+1) + self.X ) & 0xFFFF
                _data =  ((self.bus.read(_d+1) << 8) + self.bus.read(_d)) & 0xFFFF
                _addr = (_data ) & 0xFFFF

            if q['A'] == 'ABX':     # 4.3 Absolute Indexed with X
                _bytes = 3
                lo = self.bus.read(self.PC+1)
                hi = self.bus.read(self.PC+2)
                _data = (hi << 8) | lo

                _addr = (_data + self.X) & 0xFFFF

                _value = self.bus.read(_addr)

                if ((_value & 0xFF00) != (self.bus.read(self.PC+2) << 8)):
                    q['C'] += 1

            if q['A'] == 'ABY':     # 4.4 Absolute Indexed with Y
                _bytes = 3
                _data = (self.bus.read(self.PC+2) << 8) + self.bus.read(self.PC+1) & 0xFFFF
                _addr = _data + self.Y
                _value = self.bus.read(_addr & 0xFFFF)

            if q['A'] == 'IND':     # 4.5 Absolute Indirect (a)
                _bytes = 3

                ptr_lo = self.bus.read(self.PC+1)	
                ptr_hi = self.bus.read(self.PC+2)
                _data = (ptr_hi << 8) | ptr_lo

                if ptr_lo == 0x00FF: # Simulate page boundary hardware bug
                    _addr = (self.bus.read(_data & 0xFF00) << 8) | self.bus.read(_data + 0)

                else:   # Behave normally
                    _addr = self.bus.read(_data + 1) << 8 | self.bus.read(_data + 0)
	
                _value = (self.bus.read(_addr+1) << 8) + self.bus.read(_addr)
              
            if q['A'] == 'ACC':     # 4.6 Accumulator A
                _bytes = 1
                _data = self.A
                _addr = 0x0000
                _value = _data

            if q['A'] == 'IMM':     # 4.7 Immediate Addressing #
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                _addr = 0x0000
                _value = _data

            if q['A'] == 'IMP':     # 4.8 Implied - i
                _bytes = 1
                _data = 0x0000
                _addr = 0x0000
                _value = 0x0000

            if q['A'] == 'REL':     # 4.9 Program Counter Relative - r
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                if _data & 0x80:
                    _addr = _data | 0xFF00
                else:
                    _addr = _data
                _value = 0x0000

            if q['A'] == 'STA':     # 4.10 Stack - s
                _bytes = 1
                _data = 0x0000
                _addr = 0x0000
                _value = 0x0000

            if q['A'] == 'ZP0':     # 4.11 Zero Page
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                _addr = _data & 0x00FF
                _value = self.bus.read(_addr)

            if q['A'] == 'IZX':     # 4.12 Indirect X
                _bytes = 2
                _data = self.bus.read(self.PC+1)

                lo = self.bus.read((_data + self.X) & 0x00FF)
                hi = self.bus.read((_data + self.X + 1) & 0x00FF)

                _addr = (hi << 8) | lo

                _value = ((self.bus.read(_addr + 1) << 8) & 0x00FF) | ((self.bus.read(_addr)) & 0x00FF)

            if q['A'] == 'ZPX':     # Zero Page, X
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                
                _addr = (_data + self.X) & 0x00FF
                _value = self.bus.read(_addr)

            if q['A'] == 'ZPY':     # Zero Page, Y
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                _addr = (_data + self.Y) & 0x00FF
                _value = self.bus.read(_addr)       

            if q['A'] == 'IZY':     # Indirect indexed with Y
                _bytes = 2
                _data = self.bus.read(self.PC+1) & 0xFF
                lo = self.bus.read(_data & 0x00FF)
                hi = self.bus.read((_data + 1) & 0x00FF)

                _addr = ((hi << 8) | lo) + self.Y
                _value = self.bus.read(_addr)

            if q['A'] == 'ZPI':     # Zero Page Indirect
                _bytes = 2
                _data = self.bus.read(self.PC+1)

                ptr_lo = self.bus.read(_data)
                ptr_hi = self.bus.read(_data+1)
                
                _addr = (ptr_hi << 8) | ptr_lo

                if ptr_lo == 0x00FF: # Simulate page boundary hardware bug
                    _value = (self.bus.read(_addr & 0xFF00) << 8) | self.bus.read(_addr)
                else: # Behave normally
	                _value = (self.bus.read(_addr + 1) << 8) | self.bus.read(_addr)

            
	
            # --- DEBUG
            #print('=======================================')
            #print('ADDRESSING MODE -- ' + q['A'])
            #print('ADDRESSING DATA -- 0x%04X' % _data)
            #print('ADDRESSING ADDR -- 0x%04X' % _addr)
            #print('ADDRESSING VALUE -- 0x%02X' % _value)

            # -- execute the instruction

            if q['I'] == 'ADC':
                _t = self.A + _value + (1 if self.P['C'] else 0) 
                self.P['C'] = _t > 0xFF
                self.P['Z'] = (_t & 0x00FF) == 0
                self.P['V'] = bool((~(self.A ^ _value) & (self.A ^ _t)) & 0x0080)
                self.P['N'] = bool(_t & 0x80)
                self.A = _t & 0x00FF
	
            if q['I'] == 'AND':
                self.A = self.A & _value
                
                self.P['Z'] = bool(self.A == 0x00)
                self.P['N'] = bool(self.A & 0x80)

            if q['I'] == 'ASL':
                _t = _value << 1
                self.P['C'] = _t > 0xFF
                self.P['Z'] = (_t & 0x00FF) == 0
                self.P['N'] = bool(_t & 0x80)

                if q['A'] == 'ACC':
                    self.A = _t & 0x00FF
                else:
                    self.bus.write(_addr ,_t & 0x00FF)

            if q['I'] == 'BBR':
                print('TODO - BBR')
            
            if q['I'] == 'BBR':
                print('TODO - BBS')

            if q['I'] == 'BCC':
                if not self.P['C']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1
            
            if q['I'] == 'BCS':
                if self.P['C']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'BEQ':
                if self.P['Z']:
                    self.PC = self.PC + _addr

                    q['C'] += 1

            if q['I'] == 'BIT':
                _t = self.A & _value

                self.P['Z'] = bool((_t & 0x00FF) == 0)
                self.P['N'] = bool(_value & (1 << 7))
                self.P['V'] = bool(_value & (1 << 6))
    
            if q['I'] == 'BMI':
                if self.P['N']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'BNE':
                if not self.P['Z']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'BPL':
                if not self.P['N']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'BRA':
                print('TODO' + str(q['I']))
                

            if q['I'] == 'BRK':
                self.PC += 2
                self.IRQ(True)
                self.PC -= 1        # TODO - not sure if this is what BRK is supposed to do

            if q['I'] == 'BVC':
                if not self.P['V']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'BVS':
                if self.P['V']:
                    self.PC = (self.PC + _addr) & 0xFFFF

                    if (_addr & 0xFF00) != (self.PC & 0xFF00):
                        q['C'] += 1

            if q['I'] == 'CLC':
                self.P['C'] = False

            if q['I'] == 'CLD':
                self.P['D'] = False

            if q['I'] == 'CLI':
                self.P['I'] = False

            if q['I'] == 'CLV':
                self.P['V'] = False

            if q['I'] == 'CMP':
                if self.A < _value:
                    self.P['Z'] = False
                    self.P['C'] = False
                    self.P['N'] = bool(self.A & 0x80)

                if self.A == _value:
                    self.P['Z'] = True
                    self.P['C'] = True
                    self.P['N'] = False

                if self.A > _value:
                    self.P['Z'] = False
                    self.P['C'] = True
                    self.P['N'] = bool(self.A & 0x80)

            if q['I'] == 'CPX':
                if self.X < _value:
                    self.P['Z'] = False
                    self.P['C'] = False
                    self.P['N'] = bool(self.X & 0x80)

                if self.X == _value:
                    self.P['Z'] = True
                    self.P['C'] = True
                    self.P['N'] = False

                if self.X > _value:
                    self.P['Z'] = False
                    self.P['C'] = True
                    self.P['N'] = bool(self.X & 0x80)

            if q['I'] == 'CPY':
                if self.Y < _value:
                    self.P['Z'] = False
                    self.P['C'] = False
                    self.P['N'] = bool(self.A & 0x80)

                if self.Y == _value:
                    self.P['Z'] = True
                    self.P['C'] = True
                    self.P['N'] = False

                if self.Y > _value:
                    self.P['Z'] = False
                    self.P['C'] = True
                    self.P['N'] = bool(self.Y & 0x80)
            
            if q['I'] == 'DEC':
                _t = (_data - 1) & 0x00FF

                if q['A'] == 'ACC':
                    self.A = _t & 0x00FF
                else:
                    self.bus.write(_addr,_t & 0x00FF)

                self.P['Z'] = bool(_t == 0x00)
                self.P['N'] = bool(_t & 0x80)
            
            if q['I'] == 'DEX':
                self.X = (self.X - 1) & 0xFF

                self.P['Z'] = bool(self.X == 0x00)
                self.P['N'] = bool(self.X & 0x80)

            if q['I'] == 'DEY':
                self.Y = (self.Y - 1) & 0xFF

                self.P['Z'] = bool(self.Y == 0x00)
                self.P['N'] = bool(self.Y & 0x80)

            if q['I'] == 'EOR':
                self.A = self.A ^ _value
                
                self.P['Z'] = bool(self.A == 0x00)
                self.P['N'] = bool(self.A & 0x80)

            if q['I'] == 'INC':
                _t = _value + 1

                if q['A'] == 'ACC':
                    self.A = _t
                else:
                    self.bus.write(_addr , _t & 0x00FF)

                self.P['Z'] = bool(( _t & 0x00FF) == 0x0000)
                self.P['N'] = bool(_t & 0x80)

            if q['I'] == 'INX':
                self.X = (self.X + 1) & 0xFF
                self.P['Z'] = bool(self.X == 0x00)
                self.P['N'] = bool(self.X & 0x80)

            if q['I'] == 'INY':
                self.Y = (self.Y + 1) & 0xFF
                self.P['Z'] = bool(self.Y == 0x00)
                self.P['N'] = bool(self.Y & 0x80)

            if q['I'] == 'JMP':
                self.PC = _addr - _bytes

            if q['I'] == 'JSR':
                # -- push the current program counter to the stack
                self.pushStack(((self.PC + 3)>> 8) & 0x00FF)
                self.pushStack((self.PC + 3) & 0x00FF)

                # -- update the program counter
                self.PC = _addr - _bytes

            if q['I'] == 'LDA':
                self.A = _value
                self.P['Z'] = bool(self.A == 0x00)
                self.P['N'] = bool(self.A & 0x80)

            if q['I'] == 'LDX':
                self.X = _value
                self.P['Z'] = bool(self.X == 0x00)
                self.P['N'] = bool(self.X & 0x80)
           
            if q['I'] == 'LDY':
                self.Y = _value
                self.P['Z'] = bool(self.Y == 0x00)
                self.P['N'] = bool(self.Y & 0x80)

            if q['I'] == 'LSR':
                _t = _value >> 1

                self.P['C'] = bool(_value & 0x0001)
                self.P['Z'] = bool((_t & 0x00FF) == 0x0000)
                self.P['N'] = bool(_t & 0x0080)

                if q['A'] == 'ACC':
                    self.A = _t & 0x00FF
                else:
                    self.bus.write(_addr, _t & 0x00FF)

            #if q['I'] == 'NOP':
                # no action

            if q['I'] == 'ORA':
                self.A = self.A | _value
                
                self.P['Z'] = bool(self.A == 0x00)
                self.P['N'] = bool(self.A & 0x80)

            if q['I'] == 'PHA':
                self.pushStack((self.A) & 0xFF)

            if q['I'] == 'PHP':
                _p =  (0b10000000 if self.P['N'] else 0)  + (0b01000000 if self.P['V'] else 0) + (0b00100000 if self.P['5'] else 0) + (0b00010000 if self.P['B'] else 0) + (0b00001000 if self.P['D'] else 0) + (0b00000100 if self.P['I'] else 0) + (0b00000010 if self.P['Z'] else 0) + (0b00000001 if self.P['C'] else 0)
                self.pushStack(_p & 0xFF)

            if q['I'] == 'PHX':
                self.pushStack((self.X) & 0xFF)
            
            if q['I'] == 'PHY':
                self.pushStack((self.Y) & 0xFF)

            if q['I'] == 'PLA':
                self.A = self.popStack()

            if q['I'] == 'PLP':
                _p = self.popStack()

                self.P['N'] = bool(_p & 0b10000000)
                self.P['V'] = bool(_p & 0b01000000)
                self.P['5'] = bool(_p & 0b00100000)
                self.P['B'] = bool(_p & 0b00010000)
                self.P['D'] = bool(_p & 0b00001000)
                self.P['I'] = bool(_p & 0b00000100)
                self.P['Z'] = bool(_p & 0b00000010)
                self.P['C'] = bool(_p & 0b00000001)
                
            if q['I'] == 'PLX':
                self.X = self.popStack()

            if q['I'] == 'PLY':
                self.Y = self.popStack()

            if q['I'] == 'RMB':
                print('TODO' + str(q['I']))

            if q['I'] == 'ROL':
                # Move each of the bits in either A or M one place to the left.
                if q['A'] == 'ACC':
                    _t = self.A << 1
                else:
                    _t = _value << 1

                # Bit 0 is filled with the current value of the carry flag
                if self.P['C']:
                    p = 0b00000001
                else:
                    p = 0b00000000

                _t = _value << 1 | p
                # whilst the old bit 7 becomes the new carry flag value.

                self.P['C'] = bool(_t & 0xFF00)
                self.P['Z'] = bool((_t & 0xFF) == 0x0000)

                self.P['N'] = bool(_t & 0x0080)

                if q['A'] == 'ACC':
                    self.A = _t & 0x00FF
                else:
                    self.bus.write(_addr , _t & 0x00FF)

            if q['I'] == 'ROR':
                _t = (0b10000000 if self.P['C'] else 0) + (_value >> 1)

                self.P['C'] = bool(_value & 0x01)
	
                self.P['Z'] = bool((_t & 0xFF) == 0x0000)
                self.P['N'] = bool(_t & 0x0080)

                if q['A'] == 'ACC':
                    self.A = _t & 0x00FF
                else:
                    self.bus.write(_addr , _t & 0x00FF)

            if q['I'] == 'RTI':
                # -- return the P stack
                _p = self.popStack()

                self.P['N'] = bool(_p & 0b10000000)
                self.P['V'] = bool(_p & 0b01000000)
                self.P['5'] = True # bool(_p & 0b00100000)
                self.P['B'] = True # bool(_p & 0b00010000)
                self.P['D'] = bool(_p & 0b00001000)
                self.P['I'] = bool(_p & 0b00000100)
                self.P['Z'] = bool(_p & 0b00000010)
                self.P['C'] = bool(_p & 0b00000001)

                # -- return the progam counter
                self.PC = self.popStack() + (self.popStack() << 8) - _bytes


            if q['I'] == 'RTS':
                self.PC = self.popStack() + (self.popStack() << 8) - _bytes

            if q['I'] == 'SEC':
                self.P['C'] = True

            if q['I'] == 'SEI':
                self.P['I'] = True

            if q['I'] == 'SED':
                self.P['D'] = True

            if q['I'] == 'SBC':
                _t = _value ^ 0x00FF
                self.P['C'] = bool(_t > 0xFF)
                self.P['Z'] = bool((_t & 0x00FF) == 0)
                self.P['V'] = bool((~(self.A ^ _value) & (self.A ^ _t)) & 0x80)
                self.P['N'] = bool(_t & 0x80)
                self.A = _t & 0x00FF

            if q['I'] == 'SMB':
                print('TODO' + str(q['I']))

            if q['I'] == 'STA':
                self.bus.write(_addr , self.A)

            if q['I'] == 'STP':
                print (' ** PROCESSOR HALTED ***')
                input()
                exit(0)

            if q['I'] == 'STX':
                self.bus.write(_addr , self.X)

            if q['I'] == 'STZ':
                self.bus.write(_addr , 0x00)

            if q['I'] == 'STY':
                self.bus.write(_addr , self.Y)

            if q['I'] == 'TAX':
                self.X = self.A
                self.P['Z'] = bool((self.X & 0x00FF) == 0)
                self.P['N'] = bool(self.X & 0x80)

            if q['I'] == 'TAY':
                self.Y = self.A
                self.P['Z'] = bool((self.Y & 0x00FF) == 0)
                self.P['N'] = bool(self.Y & 0x80)

            if q['I'] == 'TRB':
                print('TODO' + str(q['I']))
                #address = x()
                #m = self.memory[address]
                #self.p &= ~self.ZERO
                #z = m & self.a
                #if z == 0:
                #    self.p |= self.ZERO
                #self.memory[address] = m & ~self.a

            if q['I'] == 'TSB':
                print('TODO' + str(q['I']))
                #address = x()
                #m = self.memory[address]
                #self.p &= ~self.ZERO
                #z = m & self.a
                #if z == 0:
                #   self.p |= self.ZERO
                #self.memory[address] = m | self.a

            if q['I'] == 'TSX':
                print('TODO' + str(q['I']))

            if q['I'] == 'TXA':
                self.A = self.X
                self.P['Z'] = bool((self.A & 0x00FF) == 0)
                self.P['N'] = bool(_t & 0x80)

            if q['I'] == 'TXS':
                self.SP = self.X
        
            if q['I'] == 'TYA':
                self.A = self.Y
                self.P['Z'] = bool((self.A & 0x00FF) == 0)
                self.P['N'] = bool(_t & 0x80)

            if q['I'] == 'WAI':
                print('TODO' + str(q['I']))

            # -- generate the asm line
            c = {
                'ABS' : [ ''  , ''    ],
                'IAX' : [ '(' , ',x) '],
                'ABX' : [ ''  , ',x'  ],
                'ABY' : [ ''  , ',y'  ],
                'ACC' : [ 'A' , ''    ],
                'IMM' : [ '#' , ''    ],
                'IMP' : [ ''  , ''    ],
                'REL' : [ ''  , ''    ],
                'STA' : [ ''  , ''    ],
                'ZP0' : [ '(' , ',x) '],
                'IZX' : [ '(' , ',x)' ],
                'ZPX' : [ ''  , ',x'  ],
                'ZPY' : [ ''  , ',y'  ],
                'ZPI' : [ '(' , ')'   ],
                'IZY' : [ '(' , '),y' ]
            }

            p1 = c.get(q['A'],['',''])[0]
            p2 = c.get(q['A'],['',''])[1]

            if _bytes == 2:
                self.asm = '--> $%04X' % self.PC + ' : ' + q['I'] + ' ' + p1 + '$%02X' % _data + ' ' + p2 + '   [ %02X' % self.bus.read(self.PC) + ' %02X' % self.bus.read(self.PC + 1) + ' ]'
            else:
                self.asm = '--> $%04X' % self.PC + ' : ' + q['I'] + ' ' + p1 + '$%04X' % _data + ' ' + p2 + '   [ %02X' % self.bus.read(self.PC) + ' %02X' % self.bus.read(self.PC + 1)  + ' %02X' % self.bus.read(self.PC + 2)  + ' ]'

            self.PC += _bytes

            self.CYCLES = q['C']


        # -- did any of our values grow too far?
        self.X = self.X & 0xFF
        self.Y = self.Y & 0xFF
        self.A = self.A & 0xFF
        self.SP = self.SP & 0xFF
        self.PC = self.PC & 0xFFFF


