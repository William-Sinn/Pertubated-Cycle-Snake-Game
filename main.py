from tkinter import *
from time import sleep
import random

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


def generate_path(n):
    matrix = []
    array = []
    for i in range(n):
        for j in range(n):
            array.append(i * n + j)
        matrix.append(array)
        array = []
    return matrix


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
    path = [
        [899, 0, 1, 2, 3, 4, 17, 18, 159, 160, 161, 162, 163, 164, 165, 166, 171, 172, 177, 178, 179, 180, 181, 182,
         183, 184, 185, 186, 187, 188
         ],
        [898, 9, 8, 7, 6, 5, 16, 19, 158, 153, 152, 151, 150, 149, 148, 167, 170, 173, 176, 231, 230, 229, 228, 215,
         214, 213, 212, 195, 194, 189
         ],
        [897, 10, 11, 12, 13, 14, 15, 20, 157, 154, 143, 144, 145, 146, 147, 168, 169, 174, 175, 232, 233, 234, 227,
         216, 217, 218, 211, 196, 193, 190
         ],
        [896, 879, 878, 873, 872, 23, 22, 21, 156, 155, 142, 137, 136, 131, 130, 125, 124, 123, 122, 237, 236, 235, 226,
         225, 224, 219, 210, 197, 192, 191
         ],
        [895, 880, 877, 874, 871, 24, 25, 26, 27, 28, 141, 138, 135, 132, 129, 126, 119, 120, 121, 238, 243, 244, 245,
         246, 223, 220, 209, 198, 199, 200
         ],
        [894, 881, 876, 875, 870, 37, 36, 31, 30, 29, 140, 139, 134, 133, 128, 127, 118, 117, 116, 239, 242, 257, 256,
         247, 222, 221, 208, 203, 202, 201
         ],
        [893, 882, 883, 884, 869, 38, 35, 32, 49, 50, 51, 52, 53, 54, 111, 112, 113, 114, 115, 240, 241, 258, 255, 248,
         313, 314, 207, 204, 321, 322
         ],
        [892, 887, 886, 885, 868, 39, 34, 33, 48, 47, 46, 61, 60, 55, 110, 105, 104, 103, 102, 261, 260, 259, 254, 249,
         312, 315, 206, 205, 320, 323
         ],
        [891, 888, 865, 866, 867, 40, 41, 42, 43, 44, 45, 62, 59, 56, 109, 106, 99, 100, 101, 262, 263, 264, 253, 250,
         311, 316, 317, 318, 319, 324
         ],
        [890, 889, 864, 859, 858, 757, 756, 755, 754, 753, 752, 63, 58, 57, 108, 107, 98, 93, 92, 267, 266, 265, 252,
         251, 310, 305, 304, 327, 326, 325
         ],
        [849, 850, 863, 860, 857, 758, 763, 764, 769, 770, 751, 64, 65, 66, 83, 84, 97, 94, 91, 268, 285, 286, 287, 288,
         309, 306, 303, 328, 333, 334
         ],
        [848, 851, 862, 861, 856, 759, 762, 765, 768, 771, 750, 745, 744, 67, 82, 85, 96, 95, 90, 269, 284, 283, 282,
         289, 308, 307, 302, 329, 332, 335
         ],
        [847, 852, 853, 854, 855, 760, 761, 766, 767, 772, 749, 746, 743, 68, 81, 86, 87, 88, 89, 270, 271, 272, 281,
         290, 291, 292, 301, 330, 331, 336
         ],
        [846, 833, 832, 831, 830, 777, 776, 775, 774, 773, 748, 747, 742, 69, 80, 79, 78, 77, 76, 275, 274, 273, 280,
         295, 294, 293, 300, 339, 338, 337
         ],
        [845, 834, 827, 828, 829, 778, 779, 780, 781, 782, 739, 740, 741, 70, 71, 72, 73, 74, 75, 276, 277, 278, 279,
         296, 297, 298, 299, 340, 341, 342
         ],
        [844, 835, 826, 825, 824, 791, 790, 789, 788, 783, 738, 733, 732, 731, 730, 513, 512, 511, 510, 501, 500, 499,
         498, 493, 492, 491, 490, 349, 348, 343
         ],
        [843, 836, 837, 838, 823, 792, 797, 798, 787, 784, 737, 734, 727, 728, 729, 514, 515, 516, 509, 502, 503, 504,
         497, 494, 487, 488, 489, 350, 347, 344
         ],
        [842, 841, 840, 839, 822, 793, 796, 799, 786, 785, 736, 735, 726, 721, 720, 523, 522, 517, 508, 507, 506, 505,
         496, 495, 486, 485, 484, 351, 346, 345
         ],
        [633, 634, 819, 820, 821, 794, 795, 800, 801, 802, 687, 688, 725, 722, 719, 524, 521, 518, 539, 540, 473, 474,
         475, 476, 477, 478, 483, 352, 353, 354
         ],
        [632, 635, 818, 817, 816, 807, 806, 805, 804, 803, 686, 689, 724, 723, 718, 525, 520, 519, 538, 541, 472, 471,
         470, 465, 464, 479, 482, 357, 356, 355
         ],
        [631, 636, 637, 638, 815, 808, 809, 810, 679, 680, 685, 690, 711, 712, 717, 526, 527, 528, 537, 542, 451, 452,
         469, 466, 463, 480, 481, 358, 367, 368
         ],
        [630, 629, 628, 639, 814, 813, 812, 811, 678, 681, 684, 691, 710, 713, 716, 531, 530, 529, 536, 543, 450, 453,
         468, 467, 462, 461, 460, 359, 366, 369
         ],
        [625, 626, 627, 640, 641, 642, 675, 676, 677, 682, 683, 692, 709, 714, 715, 532, 533, 534, 535, 544, 449, 454,
         455, 456, 457, 458, 459, 360, 365, 370
         ],
        [624, 619, 618, 645, 644, 643, 674, 673, 672, 667, 666, 693, 708, 707, 706, 549, 548, 547, 546, 545, 448, 447,
         446, 433, 432, 431, 430, 361, 364, 371
         ],
        [623, 620, 617, 646, 647, 648, 657, 658, 671, 668, 665, 694, 699, 700, 705, 550, 551, 552, 553, 554, 443, 444,
         445, 434, 427, 428, 429, 362, 363, 372
         ],
        [622, 621, 616, 651, 650, 649, 656, 659, 670, 669, 664, 695, 698, 701, 704, 559, 558, 557, 556, 555, 442, 437,
         436, 435, 426, 421, 420, 379, 378, 373
         ],
        [613, 614, 615, 652, 653, 654, 655, 660, 661, 662, 663, 696, 697, 702, 703, 560, 401, 402, 403, 404, 441, 438,
         411, 412, 425, 422, 419, 380, 377, 374
         ],
        [612, 611, 610, 601, 600, 587, 586, 585, 584, 583, 582, 577, 576, 571, 570, 561, 400, 399, 398, 405, 440, 439,
         410, 413, 424, 423, 418, 381, 376, 375
         ],
        [607, 608, 609, 602, 599, 588, 589, 590, 591, 592, 581, 578, 575, 572, 569, 562, 563, 564, 397, 406, 407, 408,
         409, 414, 415, 416, 417, 382, 383, 384
         ],
        [606, 605, 604, 603, 598, 597, 596, 595, 594, 593, 580, 579, 574, 573, 568, 567, 566, 565, 396, 395, 394, 393,
         392, 391, 390, 389, 388, 387, 386, 385
         ]
    ]

snake = Snake()
apple = Apple(snake)
turn_progress(snake, apple)

window.mainloop()
