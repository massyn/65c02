from cpu65c02 import cpu65c02
from c64display import c64display

import argparse
import time

class bus:

    

    
    def __init__(self,v = None):
        self.rw = False     # Read - False, Write - True
        self.RAM = bytearray([0x00] * 65536)

        self.videoAddress = int(v)  #TODO - if the input is hex, convert it

        if self.videoAddress:
            self.video = c64display(self.videoAddress)
        

    def load(self,romStart,image):
        print('Reading rom image : ' + image)
        in_file = open(image, "rb")
        data = in_file.read()
        in_file.close()
        r = romStart

        self.romStart = romStart
        self.romEnd = romStart + len(data)

        for c in data:
            self.RAM[r] = c
            r += 1

    def read(self,loc):
        d = self.RAM[loc]
        #print('Reading bus - $%04X' % loc + ' $%02X' % d)
        self.rw = False
        self.loc = loc
        self.d = d
        return d

    def write(self,loc,d):
        #print('Writing bus - $%04X' % loc + ' $%02X' % d)
        if loc <= self.romStart & loc >= self.romEnd:
            print ('** trying to write to rom')
            #print('Writing bus - $%04X' % loc + ' $%02X' % d)
        else:
            self.RAM[loc] = d & 0xFF # only 16 bit addresses
            self.d = d

            if self.videoAddress:
                if loc >= self.videoAddress and loc <= self.videoAddress + 1000:
                    self.video.printChar(loc,d)

        self.rw = True
        self.loc = loc
        self.d = d

# =============
    

def hexdump(data,start,r = 0xff):
    for a in range(start,start + r,16):
        print('0x%04X' % a + ' : ' + ' '.join(data[a:a+16].hex()[i:i+2] for i in range(0,len(data[a:a+16].hex()),2)))

def screendump(data,start,width,height):
    screen = ''
    for y in range(1,height):
        for x in range(1,width):
            p = start + (x - 1) + ((y - 1) * width)
            screen += chr(data[p])
        screen += '\n'

    print('--------------------------------------------')
    print(screen)
    print('--------------------------------------------')

# == start of everything -- let's parse our parameters            
parser = argparse.ArgumentParser(description='6502py')
parser.add_argument('--romImage', required=True, help='The ROM image to load into the CPU RAM')
parser.add_argument('--cycleLimit', help='How many CPU cycles to run before stopping - default will run forever')
parser.add_argument('--step',help='Pause after every step executed')
parser.add_argument('--display',help='Show the display')
#parser.add_argument('--romStart', default = '0x8000', help='The ROM image to load into the CPU RAM')
parser.add_argument('--ramDump', help='Specify the address to do a ram dump after every clock cycle.')

args = parser.parse_args()

b = bus(args.display)   # pass the video memory location
chip = cpu65c02(b)

b.load(0x8000, args.romImage)



chip.RESET()
_pc = chip.PC
_cycle = 0

while chip.ENABLE:

    chip.CLOCK()
    print (chip.asm)
    chip.cpudump()

    if args.ramDump:
        hexdump(b.RAM,int(args.ramDump))

    # TODO - this is now in the bus
    if args.display:
        b.video.loop()
    
    #hexdump(chip.RAM,0x0100,0xFF)   # Stack

#    hexdump(chip.RAM,0x8000)
    #if args.display != None:
        #screendump(chip.RAM,0x0400,40,25)
        #video.loop(chip.RAM[0x0400:0x07E8])

    #print('---------------------')

    #screendump(b.RAM,0x0400,40,25)

    if args.step != None:
        #time.sleep(1)
        input()


    # == if the CPU runs away from us, stop it
    if args.cycleLimit != None:

        if _cycle >= int(args.cycleLimit):
            print(' ** cycleLimit reached.. Stopping')
            chip.ENABLE = False

    # == if the program counter is stuck, the CPU is not moving
    if _pc == chip.PC:
        screendump(b.RAM,0x0400,40,25)
        print ('ERROR - Program Counter is stuck')
        chip.ENABLE = False
    
    _pc = chip.PC + 0x999999999
    _cycle += 1
    
