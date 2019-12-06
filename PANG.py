import pygame
from pygame import *
import random
import time



pygame.init()


#BOUNDING VARIABLES
WINDOW_X = 800
WINDOW_Y = 650
MIN_X = 30
MAX_X = WINDOW_X - MIN_X +2
PLAYER_MAX_X = WINDOW_X - MIN_X - 50 + 6
WINDOW_SIZE = (WINDOW_X, WINDOW_Y)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


#NUMERAL VARIABLES
GROUND_LEVEL = 570
PLAYER_HEIGHT = 100
PLAYER_LARG = 50


#SPRITES
simple_block = pygame.image.load("Bloco1.png")
player_png = pygame.image.load("ASD123.png")
mapping = pygame.image.load("bitmap.png")


#OBJECTS DEFINITION
class Map:
    def __init__(self, window, walls, pos):
        self.window = window
        self.walls = walls
        self.pos = pos
    def draw(self):
        self.window.blit(self.walls, self.pos)


class Block:
    def __init__(self, window, block_type, pos):
        self.window = window
        self.block_type = block_type
        self.pos = pos
    def draw(self):
        self.window.blit(self.block_type, self.pos)


class Ball:
    def __init__(self, window, color, pos, radius, speed):
        self.window = window
        self.color = color
        self.pos = pos.copy()
        self.radius = radius
        self.speed = speed.copy()
    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.radius,0)
        pygame.draw.circle(self.window, (255,255,255), self.pos, self.radius, 1)
    def change_x_direction(self):
        self.speed[0] *= -1


class Shot:
    def __init__(self, window, start_pos, end_pos, shot_existence):
        self.window = window
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.shot_existence = shot_existence
    def draw(self):
        pygame.draw.line(self.window, (255, 0,0), self.start_pos, self.end_pos, 3)

    
class Level_Matrix:
    def __init__(self, window, blocks1, blocks2):
        self.window = window
        self.blocks1 = blocks1
        self.blocks2 = blocks2
    def draw(self):
        for block in self.blocks1:
            self.window.blit(simple_block, block)
        for block in self.blocks2:
            self.window.blit(simple_block, block)


class Player:
    def __init__(self, window, player_avatar, pos, speed, buttons, shot):
        self.window = window
        self.player_avatar = player_avatar
        self.pos = pos
        self.speed = speed
        self.buttons = buttons
        self.shot = shot
    def spawn(self):
        self.window.blit(self.player_avatar, self.pos)
    def forward(self):
        self.speed = 2
    def backwards(self):
        self.speed = -2
    def stop(self):
        self.speed = 0


#FUNCTIONS
def check_player_collisions(ball, players):
    for player in players:
        if (ball.pos[0] + ball.radius >= player.pos[0] and ball.pos[0] + ball.radius <= player.pos[0] + PLAYER_LARG and ball.pos[1] + ball.radius >= player.pos[1]) or (ball.pos[0] - ball.radius >= player.pos[0] and ball.pos[0] - ball.radius <= player.pos[0] + 50 and ball.pos[1] + ball.radius >= player.pos[1]):
            return True
    return False


def check_shot_collisions(ball, players):
    for player in players:
        if player.shot.end_pos[0] >= ball.pos[0] - ball.radius and player.shot.end_pos[0] <= ball.pos[0] + ball.radius and ball.pos[1] + ball.radius > player.shot.end_pos[1] and player.shot.shot_existence:
            player.shot.shot_existence = False
            player.shot.end_pos[1] = GROUND_LEVEL
            return True
    return False


def check_shot_block_collisions(player, blocks):
    for block in blocks:
        if player.shot.end_pos[0] >= block[0] and player.shot.end_pos[0] + 3 <= block[0] + 50 and player.shot.end_pos[1] >= block[1] and player.shot.end_pos[1] <= block[1] + 10:
            return True
    return False


def check_ball_block_vertical_collisions(ball, blocks):
    for block in blocks:
        if (ball.pos[1] + ball.radius <= block[1] + 10 and ball.pos[1] + ball.radius >= block[1] and ball.pos[0] <= block[0] + 50 and ball.pos[0] >= block[0]) or (ball.pos[1] <= block[1] + 10 and ball.pos[1] >= block[1] and ball.pos[0] <= block[0] + 50 and ball.pos[0] >= block[0]):
            return True
    return False 


def check_ball_block_horizontal_collisions(ball, blocks):
    for block in blocks:
        if (ball.pos[0] + ball.radius >= block[0] and ball.pos[0] + ball.radius <= block[0] + 50 and block[1] <= ball.pos[1] + ball.radius and block[1] >= ball.pos[1] - ball.radius) or (ball.pos[0] >= block[0] and ball.pos[0] <= block[0] + 50 and block[1] <= ball.pos[1] + ball.radius and block[1] >= ball.pos[1] - ball.radius): 
            return True
    return False


def psychadelic_balls(ball):
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#Defining the map and types of blocks
map_draw = Map(WINDOW, mapping, (0,0))
block_as = Block(WINDOW, simple_block, (400,300))

#Defining balls and levels
lvl1_ball1 = Ball(WINDOW, (200, 0, 0), [200, 300], 25, [1,1])
lvl1_ball2 = Ball(WINDOW, (200, 0, 0), [500, 200], 25, [1,1])
lvl1_ball3 = Ball(WINDOW, (200, 0, 0), [400, 150], 25, [-1,1])
lvl1_ball4 = Ball(WINDOW, (200, 0, 0), [600, 200], 25, [-1,1])
lvl1_ball5 = Ball(WINDOW, (200, 0, 0), [200, 250], 25, [-1,1])
lvl1_balls = [lvl1_ball1,lvl1_ball2, lvl1_ball3, lvl1_ball4, lvl1_ball5]
#lvl1_matrix = Level_Matrix(WINDOW, simple_block, simple_block, ((400,300), (450,300)), ())

#Defining players
player1_shot = Shot(WINDOW, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
player1 = Player(WINDOW, player_png, [400,470], 0, [K_LEFT, K_RIGHT, K_DOWN], player1_shot)
#player2 = Player(WINDOW, simple_block, [400,530], 0, [K_a, K_d, K_s])
players = [player1]

#Utility variables
lives = 100
count = 0
check = False
lost = False


def options_menu():
    """
    NEEDS FINISHING - MOUSE OVER DETAILS AND BUTTONS FOR ONE AND TWO PLAYERS
    """
    global lives
    global GROUND_LEVEL
    global player1
    global player2
    global players
    while True:
        if players == [player1]:
            players_1_col = (0,200,0)
            players_2_col = (200,200,0)
        elif players == [player1, player2]:
            players_1_col = (200,200,0)
            players_2_col = (0,200,0)
        WINDOW.fill((0,0,0))
        font = pygame.font.Font('freesansbold.ttf', 64) 
        pygame.draw.rect(WINDOW, (200,200, 0), (200, 500, 400, 100))
        pygame.draw.rect(WINDOW, (150,150, 0), (200, 500, 400, 100), 5)
        back_txt = font.render('BACK', True, (0,0,0), (200,200,0))
        back_rect = back_txt.get_rect()
        back_rect.center = (400, 555)
        players_1_txt = font.render("1 PLAYER", True, (0,0,0), players_1_col)
        players_1_rect = players_1_txt.get_rect()
        players_1_rect.center = (250, 250)
        pygame.draw.rect(WINDOW, (0,200,0), (75, 200, 350, 100))
        pygame.draw.rect(WINDOW, (150, 150, 0), (75, 200, 350, 100), 5)
        for event in pygame.event.get():
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_buttons[0] == 1:
                if 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
                    main_menu()
        WINDOW.blit(back_txt, back_rect)
        WINDOW.blit(players_1_txt, players_1_rect)
        pygame.display.flip()
        clock.tick(120)
 
    
def main_menu():
    global lives
    global GROUND_LEVEL
    global player1
    global player2
    global players
    pygame.mouse.set_visible(True)
    while True:
        WINDOW.fill((0,0,0))
        mouse_pos = pygame.mouse.get_pos()
        font = pygame.font.Font('freesansbold.ttf', 64)
        if 200 <= mouse_pos[0] <= 600 and 250 <= mouse_pos[1] <= 350:
            first_but_txt = font.render('PLAY', True, (0,0,0), (250,250,0))
            pygame.draw.rect(WINDOW, (250,250, 0), (200, 250, 400, 100))
        else:
            first_but_txt = font.render('PLAY', True, (0,0,0), (200,200,0))
            pygame.draw.rect(WINDOW, (200,200, 0), (200, 250, 400, 100))
        if 200 <= mouse_pos[0] <= 600 and 375 <= mouse_pos[1] <= 475:
            second_but_txt = font.render('OPTIONS', True, (0,0,0), (250,250,0))
            pygame.draw.rect(WINDOW, (250,250, 0), (200, 375, 400, 100))
        else:
            second_but_txt = font.render('OPTIONS', True, (0,0,0), (200,200,0))
            pygame.draw.rect(WINDOW, (200,200, 0), (200, 375, 400, 100))
        if 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
            third_but_txt = font.render('QUIT', True, (0,0,0), (250,250,0))
            pygame.draw.rect(WINDOW, (250,250, 0), (200, 500, 400, 100))
        else:
            third_but_txt = font.render('QUIT', True, (0,0,0), (200,200,0))
            pygame.draw.rect(WINDOW, (200,200, 0), (200, 500, 400, 100))
        first_but_txt_rect = first_but_txt.get_rect()
        first_but_txt_rect.center = (400, 305)
        second_but_txt_rect = second_but_txt.get_rect()
        second_but_txt_rect.center = (400, 430)
        third_but_txt_rect = third_but_txt.get_rect()
        third_but_txt_rect.center = (400, 555)
        pygame.draw.rect(WINDOW, (150,150, 0), (200, 250, 400, 100), 5)
        pygame.draw.rect(WINDOW, (150,150, 0), (200, 375, 400, 100), 5)
        pygame.draw.rect(WINDOW, (150,150, 0), (200, 500, 400, 100), 5)
        for event in pygame.event.get():
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] == 1:
                if 200 <= mouse_pos[0] <= 600 and 250 <= mouse_pos[1] <= 350:
                    main()
                elif 200 <= mouse_pos[0] <= 600 and 375 <= mouse_pos[1] <= 475:
                    options_menu()
                elif 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
                    pygame.quit()
        WINDOW.blit(first_but_txt, first_but_txt_rect)
        WINDOW.blit(second_but_txt, second_but_txt_rect)
        WINDOW.blit(third_but_txt, third_but_txt_rect)
        pygame.display.flip()
        clock.tick(120)
        
    
def main():
    global lives
    global GROUND_LEVEL
    global player1
    global player2
    global players
    #Defining balls and levels
    lvl1_ball1 = Ball(WINDOW, (200, 0, 0), [200, 200], 25, [1,1])
    lvl1_ball2 = Ball(WINDOW, (200, 0, 0), [500, 200], 25, [1,1])
    lvl1_ball3 = Ball(WINDOW, (200, 0, 0), [400, 150], 25, [-1,1])
    lvl1_ball4 = Ball(WINDOW, (200, 0, 0), [600, 200], 25, [-1,1])
    lvl1_ball5 = Ball(WINDOW, (200, 0, 0), [200, 250], 25, [-1,1])
    lvl1_balls = [lvl1_ball1, lvl1_ball2]#, lvl1_ball3, lvl1_ball4, lvl1_ball5]
    lvl1_blocks = ((400,300), (450,300))
    lvl1 = Level_Matrix(WINDOW, ((400,300), (450,300)), ())
    #Defining players and player related variables
    player1_shot = Shot(WINDOW, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
    player1 = Player(WINDOW, player_png, [400,470], 0, [K_LEFT, K_RIGHT, K_DOWN], player1_shot)
#    player2_shot = Shot(WINDOW, [0,570], [0,570], False)
#    player2 = Player(WINDOW, player_png,  [400,470], 0, [K_a, K_d, K_s], player2_shot)
    players = [player1]
    #Utility variables
    count = 0
    lost = False
    check = False
    pygame.mouse.set_visible(False)
    while True:
        WINDOW.fill((0,0,0))
        if lost:
            if lives > 0:
                lives -= 1
                time.sleep(1)
                main()
            else:
                pygame.quit()
        map_draw.draw()
        lvl1.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                main_menu()
            for player in players:
                if event.type == pygame.KEYDOWN and event.key == player.buttons[0]:
                    player.backwards()
                if event.type == pygame.KEYUP and event.key == player.buttons[0]:
                    player.stop()
                if event.type == pygame.KEYDOWN and event.key == player.buttons[1]:
                    player.forward()
                if event.type == pygame.KEYUP and event.key == player.buttons[1]:
                    player.stop()
                if event.type == pygame.KEYDOWN and event.key == player.buttons[2]:
                    if player.shot.shot_existence == False:
                        player.shot.shot_existence = True
                        player.shot.start_pos[0] = player.pos[0] + 25
                        player.shot.end_pos[0] = player.pos[0] + 25
        for player in players:
            if player.shot.shot_existence == True:
                player.shot.draw()
                player.shot.end_pos[1] -= 4
            if player.shot.end_pos[1] <= 25 or check_shot_block_collisions(player, lvl1_blocks):
                player.shot.shot_existence = False
                player.shot.end_pos[1] = GROUND_LEVEL
            player.spawn()
            if MIN_X < player.pos[0] < PLAYER_MAX_X:
                player.pos[0] += player.speed
            elif player.pos[0] == PLAYER_MAX_X:
                player.pos[0] -= 2
                player.stop()
            elif player.pos[0] == MIN_X:
                player.pos[0] += 2
                player.stop()
        for ball in lvl1_balls:
            if check_player_collisions(ball, players):
                lost = True
#            ball.color = psychadelic_balls(ball)
            ball.draw()
            if check_shot_collisions(ball, players):
                check = True
            if check:
                check = False
                if ball.radius > 12:
                    lvl1_balls.remove(ball)
                    ball1 = Ball(ball.window, ball.color, ball.pos, int(ball.radius//1.5), ball.speed)
                    ball2 = Ball(ball.window, ball.color, ball.pos, int(ball.radius//1.5), ball.speed)
                    ball2.speed[0] *= -1
                    ball1.speed[1] = -1
                    ball2.speed[1] = -1
                    lvl1_balls.append(ball1)
                    lvl1_balls.append(ball2)
                    continue
                else:
                    lvl1_balls.remove(ball)
                    continue
            if ball.pos[1] + ball.radius >= GROUND_LEVEL:
                ball.speed[1] = -7
            if ball.pos[1] - ball.radius <= 25 or check_ball_block_vertical_collisions(ball, lvl1_blocks):
                ball.speed[1] *= -1
            elif ball.pos[0] + ball.radius >= MAX_X or ball.pos[0] == MIN_X + ball.radius or check_ball_block_horizontal_collisions(ball, lvl1_blocks):
                ball.speed[0] *= -1
            ball.pos[0] += ball.speed[0]
            ball.pos[1] += int(ball.speed[1])
            ball.speed[1] += 0.1
        pygame.display.flip()
        if count == 0:
            time.sleep(1)
            count += 1
        clock.tick(120)

main_menu()


