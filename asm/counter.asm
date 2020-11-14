RAM = 0x0000

;VIDEO = 0x0400

	.org $8000

reset:
	lda #$00
	sta RAM
	
	lda #$00
	sta RAM+1
	
	lda #$00
	sta RAM+2
	
	lda #$00
	sta RAM+3
	
	lda #$00
	sta RAM+4

V1:
  inc RAM
  BNE V1
  
V1_RESET:
  lda #$00
  sta RAM
  
V2:
  inc RAM+1
  BNE V1

V2_RESET:
  lda #$00
  sta RAM+1
  
V3:
  inc RAM+2
  BNE V2

V3_RESET:
  lda #$00
  sta RAM+2

V4:
  inc RAM+3
  BNE V3

V4_RESET:
  lda #$00
  sta RAM+3
 
EXIT:
	.byte $DB	; STP -- not supported by vasm

	.org $fffc
	.word reset
	.word $0000