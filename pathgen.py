import random


def prim_maze_gen(n):
    dirs = {}
    vert = n * n

    for i in range(n):
        for j in range(n):
            dirs[j, i] = []

    x = random.randint(0, n - 1)
    y = random.randint(0, n - 1)
    start_point = (x, y)

    curr_point = start_point

    visited = [start_point]

    adj_points = set()

    while len(visited) != vert:
        x_cord = curr_point[0]
        y_cord = curr_point[1]

        if x_cord > 0:
            adj_points.add((x_cord - 1, y_cord))

        if x_cord < n - 1:
            adj_points.add((x_cord + 1, y_cord))

        if y_cord > 0:
            adj_points.add((x_cord, y_cord - 1))

        if y_cord < n - 1:
            adj_points.add((x_cord, y_cord + 1))

        while curr_point:
            curr_point = (adj_points.pop())

            if curr_point not in visited:
                visited.append(curr_point)
                x = curr_point[0]
                y = curr_point[1]

                if (x + 1, y) in visited:
                    dirs[x, y] += ['right']
                elif (x - 1, y) in visited:
                    dirs[x - 1, y] += ['right']
                elif (x, y + 1) in visited:
                    dirs[x, y] += ['down']
                elif (x, y - 1) in visited:
                    dirs[x, y - 1] += ['down']

                break
    return dirs


def ham_cycle_gen(dirs, n):
    ham_cycle = dict()

    for i in range(n):
        for j in range(n):
            cycle_x = j * 2
            cycle_y = i * 2

            if j != n - 1 and i != n - 1 and j != 0 and i != 0:
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    if (cycle_x + 1, cycle_y + 1) in ham_cycle:
                        ham_cycle[cycle_x + 1, cycle_y + 1] += [(cycle_x + 1, cycle_y + 2)]
                    else:
                        ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                if 'right' not in dirs[j - 1, i]:
                    if (cycle_x, cycle_y) in ham_cycle:
                        ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]
                    else:
                        ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]

            elif j == n - 1 and i == n - 1:
                ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                elif 'right' not in dirs[j - 1, i]:
                    ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]

            elif j == n - 1 and i == 0:
                ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'right' not in dirs[j - 1, i]:
                    ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]

            elif j == n - 1:
                ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                if 'right' not in dirs[j - 1, i]:
                    if (cycle_x, cycle_y) in ham_cycle:
                        ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]
                    else:
                        ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]

            elif j == 0 and i == 0:
                ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    if (cycle_x + 1, cycle_y + 1) in ham_cycle:
                        ham_cycle[cycle_x + 1, cycle_y + 1] += [(cycle_x + 1, cycle_y + 2)]
                    else:
                        ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]

            elif j == 0 and i == n - 1:
                ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]
                ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] += [(cycle_x + 1, cycle_y)]

            elif j == 0:
                ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    if (cycle_x + 1, cycle_y + 1) in ham_cycle:
                        ham_cycle[cycle_x + 1, cycle_y + 1] += [(cycle_x + 1, cycle_y + 2)]
                    else:
                        ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] += [(cycle_x + 1, cycle_y)]

            elif i == 0:
                ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' in dirs[j, i]:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x, cycle_y + 2)]
                    if (cycle_x + 1, cycle_y + 1) in ham_cycle:
                        ham_cycle[cycle_x + 1, cycle_y + 1] += [(cycle_x + 1, cycle_y + 2)]
                    else:
                        ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 1, cycle_y + 2)]
                else:
                    ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'right' not in dirs[j - 1, i]:
                    ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]

            else:
                ham_cycle[cycle_x, cycle_y + 1] = [(cycle_x + 1, cycle_y + 1)]
                if 'right' in dirs[j, i]:
                    ham_cycle[cycle_x + 1, cycle_y + 1] = [(cycle_x + 2, cycle_y + 1)]
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 2, cycle_y)]
                else:
                    ham_cycle[cycle_x + 1, cycle_y] = [(cycle_x + 1, cycle_y + 1)]
                if 'down' not in dirs[j, i - 1]:
                    ham_cycle[cycle_x, cycle_y] = [(cycle_x + 1, cycle_y)]
                if 'right' not in dirs[j - 1, i]:
                    if (cycle_x, cycle_y) in ham_cycle:
                        ham_cycle[cycle_x, cycle_y] += [(cycle_x, cycle_y + 1)]
                    else:
                        ham_cycle[cycle_x, cycle_y] = [(cycle_x, cycle_y + 1)]
    return ham_cycle


def matrix_conv(cycle, n):
    path = [(0, 0)]
    prev = path[0]
    prev_dir = None
    size = n ** 2

    while len(path) != size:
        if prev in cycle and (prev[0] + 1, prev[1]) in cycle[prev] and prev_dir != 'left':
            prev = (prev[0] + 1, prev[1])
            path.append(prev)
            prev_dir = 'right'

        elif prev in cycle and (prev[0], prev[1] + 1) in cycle[prev] and prev_dir != 'up':
            prev = (prev[0], prev[1] + 1)
            path.append(prev)
            prev_dir = 'down'

        elif (prev[0] - 1, prev[1]) in cycle and prev in cycle[prev[0] - 1, prev[1]] and prev_dir != 'right':
            prev = (prev[0] - 1, prev[1])
            path.append(prev)
            prev_dir = 'left'

        else:
            prev = (prev[0], prev[1] - 1)
            path.append(prev)
            prev_dir = 'up'

    matrix_path = []
    array = []
    for x in range(n):
        for y in range(n):
            array.append(0)
        matrix_path.append(array)
        array = []

    i = 0
    for cords in path:
        matrix_path[cords[1]][cords[0]] = i
        i += 1
    return matrix_path
