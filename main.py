from tkinter import *

import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE = 50
SPEED = 500
START_SIZE = 5
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.size = START_SIZE
        self.cords = []
        self.squares = []

        for x in range(0, START_SIZE):
            self.cords.append([0, 0])

        for x, y in self.cords:
            square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Apple:
    def __init__(self):
        y = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE
        x = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE

        self.cords = [x, y]

        canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=FOOD_COLOR, tag="apple")


def turn_progress(snake_object, apple_object):
    x, y = snake_object.cords[0]

    if direc == 'up':
        y -= SPACE

    elif direc == 'down':
        y += SPACE

    elif direc == 'left':
        x -= SPACE

    elif direc == 'right':
        x += SPACE

    snake_object.cords.insert(0, (x, y))
    if not collision_check(snake_object):

        square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKE_COLOR)
        snake_object.squares.insert(0, square)

        if x == apple_object.cords[0] and y == apple_object.cords[1]:
            canvas.delete("apple")

            apple_object = Apple()

        else:
            del snake_object.cords[-1]
            canvas.delete(snake_object.squares[-1])
            del snake_object.squares[-1]

        global steps
        steps += 1
        label.config(text="Steps:{}".format(steps))

        window.after(SPEED, turn_progress, snake_object, apple_object)

    else:
        game_end()


def next_direction(new_direc):
    global direc

    if new_direc == 'left':
        if direc != 'right':
            direc = new_direc

    elif new_direc == 'right':
        if direc != 'left':
            direc = new_direc

    elif new_direc == 'up':
        if direc != 'down':
            direc = new_direc

    elif new_direc == 'down':
        if direc != 'up':
            direc = new_direc


def collision_check(snake_object):
    x, y = snake_object.cords[0]

    if x < 0 or x >= GAME_WIDTH:
        print("game end")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("game end")
        return True

    for segment in snake_object.cords[1:]:
        if x == segment[0] and y == segment[1]:
            print("game end")
            return True

    return False


def game_end():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Times", 60),
                       text="Game Over!\nSteps:{}".format(steps), fill="blue")


window = Tk()
window.title("Snake!")
window.resizable(False, False)

steps = 0
direc = 'right'

label = Label(window, text="Steps:{}".format(steps), font=('Times', 40))
label.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.bind('<Left>', lambda event: next_direction('left'))
window.bind('<Right>', lambda event: next_direction('right'))
window.bind('<Up>', lambda event: next_direction('up'))
window.bind('<Down>', lambda event: next_direction('down'))

snake = Snake()
apple = Apple()
turn_progress(snake, apple)

window.mainloop()
