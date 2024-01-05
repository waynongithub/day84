from random import randint, choice





def get_move_from_user_input(user_input):
    """Translates the user input into an index in the game_state list"""
    col = user_input[0].upper()
    colvalues = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    row = (int(user_input[1]) - 1) * 3
    move = colvalues[col] + row
    return move



class TicTacToe():
    def __init__(self):
        self.player = ['X', 'O']
        self.game_state = ['', '', '', '', '', '', '', '', '']
        self.winners = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        self.current_player = None
        self.main()

    def main(self):
        # print(f"in main")
        self.current_player = choice(self.player)
        print(f"You are X, {self.current_player} begins.")
        game_finished = False
        self.draw_board()
        while not game_finished:
            if self.current_player == 'X':
                move = self.ask_user_input()
                print(f"player X move={move}")
            else:
                # move = self.get_dumb_move()
                move = self.get_algo_move()
                print(f"player O move={move}")
            self.game_state[move] = self.current_player
            self.switch_user()
            game_finished = self.check_for_game_end()
            self.draw_board()

    def draw_board(self):
        nc = "\033[0;97m"
        red = "\033[0;91m"
        green = "\033[0;92m"
        blue = "\033[0;96m"
        yellow = "\033[0;93m"
        lilac = "\033[0;95m"
        print(f"{blue}")
        row_nr = 1
        row = "  A B C"
        for idx, x in enumerate(self.game_state):
            if x == '':
                x = ' '
            if (idx + 0) % 3 == 0:
                print(row)
                row = ""
                row += f"{row_nr} {x}"
                row_nr += 1
            else:
                row += f" {x}"
        print(row)
        print(f"{nc}")

    def ask_user_input(self):
        # TODO error with input aq1
        """Ask next user_input, if valid, put in game state and redraw board"""
        is_valid = False
        move = ''
        while not is_valid:
            is_valid = True
            user_input = input("Your next user_input?  ")
            if len(user_input) != 2:
                print("A valid user_input consists of one letter (A, B, or C) and a digit (1, 2, or 3")
                is_valid = False
            else:
                if not (user_input[0].isalpha() and user_input[0].upper() in ['A', 'B', 'C']):
                    print("the first character of the user_input should be one letter (A, B, or C)")
                    is_valid = False
                if not (user_input[1].isdigit() and user_input[1] in ['1', '2', '3']):
                    print("the second charcter should be a digit (1, 2, or 3)")
                    # print(f"user_input[1].isdigit()={user_input[1].isdigit()}, user_input[1] in [1, 2, 3]={user_input[1] in [1, 2, 3]} ")
                    is_valid = False
            move = get_move_from_user_input(user_input)
            available_moves = self.get_available_moves()
            if move not in available_moves:
                print(f"this move is no longer available")
                is_valid = False
        return move

    def check_winning_combination(self, Y):
        for w in self.winners:
            if w[0] in Y and w[1] in Y and w[2] in Y:
                return True
        return False

    def get_dumb_move(self):
        """Pick randomly from a list of available moves"""
        # print(f"in get_ai_move")
        available_moves = self.get_available_moves()
        return choice(available_moves)
        # self.game_state[move] = self.current_player

    def get_moves_per_player(self):
        x_moves = []
        o_moves = []
        for idx, x in enumerate(self.game_state):
            if x == 'X':
                x_moves.append(idx)
            elif x == 'O':
                o_moves.append(idx)
        retval = (x_moves, o_moves)
        return retval

    def get_almost_full_winning_states(self, ):
        one_pos_filled_x = []
        two_pos_filled_x = []
        # loop over all winning combinations
        for idx, combination in enumerate(self.winners):
            count = 0
            # select those that are partially filled
            for position in combination:
                if position in x_moves:
                    count += 1
            # check if the missing positions are already blocked
            if count == 2:
                two_pos_filled_x.append(idx)
            if count == 1:
                one_pos_filled_x.append(idx)

                # for position in combination:
                #     if position not in o_moves:
                #         scores[idx] = count
        to_delete = []
        if two_pos_filled_x:
            print("=================================")
            print(f"two_pos_filled_x 1={two_pos_filled_x}")
            for index, idx in enumerate(two_pos_filled_x):
                deleted = False
                print(f"iteration {index + 1}, idx={idx}")
                for position in winners[idx]:
                    # print(f"two_pos_filled_x 2, positions={position}, winners[idx]={winners[idx]}")
                    if position in o_moves:
                        print(f"combination {idx} is blocked")
                        # two_pos_filled_x.remove(idx)
                        to_delete.append(idx)
                        print(f"combination {idx} should have been removed index:{two_pos_filled_x}")
                        print(f"about to break for {winners[idx]}")
                        break
            two_pos_filled_x = [x for x in two_pos_filled_x if x not in to_delete]

            print(f"two_pos_filled_x 4={two_pos_filled_x}")
            if two_pos_filled_x:
                # TODO what if all options are blocked?
                # TODO blocked options are not deleted
                for position in winners[two_pos_filled_x[0]]:
                    if self.game_state[position] == "":
                        print(f"positions={position}")
                        return position
            else:
                return self.get_dumb_move()
        else:
            return self.get_dumb_move()

    def get_algo_move(self):
        x_moves, o_moves = self.get_moves_per_player()
        print(f"{x_moves}, {o_moves}")
        # o_moves = []
        # for idx, x in enumerate(self.game_state):
        #     if x == 'X':
        #         x_moves.append(idx)
        #     elif x == 'O':
        #         o_moves.append(idx)
        one_pos_filled_o = []
        two_pos_filled_x = []
        # block winning moves
        counts = []
        one_pos_filled_o = []
        two_pos_filled_x = []
        # loop over all winning combinations
        for idx, combination in enumerate(winners):
            count = 0
            # select those that are partially filled
            for position in combination:
                if position in x_moves:
                    count += 1
            # check if the missing positions are already blocked
            if count == 2:
                two_pos_filled_x.append(idx)
            if count == 1:
                one_pos_filled_o.append(idx)

                # for position in combination:
                #     if position not in o_moves:
                #         scores[idx] = count
        to_delete = []
        if two_pos_filled_x:
            print("=================================")
            print(f"two_pos_filled_x 1={two_pos_filled_x}")
            for index, idx in enumerate(two_pos_filled_x):
                deleted = False
                print(f"iteration {index + 1}, idx={idx}")
                for position in winners[idx]:
                    # print(f"two_pos_filled_x 2, positions={position}, winners[idx]={winners[idx]}")
                    if position in o_moves:
                        print(f"combination {idx} is blocked")
                        # two_pos_filled_x.remove(idx)
                        to_delete.append(idx)
                        print(f"combination {idx} should have been removed index:{two_pos_filled_x}")
                        print(f"about to break for {winners[idx]}")
                        break
            two_pos_filled_x = [x for x in two_pos_filled_x if x not in to_delete]

            print(f"two_pos_filled_x 4={two_pos_filled_x}")
            if two_pos_filled_x:
                # TODO what if all options are blocked?
                # TODO blocked options are not deleted
                for position in winners[two_pos_filled_x[0]]:
                    if self.game_state[position] == "":
                        print(f"positions={position}")
                        return position
            else:
                return self.get_dumb_move()
        else:
            return self.get_dumb_move()


    def get_available_moves(self):
        available_moves = []
        for idx, x in enumerate(self.game_state):
            if x == '':
                available_moves.append(idx)
        return available_moves

    def check_for_game_end(self):
        """Is there a winner? Is there tie? Can game continue?"""
        green = "\033[0;92m"
        yellow = "\033[0;93m"
        x_moves = []
        o_moves = []
        for idx, x in enumerate(self.game_state):
            if x == 'X':
                x_moves.append(idx)
            elif x == 'O':
                o_moves.append(idx)

        # print(f"x_moves={x_moves}")
        # print(f"o_moves={o_moves}")
        if check_winning_combination(x_moves):
            print(f"{green}X wins")
            return True
        if check_winning_combination(o_moves):
            print(f"{green}O wins")
            return True
        if not self.get_available_moves():
            print(f"{yellow}It's a tie")
            return True
        return False

    def switch_user(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'


TicTacToe()