# Console Connect Four Consecutive Slots
# 2 layers, 1 winner
# To win the player should connect four consecutive slots, they can be in horizontal, vertical or diagonal direction.
#
def create_matrix():
    # This function creates the matrix(playground) with the
    # given from the player rows length and columns length
    try:
        rows = int(input("Enter the number of rows: "))
        columns = int(input("Enter the number of columns: "))
        matrix = []

        for row in range(rows):
            matrix.append([0] * columns)
    except ValueError:
        print("Please enter a valid numbers for the rows and the columns")
        matrix = create_matrix()
    return matrix


def print_function(playground):

    for row in playground:
        print(*row, sep="  ")


def player_choice(player, columns):
    try:
        choice = int(input(f"Player {player}, please choose a column to play: "))
        if choice not in range(1, columns + 1):
            print(f"Please enter a valid column number in range [1, {columns}]")
            choice = player_choice(player, columns)

    except ValueError:
        print(f"Please enter a valid column number in range [1, {columns}]")
        choice = player_choice(player, columns)

    return choice


def check_if_win_combination(row_index, column_index, playground, win_combination):
    # This function checks all possible combinations and
    # returns True or False depends on what the function found in the matrix

    def check_horizontal_win_combination(playground, left_column_index, right_column_index, win_combination):
        # This function checks the horizontal values in the matrix for a win combination
        # If a win combination is found, the function returns True, otherwise returns False

        win_combination_found = False

        for i in range(left_column_index, right_column_index - win_combination + 2):
            current_combination = []

            for j in range(win_combination):
                current_combination.append(playground[row_index][i + j])

            if len(set(current_combination)) == 1 and 0 not in current_combination:
                win_combination_found = True
                break
        return win_combination_found

    def check_vertical_win_combination(playground, up_row_index, down_row_index, win_combination):
        # This function checks the vertical values in the matrix for a win combination
        # If a win combination is found, the function returns True, otherwise returns False

        win_combination_found = False

        for i in range(up_row_index, down_row_index - win_combination + 2):
            current_combination = []

            for j in range(win_combination):
                current_combination.append(playground[i + j][column_index])

            if len(set(current_combination)) == 1 and 0 not in current_combination:
                win_combination_found = True
                break
        return win_combination_found

    def check_right_diagonal_win_combination(playgroud, left_column_index, right_column_index,
                                             up_row_index, down_row_index, win_combination):
        # This function checks the values in the anti-diagonal way of the matrix
        # If a win combination is found, the function returns True, otherwise returns False

        if down_row_index - row_index > column_index - left_column_index:  # In this if-else block, we're finding the
            start_column_index = left_column_index  # starting position for the for-loop, so we
            start_row_index = row_index + (column_index - left_column_index)  # can check all possible combinations

        elif column_index - left_column_index > down_row_index - row_index:
            start_column_index = column_index - (down_row_index - row_index)
            start_row_index = down_row_index
        else:
            start_column_index = left_column_index
            start_row_index = down_row_index

        win_combination_found = False

        if row_index - up_row_index >= right_column_index - column_index:
            # In this if-else block we check if the current position of the current player is closer to
            # the upper row boundary or to the right column boundary, so we don't get an index error and loop correctly
            for column in range(start_column_index, right_column_index - win_combination + 2):
                current_row = start_row_index
                current_combination = []

                for j in range(win_combination):
                    current_combination.append(playgroud[current_row][column + j])
                    current_row -= 1

                start_row_index -= 1

                if len(set(current_combination)) == 1 and 0 not in current_combination:
                    win_combination_found = True
                    break
        else:
            for row in range(start_row_index, up_row_index + win_combination - 2, -1):
                current_col = start_column_index
                current_combination = []

                for j in range(win_combination):
                    current_combination.append(playgroud[row - j][current_col])
                    current_col += 1

                start_column_index += 1

                if len(set(current_combination)) == 1 and 0 not in current_combination:
                    win_combination_found = True
                    break

        return win_combination_found

    def check_left_diagonal_win_combination(playgroud, left_column_index,
                                            right_column_index, up_row_index, down_row_index, win_combination):
        # This function checks the values in the main-diagonal way of the matrix
        # If a win combination is found, the function returns True, otherwise returns False

        if row_index - up_row_index > column_index - left_column_index:  # In this if-else block, we're finding the
            start_row_index = row_index - (column_index - left_column_index)  # starting position for the for-loop
            start_column_index = left_column_index  # so we can check all possible combinations

        elif column_index - left_column_index > row_index - up_row_index:
            start_row_index = up_row_index
            start_column_index = column_index - (row_index - up_row_index)

        else:
            start_row_index = up_row_index
            start_column_index = left_column_index

        win_combination_found = False

        if down_row_index - row_index > right_column_index - column_index:
            # In this if-else block we check if the current position of the current player is closer to
            # the upper row boundary or to the right column boundary, so we don't get an index error and loop correctly
            for column in range(start_column_index, right_column_index - win_combination + 1):
                current_row = start_row_index
                current_combination = []
                for j in range(win_combination):
                    current_combination.append(playgroud[current_row][column + j])
                    current_row += 1
                start_row_index += 1

                if len(set(current_combination)) == 1 and 0 not in current_combination:
                    win_combination_found = True
                    break
        else:
            for row in range(start_row_index, (down_row_index - win_combination) + 2):
                current_col = start_column_index
                current_combination = []
                for j in range(win_combination):
                    current_combination.append(playgroud[row + j][current_col])
                    current_col += 1
                start_column_index += 1

                if len(set(current_combination)) == 1 and 0 not in current_combination:
                    win_combination_found = True
                    break
        return win_combination_found

    # Finding the boundary indexes, so we can easily loop through the matrix
    min_left_column_index = max(column_index - win_combination + 1, 0)
    max_right_column_index = min(column_index + win_combination - 1, len(playground[row_index]) - 1)
    min_up_row_index = max(row_index - win_combination + 1, 0)
    max_down_row_index = min(row_index + win_combination - 1, len(playground) - 1)

    # horizontal combination checker
    horizontal_value = check_horizontal_win_combination(playground, min_left_column_index,
                                                        max_right_column_index, win_combination)
    # vertical combination checker
    vertical_value = check_vertical_win_combination(playground, min_up_row_index, max_down_row_index, win_combination)
    # right diagonal checker
    right_diagonal_value = check_right_diagonal_win_combination(playground,
                                                                min_left_column_index, max_right_column_index,
                                                                min_up_row_index, max_down_row_index, win_combination)
    # left diagonal checker
    left_diagonal_value = check_left_diagonal_win_combination(playground, min_left_column_index, max_right_column_index,
                                                              min_up_row_index, max_down_row_index, win_combination)

    possible_winner_checker = [
        horizontal_value,
        vertical_value,
        right_diagonal_value,
        left_diagonal_value,
    ]

    return any(current_value for current_value in possible_winner_checker)


def implement_data_to_main_logic(playground, player_index, player):
    # This function writes the player's number in the chosen column
    start_row_index = len(playground) - 1

    while start_row_index >= 0 and playground[start_row_index][player_index] != 0:
        start_row_index -= 1

    if playground[start_row_index][player_index] == 0:
        playground[start_row_index][player_index] = player
    else:
        print("The column is actually full, please enter another column to play!")
        second_player_choice = player_choice(player)
        start_row_index, player_index = implement_data_to_main_logic(playground, second_player_choice, player)

    return start_row_index, player_index


def game_play_function(playground, win_combination):
    current_player, second_player = 1, 2

    while True:
        current_player_choice = player_choice(current_player, len(playground[0])) - 1
        row_index, column_index = implement_data_to_main_logic(playground, current_player_choice, current_player)
        print_function(playground)

        if check_if_win_combination(row_index, column_index, playground, win_combination):
            print(f"The winner is player {current_player}")
            break
        current_player, second_player = second_player, current_player


def play():
    winning_combination = 4
    playground_matrix = create_matrix()
    game_play_function(playground_matrix, winning_combination)


play()
