;set the video address
VIDEO = 0x0400

	.org $8000

reset:

print:
	lda message,x
	beq loop
	jsr print_char
	inx
	jmp print

loop:
	jmp loop

message: .asciiz "Hello, world!"

print_char:
	sta VIDEO,x
	rts
  
	.org $fffc
	.word reset
	.word $0000