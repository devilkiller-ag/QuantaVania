import pygame,sys

from settings import *
from support import import_images_from_folder
from qubo_challenge import *
pygame.init()

class Buttons:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale), int(height*scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                #print("clicked")
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

class BarH:
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
        pygame.draw.rect(surface, (0,255,0),(self.x,self.y,self.w*ratio,self.h))


class MiniGame:
    def __init__(self, surface, file_name):
        self.file_name= file_name
        self.pf_max = 1
        self.pf_min = 0
        self.r_max = PARAMETER_RANGE[file_name][0]
        self.r_min = PARAMETER_RANGE[file_name][1]
        self.QuboInstance = SolveQubo(f"challenges/{file_name}")
        self.pf_current = self.energy = self.QuboInstance.run(self.r_max)
        self.minigame_surface = surface
        self.font = pygame.font.Font("graphics/ui/ARCADEPI.TTF" , 20)
        self.pf_bar = Bar(906,60,45,385,self.pf_min, self.pf_max)
        self.r_bar = BarH(150,500,980,45,self.r_min,self.r_max)
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
        
    def draw_graphs(self, surface):
        graph1 = pygame.image.load("problem.png").convert_alpha()
        graph1 = pygame.transform.scale(graph1,(350,400))
        try:
            graph2 = pygame.image.load("solution.png").convert_alpha()
            graph2 = pygame.transform.scale(graph2,(350,400))
        except FileNotFoundError:
            #print("No Solution available")
            pass
        try:
            graph2 = pygame.transform.scale(graph2,(350,400))
        except UnboundLocalError:
            pass
        surface.blit(graph1, (80,60))
        try:
            surface.blit(graph2,(485,60))
        except UnboundLocalError:
            pass

    def draw_buttons(self,surface):
        
        self.increment_button.draw(surface)
        self.decrement_button.draw(surface)
        self.calculate_button.draw(surface)
        self.calculate_button_qa.draw(surface)
        self.back_button.draw(surface)

    def draw_bars(self, surface):
        # self.pf_bar.current
        self.pf_bar.draw(surface)
        # self.r_bar.current
        self.r_bar.draw(surface)

    def draw_bg(self):
        bg= pygame.image.load("graphics/ui/minigame bg.png").convert_alpha()
        self.minigame_surface.blit(bg, (0,0))

    def draw_text(self, energy_txt, pf_text, r_text):
        energy_surface = self.font.render(f"Energy: {energy_txt}",False, STATS_TEXT_COLOR)
        pf_surface = self.font.render(f"Pf: {pf_text}",False, STATS_TEXT_COLOR)
        r_surface = self.font.render(f"R: {r_text}",False, STATS_TEXT_COLOR)
        self.minigame_surface.blit(energy_surface, (970,64))
        self.minigame_surface.blit(pf_surface, (970,114))
        self.minigame_surface.blit(r_surface, (970,164))

    def event_loop(self):
        for event in pygame.event.get():
            # Detect if user wants to quit the game
            if event.type == pygame.QUIT :
                pygame.quit()
                sys.exit()

    def input(self):
        #print(self.increment_button.draw(self.minigame_surface))
        if self.increment_button.draw(self.minigame_surface):
            print("increase")
            self.r_bar.current += (self.r_max-self.r_min)/100
        if self.decrement_button.draw(self.minigame_surface):
            print("decrease") 
            self.r_bar.current-= (self.r_max-self.r_min)/100
        if self.calculate_button.draw(self.minigame_surface):
            print("calculate")
            self.pf_bar.current, energy_txt = self.QuboInstance.run(self.r_bar.current)
            self.draw_text(energy_txt,self.pf_bar.current, self.r_bar.current)
            self.draw_graphs(self.minigame_surface)
        if self.back_button.draw(self.minigame_surface):
            print("go back to main menu")
        self.draw_bars(self.minigame_surface)
            #self.create_mainmenu()
    def run(self):
        self.event_loop
        self.draw_bg()
        self.input()
        self.draw_buttons(self.minigame_surface)
        
        self.draw_bars(self.minigame_surface)
        self.draw_graphs(self.minigame_surface)
        self.draw_text(self.energy, self.pf_bar.current, self.r_bar.current)
        

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("TSP QUBO Solver")
game_test = MiniGame(screen, "rat195.tsp")
running = True
while running:
   
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
    
    game_test.run()
    pygame.display.update()