import pygame,sys

from settings import *
from qubo_challenge import *

class Buttons:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.toprect = (x,y)
        self.clicked = False

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

    
class Bar:
    def __init__(self, x, y, w, h, range_min, range_max):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.range_min = range_min
        self.range_max = range_max
        self.current = range_max

    def draw(self, surface):
        ratio = (self.current - self.range_min)/(self.range_max-self.range_min)
        pygame.draw.rect(surface, (255,0,0),(self.x,self.y,self.w,self.h))
        pygame.draw.rect(surface, (0,255,0),(self.x,self.y,self.w,self.h*ratio))


class MiniGame:
    def __init__(self, surface, file_name):
        self.file_name= file_name
        self.pf_max = 1
        self.pf_min = 0
        self.r_max = PARAMETER_RANGE[file_name][0]
        self.r_min = PARAMETER_RANGE[file_name][1]
        self.QuboInstance = SolveQubo(file_name)
        self.minigame_surface = surface
        self.font = pygame.font.Font("graphics/ui/ARCADEPI.TTF" , 20)
        
    def draw_graphs(self, surface):
        graph1 = pygame.image.load("problem.png").convert_alpha()
        graph1 = pygame.transform.scale(graph1,(350,400))
        graph2 = pygame.image.load("solution.png").convert_alpha()
        graph2 = pygame.transform.scale(graph2,(350,400))
        surface.blit(self.graph1, (80,60))
        surface.blit(self.graph2,(485,60))

    def draw_buttons(self,surface):
        increment = pygame.image.load("graphics/ui/increment.png")
        decrement = pygame.image.load("graphics/ui/decrement.png")
        calculate = pygame.image.load("graphics/ui/calculate.png")
        calculate_qa = pygame.image.load("graphics/ui/Calculate(QA).png")
        back = pygame.image.load("graphics/ui/back.png")
        self.increment_button = Buttons(1141,500,increment,1)
        self.decrement_button = Buttons(75,500,decrement,1)
        self.calculate_button = Buttons(817,622,calculate,1)
        self.calculate_button_qa = Buttons(400,622,calculate_qa,1)
        self.back_button = Buttons(100,600,back,1)
        self.increment_button.draw(surface)
        self.decrement_button.draw(surface)
        self.calculate_button.draw(surface)
        self.calculate_button_qa.draw(surface)
        self.back_button.draw(surface)

    def draw_bars(self):
        pf_bar = Bar(906,60,45,385,self.pf_min, self.pf_max)
        r_bar = Bar(150,550,1066,45, self.r_min, self.r_max)

    def draw_bg(self):
        bg= pygame.image.load("graphics/ui/minigame bg.png").convert_alpha()
        self.minigame_surface.blit(bg, (0,0))

    def draw_text(self, energy_txt, pf_text, r_text):
        energy_surface = pygame.font.render(f"Objective energy: {energy_txt}",False, DIALOG_TEXT_COLOR)
        pf_surface = pygame.font.render(f"Probability of Feasibility: {pf_txt}",False, DIALOG_TEXT_COLOR)
        r_surface = pygame.font.render(f"Relaxation Parameter : {r_txt}",False, DIALOG_TEXT_COLOR)
        self.minigame_surface.blit(energy_surface, (970,64))
        self.minigame_surface.blit(pf_surface, (970,114))
        self.minigame_surface.blit(r_surface, (970,164))

    def event_loop(self):
        for event in pygame.event.get():
            # Detect if user wants to quit the game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def input(self):
        if self.increment_button.draw(self.minigame_surface):
            print("increase")
            self.r_bar.current += (self.r_max-self.r_min)/100
        if self.decrement_button.draw(self.minigame_surface):
            print("decrease") 
            self.r_bar.current -= (self.r_max-self.r_min)/100
        if self.calculate_button.draw(self.minigame_surface):
            print("calculate")
            self.pf_bar.current, energy_txt = self.QuboInstance.run()
            self.draw_text(energy_txt, self.pf_bar.current, self.r_bar.current)
        if self.back_button.draw(self.minigame_surface):
            print("go back to main menu")
            #self.create_mainmenu()
    def run(self):
        self.event_loop
        self.draw_bg
        self.draw_buttons()
        self.input()
        self.draw_bars()
        self.draw_graphs()
        self.draw_text()