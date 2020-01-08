import pygame
from pygame import *
import random
import time


pygame.init()


#BOUNDING VARIABLES

WINDOW_X = 800
WINDOW_Y = 650
MIN_X = 30
MAX_X = WINDOW_X - MIN_X + 2

GROUND_LEVEL = 570
PLAYER_HEIGHT = 36
PLAYER_LARG = 28
PLAYER_MAX_X = WINDOW_X - MIN_X - PLAYER_LARG + 6
WINDOW_SIZE = (WINDOW_X, WINDOW_Y)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()
TIME_PER_FRAME = 50


#SPRITES
simple_block = pygame.image.load("Bloco1.png")
player1_right1 = pygame.image.load("right_frame_1.png")
player1_right2 = pygame.image.load("right_frame_2.png")
player1_right3 = pygame.image.load("right_frame_3.png")
player1_right4 = pygame.image.load("right_frame_4.png")

player1_images_right = [player1_right1, player1_right2, player1_right3,player1_right4]

player1_left1= pygame.image.load("left_frame1.png")
player1_left2 = pygame.image.load("left_frame2.png")
player1_left3 = pygame.image.load("left_frame3.png")
player1_left4 = pygame.image.load("left_frame4.png")

player1_images_left = [player1_left1, player1_left2, player1_left3, player1_left4]

player1_static = pygame.image.load("static_frame.png")

mapping = pygame.image.load("bitmap.png")
pang_logo = pygame.image.load("Pang_logo.png")
background = pygame.image.load("background.png")


#PLAYER BEAM COLORS
dark_green = (0,100,0)
green = (0, 255,0)
orange = (255, 100,0)
yellow = (200,200,0)
red = (255,0,0)
cyan = (0,100,255)
blue = (0,0,255)
pink = (255,0,150)
colors = [red, yellow, orange, pink, green, cyan, blue, dark_green]

#OBJECTS DEFINITION
class Menu_Button:
    def __init__(self, window, text, letter_size, letter_color, bgrnd_color, ext_color, center, box):
        self.window = window
        self.text = text
        self.letter_size = letter_size
        self.letter_color = letter_color
        self.bgrnd_color = bgrnd_color
        self.ext_color = ext_color
        self.center = center
        self.box = box
    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', self.letter_size)
        txt = font.render(self.text, True, self.letter_color, self.bgrnd_color)
        txt_rect = txt.get_rect()
        txt_rect.center = self.center
        pygame.draw.rect(self.window, self.bgrnd_color, self.box)
        pygame.draw.rect(self.window, self.ext_color, self.box, 5)
        self.window.blit(txt, txt_rect)        


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
    def __init__(self, window, color, start_pos, end_pos, shot_existence):
        self.window = window
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.shot_existence = shot_existence
    def draw(self):
        pygame.draw.line(self.window, self.color, self.start_pos, self.end_pos, 3)

    
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
    def __init__(self, window, images_right, images_left, image_static, pos, speed, buttons, shot, points,status):
        self.window = window
        self.images_right = images_right
        self.images_left = images_left
        self.image_static = image_static
        self.pos = pos
        self.speed = speed
        self.buttons = buttons
        self.shot = shot
        self.points = points
        self.status = status
        self.last_dir = None

    def spawn(self):
        global TIME_PER_FRAME
        if self.status == "moving right":
            current_time = pygame.time.get_ticks()
            current_frame = (current_time // TIME_PER_FRAME)  % len(self.images_right)
            self.window.blit(self.images_right[current_frame], self.pos)
        elif self.status == "moving left":
            current_time = pygame.time.get_ticks()
            current_frame = (current_time // TIME_PER_FRAME)  % len(self.images_left)
            self.window.blit(self.images_left[current_frame], self.pos)
        elif self.status == "static":
            self.window.blit(self.image_static, self.pos)
        # elif self.status == "static+":
        #     self.window.blit(self.image_static, self.pos)
        #     if self.speed > 0:
        #         self.status = "moving right"
        #     elif self.speed < 0:
        #         self.status = "moving left"
    def forward(self):
        self.status = "moving right"
        self.speed = 2
        self.last_dir = 'right'
    def backwards(self):
        self.status = "moving left"
        self.speed = -2
        self.last_dir = 'left'
    def stop(self):
        self.status = "static"
        self.speed = 0


#FUNCTIONS
def check_player_collisions(ball, players):
    for player in players:
        if (ball.pos[0] + ball.radius >= player.pos[0] and ball.pos[0] + ball.radius <= player.pos[0] + PLAYER_LARG and ball.pos[1] + ball.radius >= player.pos[1]) or (ball.pos[0] - ball.radius >= player.pos[0] and ball.pos[0] - ball.radius <= player.pos[0] + PLAYER_LARG and ball.pos[1] + ball.radius >= player.pos[1]):
            return True
    return False


def check_shot_collisions(ball, players):
    for player in players:
        if player.shot.end_pos[0] >= ball.pos[0] - ball.radius and player.shot.end_pos[0] <= ball.pos[0] + ball.radius and ball.pos[1] + ball.radius > player.shot.end_pos[1] and player.shot.shot_existence:
            player.points += 10*ball.radius
            player.shot.shot_existence = False
            player.shot.end_pos[1] = GROUND_LEVEL
            return True
    return False


def check_shot_block_collisions(player, blocks):
    for block in blocks:
        if player.shot.end_pos[0] >= block[0] and player.shot.end_pos[0] + 3 <= block[0] + 100 and player.shot.end_pos[1] >= block[1] and player.shot.end_pos[1] <= block[1] + 20:
            return True
    return False


def check_ball_block_vertical_collisions(ball, blocks):
    for block in blocks:
        if ball.pos[1] + ball.radius <= block[1] + 20 and ball.pos[1] + ball.radius >= block[1] and ball.pos[0] <= block[0] + 100 and ball.pos[0] >= block[0]:
            ball.pos[1] -= 1
            return True
        elif ball.pos[1] - ball.radius <= block[1] + 20 and ball.pos[1] - ball.radius>= block[1] and ball.pos[0] <= block[0] + 100 and ball.pos[0] >= block[0]:
            ball.pos[1] += 1
            return True
    return False 


def check_ball_block_horizontal_collisions(ball, blocks):
    for block in blocks:
        if ball.pos[0] + ball.radius >= block[0] and ball.pos[0] + ball.radius <= block[0] + 100 and block[1] + 20 <= ball.pos[1] + ball.radius and block[1] >= ball.pos[1] - ball.radius:
            ball.pos[0] -= 1
            return True
        elif ball.pos[0] - ball.radius >= block[0] and ball.pos[0] - ball.radius <= block[0] + 100 and block[1] + 20 <= ball.pos[1] + ball.radius and block[1] >= ball.pos[1] - ball.radius:
            ball.pos[0] += 1
            return True
    return False


#Defining the map and types of blocks
map_draw = Map(WINDOW, mapping, (0,0))
block_as = Block(WINDOW, simple_block, (400,300))

#Defining all the levels, in other words, defining the balls and the blocks mapping of the different levels
lvl1_ball1 = Ball(WINDOW, (200, 0, 0), [200, 200], 25, [1,1])
lvl1_balls = [lvl1_ball1]
lvl1_blocks = (())
lvl1 = Level_Matrix(WINDOW, lvl1_blocks, ())
lvl1_info = [lvl1_balls, lvl1_blocks, lvl1]

lvl2_ball1 = Ball(WINDOW, (0, 255, 0), [200, 200], 25, [1,1])
lvl2_ball2 = Ball(WINDOW, (0, 255, 0), [520, 300], 25, [1,1])
lvl2_balls = [lvl2_ball1, lvl2_ball2]
lvl2_blocks = ((200,400), (600,400))
lvl2 = Level_Matrix(WINDOW, lvl2_blocks, ())
lvl2_info = [lvl2_balls, lvl2_blocks, lvl2]

lvl3_ball1 = Ball(WINDOW, (0, 150, 255), [400, 200], 25, [1,1])
lvl3_ball2 = Ball(WINDOW, (0, 150, 255), [400, 300], 25, [1,1])
lvl3_balls = [lvl3_ball1,lvl3_ball2]
lvl3_blocks = ((375,250), (265,185), (490, 185))
lvl3 = Level_Matrix(WINDOW, lvl3_blocks, ())
lvl3_info = [lvl3_balls, lvl3_blocks, lvl3]

lvl4_ball1 = Ball(WINDOW, pink, [300,200], 30, [-1,1])
lvl4_balls = [lvl4_ball1]
lvl4_blocks = ((400, 370), (200, 450), (550, 400))
lvl4 = Level_Matrix(WINDOW, lvl4_blocks, ())
lvl4_info = [lvl4_balls, lvl4_blocks, lvl4]

"""
pelo menos 5 níveis
"""

#List with all the different levels of the game
levels = [lvl1_info, lvl2_info, lvl3_info, lvl4_info]


#Defining players
player1_color = (255,0,0)
player2_color = (255,0,0)
player1_points = 0
player2_points = 0
player1_shot = Shot(WINDOW, player1_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
player1 = Player(WINDOW, player1_images_right, player1_images_left, player1_static, [400,570], 0, [K_LEFT, K_RIGHT, K_DOWN], player1_shot, player1_points, "static")
player2_shot = Shot(WINDOW, player2_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
player2 = Player(WINDOW, player1_images_right, player1_images_left, player1_static, [400,530], 0, [K_a, K_d, K_s], player2_shot, player2_points, "static")

#Players that will participate in the game (set to only player 1 by default)
players = [player1]

#Utility variables
current_level = 0
lives = 5
count = 0
check = False
lost = False


def won_game_transition():
    """
       A transition that plays whenever the player or players win the game. Shows the final gained
       points and how many lives weren't used up, being awarded bonus points for each one of those.
    """
    global current_level
    global lives
    global player1
    global player2
    check = False
    first_check = False
    second_check = False
    extra_points = 0
    final_points = 0
    end = Menu_Button(WINDOW, "Press ESC to go back to the main menu.", 30, (255,255,255), (0,0,0), (0,0,0), (400, 400), (1000,1000,100,100))
    while True:
        total_score = Menu_Button(WINDOW, "Total score: " + str(final_points), 30, (255,255,255), (0,0,0), (0,0,0), (400, 300), (1000,1000,100,100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE and check:
                main_menu()
        first_message = Menu_Button(WINDOW, "You have won the game with " + str(lives) + " remaining lives.", 30, (255,255,255), (0,0,0), (0,0,0), (400, 200), (1000,1000,100,100))
        if extra_points < 1000*lives and not second_check:
            extra_points += 10
        else:
            first_check = True
        extra_pts = Menu_Button(WINDOW, "Extra points: " + str(extra_points), 30, (255,255,255), (0,0,0), (0,0,0), (400, 250), (1000,1000,100,100))
        if first_check:
            if final_points < extra_points + player1.points + player2.points:
                final_points += 10
            else:
                second_check = True
                
                
        WINDOW.fill((0,0,0))
        if first_check:
            total_score.draw()
        extra_pts.draw()
        first_message.draw()
        if second_check:
            check = True
            end.draw()
        pygame.display.flip()
        clock.tick(120)


def lost_game_transition():
    """
       A transition that plays whenever the player(s) lose the game. Shows obtained points and how far
       in the game the player(s) went.
    """
    global current_level
    global lives
    global player1
    global player2
    check = False
    first_check = False
    final_points = 0
    stats = Menu_Button(WINDOW, "Having reached level " + str(current_level + 1) + ", you lost the game." , 30, (255,255,255), (0,0,0), (0,0,0), (400, 200), (1000,1000,100,100))
    end = Menu_Button(WINDOW, "Press ESC to go back to the main menu.", 30, (255,255,255), (0,0,0), (0,0,0), (400, 400), (1000,1000,100,100))
    while True:
        WINDOW.fill((0,0,0))
        total_score = Menu_Button(WINDOW, "Total score: " + str(final_points), 30, (255,255,255), (0,0,0), (0,0,0), (400, 300), (1000,1000,100,100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE and check:
                main_menu()
        if final_points < player1.points + player2.points:
            final_points += 10
        else:
            first_check = True
            
            
        WINDOW.fill((0,0,0))
        if first_check:
            check = True
            end.draw()
        stats.draw()
        total_score.draw()
        pygame.display.flip()
        clock.tick(120)


def level_transition():
    """
       A transition between levels. Shows current obtained points. The load isn't actually loading
       anything, it only serves as a break for the animation to display and to allow a break.
    """
    global current_level
    global lives
    global player1
    global player2
    check = False
    first_check = False
    current_points = 0
    txt = "Loading next level..."
    end = Menu_Button(WINDOW, "Press the up key to go to the next level.", 30, (255,255,255), (0,0,0), (0,0,0), (400, 400), (1000,1000,100,100))
    while True:
        WINDOW.fill((0,0,0))
        load = Menu_Button(WINDOW, txt , 30, (255,255,255), (0,0,0), (0,0,0), (400, 200), (1000,1000,100,100))
        current_score = Menu_Button(WINDOW, "Current score: " + str(current_points), 30, (255,255,255), (0,0,0), (0,0,0), (400, 300), (1000,1000,100,100))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_UP and check:
                LEVEL(levels[current_level])
        if current_points < player1.points + player2.points:
            current_points += 10
        else:
            first_check = True
            
            
        WINDOW.fill((0,0,0))
        if first_check:
            check = True
            txt = "Loaded!"
            end.draw()
        load.draw()
        current_score.draw()
        pygame.display.flip()
        clock.tick(120)

        
def options_menu():
    """
       The options menu allows the user to choose between a single-player game or a two-players
       game. It also allows to enter the beam colors menu.
    """
    global lives
    global GROUND_LEVEL
    global player1
    global player2
    global players
    back_button = Menu_Button(WINDOW, "BACK", 62, (0,0,0), (200,200,0), (150,150,0), (400,555), (200,500,400,100))        
    beam_colors_button = Menu_Button(WINDOW, "BEAM COLORS", 62, (0,0,0), (200,200,0), (150,150,0), (400,400), (125, 350, 550, 100))
    while True:
        if len(players) == 1:
            players_1_col = (0,200,0)
            players_2_col = (200,200,0)
        elif players == [player1, player2]:
            players_1_col = (200,200,0)
            players_2_col = (0,200,0)
        for event in pygame.event.get():
            mouse_buttons = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if mouse_buttons[0] == 1:
                if 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
                    main_menu()
                if 25 <= mouse_pos[0] <= 375 and 200 <= mouse_pos[1] <= 300:
                    players = [player1]
                if 425 <= mouse_pos[0] <= 775 and 200 <= mouse_pos[1] <= 300:
                    players = [player1,player2]
                if 125 <= mouse_pos[0] <= 675 and 350 <= mouse_pos[1] <= 450:
                    beam_colors_menu()
        players1_button = Menu_Button(WINDOW, "1 PLAYER", 62, (0,0,0), players_1_col, (150,150,0), (200,250), (25,200,350,100))
        players2_button = Menu_Button(WINDOW, "2 PLAYERS", 62, (0,0,0), players_2_col, (150,150,0), (600,250), (425,200,350,100))
        
        WINDOW.fill((0,0,0))
        back_button.draw()
        players1_button.draw()
        players2_button.draw()
        beam_colors_button.draw()
        pygame.display.flip()
        clock.tick(120)


def beam_colors_menu():
    """
       The beam colors menu allows the player(s) to choose their color(s) for the shot beam.
    """
    global lives
    global GROUND_LEVEL
    global player1
    global player2
    global players
    global player1_color
    global player2_color
    global colors
    p1 = colors.index(player1_color)
    p2 = colors.index(player2_color)
    back_button = Menu_Button(WINDOW, "BACK", 62, (0,0,0), (200,200,0), (150,150,0), (400,555), (200,500,400,100))
    player1_button = Menu_Button(WINDOW, "PLAYER 1", 62, (0,0,0), (200,200,0), (150,150,0), (200,250), (25,200,350,100))
    player2_button = Menu_Button(WINDOW, "PLAYER 2", 62, (0,0,0), (200,200,0), (150,150,0), (200,375), (25,325,350,100))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] == 1:
                if 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
                    options_menu()
                if 680 <= mouse_pos[0] <= 730 and 225 <= mouse_pos[1] <= 275:
                    p1 += 1
                    player1_color = colors[p1%len(colors)]
                    player1_shot = Shot(WINDOW, player1_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
                    player1 = Player(WINDOW, player1_images_right, player1_images_left, player1_static,  [400,570], 0, [K_LEFT, K_RIGHT, K_DOWN], player1_shot, player1_points, "static")
                    if len(players) == 1:
                        players = [player1]
                    else:
                        players = [player1, player2]
                if 470 <= mouse_pos[0] <= 520 and 225 <= mouse_pos[1] <= 275:
                    p1 -= 1
                    player1_color = colors[p1%len(colors)]
                    player1_shot = Shot(WINDOW, player1_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
                    player1 = Player(WINDOW, player1_images_right, player1_images_left, player1_static, [400,570], 0, [K_LEFT, K_RIGHT, K_DOWN], player1_shot, player1_points, "static")
                    if len(players) == 1:
                        players = [player1]
                    else:
                        players = [player1, player2]
                if 680 <= mouse_pos[0] <= 730 and 350 <= mouse_pos[1] <= 400:
                    p2 += 1
                    player2_color = colors[p2%len(colors)]
                    player2_shot = Shot(WINDOW, player2_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
                    player2 = Player(WINDOW, player1_images_right, player1_images_left, player1_static, [400,570], 0, [K_a, K_d, K_s], player2_shot, player2_points, "static")
                    if len(players) == 1:
                        players = [player1]
                    else:
                        players = [player1, player2]
                if 470 <= mouse_pos[0] <= 520 and 350 <= mouse_pos[1] <= 400:
                    p2 -= 1
                    player2_color = colors[p2%len(colors)]
                    player2_shot = Shot(WINDOW, player2_color, [0,GROUND_LEVEL], [0,GROUND_LEVEL], False)
                    player2 = Player(WINDOW, player1_images_right, player1_images_left, player1_static, [400,570], 0, [K_a, K_d, K_s], player2_shot, player2_points, "static")
                    if len(players) == 1:
                        players = [player1]
                    else:
                        players = [player1, player2]
                        
                        
        WINDOW.fill((0,0,0))
        pygame.draw.rect(WINDOW, player1_color, (550,200,100,100))
        pygame.draw.rect(WINDOW, (255,255,255), (550,200, 100,100), 5)
        pygame.draw.rect(WINDOW, player2_color, (550,325,100,100))
        pygame.draw.rect(WINDOW, (255,255,255), (550,325, 100,100), 5)
        pygame.draw.polygon(WINDOW, (200,200,0), ((680,200), (680,300), (730,250)))
        pygame.draw.polygon(WINDOW, (150,150,0), ((680,200), (680,300), (730,250)), 5)
        pygame.draw.polygon(WINDOW, (200,200,0), ((680,325), (680,425), (730,375)))
        pygame.draw.polygon(WINDOW, (150,150,0), ((680,325), (680,425), (730,375)), 5)
        pygame.draw.polygon(WINDOW, (200,200,0), ((520,200), (520,300), (470,250)))
        pygame.draw.polygon(WINDOW, (150,150,0), ((520,200), (520,300), (470,250)), 5)
        pygame.draw.polygon(WINDOW, (200,200,0), ((520,325), (520,425), (470,375)))
        pygame.draw.polygon(WINDOW, (150,150,0), ((520,325), (520,425), (470,375)), 5)
        back_button.draw()
        player1_button.draw()
        player2_button.draw()
        pygame.display.flip()
        clock.tick(120)


def main_menu():
    """
       The main menu of the game is the starting point of the program. It allows the user to start the
       game, to enter the options menu or to quit the game (it is the only menu from which you can 
       close the program). It also displays the logo of the game and is the only menu in which the
       buttons are highlighted when hovered.
    """
    global lives
    global current_level
    lives = 5
    current_level = 0
    player1.points = 0
    player2.points = 0
    pygame.mouse.set_visible(True)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0] == 1:
                if 200 <= mouse_pos[0] <= 600 and 250 <= mouse_pos[1] <= 350:
                    LEVEL(levels[current_level])
                elif 200 <= mouse_pos[0] <= 600 and 375 <= mouse_pos[1] <= 475:
                    options_menu()
                elif 200 <= mouse_pos[0] <= 600 and 500 <= mouse_pos[1] <= 600:
                    return pygame.quit()
        
        WINDOW.fill((0,0,0))
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
        WINDOW.blit(first_but_txt, first_but_txt_rect)
        WINDOW.blit(second_but_txt, second_but_txt_rect)
        WINDOW.blit(third_but_txt, third_but_txt_rect)
        WINDOW.blit(pang_logo, (275,100))
        pygame.display.flip()
        clock.tick(120)
        
    
def LEVEL(level_info):
    """This function contains all of the game's mechanics. The parameter has to be a list, containing
       nested lists with the informations about the levels, as declared above.
       The main menu can be accessed anytime while this function is running by simply pressing the ESC
       key. However, doing so will cause the game to restart, restoring lives, zeroing points and taking
       the player(s) back to Level 1.
    """
    global lives
    global GROUND_LEVEL
    global player1_color
    global player2_color
    global player1
    global player2
    global players
    global current_level
    global levels
    
    #Setting up the players for the game
    player1.pos = [200, GROUND_LEVEL - PLAYER_HEIGHT + 3]
    player2.pos = [400, GROUND_LEVEL - PLAYER_HEIGHT]
    player1.shot.shot_existence = False
    player2.shot.shot_existence = False
    player1.shot.end_pos[1] = GROUND_LEVEL + 25
    player2.shot.end_pos[1] = GROUND_LEVEL + 25
    
    #Making a copy of the level so, in case of defeat, the restart point will always be the same
    lvl_info = level_info[:]
    lvl_balls = []
    for i in lvl_info[0]:
        lvl_balls.append(Ball(i.window, i.color[:], i.pos.copy(), i.radius, i.speed.copy()))
    lvl_info[0] = lvl_balls
    
    #Utility variables
    count = 0
    lost = False
    check = False
    pygame.mouse.set_visible(False)
    
    while True:
        # WINDOW.blit(background, (0,-5))
        WINDOW.fill((0,0,0))
        
        #Game processes
        cur_lives = Menu_Button(WINDOW, "LIVES: " + str(lives), 50, (255,255,255), (0,0,0), (0,0,0), (150, 625), (1000,1000,100,100))
        points = Menu_Button(WINDOW , "POINTS : " + str(player1.points + player2.points), 50, (255,255,255), (0,0,0), (0,0,0), (600,625), (1000,1000,100,100))
        if len(lvl_info[0]) == 0:
            if current_level  + 1 == len(levels):
                won_game_transition()
            else:
                current_level += 1
                level_transition()
        if lost or lives == 0:
            if lives > 0:
                lives -= 1
                time.sleep(1)
                LEVEL(level_info)
            else:
                lost_game_transition()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                main_menu()
            for player in players:
                if event.type == pygame.KEYDOWN and event.key == player.buttons[2]:
                    if player.shot.shot_existence == False:
                        player.stop()
                        player.shot.shot_existence = True
                        player.shot.start_pos[0] = player.pos[0] + 15
                        player.shot.end_pos[0] = player.pos[0] + 15
                if event.type == pygame.KEYUP and event.key == player.buttons[2]:
                    if player.last_dir == 'right':
                        player.forward()
                    elif player.last_dir == 'left':
                        player.backwards()
        for player in players:
            keys = pygame.key.get_pressed()
            for player in players:
                if keys[player.buttons[0]] and keys[player.buttons[1]]:
                    player.stop()
                elif keys[player.buttons[0]]:
                    player.backwards()
                elif keys[player.buttons[1]]:
                    player.forward()
                else:
                    player.stop()
            if player.shot.end_pos[1] <= 25 or check_shot_block_collisions(player, lvl_info[1]):
                player.shot.shot_existence = False
                player.shot.end_pos[1] = GROUND_LEVEL
            if MIN_X < player.pos[0] < PLAYER_MAX_X:
                player.pos[0] += player.speed
            elif player.pos[0] == PLAYER_MAX_X:
                player.pos[0] -= 2
                player.stop()
            elif player.pos[0] == MIN_X:
                player.pos[0] += 2
                player.stop()
        for ball in lvl_info[0]:
            if check_player_collisions(ball, players):
                lost = True
            if check_shot_collisions(ball, players):
                check = True
            if check:
                check = False
                if ball.radius > 12:
                    lvl_info[0].remove(ball)
                    ball1 = Ball(ball.window, ball.color, ball.pos, int(ball.radius//1.5), ball.speed)
                    ball2 = Ball(ball.window, ball.color, ball.pos, int(ball.radius//1.5), ball.speed)
                    ball2.speed[0] *= -1
                    ball1.speed[1] = -1
                    ball2.speed[1] = -1
                    lvl_info[0].append(ball1)
                    lvl_info[0].append(ball2)
                    continue
                else:
                    lvl_info[0].remove(ball)
                    continue
            if ball.pos[1] + ball.radius >= GROUND_LEVEL:
                ball.speed[1] = -7
            if ball.pos[1] - ball.radius <= 25 or check_ball_block_vertical_collisions(ball, lvl_info[1]):
                ball.speed[1] *= -1
            elif ball.pos[0] + ball.radius >= MAX_X or ball.pos[0] == MIN_X + ball.radius or check_ball_block_horizontal_collisions(ball, lvl_info[1]):
                ball.speed[0] *= -1
            ball.pos[0] += ball.speed[0]
            ball.pos[1] += int(ball.speed[1])
            ball.speed[1] += 0.1
        
        
        #Game rendering/drawing
        map_draw.draw()
        lvl_info[2].draw()
        for player in players:
            if player.shot.shot_existence == True:
                player.shot.draw()
                player.shot.end_pos[1] -= 4
            player.spawn()
        for ball in lvl_info[0]:
            ball.draw()
        points.draw()
        cur_lives.draw()
        pygame.display.flip()
        if count == 0:
            time.sleep(1)
            count += 1
        clock.tick(120)
    

main_menu()

