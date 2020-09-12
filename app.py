import math

POSIBLE_VALUES = list(range(1,10))
SIZE_POSIBLE_VALUES = len(POSIBLE_VALUES)
DEFAULT_VALUE = 'x'
MENU_SPACING = 50

matrix = []
quadrants = {
    '1': {'column': 0, 'row': 0},
    '2': {'column': 3, 'row': 0},
    '3': {'column': 6, 'row': 0},
    '4': {'column': 0, 'row': 3},
    '5': {'column': 3, 'row': 3},
    '6': {'column': 6, 'row': 3},
    '7': {'column': 0, 'row': 6},
    '8': {'column': 3, 'row': 6},
    '9': {'column': 6, 'row': 6}
}

def define_quadrants():
    count = 1
    number_quadrants = math.sqrt(len(POSIBLE_VALUES))

    for row in range(len(POSIBLE_VALUES)):
        for column in range(len(POSIBLE_VALUES)):
            quadrants[{}.format(count)] = {
                column
            }
    pass

def start_matrix():
    """
    for row in range(SIZE_POSIBLE_VALUES):
        matrix.append([])
        for column in range(SIZE_POSIBLE_VALUES):
            matrix[row].append(DEFAULT_VALUE)
            """
    test_matriz()


def test_matriz():
    matrix.append([0, 0, 0, 0, 8, 0, 0, 0, 0]);
    matrix.append([3, 0, 0, 0, 0, 0, 6, 0, 0]);
    matrix.append([5, 0, 0, 4, 2, 0, 0, 0, 0]);
    matrix.append([9, 0, 0, 0, 0, 1, 0, 0, 5]);
    matrix.append([8, 0, 5, 3, 0, 0, 0, 0, 6]);
    matrix.append([0, 0, 7, 0, 0, 0, 8, 0, 1]);
    matrix.append([7, 0, 0, 0, 0, 0, 1, 0, 2]);
    matrix.append([0, 5, 0, 0, 3, 2, 0, 7, 9]);
    matrix.append([2, 9, 0, 0, 0, 4, 0, 3, 0]);
    for row in range(SIZE_POSIBLE_VALUES):
        for column in range(SIZE_POSIBLE_VALUES):
            if matrix[row][column] == 0:
                matrix[row][column] = DEFAULT_VALUE


def show_detail_change(func, action, column, row, value):
    print('{} => {} => (c={}, r={}): {}'.format(func, action, column, row, value))

def show_matrix():
    print("0  ", end=" ")
    for row in range(SIZE_POSIBLE_VALUES):
        print('{} '.format(row+1), end =" ")
    print("\n"*1)
    for row in range(SIZE_POSIBLE_VALUES):
        print('{} '.format(row+1), end =" ")
        for column in range(SIZE_POSIBLE_VALUES):
            print(' {}'.format(matrix[row][column]), end =" ")
        print()


def valid_insert_value(field):
    value = input('{} (1-{}): '.format(field, SIZE_POSIBLE_VALUES))
    while not value.isdigit() or int(value) > SIZE_POSIBLE_VALUES:
        value = input('Error: Invalid Value, {} (1-{}): '.format(field.lower(), SIZE_POSIBLE_VALUES))
    return int(value)


def insert_value():
    show_matrix()
    print()
    column_number = valid_insert_value('Column number')
    row_number = valid_insert_value('Row number')
    new_value = valid_insert_value('New Value')
    matrix[row_number - 1][column_number - 1] = int(new_value)
    print()
    show_matrix()


def show_instructions():
    print('Instructions')


def solve_sudoku():
    print('Solving Sudoku Game')
    posibilities = {}
    is_solved = False
    count = 0

    while not is_solved:
        have_change = False
        show_matrix()
        #input('Press key to continue')
        count += 1
        print()
        print()
        print('Intentos de solucion: {}'.format(count))
        for row in range(SIZE_POSIBLE_VALUES):
            for column in range(SIZE_POSIBLE_VALUES):
                if matrix[row][column] == DEFAULT_VALUE:
                    key_dict = '{}-{}'.format(column, row)
                    show_detail_change('is_solved', 'key', column, row, key_dict)
                    posibilities[key_dict] = POSIBLE_VALUES.copy()

                    change_row = solve_row(posibilities, key_dict, row)
                    change_column = solve_column(posibilities, key_dict, column)
                    change_quadrant = solve_quadrant(posibilities, key_dict)

                    show_detail_change('is_solved', 'posibles values', column, row, posibilities[key_dict])

                    if change_row or change_column or change_quadrant:
                        have_change = True

                    if len(posibilities[key_dict]) == 1:
                        show_detail_change('is_solved', 'find', column, row, posibilities[key_dict][0])
                        matrix[row][column] = posibilities[key_dict][0]
                else:
                    show_detail_change('is_solved', 'already', column, row, matrix[row][column])
                input('Press key to continue')
        is_solved = check_solved()
        if not have_change:
            show_matrix()
            input('No more changes. Press key to continue')
    show_matrix()


def check_solved():
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            if matrix[row][column] == DEFAULT_VALUE:
                return False
    return True


def solve_row(dic, key, row):
    change = False
    for column in range(len(matrix[row])):
        if not matrix[row][column] == DEFAULT_VALUE:
            if matrix[row][column] in dic[key]:
                show_detail_change('solve_row', 'removing', column, row, matrix[row][column])
                dic[key].remove(matrix[row][column])
                change = True
    return change


def solve_column(dic, key, column):
    change = False
    for row in range(len(matrix)):
        if not matrix[row][column] == DEFAULT_VALUE:
            if matrix[row][column] in dic[key]:
                show_detail_change('solve_column', 'removing', column, row, matrix[row][column])
                dic[key].remove(matrix[row][column])
                change = True
    return change


def valid_quadrant(key_value, quadrant_value):
    if int(key_value) >= int(quadrant_value) and int(key_value) <= (int(quadrant_value) + 2):
        return True
    else:
        return False


def solve_quadrant(dic, key_dict):
    change = False
    quadrant = None
    for key, value in quadrants.items():
        key_column = key_dict.split('-')[0]
        key_row = key_dict.split('-')[1]
        if  valid_quadrant(key_column, value['column']) and valid_quadrant(key_row, value['row']):
            quadrant = value
    column = quadrant['column']
    row = quadrant['row']
    for r in range(row, row + 3):
        for c in range(column, column + 3):
            if not matrix[r][c] == DEFAULT_VALUE:
                if matrix[r][c] in dic[key_dict]:
                    show_detail_change('solve_column', 'removing', c, r, matrix[r][c])
                    dic[key_dict].remove(matrix[r][c])
                    change = True
    return change


def select_menu_option():
    option = input('Select an option: ')
    menu_border_format(False)
    if option == "1":
        show_instructions()
    elif option == "2":
        show_matrix()
    elif option == "3":
        insert_value()
    elif option == "4":
        solve_sudoku()
    elif option == "5":
        start_matrix()
        show_matrix()
    elif option.lower() == "q":
        exit_program()
    else:
        print('Option not found!!!')


def menu_border_format(isPrincpal):
    if isPrincpal:
        print('_'*(MENU_SPACING+8))
    else:
        print('_'*(int(MENU_SPACING / 2)+8))


def menu_title_format(text):
    print('| {:^54} |'.format(text, '|'))


def menu_options_format(text):
    print('| {:50} {:>5}'.format(text, '|'))


def menu():
    #print("\n"*3)
    menu_border_format(True)
    menu_title_format('MENU')
    menu_border_format(True)
    menu_options_format("1. Instructions")
    menu_options_format("2. Show Matrix")
    menu_options_format("3. Add or Change Value")
    menu_options_format("4. View solution")
    menu_options_format("5. Reset Matrix")
    menu_options_format("Press Q or q to exit!")
    select_menu_option()


def welcome():
    print("WELCOME TO SODUKO SOLVER")
    start_matrix()
    while True:
        menu()
        print("\n"*3)


def exit_program():
    print("SUDOKU RESOLVER")
    print("{} {} {}".format('*'*5, 'Jose Gallegos', '*'*5))
    exit()


if __name__ == "__main__":
    welcome()
