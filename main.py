from os import wait
import pygame
import sys
import time
from datetime import timedelta

from pygame import display
from models import *

def playagain():
    global screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                screen.fill(bg_color)
                display.flip()
                reset_game()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                pygame.quit()
                sys.exit()
        time.sleep(1)

    

def reset_game():
    global snake, food, direction, play_time, last_time,start_time
    del snake
    food = None
    start_time = pygame.time.get_ticks()
    snake = Snake()
    food = Food()
    direction = 'right'
    play_time = 0
    last_time = 0       

# General setup
pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(100)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')

# Game objects
snake = Snake()
food = Food()
#score = Score_board()
font = pygame.font.Font('freesansbold.ttf', 20)


# Game variables
direction = 'right'
level_speed = 80
last_tick = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
play_time = 0
last_time = 0

# Game Loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            direction = 'up'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            direction = 'left'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            direction = 'right'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            direction = 'down'
    
    if pygame.time.get_ticks() - last_tick > level_speed:
        snake.move(direction,food)
        last_tick = pygame.time.get_ticks()
    
    food.food_update(snake)
    screen.fill(bg_color)

    if snake.status == ALIVE:
        pygame.draw.rect(screen,head_color,snake.head)
        for i in range(len(snake.body)):
            pygame.draw.rect(screen,tail_color,snake.body[i],0,4)
    else:
        for i in range(len(snake.body)):
            pygame.draw.rect(screen,tail_color,snake.body[i],0,4)
        
        pygame.draw.rect(screen,pygame.Color('yellow'),snake.head)
        level_text = font.render('You died!',False,pygame.Color('white'))
        screen.blit(level_text,(285,250))
        level_text = font.render('Play again? (Y/N)',False,pygame.Color('white'))
        screen.blit(level_text,(250,280))
  
    pygame.draw.lines(screen,line_color,True,border,4)
    pygame.draw.rect(screen,pygame.Color('red'),food.meal)

    level_text = font.render(f'LEVEL: {snake.level}',False,pygame.Color('white'))
    screen.blit(level_text,(150,625))

    play_time = timedelta(milliseconds=(pygame.time.get_ticks()-start_time))

    play_time = (play_time - timedelta(microseconds=play_time.microseconds))
    level_text = font.render(f'TIME: {play_time}',False,pygame.Color('white'))
    screen.blit(level_text,(300,625))

    pygame.display.flip()

    if snake.status == DEAD:
        playagain()

    clock.tick(60)