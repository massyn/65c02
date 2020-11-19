
; -- our pong needs a couple of variables.
BALLlocationL = $00	; The memory location we will write to to display the ball
BALLlocationH = $01

ballX = $02
ballY = $03

directionX = $04
directionY = $05

	.org $fffc  ; reset vector
	.word reset
	.word $0000
	
	.org $8000  ; The ROM image starts at $8000







; -- we start with reset -- set things up, ready for us to go

reset:

	LDA #$11
	STA ballX
	STA ballY
	STA BALLlocationL
	STA BALLlocationH
	
	; set the starting direction

	LDA #$00
	STA directionX
	STA directionY

	JSR drawBall

	

	



loop:
	JSR eraseBall
	JSR moveBall
	JSR drawBall
	

	JSR spinWheels

    JMP loop

moveBall:
	;LDX #$00
	;LDY #$00

	; left or right
	LDA #$00
	CMP directionX
	BCS decX
	INC ballX
	
	RTS	; this may not work
decX:
	DEC ballX



	;INC ballY
	RTS

; draw a ball at the X / Y coordinates
drawBall:

; the ball reset will reset to $0400 - the starting memory location of the display - we set it however to $03D7 (one row higher) due to the looping mechanism
ballreset:
	LDA #$D7
	STA BALLlocationL
	LDA #$03
	STA BALLlocationH

	; multiply ballY by $28 and store it in BallLocation L & H
	LDY ballY
loopY:
	CLC
	LDA BALLlocationL
	ADC #$28
	STA BALLlocationL
	BCC okY
	INC BALLlocationH
okY:
	DEY
	BNE loopY

	; now add X to BallLocation
	CLC
	LDA BALLlocationL
	ADC ballX
	STA BALLlocationL
	BCC okX
	INC BALLlocationH
okX:

	LDA #"o"
	LDY #0
	STA (BALLlocationL),y

	RTS

eraseBall:
	LDA #" "
	LDY #0
	STA (BALLlocationL),y
	RTS

spinWheels:
  ldx #$10
spinloop:
  nop
  ;nop
  dex
  bne spinloop
  rts



EXIT:
	.byte $DB	; STP -- not supported by vasm