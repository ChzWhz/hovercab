###HOVERCAB V.02 COPYRIGHT 2017 BY ZACHARY HAYES & BRIAN HEALY

###HOVERCAB - LIFE ISN'T FARE

#If you can't find the solution, you don't understand the problem;

import pygame
import time
import random
import pickle

with open('highscore.dat', 'rb') as file:
    oldscore = float(pickle.load(file))

    
print("HOVER CAB ~ LIFE ISN'T FARE\nV.02 COPYRIGHT 2017\n~a game by Zachary Hayes, art by Brian Healy~\nHigh score: ${}".format(oldscore))

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

carImg = pygame.image.load('cab.png') #Loads car image
hoverImg = pygame.image.load('cabhover.png')
car_width, car_height = carImg.get_rect().size #Used to reference width or height of car image
    
###FUNCTIONS
def highscore(newscore):
    """Load the previous score if it exists"""
    newscore = float("%.2f" % newscore)
    try:
        with open('highscore.dat', 'rb') as file:
            score = float(pickle.load(file))
    except:
        score = 0
    
    if newscore > score:
        with open('highscore.dat', 'wb+') as file:
            pickle.dump(str(newscore), file)
            print("NEW HIGH SCORE!")
    
def fare(score):
    """Produces Fare display"""
    font = pygame.font.Font('PressStart2P-Regular.ttf', 15)
    text = font.render("Fare: $" + "%.2f" % score, True, black)
    gameDisplay.blit(text, (0,0))
    
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
    
def message_display(text):
    """Displays message"""
    font = pygame.font.Font('ARCADECLASSIC.ttf',115)
    TextSurf, TextRect = text_objects(text,font)
    TextRect.center = ((display_width/2),(display_height/2)) #Puts message in center of window
    gameDisplay.blit(TextSurf, TextRect) #Displays message in window
    pygame.display.update() #Update display
    time.sleep(3) #Delays image on screen
    game_loop() #Restart game
    
def fuelgauge(fuel):
    """Produces fuel display"""
    color = red
    if fuel < 0:
        fuel = 0
    if fuel > 20:
        color = yellow
    if fuel > 40:
        color = green
    pygame.draw.rect(gameDisplay, color, [675, 5, fuel, 20])
    font = pygame.font.Font('PressStart2P-Regular.ttf', 10)
    text = font.render("Fuel: {}g".format(fuel), True, black)
    gameDisplay.blit(text, (675,10))

def crash():
    """Runs crash response"""
    message_display('You Crashed')
    
###CLASSES
class Obstacle:
    def __init__(self, desc, img, points, starty, hoverable, minr, maxr,destruct):
        self.name = self
        self.imgfile = img
        self.maxr = maxr
        self.minr = minr
        self.desc = desc
        self.img = pygame.image.load(self.imgfile)
        self.width, self.height = self.img.get_rect().size
        self.starty = starty
        self.startx = random.randrange(0, (display_width - self.width))
        self.points = points
        self.hoverable = hoverable
        self.rrange = random.randrange(minr, maxr)
        self.destruct = pygame.image.load(destruct)
        
    def resetimg(self):
        self.img = pygame.image.load(self.imgfile)
        
    def changewh(self,neww,newh):
        self.width, self.height = neww,newh
        
    def obstacle(self):
        """Display obstacle"""
        gameDisplay.blit(self.img,(self.startx,self.starty))
         
    def checkobst(self,other):
        """Corrects for obstacle overlays"""
        if self.starty < other.starty + other.height and self.starty + self.height > other.starty:
            if other.startx < self.startx + self.width and other.startx + other.width > self.startx:
                self.starty -= 250
                
    def changerrange(self,carspeed):
        if carspeed > 14:
            self.minr *= (float(carspeed)*.1)
            self.maxr *= (float(carspeed)*.1)
    
    def impact(self,x,y,points,hover,other):
        """Impact logic for obstacles"""
        if self.starty > display_height: #Resets obstacle
            self.starty = 0 - self.height - self.rrange
            self.startx = random.randrange(0, (display_width - self.width))
            if self.desc == 'damage':
                points += self.points
            self.resetimg()
        for obj in other:
            if obj != self:
                self.checkobst(obj)
            else:
                pass
            
        if y < self.starty + self.height and y + car_height > self.starty: #y crossover
            if self.startx < x + car_width and self.startx + self.width > x: #x crossover
                if self.hoverable == True and hover == True:
                    if self.desc == 'damage':
                        points += .25
                else:
                    if self.desc == 'powerup':
                        if self.img != self.destruct or self.points == 100: #OR added for fuel
                            points = self.points
                        else:
                            points = 0
                    else:
                        print("Your score: $%.2f" % points)
                        highscore(points)                    
                        crash()
                    self.img = self.destruct
                    
        return points    
                
###MAIN FUNCTION
def game_loop():
    """Runs game"""
      
    x = (display_width * 0.45) #Car starting point
    y = (display_height * 0.8)
    
    score = 0.00
    speed = -4
    phase = 0
    gameExit = False
    hover = False
    fuel = 100
    carspeed = 5
    x_change = 0
    accelerate = 10
    newgame = True
    gear = 1
    boost = 0
    
    ###OBJECTS
    boulder = Obstacle('damage', 'boulder.png', .10, -600, False, 0, 500, 'boulder.png')
    boulder2 = Obstacle('damage', 'boulder.png', .10, -2000, False, 400, 1200, 'boulder.png')
    barrier = Obstacle('damage', 'barrier.png', .20, -6000, True, 0, 750, 'barrier.png')
    gas = Obstacle('powerup','gascan.png', 100, -5000, True, 2000, 20000, 'gasdest.png')
    missilepu = Obstacle('powerup', 'Missilepowerup.gif', 0, -200, True, 2000, 20000, 'Missilepowerup.gif')
    speedboost = Obstacle('powerup', 'speedboost.gif', 2, -7000, True, 6000, 60000, 'gasdest.png')
    
    boulder.changewh(boulder.width - 5, boulder.height - 15)
    boulder2.changewh(boulder.width - 5, boulder.height - 15)
    barrier.changewh(barrier.width,17) #Lets car crash closer to barrier

    ###PLAY LOOP
    while not gameExit:
        for event in pygame.event.get(): #Loops events
            if event.type == pygame.QUIT: #Quits game if x pressed
                pygame.quit()
                #quit()
            
            if event.type == pygame.KEYDOWN: #Keyboard controls
                if event.key == pygame.K_LEFT:
                    x_change += -(carspeed)
                elif event.key == pygame.K_RIGHT:
                    x_change += carspeed + boost
                elif event.key == pygame.K_SPACE:
                    hover = True
                elif event.key == pygame.K_a:
                    accelerate = True

            if event.type == pygame.KEYUP: #Resets x_change after key release
                if newgame == True:
                    continue
                elif event.key == pygame.K_LEFT:
                    x_change += carspeed
                elif event.key == pygame.K_RIGHT:
                    x_change += -(carspeed)
                elif event.key == pygame.K_SPACE:
                    hover = False
                elif event.key == pygame.K_a:
                    accelerate = False
                    
            newgame = False

        if hover == True: #Checks for fuel
            fuel -= 1
            if fuel <= 0:
                hover = False
       
        if accelerate == True and fuel > 0: #Checks if accelerate is activated and changes gears accordingly.
            gear = 2
            fuel -= 1
        elif accelerate == False:
            gear = 1        
            
        if x > display_width - car_width or x < 0: #Creates boundaries on window edge
            crash()
        
        other = (boulder, boulder2, barrier, gas, speedboost)
        score = boulder.impact(x,y,score,hover,other)
        score = boulder2.impact(x,y,score,hover,other)
        score = barrier.impact(x,y,score,hover,other)
        score += .001
        
        missiles = 0
        
        if speedboost.impact(x,y,0,hover,other) == speedboost.points: #Adds speedboost to carspeed and changes x_change to compensate.
            carspeed += speedboost.points
            speedboost.changerrange(carspeed)
            print("Speed Boost!")
            if x_change > 0:
                x_change += speedboost.points
            elif x_change < 0:
                x_change -= speedboost.points
            
        fuel = gas.impact(x,y,fuel,hover,other)

        x += x_change * gear
        gameDisplay.fill(white) #Fills background
        
        gas.obstacle()
        speedboost.obstacle()
        barrier.obstacle()
        car(hover,x,y)
        boulder.obstacle()
        boulder2.obstacle()
        boulder.starty += speed
        boulder2.starty += speed
        barrier.starty += speed
        gas.starty += speed
        #gas.impact += speed
        speedboost.starty += speed
        fuelgauge(fuel)
        fare(score)
        if score >= phase * 1.50: #Changes the speed based on fare
            phase = score
            speed += 1
            if phase > 15:
                fuel += 30
                print("Fuel +30g!")
                if fuel > 100:
                    fuel = 100

        pygame.display.update() #pygame.display.flip()
        clock.tick(30) #fps

game_loop() #Runs game function
pygame.quit() #Ends game
#quit()