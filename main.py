import numpy as np


class Node:
    def __init__(self, row, col, value):
        self.row = int(row)
        self.col = int(col)
        self.dom = []
        self.dom.append(int(0))
        self.dom.append(int(1))
        self.value = int(value)


# get row and column of matrix
row_number, col_number = map(int, input().split())

# initializing an empty matrix
matrix = []
# taking 2x2 matrix from the user
for i in range(row_number):
    # taking row input from the user
    row = list(input().split())
    # appending the 'row' to the 'matrix'
    matrix.append(row)

# create 2d matrix for every node
matrix_node = [[0 for i in range(row_number)] for i in range(col_number)]
# initializing matrix_node
for i in range(row_number):
    for j in range(col_number):
        if matrix[i][j] == '-':
            matrix[i][j] = '8'
        matrix_node[i][j] = Node(i, j, int(matrix[i][j]))


# this method check that process finished or not
def finish():
    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].value == 8:
                return False
    return True


# this method check that we in safe position or not
def safe(selected):
    # this method check that last forwardchecking was safe or not
    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].value == 8 and len(matrix_node[i][j].dom) == 0:
                print("false=====", i, j)
                return False

    # check constraint 1
    # if not check_constraint_safe(selected):
    #   return False
    return True


# this method select the cell with mrv algorithm
def selection():
    for i in range(row_number):
        for j in range(col_number):
            if len(matrix_node[i][j].dom) == 1 and matrix_node[i][j].value == 8:
                return matrix_node[i][j]

    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].value == 8:
                return matrix_node[i][j]


# this method constraint propagation of first limitation
def first_constraint_propagation(selected, forwardchecking_list):
    zero_number_row = 0
    zero_number_col = 0
    one_number_row = 0
    one_number_col = 0
    for row_index in range(row_number):
        if matrix_node[row_index][selected.col].value == 0:
            zero_number_row += 1
        if matrix_node[row_index][selected.col].value == 1:
            one_number_row += 1
    for col_index in range(col_number):
        if matrix_node[selected.row][col_index].value == 0:
            zero_number_col += 1
        if matrix_node[selected.row][col_index].value == 1:
            one_number_col += 1

    if 2 * zero_number_col > col_number:
        return False
    if 2 * one_number_col > col_number:
        return False
    if 2 * zero_number_row > row_number:
        return False
    if 2 * one_number_row > row_number:
        return False
    if 2 * zero_number_col == col_number:
        for col_index in range(col_number):
            if matrix_node[selected.row][col_index].value == 8 and (0 in matrix_node[selected.row][col_index].dom):
                matrix_node[selected.row][col_index].dom.remove(0)
                forwardchecking_list.append(str(selected.row) + "," + str(col_index) + "," + str(0))

    if 2 * one_number_col == col_number:
        for col_index in range(col_number):
            if matrix_node[selected.row][col_index].value == 8 and (1 in matrix_node[selected.row][col_index].dom):
                matrix_node[selected.row][col_index].dom.remove(1)
                forwardchecking_list.append(str(selected.row) + "," + str(col_index) + "," + str(1))

    if 2 * zero_number_row == row_number:
        for row_index in range(row_number):
            if matrix_node[row_index][selected.col].value == 8 and (0 in matrix_node[row_index][selected.col].dom):
                matrix_node[row_index][selected.col].dom.remove(0)
                forwardchecking_list.append(str(row_index) + "," + str(selected.col) + "," + str(0))

    if 2 * one_number_row == row_number:
        for row_index in range(row_number):
            if matrix_node[row_index][selected.col].value == 8 and (1 in matrix_node[row_index][selected.col].dom):
                matrix_node[row_index][selected.col].dom.remove(1)
                forwardchecking_list.append(str(row_index) + "," + str(selected.col) + "," + str(1))

    return True


def check_is_complete(selected, is_row):
    if is_row:
        for col in range(col_number):
            if matrix_node[selected.row][col] == 8:
                return False
        return True
    else:
        for row in range(row_number):
            if matrix_node[row][selected.col] == 8:
                return False
        return True


#def second_constraint_propagation(selected, forwardchecking_list):
   # if check_is_complete(selected, True):
    #    for i in range(row_number):
     #       if i != selected.row:
      #          if (np_matrix[selected.row] == np_matrix[i]).all():
       #             return False


def third_constraint_propagation(selected, forwardchecking_list):
    # check row left
    if selected.row - 1 in range(row_number):
        if matrix_node[selected.row - 1][selected.col].value == selected.value:
            if selected.row - 2 in range(row_number):
                if matrix_node[selected.row - 2][selected.col].value == selected.value:
                    return False

    # check row right
    if selected.row + 1 in range(row_number):
        if matrix_node[selected.row + 1][selected.col].value == selected.value:
            if selected.row + 2 in range(row_number):
                if matrix_node[selected.row + 2][selected.col].value == selected.value:
                    return False

    # check col down
    if selected.col - 1 in range(col_number):
        if matrix_node[selected.row][selected.col - 1].value == selected.value:
            if selected.col - 2 in range(col_number):
                if matrix_node[selected.row][selected.col - 2].value == selected.value:
                    return False

    # check col up
    if selected.col + 1 in range(col_number):
        if matrix_node[selected.row][selected.col + 1].value == selected.value:
            if selected.col + 2 in range(col_number):
                if matrix_node[selected.row][selected.col + 2].value == selected.value:
                    return False

    # check row mid
    if selected.row - 1 in range(row_number) and selected.row + 1 in range(row_number):
        if matrix_node[selected.row - 1][selected.col].value == selected.value and matrix_node[selected.row + 1][
            selected.col].value == selected.value:
            return False

    # check col mid
    if selected.col - 1 in range(col_number) and selected.col + 1 in range(col_number):
        if matrix_node[selected.row][selected.col - 1].value == selected.value and matrix_node[selected.row][
            selected.col + 1].value == selected.value:
            return False

    # check row left
    if selected.row - 1 in range(row_number):
        if matrix_node[selected.row - 1][selected.col].value == selected.value:
            if selected.row + 1 in range(row_number) and selected.value in matrix_node[selected.row + 1][
                selected.col].dom:
                matrix_node[selected.row + 1][selected.col].dom.remove(selected.value)
                forwardchecking_list.append(
                    str(selected.row + 1) + "," + str(selected.col) + "," + str(selected.value))
            if selected.row - 2 in range(row_number):
                if matrix_node[selected.row - 2][selected.col].value == 8 and selected.value in \
                        matrix_node[selected.row - 2][selected.col].dom:
                    matrix_node[selected.row - 2][selected.col].dom.remove(selected.value)
                    forwardchecking_list.append(
                        str(selected.row - 2) + "," + str(selected.col) + "," + str(selected.value))

    # check row right
    if selected.row + 1 in range(row_number):
        if matrix_node[selected.row + 1][selected.col].value == selected.value:
            if selected.row - 1 in range(row_number) and selected.value in matrix_node[selected.row - 1][
                selected.col].dom:
                matrix_node[selected.row - 1][selected.col].dom.remove(selected.value)
                forwardchecking_list.append(
                    str(selected.row - 1) + "," + str(selected.col) + "," + str(selected.value))
            if selected.row + 2 in range(row_number):
                if matrix_node[selected.row + 2][selected.col].value == 8 and selected.value in \
                        matrix_node[selected.row + 2][selected.col].dom:
                    matrix_node[selected.row + 2][selected.col].dom.remove(selected.value)
                    forwardchecking_list.append(
                        str(selected.row + 2) + "," + str(selected.col) + "," + str(selected.value))

    # check col down
    if selected.col - 1 in range(col_number):
        if matrix_node[selected.row][selected.col - 1].value == selected.value:
            if selected.col + 1 in range(col_number) and selected.value in matrix_node[selected.row][
                selected.col + 1].dom:
                matrix_node[selected.row][selected.col + 1].dom.remove(selected.value)
                forwardchecking_list.append(
                    str(selected.row) + "," + str(selected.col + 1) + "," + str(selected.value))
            if selected.col - 2 in range(col_number):
                if matrix_node[selected.row][selected.col - 2].value == 8 and selected.value in \
                        matrix_node[selected.row][selected.col - 2].dom:
                    matrix_node[selected.row][selected.col - 2].dom.remove(selected.value)
                    forwardchecking_list.append(
                        str(selected.row) + "," + str(selected.col - 2) + "," + str(selected.value))

    # check col up
    if selected.col + 1 in range(col_number):
        if matrix_node[selected.row][selected.col + 1].value == selected.value:
            if selected.col - 1 in range(col_number) and selected.value in matrix_node[selected.row][
                selected.col - 1].dom:
                matrix_node[selected.row][selected.col - 1].dom.remove(selected.value)
                forwardchecking_list.append(
                    str(selected.row) + "," + str(selected.col - 1) + "," + str(selected.value))
            if selected.col + 2 in range(col_number):
                if matrix_node[selected.row][selected.col + 2].value == 8 and selected.value in \
                        matrix_node[selected.row][selected.col + 2].dom:
                    matrix_node[selected.row][selected.col + 2].dom.remove(selected.value)
                    forwardchecking_list.append(
                        str(selected.row) + "," + str(selected.col + 2) + "," + str(selected.value))

    # check mid row left
    if selected.row - 2 in range(row_number):
        if matrix_node[selected.row - 2][selected.col] == selected.value:
            matrix_node[selected.row - 1][selected.col].dom.remove(selected.value)
            forwardchecking_list.append(
                str(selected.row - 1) + "," + str(selected.col) + "," + str(selected.value))

    # check mid row right
    if selected.row + 2 in range(row_number):
        if matrix_node[selected.row + 2][selected.col] == selected.value:
            matrix_node[selected.row + 1][selected.col].dom.remove(selected.value)
            forwardchecking_list.append(
                str(selected.row + 1) + "," + str(selected.col) + "," + str(selected.value))

    # check mid col down
    if selected.col - 2 in range(col_number):
        if matrix_node[selected.row][selected.col - 2] == selected.value:
            matrix_node[selected.row][selected.col - 1].dom.remove(selected.value)
            forwardchecking_list.append(
                str(selected.row) + "," + str(selected.col - 1) + "," + str(selected.value))

    # check mid col up
    if selected.col + 2 in range(col_number):
        if matrix_node[selected.row][selected.col + 2] == selected.value:
            matrix_node[selected.row][selected.col + 1].dom.remove(selected.value)
            forwardchecking_list.append(
                str(selected.row) + "," + str(selected.col + 1) + "," + str(selected.value))

    return True


def add_remind_item(mac_list, mac_list_temp):
    for item in mac_list_temp:
        mac_list.append(item)

def mac(selected):
    mac_list = []
    mac_list_temp = []

    if not first_constraint_propagation(selected,mac_list_temp):
        list_undo_forward.append(mac_list_temp)
        return False

    if not third_constraint_propagation(selected,mac_list_temp):
        list_undo_forward.append(mac_list_temp)
        return False

    while len(mac_list_temp) != 0:
        now_select_string = mac_list_temp.pop()
        split = now_select_string.split(",")
        if split[2] == "False":
            split[2] = '0'
            now_select_string = split[0]+","+split[1]+","+split[2]
        if split[2] == "True":
            split[2] = '1'
            now_select_string = split[0] + "," + split[1] + "," + split[2]
        mac_list.append(now_select_string)
        print("string", now_select_string)
        value = int(split[2])
        now_select = matrix_node[int(split[0])][int(split[1])]
        now_select.value = not value
        if not first_constraint_propagation(now_select, mac_list_temp):
            add_remind_item(mac_list, mac_list_temp)
            now_select.value = 8
            list_undo_forward.append(mac_list)
            return False
        if not third_constraint_propagation(now_select, mac_list_temp):
            add_remind_item(mac_list, mac_list_temp)
            now_select.value = 8
            list_undo_forward.append(mac_list)
            return False

        now_select.value = 8

    print("mac_list---->", mac_list)
    list_undo_forward.append(mac_list)
    return True


def forwardchecking(selected):
    forwardchecking_list = []
    first_bool = first_constraint_propagation(selected, forwardchecking_list)
    #second_bool = second_constraint_propagation(selected, forwardchecking_list)
    third_bool = third_constraint_propagation(selected, forwardchecking_list)

    print("forward checking =>", forwardchecking_list)
    #print(second_bool)
    list_undo_forward.append(forwardchecking_list)
    if first_bool and third_bool :
        return True
    else:
        return False


list_undo_forward = []


def undo_forwardchecking():
    undo = list_undo_forward.pop()
    print(len(list_undo_forward))
    print(list_undo_forward)
    for item in undo:
        split = item.split(",")
        row_split = int(split[0])
        col_split = int(split[1])
        if split[2] == "False":
            split[2] = '0'
        if split[2] == "True":
            split[2] = '1'
        value = int(split[2])
        matrix_node[row_split][col_split].dom.append(value)
        print("undo----------------->", row_split, col_split, "///", value)
    # list_undo_forward.remove(undo)


def termianl_show(row, col):
    print("amir---->", row, col)
    for i in range(row_number):
        for j in range(col_number):
            if row == i and col == j:
                print('\033[92m' + str(matrix_node[i][j].value) + '\033[0m', end=" ")
            else:
                print(matrix_node[i][j].value, end=" ")
        print('\n')
    print('*****************************************************')


def solve(selected_input):
    # return false if we have cell with empty domain
    if not safe(selected_input):
        return False
    # if no empty cell return true
    if finish():
        return True
    # select the cell with mrv or lcv
    selected = selection()

    for num in selected.dom:
        selected.value = num
        print(selected.row, selected.col)
        print("bug--------------------->",  matrix_node[3][2].dom)
        termianl_show(selected.row, selected.col)
        print(list_undo_forward)
        #if not forwardchecking(selected):
        if not mac(selected):
            print("ishere")
            selected.value = 8
            undo_forwardchecking()
            continue
        if solve(selected):
            return True

        selected.value = 8
        print("undo*")
        undo_forwardchecking()

    return False


selected_first = selection()
solve(selected_first)

for i in range(row_number):
    for j in range(col_number):
        print(matrix_node[i][j].value, end=" ")
    print("\n")
