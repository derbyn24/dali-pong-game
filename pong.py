# Author: Nick Derby
# Date: 24 Oct 2021
# Purpose: Create an Atari Pong game

from cs1lib import *
from random import *

# paddle variables
LEFT_PADDLE_X = 0  # x position of top left corner
left_paddle_y = 0  # y position of top left corner
RIGHT_PADDLE_X = 380  # x position of top left corner
right_paddle_y = 320  # y position of top left corner
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80
PADDLE_MOVE = 13  # how fast the paddle moves when the keys are pressed

# key press variables
a_pressed = False
z_pressed = False
k_pressed = False
m_pressed = False

# ball movement variables
ball_x = 200  # x position
ball_y = 200  # y position
ball_vx = 7  # x velocity
ball_vy = 5  # y velocity

# ball setup variables
BALL_SIZE = 10  # radius
ball_blue = 0  # ball blue color value
ball_green = 1  # ball green color value
ball_red = 0  # ball red color value

WINDOW_SIZE = 400  # height and width of square window

game_in_progress = False

left_score = 0  # score of left player
right_score = 0  # score of right player


def my_key_press(value):
    global a_pressed, z_pressed, k_pressed, m_pressed, game_in_progress
    if value == "a":
        a_pressed = True

    if value == "z":
        z_pressed = True

    if value == "k":
        k_pressed = True

    if value == "m":
        m_pressed = True

    if value == "q":
        cs1_quit()

    if value == " ":
        game_in_progress = True


def my_key_release(value):
    global a_pressed, z_pressed, k_pressed, m_pressed
    if value == "a":
        a_pressed = False

    if value == "z":
        z_pressed = False

    if value == "k":
        k_pressed = False

    if value == "m":
        m_pressed = False


# returns True if left paddle is hit
def left_paddle_hit():
    if ball_x < PADDLE_WIDTH + BALL_SIZE \
            and left_paddle_y < ball_y < left_paddle_y + PADDLE_HEIGHT:
        return True

    return False


# returns True if right paddle is hit
def right_paddle_hit():
    if ball_x > WINDOW_SIZE - PADDLE_WIDTH - BALL_SIZE \
            and right_paddle_y < ball_y < right_paddle_y + PADDLE_HEIGHT:
        return True

    return False


# returns True if left vertical wall is hit
def left_wall_hit():
    if ball_x < BALL_SIZE:
        return True

    return False


# returns True if right vertical wall is hit
def right_wall_hit():
    if ball_x > WINDOW_SIZE - BALL_SIZE:
        return True

    return False


# returns True if either the top or bottom horizontal wall is hit
def horiz_wall_hit():
    if ball_y > WINDOW_SIZE - BALL_SIZE or ball_y < BALL_SIZE:
        return True

    return False


# draws and controls the motion of the ball
def ball():
    global ball_x, ball_y, ball_vx, ball_vy, right_score, left_score, \
        game_in_progress, ball_blue, ball_green, ball_red

    # set ball color
    disable_stroke()
    set_fill_color(ball_red, ball_green, ball_blue)

    # ensures the ball remains visible against black background
    if ball_red < .33 and ball_green < .33 and ball_blue < .33:
        set_stroke_color(1, 1, 1)
        set_stroke_width(1)
        enable_stroke()

    # draw ball
    draw_circle(ball_x, ball_y, BALL_SIZE)

    if game_in_progress:
        # moves ball according to velocity variables
        ball_x += ball_vx
        ball_y += ball_vy

        if right_paddle_hit() or left_paddle_hit():
            ball_vx = -ball_vx  # bounces ball off paddles
            ball_vy = randint(-8, 8)  # randomizes the y velocity of the ball
            ball_red = uniform(0, 1)  # changes red color value of the ball
            ball_green = uniform(0, 1)  # changes green color value of the ball
            ball_blue = uniform(0, 1)  # changes blue color value of the ball

        if horiz_wall_hit():
            # if -2 < ball_vy < 2:
            ball_vy = -ball_vy  # bounces ball off horizontal walls

        if left_wall_hit():
            right_score += 1  # awards point to right player
            game_in_progress = False  # ends game round

        if right_wall_hit():
            left_score += 1  # awards point to left player
            game_in_progress = False  # ends game round

    else:  # resets ball to original settings when game is not in progress
        ball_x = WINDOW_SIZE / 2
        ball_y = WINDOW_SIZE / 2
        ball_red = 0
        ball_green = 1
        ball_blue = 0


# draws and controls the motion of the paddles
def paddles():
    global left_paddle_y, right_paddle_y
    draw_rectangle(LEFT_PADDLE_X, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    draw_rectangle(RIGHT_PADDLE_X, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    if a_pressed:  # moves left paddle up
        if left_paddle_y > 0:
            left_paddle_y -= PADDLE_MOVE

    if z_pressed:  # moves left paddle down
        if left_paddle_y < WINDOW_SIZE - PADDLE_HEIGHT:
            left_paddle_y += PADDLE_MOVE

    if k_pressed:  # moves right paddle up
        if right_paddle_y > 0:
            right_paddle_y -= PADDLE_MOVE

    if m_pressed:  # moves right paddle down
        if right_paddle_y < WINDOW_SIZE - PADDLE_HEIGHT:
            right_paddle_y += PADDLE_MOVE


# displays a scoreboard in the top part of the playing area
def print_scores():
    enable_stroke()
    set_stroke_color(1, 1, 1)
    set_font_size(20)
    draw_text(str(left_score), 100, 25)
    draw_text(str(right_score), 295, 25)


# master draw function called in the start_graphics function
def pong():
    # set up play area
    set_clear_color(0, 0, 0)
    clear()
    set_fill_color(0, 1, 0)
    disable_stroke()

    paddles()

    ball()

    print_scores()


start_graphics(pong, key_press=my_key_press, key_release=my_key_release)
