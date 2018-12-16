import turtle as t
from copy import deepcopy
import time
import random
# initialize lists of results:
result_label = []
number = []


def lcm(j, k):
    """
    Finding the lowest public times
    :param j: the first number
    :param k: the second number
    :return: the lowest public times
    """
    # obtain the largest number
    if j > k:
        greater = j
    else:
        greater = k

    while True:
        if (greater % j == 0) and (greater % k == 0):
            low_cm = greater
            break
        greater += 1

    return low_cm


def input_validation(prompt, valid_type):
    """
    This is a function designed to check if the input is valid
    :param prompt: String type
    :param valid_type: Type type
    :return: a proper form of input, if invalid, loop until validation is passed
    """
    print('Please enter ' + prompt)
    isPass = False
    result = ''
    while not isPass:
        result = input()
        try:
            result = valid_type(result)
            isPass = True
        except ValueError:
            print("Invalid Input! It's not {}!".format(str(valid_type)))
    if isPass:
        return result


def print_sheet(sheet_list, title):
    """
    Print a list in a specific mode
    :param sheet_list: A list type
    :return: None
    """
    print('\033[1;32;m{}\033[0m'.format(title), end='\n')
    for row in sheet_list:
        for col in row:
            print(col, end='\t')
        print('', end='\n')


def generate_sheet(length, width):
    hash_s = []
    for line_index in range(0, width):
        line = []
        for col_index in range(0, length):
            line.append(0)
        hash_s.append(line)
    return hash_s


# size of wall is m x n
m, n = input_validation('the length of the wall', int), input_validation('the width of the wall', int)
print('The Size of the wall is \033[1;32;m{}x{}\033[0m.'.format(m, n))
# size of brick is a x b
a, b = input_validation('the length of the bricks', int), input_validation('the width of the wall', int)
print('The Size of the brick is \033[1;32;m{}x{}\033[0m.'.format(a, b))

start = time.time()
# generating the hash sheets
hash_sheet = generate_sheet(m, n)
# generating a label sheet as output
label_sheet = generate_sheet(m, n)


def coordinate_matrix_modify(hash_matrix, lx, ly, rx, ry, to_value, check_same=False, check_value=0):
    """
    Made to modify values in matrix(hash_sheets for example)
    :param hash_matrix: a complexed list(type List)
    :param lx: NW corner x coordinate, int type
    :param ly: NW corner y coordinate, int type
    :param rx: SE corner x coordinate, int type
    :param ry: SW corner y coordinate, int type
    :param to_value: The value you want change to
    :param check_same: Default False. If true, will not modify the blocks if it is already the given value_to
    :param check_value: check if the given value is check_value
    :return: Return skip_row, a boolean variable
    """
    rows = range(ly, ry+1)
    cols = range(lx, rx+1)
    skip_row = False
    if check_same:
        for row in rows:
            for col in cols:
                if hash_matrix[row][col] != check_value:
                    skip_row = True
                    break

    if not skip_row:
        for row in rows:
            for col in cols:
                hash_matrix[row][col] = to_value

    return skip_row


def recursion(step, coor_x, coor_y):
    global fill_times
    if step < fill_times:
        for thing in all_mode:
            if not thing['used']:
                isFind = False
                for row in range(coor_y, n):
                    if not isFind:
                        for col in range(0, m):
                            if hash_sheet[row][col] == 0:
                                if (row == 0 or hash_sheet[row - 1][col] == 1) and (col == 0 or hash_sheet[row][col - 1] == 1):
                                    coor_y = row
                                    coor_x = col
                                    isFind = True
                    else:
                        break
                if coor_x == thing['x_l'] and coor_y == thing['y_l']:
                    if not coordinate_matrix_modify(hash_sheet, thing['x_l'], thing['y_l'],
                                                    thing['x_r'], thing['y_r'], 1, check_same=True):
                        coordinate_matrix_modify(label_sheet, thing['x_l'], thing['y_l'],
                                                 thing['x_r'], thing['y_r'], step + 1)
                        thing['used'] = True
                        # recurse the next step
                        recursion(step + 1, coor_x, coor_y)
                        thing['used'] = False
                        # if dont recurse, undo the changes
                        coordinate_matrix_modify(hash_sheet, thing['x_l'], thing['y_l'],
                                                 thing['x_r'], thing['y_r'], 0)
                        coordinate_matrix_modify(label_sheet, thing['x_l'], thing['y_l'],
                                                 thing['x_r'], thing['y_r'], 0)

    elif step == fill_times:
        # print_sheet(hash_sheet, 'Hash check:')
        label = deepcopy(label_sheet)
        result_label.append(label)
        t = time.time()
        global number
        number.append(0)
        print('\rTime {:.2f} s, the {} th'.format(t-start, len(number)), flush=True, end='')


# check if the brick can fill the wall completely
canFill = True
if (m*n) % (a*b) != 0:
    canFill = False
    print('The wall can \033[1;31;mNEVER\033[0m be completely filled by this kind of brick!')

# making series of arrangements of motif blocks that correspond to the shape of brick
# The NW corner is (0,0) and the SE corner is (m-1,n-1)
ll_mode = []
lw_mode = []

for x in range(0, m):
    for y in range(0, n):
        # recursively look at every coordinate
        # set the NW corner of the brick at this coordinate
        # length-length mode:
        ll_dict = {}
        lw_dict = {}
        end_x, end_y = x+a-1, y+b-1
        if end_x < m and end_y < n:
            ll_dict['x_l'] = x
            ll_dict['y_l'] = y
            ll_dict['x_r'] = end_x
            ll_dict['y_r'] = end_y
            ll_dict['used'] = False
            ll_mode.append(ll_dict)
        # length-width mode:
        end_x, end_y = x+b-1, y+a-1
        if end_x < m and end_y < n:
            lw_dict['x_l'] = x
            lw_dict['y_l'] = y
            lw_dict['x_r'] = end_x
            lw_dict['y_r'] = end_y
            lw_dict['used'] = False
            lw_mode.append(lw_dict)
# below print only for test
fill_times = int(m*n/a/b)
# here begin the main analyse and arrangements of the brick
if a == b:
    all_mode = ll_mode
else:
    all_mode = ll_mode+lw_mode
if canFill:
    recursion(0, 0, 0)

end = time.time()
duration = end - start

# converting hash into standard form:
print('\nNow converting results into standard results, please wait')
standard_result = []
s_time = time.time()
for thing in result_label:
    all_brick = []
    while len(all_brick) < m*n/a/b:
        for index in range(1, int(m*n/a/b) + 1):
            brick = []
            while len(brick) < a*b:
                for row in range(0, len(thing)):
                    for col in range(0, len(thing[row])):
                        if thing[row][col] == index:
                            coor = row*len(thing[row]) + col + 1
                            brick.append(coor)
            all_brick.append(brick)
    standard_result.append(all_brick)
    proc = len(standard_result)/len(result_label)
    cur_time = time.time()
    print('\rCurrent process {:.2%}, remaining time {:.2f} s'.format(proc, (cur_time - s_time)/proc*(1-proc)), end='', flush=True)

print('\nThere are {} forms of arrangements'.format(len(result_label)))
print('Time consuming: {:.3}s'.format(duration))
print('All results will be print when the turtle has done all maps(or turtle has been turned off)')
# generating colors in random:
colors = []
for times in range(0, int(m*n/a/b)):
    r, g, l = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    colors.append((r, g, l))
# drawing the rectangle
screen = t.Screen()
a_t = t.Turtle()
a_t.speed(0)
a_t.up()
a_t.goto(0, -300)
a_t.down()
# drawing inner rectangle
width = 500/min(m, n)
a_t.right(90)


if a == b:
    result = result_label[0]
else:
    result = result_label[random.randint(0, len(result_label))]

for row in range(0, len(result)):
    for col in range(0, len(result[row])):
        a_t.up()
        a_t.goto(-300 + col * width, 300 - row * width)
        screen.colormode(255)
        a_t.fillcolor(colors[(result[row][col]) - 1])
        a_t.begin_fill()
        for i in range(0, 4):
            a_t.forward(width)
            a_t.left(90)
        a_t.end_fill()
t.done()
for thing in standard_result:
    print(thing)
