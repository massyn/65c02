# 65c02
65c02 emulator in Python
## Why build an emulator?
I'm certainly not the first to do it.  For me there's a nostalgic aspect to it.  I started programming the Commodore 64, back when it was still cool.  So playing with the 6502 CPU is a way to learn more about the chip, and how it revolutinzed the computer industry.
With this project, the goal is not to reproduce the C64.  The more I learn about the C64, the more I realize that there's a lot of components that will need to be reproduced.  I do not have the time, the skill, or the patience to build it all.  Instead, I will build a very basic sbc (single board computer), all in software of course, that would represent some sort of computer.

## SBC memory map
The SBC is laid out with RAM and ROM, each 32K in size.
```
$0000:$7FFF - RAM
$8000:$FFFF - ROM
```

Should you use the display, you can allocate a memory location for the display.  The C64 would typically use $0C00 for it's memory, so when running any of the sample programs, you need to specify to the SBC command line to use 1024 ($0C00)

You can easily adjust these memory locations.  The sbc.py script will wrap everything together, allowing you to customize the bus for other "virtual" devices.

## Getting started
To run the simple counter app, execute the following
```
python sbc.py --romImage rom/counter.bin --display 1024
```

## Assembler
The files provied in this emulator has been assembled with [vasm|http://www.compilers.de/vasm.html].  If you couldn't be bothered, the assembler files (in asm) have been assembled as rom inages in the rom folder.
To assemble it yourself, download vasm, and run this command
```
vasm6502_oldstyle.exe helloworld.asm -dotdir -Fbin
```
The assembled rom image will be saved as a.out

## Caveats
Not everything is perfect.  Chances are that some 65c02 binaries won't run exactly as expected.  I'm welcome to get feedback and fix any bugs that may exist. Some issues I am aware of...

[ ] - It is closer to a 6502, rather than 65c02.  I need to fix that up.  The idea is to have something that you can actually purchase and use, and sticking to the 6502 just doesn't cut it.
[ ]  - The CPU clock is not implemented very well.  Where the actual 65c02 may take 4 or 5 clock cycles to do an instruction, my emulator does it all in one hit.  This may not really be an issue, except in applications that need certain actions to occur on a certain cycle.  There is a provision to handle this.  More on this later.
[ ] - The display is more like a graphics card that does all the heavy lifting.  A C64 would refer to some ROM image to get the characters to be displayed.  This emulator simply uses a font.  The idea with this emulator is that there is a _screen card_ attached to the ROM that will render whatever is in memory onto the screen.

## Todo list
There is still some work to be done with this emulator, like :

[ ] - Not all the 65c02 instructions are implemented yet.
[ ] - There is no "keyboard" yet.  So any input is still getting ignored.
[ ] - Add a few more command line options to sbc.py

## FAQ
### Can it run Commodore BASIC?
Not yet.  There's a lot of components involved with Commodore Basic.  It is still a work in progress.