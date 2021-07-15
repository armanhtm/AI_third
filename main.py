import sys
import turtle

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
temp_matrix = []
# taking 2x2 matrix from the user
for i in range(row_number):
    # taking row input from the user
    row = list(input().split())
    # appending the 'row' to the 'matrix'
    matrix.append(row)
    temp_matrix.append(row)

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
def safe():
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
            if matrix_node[selected.row][col].value == 8:
                return False
        return True
    if not is_row:
        for row in range(row_number):
            if matrix_node[row][selected.col].value == 8:
                return False
        return True


def check_is_complete_half(selected, row_or_col, is_row):
    if is_row:
        for col in range(col_number):
            if col == selected.col:
                if matrix_node[row_or_col][col].value != 8:
                    return False
            else:
                if matrix_node[row_or_col][col].value != matrix_node[selected.row][col].value:
                    return False
        return True

    if not is_row:
        for row in range(row_number):
            if row == selected.row:
                if matrix_node[row][row_or_col].value != 8:
                    return False
            else:
                if matrix_node[row][row_or_col].value != matrix_node[row][selected.col].value:
                    return False
        return True


def second_constraint_propagation(selected, forwardchecking_list):
    # check we have same row or not
    check_row = check_is_complete(selected, True)
    check_col = check_is_complete(selected, False)
    if check_row:
        for row in range(row_number):
            counter_row = 0
            if row != selected.row:
                for col in range(col_number):
                    if matrix_node[row][col].value == matrix_node[selected.row][col].value:
                        counter_row += 1
                    if counter_row == col_number:
                        #print("second_row", row, col)
                        return False
    # check we have same col or not
    if check_col:
        for col in range(col_number):
            counter_col = 0
            if col != selected.col:
                for row in range(row_number):
                    if matrix_node[row][col].value == matrix_node[row][selected.col].value:
                        counter_col += 1
                    if counter_col == row_number:
                        #print("second", row, col)
                        return False

    # forwardchecking for row
    if check_row:
        for row in range(row_number):
            if row != selected.row:
                if check_is_complete_half(selected, row, True):
                    if selected.value in matrix_node[row][selected.col].dom:
                        matrix_node[row][selected.col].remove(selected.value)
                        forwardchecking_list.append(str(row)+","+str(selected.col)+","+selected.value)

    # forwardchecking for row
    if check_col:
        for col in range(col_number):
            if col != selected.col:
                if check_is_complete_half(selected, col, False):
                    if selected.value in matrix_node[selected.row][col].dom:
                        matrix_node[selected.row][col].remove(selected.value)
                        forwardchecking_list.append(str(selected.row) + "," + str(col) + "," + selected.value)

    return True


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

    if not first_constraint_propagation(selected, mac_list_temp):
        list_undo_forward.append(mac_list_temp)
        return False

    if not second_constraint_propagation(selected, mac_list_temp):
        list_undo_forward.append(mac_list_temp)
        return False

    if not third_constraint_propagation(selected, mac_list_temp):
        list_undo_forward.append(mac_list_temp)
        return False

    if not safe():
        list_undo_forward.append(mac_list_temp)
        return False

    dom = selected.dom
    number = selected.value
    selected.value = 8
    while len(mac_list_temp) != 0:
        now_select_string = mac_list_temp.pop()
        split = now_select_string.split(",")
        if split[2] == "False":
            split[2] = '0'
            now_select_string = split[0] + "," + split[1] + "," + split[2]
        if split[2] == "True":
            split[2] = '1'
            now_select_string = split[0] + "," + split[1] + "," + split[2]

        value = int(split[2])
        now_select = matrix_node[int(split[0])][int(split[1])]

        if now_select.value != 8:
            continue
        print("string", now_select_string)
        mac_list.append(now_select_string)
        now_select.value = not value
        if not first_constraint_propagation(now_select, mac_list_temp):
            add_remind_item(mac_list, mac_list_temp)
            now_select.value = 8
            list_undo_forward.append(mac_list)
            return False
        if not second_constraint_propagation(now_select, mac_list_temp):
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
        if not safe():
            add_remind_item(mac_list, mac_list_temp)
            list_undo_forward.append(mac_list)
            selected.dom = dom
            selected.value = number
            return False

    selected.value = number
    selected.dom = dom
    print("mac_list---->", mac_list)
    list_undo_forward.append(mac_list)
    return True


def forwardchecking(selected):
    forwardchecking_list = []
    first_bool = first_constraint_propagation(selected, forwardchecking_list)
    second_bool = second_constraint_propagation(selected, forwardchecking_list)
    third_bool = third_constraint_propagation(selected, forwardchecking_list)

    print("forward checking =>", forwardchecking_list)
    print("second",second_bool)
    list_undo_forward.append(forwardchecking_list)
    if first_bool and third_bool and second_bool:
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


def solve():
    # return false if we have cell with empty domain
    if not safe():
        return False
    # if no empty cell return true
    if finish():
        return True
    # select the cell with mrv or lcv
    selected = selection()

    for num in selected.dom:
        selected.value = num
        print(selected.row, selected.col)
        print("bug--------------------->", matrix_node[0][2].dom)
        termianl_show(selected.row, selected.col)
        print(list_undo_forward)
        #if not forwardchecking(selected):
        if not mac(selected):
            print("ishere")
            selected.value = 8
            undo_forwardchecking()
            continue
        if solve():
            return True

        selected.value = 8
        print("undo*")
        undo_forwardchecking()

    return False


#selected_first = selection()
if not solve():
    print("no way for this puzzle!!!:(")
    end_screen = turtle.Screen()
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(1)
    pen.color("green")
    pen.write("no way to solve this puzzle !!!", align="center", font=("candara", 24, "bold"))
    end_screen.mainloop()
    sys.exit()

for i in range(row_number):
    for j in range(col_number):
        print(matrix_node[i][j].value, end=" ")
    print("\n")


wn = turtle.Screen()
wn.bgcolor("white")


def draw_one(i,j,color):
    one = turtle.Turtle()
    one.color(color)
    one.penup()
    one.goto(-350 + j * (400 / ((row_number - 2) / 2 + 1)),350 - i * (400 / ((row_number - 2) / 2 + 1)))
    one.width(3)
    one.pendown()
    one.right(90)
    one.forward(20)
    one.left(180)
    one.forward(40)
    one.left(135)
    one.forward(15)
    one.hideturtle()


def draw_zero(i,j,color):
    zero = turtle.Turtle()
    zero.color(color)
    zero.penup()
    zero.goto(-350 + j * (400 / ((row_number - 2) / 2 + 1)),350 - i * (400 / ((row_number - 2) / 2 + 1)))
    zero.pendown()
    zero.shape("circle")
    zero.shapesize(2,1.5,3)
    zero.fillcolor("white")


page = turtle.Turtle()
page.speed(10)
page.penup()
first_row = 400


for i in range(row_number - 1):
    first_row -= (400 / ((row_number - 2) / 2 + 1))
    page.goto(-400,first_row)
    page.pendown()
    page.forward(800)
    page.penup()
first_col = -400
page.right(90)


for i in range(col_number - 1):
    first_col += (400 / ((row_number - 2) / 2 + 1))
    page.goto(first_col,400)
    page.pendown()
    page.forward(800)
    page.penup()
page.hideturtle()


for i in range(row_number):
    for j in range(col_number):
        if temp_matrix[i][j] == "8":
            continue
        else:
            if temp_matrix[i][j] == "1":
                draw_one(i,j,"red")
            else:
                draw_zero(i,j,"red")

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(1)
pen.shape("square")
pen.shapesize(0.5)
pen.color("green")
pen.penup()
pen.goto(-550,300)
pen.write("Start filling", align="center", font=("candara", 24, "bold"))
pen.showturtle()


for i in range(80):
    pen.left(5)


for i in range(row_number):
    for j in range(col_number):
        pen.left(10)
        if temp_matrix[i][j] == "1" or temp_matrix[i][j] == "0":
            continue
        if matrix_node[i][j].value == 1:
            draw_one(i,j,"green")
        else:
            draw_zero(i,j,"green")

pen.hideturtle()
pen.clear()
pen.write("it's done", align="center", font=("candara", 24, "bold"))
wn.mainloop()

