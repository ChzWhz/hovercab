###HOVERCAB V.02 COPYRIGHT 2017 BY ZACHARY HAYES & BRIAN HEALY

###HOVERCAB - LIFE ISN'T FARE

import pygame
import time
import random
import pickle

pygame.init() #initiates pygame module

version = .02

display_width = 800 #Used for references to window width and height
display_height = 600

black = (0,0,0) #Defines color variables
white = (255,255,255)
red = (255,0,0)
yellow = (255,255,0)
green = (0,255,0)

gameDisplay = pygame.display.set_mode((display_width,display_height)) #Defines window
pygame.display.set_caption('Hover Cab') #Window caption, game name
clock = pygame.time.Clock() #Defines variable using pygame clock

carImg = pygame.image.load('cab.png') #loads car image
hoverImg = pygame.image.load('cabhover.png')
car_width, car_height = carImg.get_rect().size #Used to reference width or height of car image
    
###FUNCTIONS
#def things_dodged(count):
    #font = pygame.font.SysFont(None, 25)
    #text = font.render("Fare: $" + str(count), True, black)
    #gameDisplay.blit(text, (0,0))
def highscore(newscore):
    # load the previous score if it exists
    try:
        with open('highscore.dat', 'rb') as file:
            score = pickle.load(file)
    except:
        score = 0
    
    if newscore > score:
        print("NEW HIGH SCORE!")
        with open('score.dat', 'wb') as file:
            pickle.dump(score, file)        
        
    
def fare(score):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Fare: $" + "%.2f" % score, True, black)
    gameDisplay.blit(text, (0,0))

#def impact(obst,name,x,y,score,x_change,hover):
    #"""Impact logic for obstacles"""
    #if obst.starty > display_height: #Resets obstacle
        #obst.starty = 0 - obst.height
        #obst.startx = random.randrange(0, (display_width - obst.width))
        #score += obst.points
        ##speed += 1
        
    #if y < obst.starty + obst.height and y + car_height > obst.starty: #y crossover
        #if obst.startx < x + car_width and obst.startx + obst.width > x: #x crossover
            #if obst.hoverable == True and hover == True:
                #score += .25
            #else:
                #crash(x_change)
            
    #return score

#def obstacle(img,x,y):
    #"""Display obstacle"""
    #gameDisplay.blit(img,(x,y))
    
#def things(thingx, thingy, thingw, thingh, color):
    #"""Box obstacle"""
    #pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])
    

def car(hover,x,y):
    """Displays car"""
    if hover == False:
        gameDisplay.blit(carImg,(x,y))
    elif hover == True:
        y -= 15
        gameDisplay.blit(hoverImg,(x,y))
    
def text_objects(text,font):
    """Creates text"""
    textSurface = font.render(text,True,black) #True parameter is anti-aliasing
    return textSurface, textSurface.get_rect() #Rect is used to position text
    
def message_display(text,x_change):
    """Displays message"""
    font = pygame.font.Font('FreeSansBold.ttf',115)
    TextSurf, TextRect = text_objects(text,font)
    TextRect.center = ((display_width/2),(display_height/2)) #Puts message in center of window
    gameDisplay.blit(TextSurf, TextRect) #Displays message in window
    pygame.display.update() #Update display
    time.sleep(3) #Delays image on screen
    game_loop(x_change) #Restart game
    
def fuelgauge(fuel):
    color = red
    if fuel < 0:
        fuel = 0
    if fuel > 20:
        color = yellow
    if fuel > 40:
        color = green
    pygame.draw.rect(gameDisplay, color, [675, 5, fuel, 20])
    font = pygame.font.SysFont(None, 25)
    text = font.render("Fuel: {}g".format(fuel), True, black)
    gameDisplay.blit(text, (675,25))    

def crash(x_change):
    """Runs crash response"""
    message_display('You Crashed',x_change)
    
###CLASSES
class Obstacle:
    def __init__(self, img, speed, points, starty, hoverable):
        self.name = self
        self.img = pygame.image.load(img)
        self.width, self.height = self.img.get_rect().size
        self.starty = starty
        self.startx = random.randrange(0, (display_width - self.width))
        self.points = points
        self.hoverable = hoverable
        
    def changewh(self,neww,newh):
        self.width, self.height = neww,newh
        
    def obstacle(self):
        """Display obstacle"""
        gameDisplay.blit(self.img,(self.startx,self.starty))
         
    def checkobst(self,other):
        if self.starty < other.starty + other.height and self.starty + self.height > other.starty:
            if other.startx < self.startx + self.width and other.startx + other.width > self.startx:
                self.starty -= 250   
    
    def impact(self,x,y,score,x_change,hover, other):
        """Impact logic for obstacles"""
        
        if self.starty > display_height: #Resets obstacle
            self.starty = 0 - self.height - random.randrange(0, 500)
            self.startx = random.randrange(0, (display_width - self.width))
            score += self.points
        for obj in other:
            if obj != self:
                self.checkobst(obj)
            else:
                pass
            
        if y < self.starty + self.height and y + car_height > self.starty: #y crossover
            if self.startx < x + car_width and self.startx + self.width > x: #x crossover
                if self.hoverable == True and hover == True:
                    score += .25
                else:
                    print("Your score: $%.2f" % score)
                    highscore(score)                    
                    crash(x_change)
                    
        return score    
                
###MAIN FUNCTION
def game_loop(x_change):
    """Runs game"""
      
    x = (display_width * 0.45) #Car starting point
    y = (display_height * 0.8)
    
    #thing_startx = random.randrange(0, display_width)
    #thing_starty = -600
    #thing_speed = 5
    #thing_width = 100
    #thing_height = 100
    
    #dodged = 0
    score = 0.00
    speed = -4
    phase = 0
    gameExit = False
    hover = False
    fuel = 100
    
    ###OBJECTS
    boulder = Obstacle('boulder.png', 7, .10, -600, False)
    barrier = Obstacle('barrier.png', 7, .20, -1000, True)
    
    barrier.changewh(barrier.width,17) #Lets car crash closer to barrier

    ###GAME LOOP
    while not gameExit:
        for event in pygame.event.get(): #Pulls event
            if event.type == pygame.QUIT: #Quits game if x pressed
                pygame.quit()
                #quit()
                
            if event.type == pygame.KEYDOWN: #Keyboard controls
                if event.key == pygame.K_LEFT:
                    x_change += -5
                elif event.key == pygame.K_RIGHT:
                    x_change += 5
                elif event.key == pygame.K_SPACE:
                    hover = True
                    
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT or event.key== pygame.K_RIGHT:
                    #x_change = 0
            if event.type == pygame.KEYUP: #Resets x_change after key release
                if event.key == pygame.K_LEFT:
                    x_change += 5
                if event.key == pygame.K_RIGHT:
                    x_change += -5
                elif event.key == pygame.K_SPACE:
                    hover = False
                    
        if hover == True: #Checks for fuel
            fuel -= 1
            if fuel <= 0:
                hover = False

        if x > display_width - car_width or x < 0: #Creates boundaries on window edge
            crash(x_change)

        #if boulder.starty > display_height: #Resets boulder
            #boulder.starty = 0 - boulder.img.get_rect().height
            #boulder.startx = random.randrange(0, (display_width - boulder.width))
            #score += boulder.points
            #boulder.speed += 1
            
        #if y < boulder.starty + boulder.height: #y crossover
            #if boulder.startx < x + car_width and boulder.startx + boulder.width > x: #x crossover
                #crash(x_change)
        
        other = [boulder, barrier]
        score = boulder.impact(x,y,score,x_change,hover, other)
        score = barrier.impact(x,y,score,x_change,hover, other)
        score += .01
            
        #if thing_starty > display_height: #Resets obstacle
            #thing_starty = 0 - thing_height
            #thing_startx = random.randrange(0, (display_width - thing_width))
            #dodged += 1 #Adds to score
            #thing_speed += 1 #Adds difficulty

        #if y < thing_starty + thing_height: #y crossover
            ##if x > thing_startx and x < thing_startx + thing_width or x + car_width > thing_startx and x + car_width < thing_startx + thing_width:
            #if thing_startx < x + car_width and thing_startx + thing_width > x:#x crossover
                #crash(x_change)

        x += x_change
        gameDisplay.fill(white) #Fills background

        #things(thingx, thingy, thingw, thingh, color)
        #things(thing_startx, thing_starty, thing_width, thing_height, black)
        barrier.obstacle()
        car(hover,x,y)
        boulder.obstacle()
        boulder.starty += speed
        barrier.starty += speed
        boulder.checkobst(barrier)
        #thing_starty += thing_speed
        fuelgauge(fuel)
        fare(score)
        if score >= phase * 1.50: #Changes the speed based on fare
            phase = score
            speed += 1
        #things_dodged(dodged)

        pygame.display.update() #pygame.display.flip()
        clock.tick(30) #fps

game_loop(0) #Runs game function
pygame.quit() #Ends game
#quit()