import turtle as t
from copy import deepcopy
import time
# initialize lists of results:
result_label = []
result_position = []
result_position_1 = []
result_position_2 = []
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

if a == b:
    rectangle = True
start = time.time()
# generating the hash sheets
hash_sheet = generate_sheet(m, n)
# below just for testing
# print_sheet(hash_sheet, 'Hash sheet of the wall:')
hash_1 = generate_sheet(m, n)
hash_2 = generate_sheet(m, n)
# generating a label sheet as output
label_sheet = generate_sheet(m, n)
# generating position pointers
position_sheet = generate_sheet(m, n)
position_1 = generate_sheet(m, n)
position_2 = generate_sheet(m, n)


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


def recursion(step):
    global fill_times
    if step < fill_times:
        new_mode = [x for x in all_mode if x['status'] is False]
        for thing in new_mode:
            edge_left = False
            edge_right = False
            if thing['x_l'] == 0 or hash_sheet[thing['y_l']][thing['x_l']-1] == 1:
                edge_left = True
            if thing['y_l'] == 0 or hash_sheet[thing['y_l']-1][thing['x_l']] == 1:
                edge_right = True
            if edge_right and edge_left:
                isSkip = coordinate_matrix_modify(hash_sheet, thing['x_l'], thing['y_l'],
                                                  thing['x_r'], thing['y_r'], 1, check_same=True)
                if not isSkip:
                    coordinate_matrix_modify(label_sheet, thing['x_l'], thing['y_l'],
                                             thing['x_r'], thing['y_r'], step + 1)
                    # print_sheet(label_sheet, 'Label sheet')
                    coordinate_matrix_modify(position_sheet, thing['x_l'], thing['y_l'],
                                             thing['x_l'], thing['y_l'], 1)
                    if thing['dirc'] == 1:
                        coordinate_matrix_modify(position_1, thing['x_l'], thing['y_l'],
                                                 thing['x_l'], thing['y_l'], 1)
                    if thing['dirc'] == 2:
                        coordinate_matrix_modify(position_2, thing['x_l'], thing['y_l'],
                                                 thing['x_l'], thing['y_l'], 1)
                    # Checking is current hash can be modified
                    suspend_1 = False
                    suspend_2 = False
                    """
                    if len(result_position_1) != 0:
                        for result in result_position_1:
                            for row in range(0, len(hash_1)):
                                for col in range(0, len(hash_1[row])):
                                    hash_1[row][col] = result[row][col] - position_1[row][col]
                            for row in hash_1:
                                for col in row:
                                    if col < 0:
                                        suspend_1 = True
                                        break
                    if len(result_position_2) != 0:
                        for result in result_position_2:
                            for row in range(0, len(hash_1)):
                                for col in range(0, len(hash_1[row])):
                                    hash_2[row][col] = result[row][col] - position_2[row][col]
                            for row in hash_2:
                                for col in row:
                                    if col < 0:
                                        suspend_2 = True
                                        break
                    """
                    if not (suspend_1 and suspend_2):
                        thing['status'] = True
                        recursion(step + 1)
                    # if dont recurse, undo the changes
                    coordinate_matrix_modify(hash_sheet, thing['x_l'], thing['y_l'],
                                             thing['x_r'], thing['y_r'], 0)
                    coordinate_matrix_modify(position_sheet, thing['x_l'], thing['y_l'],
                                             thing['x_l'], thing['y_l'], 0)
                    if thing['dirc'] == 1:
                        coordinate_matrix_modify(position_1, thing['x_l'], thing['y_l'],
                                                 thing['x_l'], thing['y_l'], 0)
                    if thing['dirc'] == 2:
                        coordinate_matrix_modify(position_2, thing['x_l'], thing['y_l'],
                                                 thing['x_l'], thing['y_l'], 0)
                    coordinate_matrix_modify(label_sheet, thing['x_l'], thing['y_l'],
                                             thing['x_r'], thing['y_r'], 0)
                    thing['status'] = False

    elif step == fill_times:
        # print_sheet(hash_sheet, 'Hash check:')
        label = deepcopy(label_sheet)
        result_label.append(label)
        position = deepcopy(position_sheet)
        pos_1 = deepcopy(position_1)
        pos_2 = deepcopy(position_2)
        result_position.append(position)
        result_position_1.append(pos_1)
        result_position_2.append(pos_2)
        t = time.time()
        global number
        number.append(1)
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
            ll_dict['status'] = False
            ll_dict['dirc'] = 1
            ll_mode.append(ll_dict)
        # length-width mode:
        end_x, end_y = x+b-1, y+a-1
        if end_x < m and end_y < n:
            lw_dict['x_l'] = x
            lw_dict['y_l'] = y
            lw_dict['x_r'] = end_x
            lw_dict['y_r'] = end_y
            lw_dict['status'] = False
            lw_dict['dirc'] = 2
            lw_mode.append(lw_dict)
# below print only for test
# print('All possible arrangements:')
# print(ll_mode, len(ll_mode), lw_mode, len(lw_mode), sep='\n')
fill_times = int(m*n/a/b)
# here begin the main analyse and arrangements of the brick
all_mode = ll_mode+lw_mode
if canFill:
    recursion(0)
"""
# only for testing
for thing in result_label:
    print_sheet(thing, "Label Diagram:")
for thing in result_position:
    print_sheet(thing, "Position Diagram:")
"""
# check if they are the same
out_label = []
out_position = []

for thing in result_position:
    if thing not in out_position:
        ind = result_position.index(thing)
        out_position.append(thing)
        out_label.append(result_label[ind])

for thing in out_label:
    print_sheet(thing, 'Final Result')
end = time.time()
duration = end - start
print('There are {} forms of arrangements'.format(len(out_label)))
print('Time consuming: {:.3}s'.format(duration))
print('Times that recurse: {}'.format(len(number)))

print("Standardized form of output:")
# converting hash into standard form:
for num in range(0, len(out_label)):
    all_brick = []
    while len(all_brick) < m*n/a/b:
        for index in range(0, int(m*n/a/b)):
            brick = []
            while len(brick) < a*b:
                for row in range(0, len(out_label[num])):
                    for col in range(0, len(out_label[num][row])):
                        if out_label[num][row][col] == index:
                            coor = row*len(out_label[num][row]) + col + 1
                            brick.append(coor)
            all_brick.append(brick)
            print(brick)
    print(all_brick)

# drawing the rectangle
screen = t.Screen()
a_t = t.Turtle()
a_t.up()
a_t.goto(0, -300)
a_t.down()
for i in range(0, 4):
    a_t.forward(300)
    a_t.left(90)
    a_t.forward(300)
# drawing inner rectangle

t.done()
