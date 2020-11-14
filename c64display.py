
import pygame
class c64display:
    
    def __init__(self,memoryStart):
        pygame.init()

        self.memoryStart = memoryStart
        # -- give me the actual size of the displayable text
        self.width = 500

        # -- screen parameters
        self.margin = int(self.width * 0.13125)
        self.height = int(self.width * 0.625)
        self.fz = int(self.width / 40)
        # == there appear to be two screen colours... Choose the set you like best
        self.foreground = (153, 204, 255) #(124, 113, 218)
        self.background = (51, 51, 204) # (62, 50, 162)

        # -- setup the screen
        self.display_surface = pygame.display.set_mode((self.width + self.margin * 2 , self.height + self.margin * 2 )) 
        pygame.display.set_caption('Commodore 64 Display') 
        #self.font = pygame.font.Font('freesansbold.ttf', self.fz) 
        self.font = pygame.font.Font('C64_Pro_Mono-STYLE.ttf', self.fz)
        
        self.display_surface.fill(self.foreground)

        pygame.draw.rect(self.display_surface, self.background, (self.margin,self.margin,self.width,self.height), 0)


    def printChar(self,loc,chd):

        if chd != 0:
            ch = chr(chd)

            t = self.font.render(ch, True, self.foreground, self.background) 
            textRect = t.get_rect()
            chc = loc - self.memoryStart
            cx = int(chc % 40) + 1
            cy = int(chc / 40)
            textRect.center = (self.margin + (cx * self.fz) - int(self.fz / 2) + 8,self.margin + (cy * self.fz ) + int(self.fz / 2) + 8) 

            
            self.display_surface.blit(t, textRect)
            pygame.display.update()

    def loop(self):

        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                pygame.quit() 
                quit() 


            #pygame.display.update()

if __name__ == "__main__":
    dsp = c64display(0x0400)

    data = [
        ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ','*','*','*','*',' ','C','O','M','M','O','D','O','R','E',' ','6','4',' ','B','A','S','I','C',' ','V','2',' ','*','*','*','*',' ',' ',' ',' ',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
        ' ','6','4','K',' ','R','A','M',' ','S','Y','S','T','E','M',' ',' ','3','8','9','1','1',' ','B','A','S','I','C',' ','B','Y','T','E','S',' ','F','R','E','E',' ',
        ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',
        'R','E','A','D','Y','.',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '
    ]

    c = 0
    for d in data:
        dsp.printChar(0x400 + c,ord(data[c]))
        c += 1

    while True:
        dsp.loop()
