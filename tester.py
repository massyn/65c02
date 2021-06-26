import json
from assembler.assemble import *

total = 0
totalok = 0
with open('tests.json') as t:
    testdata = json.load(t)

    for test in testdata:
        print('Test ==> ' + test)

        # == compile the program
        print(testdata[test]['program'])
        prg = assemble(testdata[test]['program'])

        if 'asm' in testdata[test]['expect']:
            print(' -- Expecting to test the output assembler...')
            status = True
            c = 0 
            for m in  testdata[test]['expect']['asm'].split():
                e = int(m, 16)
                if hex(e) != hex(prg[c]):
                    status = False
                    print('Did not match on position ' + str(c))
                    print(' Expecting ==> ' + hex(e))
                    print(' What we got ==> ' + hex(prg[c]))

                c = c + 1
            
        print ("")
        total = total + 1
        if status:
            print (' ****  PASSED ****')
            totalok = totalok + 1
        else:
            print (' !!!!!!!!!!!!!!!! FAILED !!!!!!!!!!!!!!!!!!!')
        
        print ("---------------------------------------------------------")
        #print(prg)


print ('Total tests   == ' + str(total))
print ('Total passed  == ' + str(totalok))
