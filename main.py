class Node:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.dom = [0, 1]
        self.dom_num = 2
        self.value = value


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
        matrix_node[i][j] = Node(i, j, matrix[i][j])


# this method check that process finished or not
def finish():
    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].value == "_":
                return False
    return True


# this method check that last forwardchecking was safe or not
def safe():
    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].dom_num <= 0:
                return False
    return True


# this method select the cell with mrv algorithm
def selection():
    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].dom_num == 1:
                return matrix_node[i][j]

    for i in range(row_number):
        for j in range(col_number):
            if matrix_node[i][j].value == "_":
                return matrix_node[i][j]


# this method constraint propagation of first limitation
def first_constraint_propagation(selected):
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

    if 2*zero_number_col == col_number:
        for col_index in range(col_number):
            if matrix_node[selected.row][col_index].value == "_":
                matrix_node[selected.row][col_index].dom.remove(0)

    if 2 * one_number_col == col_number:
        for col_index in range(col_number):
            if matrix_node[selected.row][col_index].value == "_":
                matrix_node[selected.row][col_index].dom.remove(1)

    if 2 * zero_number_row == row_number:
        for row_index in range(row_number):
            if matrix_node[row_index][selected.col].value == "_":
                matrix_node[row_index][selected.col].dom.remove(0)

    if 2 * one_number_row == row_number:
        for row_index in range(row_number):
            if matrix_node[row_index][selected.col].value == "_":
                matrix_node[row_index][selected.col].dom.remove(1)


def second_constraint_propagation(selected):
    pass


def third_constraint_propagation(selected):
    pass


def forwardchecking(selected):
    first_constraint_propagation(selected)
    #second_constraint_propagation(selected)
    #third_constraint_propagation(selected)


def undo_forwardchecking():
    pass


def solve():
    # if no empty cell return true
    if finish():
        return True
    # return false if we have cell with empty domain
    if not safe():
        return False
    # select the cell with mrv or lcv
    selected = selection()

    for num in range(2):
        if (num in selected.dom):
            selected.value = num

        forwardchecking(selected)

        if solve():
            return True

        selected.value = "_"
        #undo_forwardchecking()

    return False
solve()
for i in range(row_number):
    for j in range(col_number):
        print( matrix_node[i][j].value,end=" ")
    print("\n")