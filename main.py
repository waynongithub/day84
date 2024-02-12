from random import randint, choice


def get_move_from_user_input(user_input):
    """Translates the coordinates from the user input to an index in the game_state list"""
    col = user_input[0].upper()
    colvalues = {
        'A': 0,
        'B': 1,
        'C': 2
    }
    row = (int(user_input[1]) - 1) * 3
    move = colvalues[col] + row
    return move


def get_coordinates_from_position(move):
    """Translates game_state indexes to coordinates"""
    coordinates = ['A1', 'B1', 'C1', 'A2', 'B2', 'C2', 'A3', 'B3', 'C3']
    return coordinates[move]


class TicTacToe():
    def __init__(self):
        self.player = ['X', 'O']
        self.game_state = ['', '', '', '', '', '', '', '', '']
        self.winning_states = [
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
        self.number_of_games = 0
        self.number_of_wins = 0
        self.number_of_losses = 0
        self.number_of_ties = 0
        self.main()

    def main(self):
        yellow = "\033[0;93m"
        nc = "\033[0;97m"
        self.current_player = choice(self.player)
        print(f"\n{yellow}You are X, {self.current_player} begins.{nc}")
        print("Enter your move as coordinates (a1 to c3), case insensitive. ")
        keep_playing = 'y'
        while keep_playing == 'y':
            # reset game
            game_finished = False
            self.game_state = ['', '', '', '', '', '', '', '', '']
            self.draw_board()
            # play game
            while not game_finished:
                if self.current_player == 'X':
                    # get next move for human player
                    move = self.ask_user_input()
                    print(f"Player X: move= {get_coordinates_from_position(move)}")
                else:
                    # get next move for algorithm
                    move = self.get_algo_move()
                    print(f"Player O: move= {get_coordinates_from_position(move)}")
                # enter move into the game_state
                self.game_state[move] = self.current_player
                self.switch_user()
                self.draw_board()
                game_finished = self.check_for_game_end()
                if game_finished:
                    self.number_of_games += 1
                    keep_playing = input(f"{yellow}keep playing? (y/n){nc}  ")
        # final scores
        print(f"{self.number_of_games} games played, {self.number_of_ties} ties, "
              f"{self.number_of_wins} wins, {self.number_of_losses} losses")

    def draw_board(self):
        nc = "\033[0;97m"
        blue = "\033[0;96m"
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
        """Ask user to input the next move and validates the input. Called by main."""
        is_valid = False
        move = ''
        while not is_valid:
            is_valid = True
            user_input = input("Your next move?  ")
            if len(user_input) != 2:
                print("A valid user_input consists of one letter (A, B, or C) and a digit (1, 2, or 3")
                is_valid = False
            else:
                if not (user_input[0].isalpha() and user_input[0].upper() in ['A', 'B', 'C']):
                    print("the first character of the user_input should be one letter (A, B, or C)")
                    is_valid = False
                if not (user_input[1].isdigit() and user_input[1] in ['1', '2', '3']):
                    print("the second charcter should be a digit (1, 2, or 3)")
                    is_valid = False
            if is_valid:
                move = get_move_from_user_input(user_input)
                available_moves = self.get_available_moves()
                if move not in available_moves:
                    print(f"this move is no longer available")
                    is_valid = False
        return move

    def check_for_winning_configuration(self, player_moves):
        """Loops over all winning configurations and checks if they can be found on the board. Argument 'player_moves
        is a list with the moves of the given player"""
        for winning_state in self.winning_states:
            if winning_state[0] in player_moves and winning_state[1] in player_moves and winning_state[2] in player_moves:
                return True
        return False

    def get_random_move(self):
        """Pick randomly from a list of available moves. Used when there is no opponent's move to block or winning
        configuration to complete."""
        available_moves = self.get_available_moves()
        return choice(available_moves)

    def get_moves_per_player(self):
        """Populates lists with the moves the players have made so far. These are used to check if they
        have made a winning configuration"""
        x_moves = []
        o_moves = []
        for idx, x in enumerate(self.game_state):
            if x == 'X':
                x_moves.append(idx)
            elif x == 'O':
                o_moves.append(idx)
        retval = (x_moves, o_moves)
        return retval

    def get_almost_full_winning_states(self, moves_player_1, moves_player_2):
        """Winning configurations consist of 3 moves. This functions finds configurations where 2 out of those 3
        moves have already been made. It will then check if the 3rd required move is still available. If so, the
        function returns this move that will then either block the opponent or that will win the game. It takes
        as arguments 2 lists with all the moves of both players. The function is called twice to check for
        almost winning configurations for both players"""
        # list to hold the indexes of the winning_states that could potentially be finalised
        potential_winners = []
        # loop over all winning configurations and count how many required moves have already been made
        for idx, configuration in enumerate(self.winning_states):
            count = 0
            # select those that are partially filled
            for move in configuration:
                if move in moves_player_1:
                    count += 1
            if count == 2:
                potential_winners.append(idx)

        # some potential winners have the 3rd position already occupied. They should be removed from the list
        to_delete = []
        if potential_winners:
            for idx in potential_winners:
                for move in self.winning_states[idx]:
                    # check if one of the moves in the combination is taken by the opponent
                    if move in moves_player_2:
                        # this potential winner should be removed
                        to_delete.append(idx)
                        break
            potential_winners = [x for x in potential_winners if x not in to_delete]
        return potential_winners

    def get_algo_move(self):
        """These moves are per definition only made by the computer (player O)"""
        x_moves, o_moves = self.get_moves_per_player()

        # find potential wins for the computer
        two_pos_filled_o = self.get_almost_full_winning_states(o_moves, x_moves)
        if two_pos_filled_o:
            for move in self.winning_states[two_pos_filled_o[0]]:
                if self.game_state[move] == "":
                    return move
        else:
            # potential winners for X need to be blocked
            potential_winners_for_x = self.get_almost_full_winning_states(x_moves, o_moves)
            if potential_winners_for_x:
                # even with multiple potential winners, only one move can be made, so only the first one is checked
                for move in self.winning_states[potential_winners_for_x[0]]:
                    if self.game_state[move] == "":
                        return move
        # if there are no potential wins to make or block, make a random move
        return self.get_random_move()

    def get_available_moves(self):
        available_moves = []
        for idx, x in enumerate(self.game_state):
            if x == '':
                available_moves.append(idx)
        return available_moves

    def check_for_game_end(self):
        """Is there a winner? Is there tie? Also adjust the score."""
        green = "\033[0;92m"
        yellow = "\033[0;93m"
        red = "\033[0;91m"
        x_moves, o_moves = self.get_moves_per_player()

        if self.check_for_winning_configuration(x_moves):
            print(f"{green}X wins")
            self.number_of_wins += 1
            return True
        if self.check_for_winning_configuration(o_moves):
            print(f"{red}O wins")
            self.number_of_losses += 1
            return True
        if not self.get_available_moves():
            self.number_of_ties += 1
            print(f"{yellow}It's a tie")
            return True
        return False

    def switch_user(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'


TicTacToe()