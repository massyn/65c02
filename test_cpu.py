from cpu65c02 import cpu65c02

#from c64display import c64display

def test(desc,ref, act):
    if(ref == act):
        print('PASS   - ' + desc + ' (expected ' + str(ref) + ')')
    else:
        print('FAILED - ' + desc + ' (expected ' + str(ref) + ', got ' + str(act) + ')')

def hexdump(data,start,r = 0xff):
    for a in range(start,start + r,16):
        print('0x%04X' % a + ' : ' + ' '.join(data[a:a+16].hex()[i:i+2] for i in range(0,len(data[a:a+16].hex()),2)))

class bus:
   
    def __init__(self):
        self.rw = False     # Read - False, Write - True
        self.RAM = bytearray([0x00] * 65536)

        #self.video = c64display(0x0400)

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

        self.RAM[loc] = d & 0xFF # only 16 bit addresses
        self.d = d


        self.rw = True
        self.loc = loc
        self.d = d

tests = {
    'CLD - test_reset_clears_decimal_flag' : {
        'input'     : {
            'D' : True,
            'PC' : 0x8000,
            'RAM' : {
                0x8000 : [ 0xD8 ]
            }
        },
        'expect'    : {
            'D' : False,
            'PC' : 0x8001
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_carry_clear_in_accumulator_zeroes' : {
        'input' : {
            'A' : 0x00,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72, 0x10 ],
                0x0010 : [ 0xCD, 0xAB ],
                0xABCD : [ 0x00]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x00,
            'C' : False,
            'N' : False,
            'Z' : True
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_carry_set_in_accumulator_zero': {
        'input' : {
            'A' : 0x00,
            'C' : True,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x01,
            'N' : False,
            'Z' : False,
            'C' : False,
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_carry_clear_in_no_carry_clear_out' : {
        'input' : {
            'A' :0x01,
            'C' : False,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0xFE ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0xFF,
            'N' : True,
            'C' : False,
            'Z' : False
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_carry_clear_in_carry_set_out' : {
        'input' : {
            'A' :0x02,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0xFF ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x01,
            'N' : False,
            'C' : True,
            'Z' : False
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_overflow_cleared_no_carry_01_plus_01' : {
        'input' : {
            'C' : False,
            'A' : 0x01,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x01 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x02,
            'V' : False
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_overflow_cleared_no_carry_01_plus_ff' : {
        'input' : {
            'C' : False,
            'A' : 0x01,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0xFF ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x00,
            'V' : False
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_overflow_set_no_carry_7f_plus_01' : {
        'input' : {
            'C' : False,
            'A' : 0x7F,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x01 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x80,
            'V' : True
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_overflow_set_no_carry_80_plus_ff' : {
        'input' : {
            'C' : False,
            'A' : 0x80,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0xFF ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x7F,
            'V' : True
        }
    },
    'ADC - test_adc_bcd_off_zp_ind_overflow_set_on_40_plus_40' : {
        'input' : {
            'A' : 0x40,
            'C' : False,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x72 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x40 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x80,
            'V' : True,
            'N' : True,
            'Z' : False
        }
    },
    'AND - test_and_zp_ind_all_zeros_setting_zero_flag' : {
        'input' : {
            'A' : 0xFF,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x32 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x00,
            'N' : False,
            'Z' : True
        }
    },
    'AND - test_and_zp_ind_zeros_and_ones_setting_negative_flag' : {
        'input' : {
            'A' : 0xFF,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x32 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0xAA ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0xAA,
            'N' : True,
            'Z' : False
        }
    },
    'BIT - test_bit_abs_x_copies_bit_7_of_memory_to_n_flag_when_0' : {
        'input' : {
            'N' : True,
            'X' : 0x02,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x3C , 0xEB, 0xFE ],
                0xFEED : [ 0xFF  ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'N' : True
        }
    },
    'BIT - test_bit_abs_x_copies_bit_7_of_memory_to_n_flag_when_1' : {
        'input' : {
            'N' : True,
            'X' : 0x02,
            'PC' : 0x0000,
            'A' : 0xFF,
            'RAM' : {
                0x0000 : [ 0x3C , 0xEB, 0xFE ],
                0xFEED : [ 0x00  ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'N' : False
        }
    },
    'BIT - test_bit_abs_x_copies_bit_6_of_memory_to_v_flag_when_0' : {
        'input' : {
            'V' : False,
            'A' : 0xFF,
            'X' : 0x02,
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x3C , 0xEB , 0xFE ],
                0xFEED : [ 0xFF ]
            }
        },
        'expect' : {
            'V' : True,
            'PC' : 0x0003,
            'CYCLES' : 4
        }
    },
    'BIT - test_bit_abs_x_copies_bit_6_of_memory_to_v_flag_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'V' : True,
            'A' : 0xFF,
            'X' : 0x02,
            'RAM' : {
                0x0000 : [ 0x3C,0xEB,0xFE ],
                0xFEED : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'V' : False,
            'cycles' : 4,
            'RAM' : {
            }
        }
    },
    'test_bit_abs_x_stores_result_of_and_in_z_preserves_a_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'X' : 0x02,
            'RAM' : {
                0x0000 : [ 0x3C,0xEB,0xFE ],
                0xFEED : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'A' : 0x01,
            'cycles' : 4,
            'RAM' : {
                0xFEED : [ 0x00 ],
            }
        }
    },
    'test_bit_abs_x_stores_result_of_and_nonzero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : True,
            'A' : 0x01,
            'X' : 0x02,
            'RAM' : {
                0x0000 : [ 0x3C,0xEB,0xFE ],
                0xFEED : [ 0x01 ],
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : False,
            'A' : 0x01,
            'cycles' : 4,
            'RAM' : {
                0xFEED : [ 0x01 ],
            }
        }
    },
    'test_bit_abs_x_stores_result_of_and_when_zero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'X' : 0x02,
            'RAM' : {
                0x0000 : [ 0x3C,0xEB,0xFE ],
                0xFEED : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'A' : 0x01,
            'cycles' : 4,
            'RAM' : {
                0xFEED : [ 0x00 ],
            }
        }
    },
    'test_bit_imm_does_not_affect_n_and_z_flags' : {
        'input' : {
            'PC' : 0x0000,
            'N' : True,
            'V' : True,
            'A' : 0x00,
            'RAM' : {
                0x0000 : [ 0x89,0xff ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'N' : True,
            'V' : True,
            'A' : 0x00,
            'cycles' : 2,
            'RAM' : {
            }
        }
    },
    'test_bit_imm_stores_result_of_and_in_z_preserves_a_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'RAM' : {
                0x0000 : [ 0x89,0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'A' : 0x01,
            'cycles' : 2,
            'RAM' : {
            }
        }
    },
    'test_bit_imm_stores_result_of_and_when_nonzero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : True,
            'A' : 0x01,
            'RAM' : {
                0x0000 : [ 0x89,0x01 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : False,
            'A' : 0x01,
            'cycles' : 2,
            'RAM' : {
            }
        }
    },
    'test_bit_imm_stores_result_of_and_when_zero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'RAM' : {
                0x0000 : [ 0x89,0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'A' : 0x01,
            'cycles' : 2,
            'RAM' : {
            }
        }
    },
    'test_bit_zp_x_copies_bit_7_of_memory_to_n_flag_when_0' : {
        'input' : {
            'PC' : 0x0000,
            'N' : False,
            'A' : 0xFF,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0xFF ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'N' : True,
            'cycles' : 4,
            'RAM' : {
            }
        }
    },
    'test_bit_zp_x_copies_bit_7_of_memory_to_n_flag_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'N' : True,
            'A' : 0xFF,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'N' : False,
            'cycles' : 4,
            'RAM' : {
            }
        }
    },
    'test_bit_zp_x_copies_bit_6_of_memory_to_v_flag_when_0' : {
        'input' : {
            'PC' : 0x0000,
            'V' : False,
            'A' : 0xFF,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0xFF ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'V' : True,
            'cycles' : 4,
            'RAM' : {
            }
        }
    },
    'test_bit_zp_x_copies_bit_6_of_memory_to_v_flag_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'V' : True,
            'A' : 0xFF,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'V' : False,
            'cycles' : 4,
            'RAM' : {
            }
        }
    },
    'test_bit_zp_x_stores_result_of_and_in_z_preserves_a_when_1' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x01,
            'cycles' : 4,
            'RAM' : {
                0x0013 : [ 0x00 ],
            }
        }
    },
    'test_bit_zp_x_stores_result_of_and_when_nonzero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : True,
            'A' : 0x01,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0x01 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : False,
            'cycles' : 2,
            'RAM' : {
                0x0013 : [ 0x01 ],
            }
        }
    },
    'test_bit_zp_x_stores_result_of_and_when_zero_in_z_preserves_a' : {
        'input' : {
            'PC' : 0x0000,
            'Z' : False,
            'A' : 0x01,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x34,0x10 ],
                0x0013 : [ 0x00 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'A' : 0x01,
            'cycles' : 4,
            'RAM' : {
                0x0013 : [ 0x00 ],
            }
        }
    },
    'test_brk_clears_decimal_flag' : {
        'input' : {
            'PC' : 0xC000,
            'D' : True,
            'RAM' : {
                0xC000 : [ 0x00 ],
            }
        },
        'expect' : {
            'B' : True,
            'D' : False,
            'RAM' : {
            }
        }
    },
    'test_cmp_zpi_sets_z_flag_if_equal' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x42,
            'RAM' : {
                0x0000 : [ 0xD2,0x10 ],
                0x0010 : [ 0xCD,0xAB ],
                0xABCD : [ 0x42 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'A' : 0x42,
            'N' : False,
            'Z' : True,
            'cycles' : 5
        }
    },
    'test_cmp_zpi_resets_z_flag_if_unequal' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x43,
            'RAM' : {
                0x0000 : [ 0xD2,0x10 ],
                0x0010 : [ 0xCD,0xAB ],
                0xABCD : [ 0x42 ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'N' : False,
            'Z' : False,
            'A' : 0x43,
            'cycles' : 5,
            'RAM' : {
            }
        }
    },
    'test_eor_zp_ind_flips_bits_over_setting_z_flag' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0xFF,
            'RAM' : {
                0x0000 : [ 0x52,0x10 ],
                0x0010 : [ 0xCD,0xAB ],
                0xABCD : [ 0xFF ],
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'A' : 0x00,
            'cycles' : 5,
            'RAM' : {
                0xABCD : [ 0xFF ],
            }
        }
    },
    'Addressing - ABS - 4.1 Absolute - a' : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xAD, 0xCD, 0xAB ],
                0xABCD : [ 0x42 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'A' : 0x42
        }
    },
    'Addressing - IAX - 4.2 Indexed Indirect - (a,x)' : {
        'input' : {
            'PC' : 0x0000,
            'X' : 0x02,
            'RAM' : {
                0x0000 : [ 0x7C, 0xCD , 0xAB ],
                0xABCF : [ 0x34, 0x12 ]
            }
        },
        'expect' : {
            'PC' : 0x1234,
            'cycles' : 6
        }
    },
    'Addressing - ABX - 4.3 Absolute Indexed with X - a,x' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [0xBD , 0xCD, 0xAB ],
                0xABD0 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'A' : 0x80,
            'N' : True,
            'Z' : False
        }
    },
    'Addressing - ABY - 4.4 Absolute Indexed with Y - a,y' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'Y' : 0x03,
            'RAM' : {
                0x0000 : [0xB9 , 0xCD, 0xAB ],
                0xABD0 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'A' : 0x80,
            'N' : True,
            'Z' : False
        }
    },
    'Addressing - IND - 4.5 Absolute Indirect - (a) - test_jmp_ind_does_not_have_page_wrap_bug' : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x6C, 0xFE, 0x10],
                0x10FE : [ 0xCD, 0xAB ]
            }
        },
        'expect' : {
            'PC' : 0xABCD,
            'cycles' : 6
        }
    },
    'Addressing - IND - 4.5 Absolute Indirect - (a) - test_jmp_ind_jumps_to_indirect_address' : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x6C , 0x00 , 0x02 ],
                0x0200 : [ 0xCD , 0xAB ]
            }
        },
        'expect' : {
            'PC' : 0xABCD
        }
    },
    'Addressing - IND - 4.5 Absolute Indirect - (a) - test_jmp_jumps_to_address_with_page_wrap_bug' : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x6C, 0xFF, 0x00],
                0x00FF : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x6C00,
            'cycles' : 5
        }
    },
    'Addressing - ACC - 4.6 - Accumulator A' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x42,
            'RAM' : {
                0x0000 : [ 0x1A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0x43,
            'Z' : False,
            'N' : False
        }
    },
    'Addressing - IMM - 4.7 Immediate - #' : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xA9, 0x69 ]
            }
        },
        'expect' : {
            'A' : 0x69,
            'PC' : 0x0002,
            'cycles' : 2
        }
    },
    'Addressing - IMP - 4.8 Implied - i' : {
        'input' : {
            'PC'    : 0x0000,
            'X' : 0x09,
            'RAM' : {
                0x0000 : [ 0xE8 ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'X'     : 0x0A,
            'Z'     : False,
            'N'     : False
        }
    },
    'Addressing - REL - 4.9 Program Counter Relative - forward - r' : {
        'input' : {
            'PC'    : 0x0000,
            'Z'     : False,
            'RAM'   : {
                0x0000 : [ 0xD0, 0x06 ]
            }
        },
        'expect' : {
            'PC' : 0x0008
        }
    },
    'Addressing - REL - 4.9 Program Counter Relative - reverse - r' : {
        'input' : {
            'PC'    : 0x0050,
            'Z'     : False,
            'RAM'   : {
                0x0050 : [ 0xD0, 0xFA ]
            }

        },
        'expect' : {
            'PC' : 0x004C
        }
    },
    'Addressing - STA - 4.10 Stack - s - test_pha_pushes_a_and_updates_sp' : {
        'input' : {
            'PC'    : 0x0000,
            'A' : 0xAB,
            'RAM' : {
                0x0000 : [ 0x48 ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'A'     : 0xAB,
            'SP'    : 0xFE,
            'RAM'   : {
                0x01FF : [ 0xAB ]
            }
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - ROL c = 0 ; Z' : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'RAM' : {
                0x0010 : [ 0x00 ]
            },
            'Z' : True,
            'N' : False
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - ROL C = 0; Z=1' : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'Z' : False,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0x00 ]
            },
            'Z' : True,
            'N' : False
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - ROL - carry one clear Z' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0x01 ]
            },
            'Z' : False,
            'N' : False
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - test_rol_zp_sets_n_flag' : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0x40 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0x81 ]
            },
            'N' : True,
            'Z' : False
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - test_rol_zp_shifts_out_zero' : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0x7F ]
            }

        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0xFE ]
            },
            'C' : False
        }
    },
    'Addressing - ZP0 - 4.11 - Zero Page - zp - test_rol_zp_shifts_out_one' : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x26 , 0x10 ],
                0x0010 : [ 0xFF ]
            }

        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0xFE ]
            },
            'C' : True
        }
    },
    'Addressing - IZX - 4.12 - Zero Page Indexed Indirect - (zp,x) - test_lda_ind_indexed_x_has_page_wrap_bug' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'X' : 0xFF,
            'RAM' : {
                0x0000 : [ 0xA1 , 0x80 ],
                0x007F : [ 0xBB , 0xBB ],
                0x017F : [ 0xCD , 0xAB ],
                0xABCD : [ 0x42 ],
                0xBBBB : [ 0xEF ]
            }
        },
        'expect' : {
            'A' : 0xEF
        }
    },
    'Addressing - IZX - 4.12 - Zero Page Indexed Indirect - (zp,x) - test_lda_ind_indexed_x_loads_a_sets_n_flag' : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,
            'X'     : 0x03,
            'RAM' : {
                0x0000 : [ 0xA1, 0x10 ],
                0x0013 : [ 0xCD, 0xAB ],
                0xABCD  : [ 0x80 ],
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'A'     : 0x80,
            'N'     : True,
            'Z'     : False
        }
    },
    'Addressing - IZX - 4.12 - Zero Page Indexed Indirect - (zp,x) - test_lda_ind_indexed_x_loads_a_sets_z_flag' : {
        'input' : {
            'PC' : 0x0000,
            'A'     : 0x00,
            'X'     : 0x03,
            'RAM' : {
                0x0000 : [ 0xA1 , 0x10 ],
                0x0013 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x00 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'A'     : 0x00,
            'Z'     : True,
            'N'     : False
        }
    },
    'Addressing - ZPX - 4.13 - Zero Page Indexed with X - zp,x - test_lda_zp_x_indexed_loads_a_sets_n_flag' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0xB5, 0x10 ],
                0x0013 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'A'     : 0x80,
            'N'     : True,
            'Z'     : False
        }
    },
    'Addressing - ZPX - 4.13 - Zero Page Indexed with X - zp,x - test_lda_zp_x_indexed_loads_a_sets_z_flag' : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0xFF,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0xB5 , 0x10 ],
                0x0013 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC'        : 0x0002,
            'A'         : 0x00,
            'Z'         : True,        
            'N'         : False
        }
    },
    'Addressing - ZPY - 4.14 - Zero Page Indexed with Y - zp,y - test_ldx_zp_y_indexed_loads_x_sets_n_flag' : {
        'input' : {
            'PC' : 0x0000,
            'X' : 0x00,
            'Y' : 0x03,
            'RAM' : {
                0x0000 : [ 0xB6 , 0x10 ],
                0x0013 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'X' : 0x80,            
            'N' : True,
            'Z' : False
        }
    },
    'Addressing - ZPY - 4.14 - Zero Page Indexed with Y - zp,y - test_ldx_zp_y_indexed_loads_x_sets_z_flag' : {
        'input' : {
            'PC' : 0x0000,
            'X' : 0xFF,
            'Y' : 0x03,
            'RAM' : {
                0x0000 : [ 0xB6 , 0x10 ],
                0x0013 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'X'     : 0x00,
            'Z'     : True,
            'N'     : False
        }
    },
    'Addressing - ZPI - 4.15 - Zero Page Indirect - (zp) - test_lda_zp_ind_loads_a_sets_n_flag'  : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,
            'RAM' : {
                0x0000 : [ 0xB2 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x80 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'cycles'    : 5,
            'A'         : 0x80,
            'N'         : True,
            'Z'         : False
        }
    },
    'Addressing - ZPI - 4.15 - Zero Page Indirect - (zp) - test_lda_zp_ind_loads_a_sets_z_flag'  : {
        'input' : {
            'PC' : 0x0000,
            'A'     : 0x00,
            'RAM' : {
                0x0000 : [ 0xB2 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABCD : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'cycles'    : 5,
            'A'         : 0x00,
            'Z'         : True,
            'N'         : False
        }
    },
    'Addressing - ZPI - 4.15 - Zero Page Indirect - (zp) - test_lda_zp_ind_loads_a_sets_n_flag'  : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,
            'RAM' : {
                0x0000 : [ 0xB2, 0x10 ],
                0x0010 : [ 0xCD, 0xAB ],
                0xABCD : [ 0x80 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'cycles'    : 5,
            'A'         : 0x80,
            'N'         : True,
            'Z'         : False,
        }
    },
    'Addressing - ZPI - 4.15 - Zero Page Indirect - (zp) - test_lda_zp_ind_loads_a_sets_z_flag'  : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,
            'RAM' : {
                0x0000 : [ 0xB2, 0x10 ],
                0x0010 : [ 0xCD, 0xAB ],
                0xABCD : [ 0x00 ],
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'cycles'    : 5,
            'A'         : 0x00,
            'Z'         : True,
            'N'         : False
        }
    },
    'Addressing - IZY - 4.16 - Zero Page Indirect Indexed with Y - (zp),y - test_lda_indexed_ind_y_loads_a_sets_n_flag'  : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,
            'Y'     : 0x03,
            'RAM' : {
                0x0000 : [ 0xB1 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABD0 : [ 0x80 ]
            }
        },
        'expect' : {
            'PC'        : 0x0002,
            'A'         : 0x80,
            'N'         : True,
            'Z'         : False
        }
    },
    'Addressing - IZY - 4.16 - Zero Page Indirect Indexed with Y - (zp),y - test_lda_indexed_ind_y_loads_a_sets_z_flag'  : {
        'input' : {
            'PC'    : 0x0000,
            'A'     : 0x00,          
            'Y'     : 0x03,
            'RAM' : {
                0x0000 : [ 0xB1 , 0x10 ],
                0x0010 : [ 0xCD , 0xAB ],
                0xABD0 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC'        : 0x0002,
            'A'         : 0x00,
            'Z'         : True,
            'N'         : False
        }
    },
    'Addressing - IZY - 4.16 - Zero Page Indirect Indexed with Y - (zp),y - test_lda_indexed_ind_y_has_page_wrap_bug'  : {
        'input' : {
            'PC'    : 0x1000,
            'A'     : 0x00,
            'Y'     : 0x02,
            'RAM' : {
                0x1000 : [ 0xB1, 0xFF ],
                0x00ff : [ 0x10 ],
                0x0100 : [ 0x20 ], 
                0x0000 : [ 0x00 ],
                0x2012 : [ 0x14 ],
                0x0012 : [ 0x42 ]
            }
        },
        'expect' : {
            'A' : 0x42
        }
    }, 
    'PLA - test_pla_pulls_top_byte_from_stack_into_a_and_updates_sp'  : {
        'input' : {
            'PC' : 0x0000,
            'SP' : 0xFE,
            'RAM' : {
                0x0000 : [ 0x68 ],
                0x01FF : [ 0xAB ],
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0xAB,
            'SP'    : 0xFF
        }
    },
    'PLP - test_plp_pulls_top_byte_from_stack_into_flags_and_updates_sp'  : {
        'input' : {
            'PC'    : 0x0000,
            'SP'    : 0xFE,
            'RAM'   : {
                0x0000 : [ 0x28 ],
                0x01FF : [ 0xBA ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'SP'    : 0xFF,
            'N'     : True,
            'V'     : False,
            '5'     : True,
            'B'     : True,
            'D'     : True,
            'I'     : False,
            'Z'     : True,
            'C'     : False
        }
    },
    'PHP - test_php_pushes_processor_status_and_updates_sp'  : {
        'input' : {
            'PC' : 0x0000,
            'N' : False,
            'V' : False,
            '5' : True,
            'B' : True,
            'D' : False,
            'I' : False,
            'Z' : False,
            'C' : False,
            
            'RAM' : {
                0x0000 : [ 0x08 ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'RAM'   : {
                0x01FF : [ 0b00110000 ]
                
            },
            'SP' : 0xFE
        }
    },

    'PHX - test_phx_pushes_x_and_updates_sp'  : {
        'input' : {
            'PC'    : 0x0000,
            'X'     : 0xAB,
            'RAM' : {
                0x0000 : [ 0xDA ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'X'     : 0xAB,
            'SP'    : 0xFE,
            'cycles'    : 3,
            'RAM'   : {
                0x01FF : [ 0xAB ]
            }
        }
    },
    'PHY - test_phy_pushes_y_and_updates_sp'  : {
        'input' : {
            'PC'    : 0x0000,
            'Y'     : 0xAB,
            'RAM' : {
                0x0000 : [ 0x5A ]
            }
        },
        'expect' : {
            'PC'        : 0x0001,
            'Y'         : 0xAB,
            'SP'        : 0xFE,
            'cycles'    : 3,
            'RAM'   : {
                0x01FF : [ 0xAB ]
            }
        }
    },
    'PLX - test_plx_pulls_top_byte_from_stack_into_x_and_updates_sp'  : {
        'input' : {
            'PC' : 0x0000,
            'SP' : 0xFE,
            'RAM' : {
                0x0000 : [ 0xFA ],
                0x01FF : [ 0xAB ]
            }
        },
        'expect' : {
            'PC'        : 0x0001,
            'X'         : 0xAB,
            'SP'        : 0xFF,
            'cycles'    : 4
        }
    },
    'PLY - test_ply_pulls_top_byte_from_stack_into_y_and_updates_sp'  : {
        'input' : {
            'PC' : 0x0000,
            'SP'    : 0xFE,
            'RAM' : {
                0x0000 : [ 0x7A ],
                0x01FF : [ 0xAB ]
            }
        },
        'expect' : {
            'PC'    : 0x0001,
            'Y'     : 0xAB,
            'SP'    : 0xFF,
            'cycles'    : 4
        }
    },
    'LSR - test_lsr_accumulator_rotates_in_zero_not_carry'  : {
        'input' : {
            'PC' : 0x0000,
            'C'     : True,
            'A' : 0x00,
            'RAM' : {
                0x0000 : [ 0x4A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0x00,
            'Z' : True,
            'C' : False,
            'N' : False,
        }
    },
    'LSR - test_lsr_accumulator_sets_carry_and_zero_flags_after_rotation'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'A' : 0x01,
            'RAM' : {
                0x0000 : [ 0x4A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0x00,
            'Z' : True,
            'C' :True,
            'N' : False,
        }
    },      
    'LSR - btest_lsr_accumulator_rotates_bits_rightlank'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'A' : 0x04,
            'RAM' : {
                0x0000 : [ 0x4A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A'     : 0x02,
            'Z' : False,
            'C' : False,
            'N' : False,
        }
    },
    'LSR - test_lsr_absolute_rotates_in_zero_not_carry'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x4E, 0xCD, 0xAB ],
                0xABCD : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'C' : False,
            'N' : False,
            'RAM' : {
                0xABCD : [ 0x00 ]
            }
        }
    },
    'LSR - test_lsr_absolute_sets_carry_and_zero_flags_after_rotation'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x4E, 0xCD, 0xAB ],
                0xABCD : [ 0x01 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'C' :True,
            'N' : False,
            'RAM' : {
                0xABCD : [ 0x00]
            }
        }
    },
    'LSR - test_lsr_absolute_rotates_bits_right'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x4E, 0xCD, 0xAB ],
                0xABCD : [ 0x04 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : False,
            'C' : False,
            'N' : False,
            'RAM' : {
                0xABCD : [ 0x02 ]
            }
        }
    },
    'LSR - test_lsr_zp_rotates_in_zero_not_carry'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x46, 0x10 ],
                0x0010 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'C' : False,
            'N' : False,
            'RAM' : {
                    0x0010 : [ 0x00 ]
            }
        }
    },   
    'LSR - test_lsr_zp_sets_carry_and_zero_flags_after_rotation'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x46, 0x10 ],
                0x0010 : [ 0x01 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'C' :True,
            'N' : False,
            'RAM' : {
                0x0010 : [ 0x00 ]
            }
        }
    },
    'LSR - test_lsr_zp_rotates_bits_right'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x46, 0x10 ],
                0x0010 : [ 0x04 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : False,
            'C' : False,
            'N' : False,
            'RAM' : {
                0x0010 : [ 0x02 ]
            }
        }
    },
    'LSR - test_lsr_abs_x_indexed_rotates_in_zero_not_carry'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x5E, 0xCD, 0xAB ],
                0xABD0 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'C' : False,
            'N' : False,
            'RAM' : {
                0xABD0 : [ 0x00 ]
            }
        }
    },
    'LSR - test_lsr_abs_x_indexed_sets_c_and_z_flags_after_rotation'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x5E, 0xCD, 0xAB ],
                0xABD0 : [ 0x01 ]
            }

        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : True,
            'C' : True,
            'N' : False,
            'RAM' : {
                0xABD0 : [ 0x00 ]
            }
        }
    },     
    'LSR - test_lsr_abs_x_indexed_rotates_bits_right'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x5E, 0xCD, 0xAB ],
                0xABD0 : [ 0x04]
            }

        },
        'expect' : {
            'PC' : 0x0003,
            'Z' : False,
            'C' : False,
            'N' : False,
            'RAM' : {
                0xABD0 : [ 0x02 ]
            }
        }
    },
    'LSR - test_lsr_zp_x_indexed_rotates_in_zero_not_carry'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x56, 0x10 ],
                0x0013 : [ 0x00 ]
            }
        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'C' : False,
            'N' : False,
            'RAM' : {
                0x0013 : [ 0x00 ]
            }
        }
    },
    'LSR - test_lsr_zp_x_indexed_sets_carry_and_zero_flags_after_rotation'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : False,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x56, 0x10 ],
                0x0013 : [ 0x01 ]
            }

        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : True,
            'C' :True,
            'N' : False,
            'RAM' : {
                0x0013 : [ 0x00 ]
            }

        }
    },
    'LSR - test_lsr_zp_x_indexed_rotates_bits_right'  : {
        'input' : {
            'PC' : 0x0000,
            'C' : True,
            'X' : 0x03,
            'RAM' : {
                0x0000 : [ 0x56, 0x10 ],
                0x0013 : [ 0x04 ]
            }

        },
        'expect' : {
            'PC' : 0x0002,
            'Z' : False,
            'C' : False,
            'N' : False,
            'RAM' : {
                0x0013 : [ 0x02 ]
            }
        }
    },
    'ROR - test_ror_accumulator_shifts_out_one'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x03,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x6A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0x81,
            'C' : True
        }
    },
    'ROR - test_ror_accumulator_zero_and_carry_zero_sets_z_flag'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'C' : False,
            'RAM' : {
                0x0000 : [ 0x6A ]                
            }
        },
        'expect' : {
            'PC'        : 0x0001,
            'A'         : 0x00,
            'Z'         : True,
            'N'         : False
        }
    },
    'ROR - test_ror_accumulator_zero_and_carry_one_rotates_in_sets_n_flags'  : {
        'input' : {
            'PC' : 0x0000,
            'A'     : 0x00,
            'C'     : True,
            'RAM' : {
                0x0000 : [ 0x6A ]
            }
        },
        'expect' : {
            'PC' : 0x0001,
            'A' : 0x80,
            'Z' : False,
            'N' : True

        }
    },
    'ROR - test_ror_accumulator_shifts_out_zero'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x02,
            'C' : True,
            'RAM' : {
                0x0000 : [ 0x6A ]
            }

        },
        'expect' : {
            'PC'    : 0x0001,
            'A'     : 0x81,
            'C'     : False
        }
    },
    'test_irq_pushes_pc_and_correct_status_then_sets_pc_to_irq_vector'  : {
        'input' : {
            'PC' : 0xC123,
            '5' : True,
            'C' : False,
            'N' : False,
            'I' : False,
            'B' : False,
            'RAM' : {
                0xFFFA : [ 0x88, 0x77 ],
                0xFFFE : [ 0xCD, 0xAB ]
            },
            'function' : 'irq'
        },
        'expect' : {
            'PC'    : 0xABCD,
            'RAM'   : {
                0x1FF : [ 0xC1 ],
                0x1FE : [ 0x23 ],
                0x1FD : [ 0b00100000 ]
            },
            'SP' : 0xFC,
            '5' : True,
            'I' : True,
            'cycles' : 7
        }
    },
    'RTI - test_rti_restores_status_and_pc_and_updates_sp'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x40 ],
                0x01FD : [ 0xFC, 0x03, 0xC0 ]
            },
            'SP'    : 0xFC
        },
        'expect' : {
            'PC'    : 0xC003,
            'N'     : True,
            'V'     : True,
            '5'     : True,
            'B'     : True,
            'D'     : True,
            'I'     : True,
            'SP'    : 0xFF
        }
    },
    'RTI - test_rti_forces_break_and_unused_flags_high'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0x40 ],
                0x01FD : [ 0x00, 0x03, 0xC0 ]
            },
            'SP' : 0xFC
        },
        'expect' : {
            'B' : True,
            '5' : True
        }
    },
  
    'test_brk_interrupt - 1'  : {
        'input' : {
            'N'     : False,
            'V'     : False,
            '5'     : False,
            'B'     : False,
            'D'     : False,
            'I'     : False,
            'Z'     : False,
            'C'     : False,
            'PC' : 0x0000,
            'steps' : 1,
            'RAM' : {
                0xFFFE : [ 0x00, 0x04 ],
                0x0000 : [  0xA9, 0x01,   # LDA #$01
                            0x00, 0xEA,   # BRK + skipped byte
                            0xEA, 0xEA,   # NOP, NOP
                            0xA9, 0x03 ],  # LDA #$03

                0x0400  : [ 0xA9, 0x02,   # LDA #$02
                            0x40 ]        # RTI
            }
        },
        'expect' : {
            'A' : 0x01,
            'PC'    : 0x0002
        }
    },
    'test_brk_interrupt - 2'  : {
        'input' : {
            'N'     : False,
            'V'     : False,
            '5'     : False,
            'B'     : False,
            'D'     : False,
            'I'     : False,
            'Z'     : False,
            'C'     : False,
            'PC' : 0x0000,
            'steps' : 2,
            'RAM' : {
                0xFFFE : [ 0x00, 0x04 ],
                0x0000 : [  0xA9, 0x01,   # LDA #$01
                            0x00, 0xEA,   # BRK + skipped byte
                            0xEA, 0xEA,   # NOP, NOP
                            0xA9, 0x03 ],  # LDA #$03

                0x0400  : [ 0xA9, 0x02,   # LDA #$02
                            0x40 ]        # RTI
            }
        },
        'expect' : {
            'PC'    : 0x0400
        }
    },
    'test_brk_interrupt - 3'  : {
        'input' : {
            'N'     : False,
            'V'     : False,
            '5'     : False,
            'B'     : False,
            'D'     : False,
            'I'     : False,
            'Z'     : False,
            'C'     : False,
            'PC' : 0x0000,
            'steps' : 3,
            'RAM' : {
                0xFFFE : [ 0x00, 0x04 ],
                0x0000 : [  0xA9, 0x01,   # LDA #$01
                            0x00, 0xEA,   # BRK + skipped byte
                            0xEA, 0xEA,   # NOP, NOP
                            0xA9, 0x03 ],  # LDA #$03

                0x0400  : [ 0xA9, 0x02,   # LDA #$02
                            0x40 ]        # RTI
            }
        },
        'expect' : {
            'PC'    : 0x0402,
            'A'     : 0x02
        }
    },
    'test_brk_interrupt - 4'  : {
        'input' : {
            'N'     : False,
            'V'     : False,
            '5'     : False,
            'B'     : False,
            'D'     : False,
            'I'     : False,
            'Z'     : False,
            'C'     : False,
            'PC' : 0x0000,
            'steps' : 4,
            'RAM' : {
                0xFFFE : [ 0x00, 0x04 ],
                0x0000 : [  0xA9, 0x01,   # LDA #$01
                            0x00, 0xEA,   # BRK + skipped byte
                            0xEA, 0xEA,   # NOP, NOP
                            0xA9, 0x03 ],  # LDA #$03

                0x0400  : [ 0xA9, 0x02,   # LDA #$02
                            0x40 ]        # RTI
            }
        },
        'expect' : {
            'PC'    : 0x0004
        }
    },
    'test_brk_interrupt - 5'  : {
        'input' : {
            'N'     : False,
            'V'     : False,
            '5'     : False,
            'B'     : False,
            'D'     : False,
            'I'     : False,
            'Z'     : False,
            'C'     : False,
            'PC' : 0x0000,
            'steps' : 7,
            'RAM' : {
                0xFFFE : [ 0x00, 0x04 ],
                0x0000 : [  0xA9, 0x01,   # LDA #$01
                            0x00, 0xEA,   # BRK + skipped byte
                            0xEA, 0xEA,   # NOP, NOP
                            0xA9, 0x03 ],  # LDA #$03

                0x0400  : [ 0xA9, 0x02,   # LDA #$02
                            0x40 ]        # RTI
            }
        },
        'expect' : {
            'PC'    : 0x0008,
            'A'     : 0x03
        }
    },
    'test_dec_a_decreases_a'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x48,
            'RAM' : {
                0x0000 : [ 0x3A ]
            }

        },
        'expect' : {
            'Z' : False,
            'N' : False,
            'A' : 0x47
        }
    },
    'test_dec_a_sets_zero_flag'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x01,
            'RAM' : {
                0x0000 : [ 0x3A ]
            }

        },
        'expect' : {
            'Z' : True,
            'N' : False,
            'A' : 0x00
        }
    },
    
    'test_dec_a_wraps_at_zero'  : {
        'input' : {
            'PC' : 0x0000,
            'A' : 0x00,
            'RAM' : {
                0x0000 : [ 0x3A ]
            }
        },
        'expect' : {
            'Z' : False,
            'N' : True,
            'A' : 0xFF
        }
    },

    'test_dec_zp_decrements_memory'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xC6, 0x10 ],
                0x0010 : [ 0x10 ]
            }
        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM' : {
                0x0010 : [ 0x0F ]
            },
            'N' : False,
            'Z' : False,
        }
    },
    'test_dec_zp_below_00_rolls_over_and_sets_negative_flag'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xC6, 0x10 ],
                0x0010 : [ 0x00 ]
            }

        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0xFF ]
            },
            'Z' : False,
            'N' : True,
        }
    },
    'test_dec_zp_sets_zero_flag_when_decrementing_to_zero'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xC6, 0x10 ],
                0x0010 : [ 0x01 ]
            }

        },
        'expect' : {
            'PC'    : 0x0002,
            'RAM'   : {
                0x0010 : [ 0x00 ]
            },
            'Z' : True,
            'N' : False
        }
    },


    'blank'  : {
        'input' : {
            'PC' : 0x0000,
            'RAM' : {
                0x0000 : [ 0xea ]
            }

        },
        'expect' : {

        }
    },

}

# ------ cycle through the tests


for T in tests:
    b = bus()
    chip = cpu65c02(b)
    #print('Testing ' + T)

    # -- load memory
    for r in tests[T]['input']['RAM']:

        for loc in range(r,r + len(tests[T]['input']['RAM'][r])):
            d = loc - r
            c = tests[T]['input']['RAM'][r][d]
            chip.bus.RAM[loc] = c

    # -- set the program counter
    chip.PC = tests[T]['input']['PC']

    # set the registers (if applicable)
    if 'A' in tests[T]['input']:
        chip.A = tests[T]['input']['A']
    if 'X' in tests[T]['input']:
        chip.X = tests[T]['input']['X']
    if 'Y' in tests[T]['input']:
        chip.Y = tests[T]['input']['Y']
    if 'SP' in tests[T]['input']:
        chip.SP = tests[T]['input']['SP']

    # -- set P flags (if applicable)
    for P in ['N','V','B','D','I','Z','C']:
        if P in tests[T]['input']:
            chip.P[P] = tests[T]['input'][P]

    # -- how many steps
    if 'steps' in tests[T]['input']:
        steps = tests[T]['input']['steps']
    else:
        steps = 1

    # -- what is the function
    if 'function' in tests[T]['input']:
        function = tests[T]['input']['function']
    else:
        function = 'step'

    #chip.cpudump()
    if function == 'step':
        for k in range(0,steps):
            #print(' - step - ')
            chip.CLOCK()
            #print(chip.asm)
            #chip.cpudump()

    elif function == 'irq':
        chip.IRQ()
    else:
        print('unknown function ' + function)
        exit(1)

    

    # -- check the outputs
    for P in ['N','V','B','D','I','Z','C']:
        if P in tests[T]['expect']:
            test(T + ' - ' + P, tests[T]['expect'][P], chip.P[P])

    if 'PC' in tests[T]['expect']:
        test(T + ' - PC', '0x%04X' % tests[T]['expect']['PC'], '0x%04X' % chip.PC)

    if 'SP' in tests[T]['expect']:
        test(T + ' - SP', '0x%02X' % tests[T]['expect']['SP'], '0x%02X' % chip.SP)

    if 'A' in tests[T]['expect']:
        test(T + ' - A', '0x%02X' % tests[T]['expect']['A'], '0x%02X' % chip.A)

    if 'X' in tests[T]['expect']:
        test(T + ' - X', '0x%02X' % tests[T]['expect']['X'], '0x%02X' % chip.X)

    if 'Y' in tests[T]['expect']:
        test(T + ' - Y', '0x%02X' % tests[T]['expect']['Y'], '0x%02X' % chip.Y)

    # TODO - check the CPU cycles
    #if 'cycles' in tests[T]['expect']:
        #test(T + ' - cycles', '0x%02X' % tests[T]['expect']['cycles'], '0x%02X' % chip.CYCLES)

    # check the ram dump
    if 'RAM' in tests[T]['expect']:
        for r in tests[T]['expect']['RAM']:
            actual = ''
            expected = ''

            for loc in range(r,r + len(tests[T]['expect']['RAM'][r])):
                d = loc - r
                
                expected += '0x%02X ' % tests[T]['expect']['RAM'][r][d]
                actual += '0x%02X ' % chip.bus.RAM[loc]

            test(T + ' - 0x%04X' % loc, expected, actual)
            
            


    


    #hexdump(chip.bus.RAM,0x0100)
    #print('==========================================')
exit(0)    
