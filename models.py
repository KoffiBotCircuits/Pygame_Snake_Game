import pygame
import sys
import random

# Define some global variables
ALIVE = 1
DEAD = 0
SCREEN_WIDTH = 630
SCREEN_HEIGHT = 650
GAME_WIDTH = 615
GAME_HEIGHT = 615

# The total game area is 615 x 616 px
# It is divided in 41 x 41 squares
# Each square is 15x15

class Snake():
    # The snake is created with rect objects, with size 15x15
    # Starts with the head rect in the center of the game area
    # Start direction is right and 5 body rects are created to the left of the head
    def __init__(self):

        self.head = pygame.Rect(300,300,15,15)
        self.body = []
        self.status = ALIVE
        self.level = 1
        self.current_direction = 'right' 
        self.move_speed = 80    
        for i in range(5):
            self.body.append(pygame.Rect(self.head.x - (i+1)*15, self.head.y, 15, 15))



    def move(self,new_direction, food):
               
        if self.status == DEAD:
            return
                 
        old_pos_x = self.head.x
        old_pos_y = self.head.y
        
        self.current_direction = new_direction

        # Move the head 1 square in the current direction
        if new_direction == 'up':
            self.head.y -= 15
        if new_direction == 'down':
            self.head.y += 15
        if new_direction == 'left':
            self.head.x -= 15
        if new_direction == 'right':
            self.head.x += 15
        if new_direction == 'stop':
            pass
        
        # To emulate movement, we only move the last rect of the body
        # to the front, where the head was before               
        tail = self.body.pop(-1)
        tail.x = old_pos_x
        tail.y = old_pos_y
        self.body.insert(0, tail)
        
        # Check if the head collides with game bordersm, it self or a piece of food
        if self.head.x < 15 or self.head.x >= GAME_WIDTH:
            self.death(old_pos_x, old_pos_y)
        if self.head.y < 0 or self.head.y >= GAME_HEIGHT:
            self.death(old_pos_x, old_pos_y)
        if self.head.collidelist(self.body) != -1:
            self.death()
        if self.head.colliderect(food.meal):
            self.eat()
    
    def death(self, xpos= -1, ypos= -1):
        self.direction = 'stop'
        self.status = DEAD

        # Just to make sure the head is not drawn outside of the game area
        if xpos >= 0 and ypos >= 0:
            self.head.x = xpos
            self.head.y = ypos


    def eat(self):
        # Extend body when eating
        self.body.append(pygame.Rect(self.body[-1].x, self.body[-1].y,15,15))
        self.level += 1

class Food():
    # Food is a 15x15 rect
    # Food object is created at a random position
    meal = None
    def __init__(self):
        self.meal = pygame.Rect(random.randrange(1,40)*15, random.randrange(1,40)*15, 15, 15)
    
    def food_update(self, snake):
        # If snake head hits the food, move food to a random position
        if self.meal.colliderect(snake.head):
            self.meal.x = random.randrange(1,40)*15
            self.meal.y = random.randrange(1,40)*15



# Some game color definitions
bg_color = pygame.Color('gray10')
line_color = pygame.Color(255,255,255)
head_color = pygame.Color(255,255,255)
tail_color = pygame.Color(160,160,160)
food_color = pygame.Color('yellow')
blink_colors = [pygame.Color('black'), pygame.Color('white'),pygame.Color('red')]
border = [(12,12),(618,12),(618,618),(12,618)]

