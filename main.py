from tkinter import *
from pathgen import *

GAME_WIDTH = 660
GAME_HEIGHT = 660
SPACE = 22
SPEED = 50
START_SIZE = 1
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
            square = canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=SNAKE_COLOR)
            self.squares.append(square)


class Apple:
    def __init__(self, snake_object):
        y = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE
        x = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE

        while (x, y) in snake_object.cords:
            y = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE
            x = random.randint(0, int(GAME_WIDTH / SPACE) - 1) * SPACE

        self.cords = [x, y]
        canvas.create_rectangle(x, y, x + SPACE, y + SPACE, fill=FOOD_COLOR, tags="apple")


def check_full_board(snake_object):
    for x in range(0, int(GAME_WIDTH / SPACE) - 1):
        for y in range(0, int(GAME_WIDTH / SPACE) - 1):
            if (x * SPACE, y * SPACE) not in snake_object.cords:
                return False
    global victory
    victory = True
    return True


def turn_progress(snake_object, apple_object):
    global prev_direc
    x, y = snake_object.cords[0]
    prev_direc = direc

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

            if not check_full_board(snake_object):
                apple_object = Apple(snake_object)

        else:
            del snake_object.cords[-1]
            canvas.delete(snake_object.squares[-1])
            del snake_object.squares[-1]

        global steps
        steps += 1
        label.config(text="Steps:{}".format(steps))

        window.after(SPEED, turn_progress, snake_object, apple_object)

        if player_type.get() == 1:
            snake_turn(snake, path)

    else:
        game_end()


def next_direction(new_direc):
    global prev_direc, direc

    if new_direc == 'left':
        if prev_direc != 'right':
            direc = new_direc

    elif new_direc == 'right':
        if prev_direc != 'left':
            direc = new_direc

    elif new_direc == 'up':
        if prev_direc != 'down':
            direc = new_direc

    elif new_direc == 'down':
        if prev_direc != 'up':
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
    canvas.config(bg="white")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=("Times", 60),
                       text="Game Over!\nSteps:{}\nVictory:{}".format(steps, victory))


def new_speed(var):
    global SPEED
    SPEED = game_speed.get()


def game_start():
    global SPEED, SPACE, initial_setup
    SPEED = speed.get()
    SPACE = space.get()

    config_widow.destroy()
    initial_setup = True


def snake_turn(snake_object, matrix):
    global direc
    x = int(snake_object.cords[0][0] / space.get())
    y = int(snake_object.cords[0][1] / space.get())
    curr_position = matrix[y][x]

    if y - 1 > -1:
        up = matrix[y - 1][x]
        if up == (curr_position + 1) or (curr_position == ((len(matrix) ** 2) - 1) and up == 0):
            direc = 'up'

    if y + 1 < len(matrix):
        down = matrix[y + 1][x]
        if down == (curr_position + 1) or (curr_position == ((len(matrix) ** 2) - 1) and down == 0):
            direc = 'down'

    if x - 1 > -1:
        left = matrix[y][x - 1]
        if left == (curr_position + 1) or (curr_position == ((len(matrix) ** 2) - 1) and left == 0):
            direc = 'left'

    if x + 1 < len(matrix):
        right = matrix[y][x + 1]
        if right == (curr_position + 1) or (curr_position == ((len(matrix) ** 2) - 1) and right == 0):
            direc = 'right'


initial_setup = False

config_widow = Tk()
config_widow.title("Snake! - settings")
config_widow.geometry('300x325')
Label(config_widow, text="Speed, can be changed later", font=("Times", 10)).pack()
speed = Scale(config_widow, from_=1, to=500, orient=HORIZONTAL)
speed.pack()
speed.set(SPEED)

space = IntVar()
Label(config_widow, text='Size "N", can NOT be changed later:', font=("Times", 10)).pack()
Radiobutton(config_widow, text="N=4", value=165, variable=space).pack()
Radiobutton(config_widow, text="N=6", value=110, variable=space).pack()
Radiobutton(config_widow, text="N=10", value=66, variable=space).pack()
Radiobutton(config_widow, text="N=20", value=33, variable=space).pack()
Radiobutton(config_widow, text="N=30", value=22, variable=space).pack()
space.set(22)

player_type = IntVar()
Label(config_widow, text='Human, Unoptimized AI, or Optimized AI Player?', font=("Times", 10)).pack()
Radiobutton(config_widow, text="Human", value=0, variable=player_type).pack()
Radiobutton(config_widow, text="Unoptimized", value=1, variable=player_type).pack()
Radiobutton(config_widow, text="Optimized", value=2, variable=player_type).pack()

Button(config_widow, text="Start!", font="Times", command=game_start).pack()
config_widow.mainloop()

if not initial_setup:
    quit()

window = Tk()
window.title("Snake!")
window.resizable(False, False)

victory = False
steps = 0
direc = 'right'
prev_direc = ''

label = Label(window, text="Steps:{}".format(steps), font=('Times', 40))
label.pack()

game_speed = Scale(window, from_=1, to=500, orient=HORIZONTAL, command=new_speed)
game_speed.set(SPEED)
game_speed.pack()

canvas = Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

if player_type.get() == 0:
    window.bind('<Left>', lambda event: next_direction('left'))
    window.bind('<Right>', lambda event: next_direction('right'))
    window.bind('<Up>', lambda event: next_direction('up'))
    window.bind('<Down>', lambda event: next_direction('down'))

if player_type.get() == 1:
    n = int(GAME_WIDTH / space.get())
    maze = prim_maze_gen(int(n/2))
    cycle = ham_cycle_gen(maze, int(n/2))
    path = matrix_conv(cycle, n)

snake = Snake()
apple = Apple(snake)
turn_progress(snake, apple)

window.mainloop()
