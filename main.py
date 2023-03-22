import turtle
import math
import random
import pygame

pygame.mixer.init()
pygame.mixer.music.load("./Music/SoundTest.wav")
pygame.mixer.music.play(-1)

#sound (short)
#pygame.mixer.init()
#game_over = pygame.mixer.Sound("./Music/gameover.wav")



#game_state = "OnGame"
wn=turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Game by Rayan Al Zahabi")
wn.setup(700,700)
wn.tracer(0)

#Register shapes
images=["wizard_right.gif","wizard_left.gif",
       "treasure.gif","wall.gif",
       "enemy_left.gif","enemy_right.gif"]
for image in images:
    turtle.register_shape(image)

#Create a Pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("red")
        self.penup() # Picks the pen up so the turtle does not draw a line as it moves.
        self.speed(0)# The speed of the animation not of the motion it's something we need for the game, zero means the fatest 
    
    def end_game(self):
        wn.clear()
        #self.setposition(0, 0)
        #self.write("Game Over", True, align="left", font=("Arial", 14, "bold"))
        wn.bgpic("game_over.gif")
        pygame.mixer.music.load("./Music/gameover.wav")
        pygame.mixer.music.play(-1)
        wn.exitonclick()

    def you_win(self):
        wn.clear()
        #self.setposition(0, 0)
        #self.write("Game Over", True, align="left", font=("Arial", 14, "bold"))
        wn.bgpic("win2.gif")
        pygame.mixer.music.load("./Music/gameover.wav")
        pygame.mixer.music.play(-1)
        wn.exitonclick()
        
#Create a player

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wizard_right.gif")
        self.color("blue")
        self.penup() # Picks the pen up so the turtle does not draw a line as it moves.
        self.speed(0)
        self.gold=0

    def go_up(self):
        #Calculate the spot to move to
        move_to_x=self.xcor()
        move_to_y=self.ycor()+24
        
        #Check if the space has a wall
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def go_down(self):
        #Calculate the spot to move to
        move_to_x=self.xcor()
        move_to_y=self.ycor()-24
        #Check if the space has a wall
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y) 

    def go_left(self):
        #Calculate the spot to move to
        move_to_x=self.xcor()-24
        move_to_y=self.ycor()
        self.shape("wizard_left.gif")

        #Check if the space has a wall
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y) 
    
    def go_right(self):
        #Calculate the spot to move to
        move_to_x=self.xcor()+24
        move_to_y=self.ycor()
        self.shape("wizard_right.gif")

        #Check if the space has a wall
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        
    def is_collision(self,other):
            a=self.xcor()-other.xcor()
            b=self.ycor()-other.ycor()
            distance=math.sqrt((a**2)+(b**2))

            if distance<5:
                return True
            else:
                return False 


class Treasure(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold=100
        self.goto(x,y)
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("enemy_left.gif")
        #self.color("red")
        self.penup()
        self.speed(0)
        self.gold=25
        self.goto(x,y)
        self.direction=random.choice(["up","down","left","right"])
    
    def move(self):
        if self.direction=="up":
            dx=0
            dy=24
        elif self.direction=="down":
            dx=0
            dy=-24
        elif self.direction=="left":
            dx=-24
            dy=0
            self.shape("enemy_left.gif")
        elif self.direction=="right":
            dx=24
            dy=0
            self.shape("enemy_right.gif")
        else:
            dx=0
            dy=0
        
        #Check if player is close
        #if so, go in that direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction="left"
            elif player.xcor()>self.xcor():
                self.direction="right"
            elif player.ycor()<self.ycor():
                self.direction="down"
            elif player.ycor()>self.ycor():
                self.direction="up"

        #Calculate the spot to move to
        move_to_x=self.xcor()+dx
        move_to_y=self.ycor()+dy
        
        #Check if the space has a wall
        if(move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        else:
            #choose another direction
            self.direction=random.choice(["up","down","left","right"])
        #set the time to move next time
        turtle.ontimer(self.move, t=random.randint(100,300))
    def is_close(self,other):
        a=self.xcor()-other.xcor()
        b=self.ycor()-other.ycor()
        distance=math.sqrt((a**2)+(b**2))

        if distance < 75:
            return True
        else:
            return False

    
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

#Create levels list
levels=[""]

#Define first level
level_1=[
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP XXXXXXX          XXXXX",
"X   XXXXXX  XXXXXX  XXXXX",
"X       XX  XXXXXX  XXXXX",
"X       XX  XXX       EXX",
"XXXXXX  XX  XXX        XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X  XXX        XXXT  XXXXX",
"X  XXX  XXXXXXXXXXXXXXXXX",
"X         XXXXXXXXXXXXXXX",
"X                XXXXXXXX",
"XXXXXXXXXXXX     XXXXX  X",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXX  XXXXXXXXXX         X",
"XXXE                    X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XX   XXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XX    EXXXXXXXXXXX  XXXXX",
"XX          XXXX        X",
"XXXXE            T      X",
"XXXXXXXXXXXXXXXXXXXXXXXXX"    
]

#Add a teasure list
treasures=[]

#Add enemies list
enemies=[]

#Add maze to mazes list
levels.append(level_1)

#Create Level setupp function
def setup_maze(level):
    global game_state
    game_state = "game"
    for y in range(len(level)):
        for x in range(len(level[y])):
            #Get the character  at each x,y coordinates
            #note the order of y and x in the next line
            character=level[y][x]
            #calculate the screeen x, y coordintes
            screen_x=-288+(x*24)
            screen_y=288-(y*24)

            #check if it an X (represinting a wall)
            if character=="X":
                pen.goto(screen_x,screen_y)
                pen.shape("wall.gif")
                pen.stamp() #A turtle can stamp a copy of itself on the screen (turtle drawing area),
                            # and this will remain after the turtle has moved somewhere else
                walls.append((screen_x,screen_y))
            
            #check if it is a P (represinting the player)   
            if character=="P":
                player.goto(screen_x,screen_y)
                pen.stamp() 

            #check if it is a T(representing a treasure)
            if character=="T":
                treasures.append(Treasure(screen_x,screen_y)) 

            #check if it is an E(representing an Enemy)
            if character=="E":
                enemies.append(Enemy(screen_x,screen_y))

#create class instances
pen=Pen()
player=Player()

#Create wall coordinate list
walls=[]


#Set up the level
setup_maze(levels[1])

#keyboard Binding
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

#turn off the screen updates
wn.tracer(0)

#Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move,t=250)

#Main game loop
while True:
    
    #status="playing"
    for treasure in treasures:
        if player.is_collision(treasure):
            #Add the treasure gold to the player gold
            player.gold+=treasure.gold
            print("Player Gold:{}".format(player.gold))
            #Destroy the treasure
            treasure.destroy()
            #Remove the treasure from the treasures list
            treasures.remove(treasure)
            #game_state == "gameover"
    
    for enemy in enemies:
        if player.is_collision(enemy):
            game_state="game_over"
            break;
    if game_state=="game_over":
        pen.end_game()  
        wn.update()
        break; 
    elif player.gold==200:
        pen.you_win()
        wn.update()
        break;
    #update the screen
    
    wn.update()