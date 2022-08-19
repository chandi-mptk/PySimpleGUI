import PySimpleGUI as sg
from time import time
from random import randint

FIELD_SIZE = 400
CELL_NUM = 10
CELL_SIZE = FIELD_SIZE / CELL_NUM
DIRECTIONS = {'left': (-1, 0), 'right': (1, 0), 'up': (0, 1), 'down': (0, -1)}


def convert_pos_to_pixel(cell):
    top_left = (cell[0] * CELL_SIZE, cell[1] * CELL_SIZE)
    bottom_right = (top_left[0] + CELL_SIZE, top_left[1] + CELL_SIZE)
    return top_left, bottom_right


# Snake
snake_body = [(4, 4), (3, 4)]
direction = 'up'


def place_apple(apple_pos=(0, 0)):
    new_apple_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    while new_apple_pos in snake_body or new_apple_pos == apple_pos:
        new_apple_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)
    return new_apple_pos


# Apple
apple_pos = place_apple()

sg.theme('Green')
field = sg.Graph(
    canvas_size=(FIELD_SIZE, FIELD_SIZE),
    graph_bottom_left=(0, 0),
    graph_top_right=(FIELD_SIZE, FIELD_SIZE),
    background_color='black'
)
layout = [[field]]

window = sg.Window('Snake', layout, return_keyboard_events=True)
running = True
apple_eaten = False
start_time = time()

while running:
    event, values = window.read(timeout=10)
    if event == sg.WINDOW_CLOSED:
        running = False

    if event == 'Left:37' and direction != 'right':
        direction = 'left'
    if event == 'Right:39' and direction != 'left':
        direction = 'right'
    if event == 'Up:38' and direction != 'down':
        direction = 'up'
    if event == 'Down:40' and direction != 'up':
        direction = 'down'
    
    time_since_start = time() - start_time
    
    if time_since_start >= 0.5:
        start_time = time()
        
        # Apple Snake Collision
        if snake_body[0] == apple_pos:
            apple_pos = place_apple(apple_pos)
            apple_eaten = True
        
        # Snake Collision to Wall
        if not 0 <= snake_body[0][0] <= CELL_NUM - 1 or not 0 <= snake_body[0][1] <= CELL_NUM - 1:
            sg.Popup("Game Over")
            running = False
            
        # Snake Self Collission
        if snake_body[0] in snake_body[1:]:
            sg.Popup("Game Over")
            running = False
        
        # Snake Update
        dx = DIRECTIONS[direction][0]
        dy = DIRECTIONS[direction][1]
        new_head = (snake_body[0][0] + dx, snake_body[0][1] + dy)
        snake_body.insert(0, new_head)
        if apple_eaten:
            apple_eaten = False
        else:
            snake_body.pop()
        
        field.DrawRectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), 'black')
        
        # Draw Apple
        top_left, bottom_right = convert_pos_to_pixel(apple_pos)
        field.DrawRectangle(top_left, bottom_right, 'red')
        
        # Draw Snake
        for index, part in enumerate(snake_body):
            top_left, bottom_right = convert_pos_to_pixel(part)
            color = 'yellow' if index == 0 else 'green'
            field.DrawRectangle(top_left, bottom_right, color)

window.close()
