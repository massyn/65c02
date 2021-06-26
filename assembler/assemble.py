# 65c02 Assembler
# Phil Massyn (@massyn)

import json
import re

# Sprint 1
# DONE - Ignore comments
# DONE - remove white space in the commands
# DONE - Understand addressing modes
# DONE - Understand decimal, hexadecimal and binary
# DONE - Translate nmeumonic to characters

# Sprint 2
# - Write assembler binary file
# - Write list file
# - Run the compiled code

# Spring 3
# - Labels (for branching)
#    - Relative addressing to be calculated
# - .org addressing
# - simple constant variables
# - bytes & words

# Sprint 4
# - handle 4 character opcodes (like BBRx)
# - include files


def line(t):
    print(' --> ' + str(t))

def _assemble_sanitize(input):
    
    # -- remove anything after the ; -- those are comments
    comment = input.find(';')
    if comment != -1:
        new = input[0:comment]
    else:
        new = input

    # == Remove all the whitespace - we want it raw
    new = new.strip().replace(' ','').replace('\t','')

    return new

def _assemble_code(statement):
    machine_code = {
        "ADDR" : {
            "ABS" : {
                "detail"    : "4.1 - Absolute a",
                "bytes"     : 3,
                "regex"     : [
                    r"^(\$[a-f0-9][a-f0-9][a-f0-9][a-f0-9])$",
                    r"^(\%................)$",
                    r"^(\d\d\d\d)$"
                ]
            },
            "IAX" : {
                "detail"    : "4.2 - Absolute Indexed Indirect (a,x)",
                "bytes"     : 3,
                "regex" : [
                    r"^\((\$[a-f0-9][a-f0-9][a-f0-9][a-f0-9]),x\)$"
                ]
            },
            "ABX" : {
                "detail"    : "4.3 - Absolute Indexed with X a,x",
                "bytes"     : 3,
                "regex"     : [
                    r"^(\$[a-f0-9][a-f0-9][a-f0-9][a-f0-9]),x$",
                    r"^(\%................),x$",
                    r"^(\d\d\d\d),x$"
                ]
            },
            "ABY" : {
                "detail"    : "4.4 - Absolute Indexed with Y a,y",
                "bytes"     : 3,
                "regex"     : [
                    r"^(\$[a-f0-9][a-f0-9][a-f0-9][a-f0-9]),y$",
                    r"^(\%................),y$",
                    r"^(\d\d\d\d),y$"
                ]
            },
            "IND" : {
                "detail"    : "4.5 - Absolute Indirect (a)",
                "bytes"     : 3,
                "regex"     : [
                    r"^\((\$[a-f0-9][a-f0-9][a-f0-9][a-f0-9])\)$",
                    r"^\((\%................)\)$",
                    r"^\((\d\d\d\d)\)$"
                ]
            },
            "ACC" : {
                "detail"    : "4.6 - Accumulator A",
                "bytes"     : 1,
                "regex" : [
                    r"^A$"
                ]
            },
            "IMM" : {
                "detail"    : "4.7 - Immediate Addressing #",
                "bytes"     : 2,
                "regex"     : [
                    r"^#(\$[a-f0-9][a-f0-9])$",
                    r"^#(\%........)$",
                    r"^#(\d\d\d)$"
                ]
            },
            "IMP" : {
                "detail"    : "4.8 - Implied i",
                "bytes" : 1,
                "regex" : [
                    r"^$"
                ]
            },
            "ZP0" : {
                "detail"    : "4.11 - Zero Page zp",
                "bytes"     : 2,
                "regex"     : [
                    r"^(\$[a-f0-9][a-f0-9])$",
                    r"^(\%........)$",
                    r"^(\d\d\d)$"
                ]
            },
            "IZX" : {
                "detail" : "4.12 - Zero Page Indexed Indirect (zp,x)",
                "bytes" : 2,
                "regex" : [
                    r"^\((\$[a-f0-9][a-f0-9]),x\)$",
                    r"^\((\$[a-f0-9][a-f0-9]),X\)$",
                    r"^\((\%........),x\)$",
                    r"^\((\d\d\d),x\)$"
                ]
            },
            "ZPX" : {
                "detail"    : "4.13 - Zero Page Indexed with X zp,x",
                "bytes" : 2,
                "regex" : [
                    r"^(\$[a-f0-9][a-f0-9]),x$",
                    r"^(\%........),x$",
                    r"^(\d\d\d),x$"
                ]
            },
            "ZPY" : {
                "detail"    : "4.14 - Zero Page Indexed with Y zp,y",
                "bytes" : 2,
                "regex" : [
                    r"^(\$[a-f0-9][a-f0-9]),y$",
                    r"^(\%........),y$",
                    r"^(\d\d\d),y$"
                ]
            },
            "ZPI" : {
                "detail"    : "4.15 - Zero Page Indirect (zp)",
                "bytes" : 2,
                "regex" : [
                    r"^\((\$[a-f0-9][a-f0-9])\)$",
                    r"^\((\%........)\)$",
                    r"^\((\d\d\d)\)$"
                ]
            },
            "IZY" : {
                "detail" : "4.16 - Zero Page Indirect Indexed with Y (zp),y",
                "bytes" : 2,
                "regex" : [
                    r"^\((\$[a-f0-9][a-f0-9])\),y$",
                    r"^\((\%........)\),y$",
                    r"^\((\d\d\d)\),y$"
                ]
            }

        },
        "OPCODE" : 
        {
            "BRK": {
                "STA": 0x0
            },
            "ORA": {
                "IZX": 0x1,
                "ZP0": 0x5,
                "IMM": 0x9,
                "ABS": 0xd,
                "IZY": 0x11,
                "ZPI": 0x12,
                "ZPX": 0x15,
                "ABY": 0x19,
                "ABX": 0x1d
            },
            "TSB": {
                "ZP0": 0x4,
                "ABS": 0xc
            },
            "ASL": {
                "ZP0": 0x6,
                "ACC": 0xa,
                "ABS": 0xe,
                "ZPX": 0x16,
                "ABX": 0x1e
            },
            "RMB": {
                "ZP0": 0x77
            },
            "PHP": {
                "STA": 0x8
            },
            "BBR": {
                "REL": 0x7f
            },
            "BPL": {
                "REL": 0x10
            },
            "TRB": {
                "ZP0": 0x14,
                "ABS": 0x1c
            },
            "CLC": {
                "IMP": 0x18
            },
            "INC": {
                "ACC": 0x1a,
                "ZP0": 0xe6,
                "ABS": 0xee,
                "ZPX": 0xf6,
                "ABX": 0xfe
            },
            "JSR": {
                "ABS": 0x20
            },
            "AND": {
                "IZX": 0x21,
                "ZP0": 0x25,
                "IMM": 0x29,
                "ABS": 0x2d,
                "IZY": 0x31,
                "ZPI": 0x32,
                "ZPX": 0x35,
                "ABY": 0x39,
                "ABX": 0x3d
            },
            "BIT": {
                "ZP0": 0x24,
                "ABS": 0x2c,
                "ZPX": 0x34,
                "ABX": 0x3c,
                "IMM": 0x89
            },
            "ROL": {
                "ZP0": 0x26,
                "ACC": 0x2a,
                "ABS": 0x2e,
                "ZPX": 0x36,
                "ABX": 0x3e
            },
            "PLP": {
                "STA": 0x28
            },
            "BMI": {
                "REL": 0x30
            },
            "SEC": {
                "IMP": 0x38
            },
            "DEC": {
                "ACC": 0x3a,
                "ZP0": 0xc6,
                "ABS": 0xce,
                "ZPX": 0xd6,
                "ABX": 0xde
            },
            "RTI": {
                "STA": 0x40
            },
            "EOR": {
                "IZX": 0x41,
                "ZP0": 0x45,
                "IMM": 0x49,
                "ABS": 0x4d,
                "IZY": 0x51,
                "ZPI": 0x52,
                "ZPX": 0x55,
                "ABY": 0x59,
                "ABX": 0x5d
            },
            "LSR": {
                "ZP0": 0x46,
                "ACC": 0x4a,
                "ABS": 0x4e,
                "ZPX": 0x56,
                "ABX": 0x5e
            },
            "PHA": {
                "STA": 0x48
            },
            "JMP": {
                "ABS": 0x4c,
                "IND": 0x6c,
                "IAX": 0x7c
            },
            "BVC": {
                "REL": 0x50
            },
            "CLI": {
                "IMP": 0x58
            },
            "PHY": {
                "STA": 0x5a
            },
            "RTS": {
                "STA": 0x60
            },
            "ADC": {
                "IZX": 0x61,
                "ZP0": 0x65,
                "IMM": 0x69,
                "ABS": 0x6d,
                "IZY": 0x71,
                "ZPI": 0x72,
                "ZPX": 0x75,
                "ABY": 0x79,
                "ABX": 0x7d
            },
            "STZ": {
                "ZP0": 0x64,
                "ZPX": 0x74,
                "ABS": 0x9c,
                "ABX": 0x9e
            },
            "ROR": {
                "ZP0": 0x66,
                "ACC": 0x6a,
                "ABS": 0x6e,
                "ZPX": 0x76,
                "ABX": 0x7e
            },
            "PLA": {
                "STA": 0x68
            },
            "BVS": {
                "REL": 0x70
            },
            "SEI": {
                "IMP": 0x78
            },
            "PLY": {
                "STA": 0x7a
            },
            "BRA": {
                "REL": 0x80
            },
            "STA": {
                "IZX": 0x81,
                "ZP0": 0x85,
                "ABS": 0x8d,
                "IZY": 0x91,
                "ZPI": 0x92,
                "ZPX": 0x95,
                "ABY": 0x99,
                "ABX": 0x9d
            },
            "STY": {
                "ZP0": 0x84,
                "ABS": 0x8c,
                "ZPX": 0x94
            },
            "STX": {
                "ZP0": 0x86,
                "ABS": 0x8e,
                "ZPY": 0x96
            },
            "SMB": {
                "ZP0": 0xf7
            },
            "DEY": {
                "IMP": 0x88
            },
            "TXA": {
                "IMP": 0x8a
            },
            "BBS": {
                "REL": 0xff
            },
            "BCC": {
                "REL": 0x90
            },
            "TYA": {
                "IMP": 0x98
            },
            "TXS": {
                "IMP": 0x9a
            },
            "LDY": {
                "IMM": 0xa0,
                "ZP0": 0xa4,
                "ABS": 0xac,
                "ZPX": 0xb4,
                "ABX": 0xbc
            },
            "LDA": {
                "IZX": 0xa1,
                "ZP0": 0xa5,
                "IMM": 0xa9,
                "ABS": 0xad,
                "IZY": 0xb1,
                "ZPI": 0xb2,
                "ZPX": 0xb5,
                "ABY": 0xb9,
                "ABX": 0xbd
            },
            "LDX": {
                "IMM": 0xa2,
                "ZP0": 0xa6,
                "ABS": 0xae,
                "ZPY": 0xb6,
                "ABY": 0xbe
            },
            "TAY": {
                "IMP": 0xa8
            },
            "TAX": {
                "IMP": 0xaa
            },
            "BCS": {
                "REL": 0xb0
            },
            "CLV": {
                "IMP": 0xb8
            },
            "TSX": {
                "IMP": 0xba
            },
            "CPY": {
                "IMM": 0xc0,
                "ZP0": 0xc4,
                "ABS": 0xcc
            },
            "CMP": {
                "IZX": 0xc1,
                "ZP0": 0xc5,
                "IMM": 0xc9,
                "ABS": 0xcd,
                "IZY": 0xd1,
                "ZPI": 0xd2,
                "ZPX": 0xd5,
                "ABY": 0xd9,
                "ABX": 0xdd
            },
            "INY": {
                "IMP": 0xc8
            },
            "DEX": {
                "IMP": 0xca
            },
            "WAI": {
                "IMP": 0xcb
            },
            "BNE": {
                "REL": 0xd0
            },
            "CLD": {
                "IMP": 0xd8
            },
            "PHX": {
                "IMP": 0xda
            },
            "STP": {
                "IMP": 0xdb
            },
            "CPX": {
                "IMM": 0xe0,
                "ZP0": 0xe4,
                "ABS": 0xec
            },
            "SBC": {
                "IZX": 0xe1,
                "ZP0": 0xe5,
                "IMM": 0xe9,
                "ABS": 0xed,
                "IZY": 0xf1,
                "ZPI": 0xf2,
                "ZPX": 0xf5,
                "ABY": 0xf9,
                "ABX": 0xfd
            },
            "INX": {
                "IMP": 0xe8
            },
            "NOP": {
                "IMP": 0xea
            },
            "BEQ": {
                "REL": 0xf0
            },
            "SED": {
                "IMP": 0xf8
            },
            "PLX": {
                "STA": 0xfa
            }
        }
    }

    # convert STA to IMP, and REL to ZP0

    STAIMP = []
    RELZP0 = []
    for OPC in machine_code['OPCODE']:
        for x in machine_code['OPCODE'][OPC]:
            if x == 'STA':
                STAIMP.append(OPC)
            if x == 'REL':
                RELZP0.append(OPC)
    for OPC in STAIMP:
        machine_code['OPCODE'][OPC]['IMP'] = machine_code['OPCODE'][OPC]['STA']

    for OPC in RELZP0:
        machine_code['OPCODE'][OPC]['ZP0'] = machine_code['OPCODE'][OPC]['REL']
        

    


    asm = []    # this will contain the assembled code

    # if the line is empty, simply ignore it
    if statement != '':
        OPC = statement[0:3]
        VAL = statement[3:].lower() 
        
        # == Determine the addressing mode
        ADDR = "IMP"    # -- we assume everything is implied -- this is just the default
        for x in machine_code['ADDR']:
            b = machine_code['ADDR'][x]['bytes']
            
            for regex in machine_code['ADDR'][x]['regex']:
                # == Do a match on the 
                for v in re.findall(regex,VAL):
                
                    LB = -1
                    HB = -1
                    
                    ADDR = x

                    # == lookup the machine code
                    if not ADDR in machine_code['OPCODE'][OPC]:
                        print ('** ERROR ** Address ' + ADDR + ' is missing from ' + OPC)
                        print(statement)
                        exit(1)
                    mc = machine_code['OPCODE'][OPC][ADDR]
                    asm.append(mc)

                    if b != 1:
                        # translate the value we got
                        if v[0] == '$':
                            c = 16
                        elif v[0] == '%':
                            c = 2
                        else:
                            c = 10
                        
                        if b == 2:
                            LB = int(v[1:], c)
                            asm.append(LB)
                        else:
                            h = int(v[1:], c)
                            HB = h >> 8
                            LB = h & 0xFF
                            
                            asm.append(LB)
                            asm.append(HB)

    return asm

def assemble(prg,options = None):

    output = []

    for l in prg:
        
        new = _assemble_sanitize(l)

        
        asm = _assemble_code(new)
        
        for a in asm:
            #line(' assembler -- ' + hex(a))
            output.append(a)

    return output

def debug():

    # load the program into an array
    program = [
        "; This is the assembler program I will use to test the assembler",
        " ; let's test immediate",
        "LDA #$5678",
        "LDA #$34   ; load the accumulator with the value of $34",
        "   LDA #%00110001  ; so load the accumulator with a binary value",
        "  LDA     #32          ; same thing, but this time we ; just shove a decimal value in",
        "LDA #1234",
        "JMP ($8765,x)",
        "STP"

    ]

    assemble(program,'asm') # mode is either asm, or list

    

if __name__ == "__main__":
    debug()
