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
    x_temp, y_temp = snake_object.cords[0]
    if not collision_check(x_temp, y_temp, snake_object):

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
            simple_snake_turn(snake, path)
        if player_type.get() == 2:
            optimized_snake_turn(snake_object, apple_object, path)

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


def collision_check(x, y, snake_object):
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for segment in snake_object.cords[1:]:
        if x == segment[0] and y == segment[1]:
            return True

    return False


def game_end():
    global direc
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


def get_dist(a, b):
    if a < b:
        return b - a - 1
    else:
        return b - a - 1 + int(GAME_WIDTH / space.get()) ** 2


def optimized_snake_turn(snake_object, apple_object, matrix):
    global direc
    x = int(snake_object.cords[0][0] / space.get())
    y = int(snake_object.cords[0][1] / space.get())

    i = int(apple_object.cords[0] / space.get())
    j = int(apple_object.cords[1] / space.get())

    a = int(snake_object.cords[-1][0] / space.get())
    b = int(snake_object.cords[-1][1] / space.get())

    head_position = matrix[x][y]
    apple_position = matrix[i][j]
    tail_position = matrix[a][b]
    board_size_n = int(GAME_WIDTH / space.get())
    board_size = board_size_n ** 2

    apple_dist = get_dist(head_position, apple_position)
    tail_dist = get_dist(head_position, tail_position)
    cutting_space = tail_dist - len(snake_object.cords) - 3
    empty_spaces = board_size - len(snake_object.cords)

    global tapsell_bind
    if tapsell_bind.get():
        if empty_spaces < board_size / 2:
            cutting_space = 0
        if apple_dist < tail_dist:
            cutting_space -= (len(snake_object.cords))
            if (tail_dist - apple_dist) * 4 > empty_spaces:
                cutting_space -= 10

    desired_space = apple_dist
    if desired_space < cutting_space:
        cutting_space = desired_space
    if cutting_space < 0:
        cutting_space = 0

    can_go_right = not collision_check((x + 1) * space.get(), y * space.get(), snake_object)
    can_go_left = not collision_check((x - 1) * space.get(), y * space.get(), snake_object)
    can_go_down = not collision_check(x * space.get(), (y + 1) * space.get(), snake_object)
    can_go_up = not collision_check(x * space.get(), (y - 1) * space.get(), snake_object)

    best_dir = 'none'
    best_dist = -1

    if can_go_right and x + 1 < board_size_n:
        dist = get_dist(head_position, matrix[x + 1][y])
        if cutting_space >= dist > best_dist:
            best_dir = 'right'
            best_dist = dist

    if can_go_left and x - 1 > - 1:
        dist = get_dist(head_position, matrix[x - 1][y])
        if cutting_space >= dist > best_dist:
            best_dir = 'left'
            best_dist = dist

    if can_go_down and y + 1 < board_size_n:
        dist = get_dist(head_position, matrix[x][y + 1])
        if cutting_space >= dist > best_dist:
            best_dir = 'down'
            best_dist = dist

    if can_go_up and y - 1 > -1:
        dist = get_dist(head_position, matrix[x][y - 1])
        if cutting_space >= dist > best_dist:
            best_dir = 'up'
            best_dist = dist

    if best_dist >= 0:
        direc = best_dir
        return

    if can_go_up:
        direc = 'up'
        return

    if can_go_left:
        direc = 'left'
        return

    if can_go_down:
        direc = 'down'
        return

    if can_go_right:
        direc = 'right'
        return


def simple_snake_turn(snake_object, matrix):
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
config_widow.geometry('300x340')
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
tapsell_bind = BooleanVar()
Label(config_widow, text='Human, Unoptimized AI, or Optimized AI Player?', font=("Times", 10)).pack()
Radiobutton(config_widow, text="Human", value=0, variable=player_type).pack()
Radiobutton(config_widow, text="Unoptimized", value=1, variable=player_type).pack()
Radiobutton(config_widow, text="Optimized", value=2, variable=player_type).pack()
Checkbutton(config_widow, text="Enable Tapsell's Bind?", variable=tapsell_bind).pack()
tapsell_bind.set(True)

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

else:
    n = int(GAME_WIDTH / space.get())
    maze = prim_maze_gen(int(n / 2))
    cycle = ham_cycle_gen(maze, int(n / 2))
    path = matrix_conv(cycle, n)


snake = Snake()
apple = Apple(snake)
turn_progress(snake, apple)

window.mainloop()
