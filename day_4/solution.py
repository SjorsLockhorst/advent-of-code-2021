from pprint import pprint
from dataclasses import dataclass
from typing import Dict, List, Tuple


class Board:
    """
    Class to hold BingoBoard
    """

    @dataclass
    class Number:
        """
        Dataclass for a number
        """

        value: int
        row: int
        col: int
        marked: bool

    def __init__(self, numbers: List[List[Number]], numbers_map: Dict[int, Number]):
        self.numbers = numbers
        self.number_map = numbers_map
        self.is_winner = False

    def __repr__(self):
        """
        Override repr to create nicer representation of the board
        """
        result = "Board: \n"
        for row in self.numbers:
            for number in row:
                if number.marked:
                    result += "*" + str(number.value) + "*"
                else:
                    result += " " + str(number.value) + " "
                result += " "
                if len(str(number.value)) == 1:
                    result += " "
            result += "\n"
        result += "\n"
        return result

    def has_won(self, num: Number) -> bool:
        """
        Call two helper methods to check if from a number
        """
        return self.check_row(num.row) or self.check_column(num.col)

    def check_row(self, row: int) -> bool:
        for num in self.numbers[row]:
            if not num.marked:
                return False
        return True

    def check_column(self, col: int) -> bool:
        for row in self.numbers:
            if not row[col].marked:
                return False
        return True


class BingoGame:
    def __init__(self, path: str = "input.txt", board_size: int = 5):
        inputs: List[str] = [line.strip() for line in open(path)]
        self.draw_numbers: List[int] = [int(number) for number in inputs[0].split(",")]

        self.board_size = board_size
        self.boards: List[Board] = self._load_boards(inputs)

        self.current_num = 0
        self.winners = []

    def is_finished(self) -> bool:
        return self.current_num >= len(self.draw_numbers)

    def draw_number(self) -> int:
        number = self.draw_numbers[self.current_num]
        self.current_num += 1
        return number

    def play(self):

        while not self.is_finished():
            num = self.draw_number()
            for board in self.boards:
                if not board.is_winner:
                    if num in board.number_map:
                        number_obj = board.number_map[num]
                        number_obj.marked = True
                        if board.has_won(number_obj):
                            self.winners.append((board, number_obj))
                            board.is_winner = True

        return self.winners

    def find_last_winner(self):
        while len(self.boards) != 1:
            board, _ = self.play()
            self.boards.remove(board)
        return self.boards[0]

    def _load_boards(self, inputs: List[str]):
        """Create boards from input"""
        i = 2

        boards = []
        while i < len(inputs):
            board_inputs = inputs[i : i + self.board_size]
            i = i + self.board_size + 1

            numbers = [
                [Board.Number(0, 0, 0, False) for _ in range(self.board_size)]
                for _ in range(self.board_size)
            ]

            number_map = {}

            for row_i, str_row in enumerate(board_inputs):
                row = [int(num) for num in str_row.split(" ") if num != ""]
                for col_i, val in enumerate(row):

                    number = Board.Number(val, row_i, col_i, False)
                    number_map[val] = number
                    numbers[row_i][col_i] = number

            boards.append(Board(numbers, number_map))

        return boards


def get_winner_score(winner: Tuple[Board, Board.Number]):

    winner_board, winner_number = winner

    return (
        sum(
            [
                number.value
                for number in winner_board.number_map.values()
                if not number.marked
            ]
        )
        * winner_number.value
    )


def part_1():
    bingo_game = BingoGame(path="input.txt")
    first_winner = bingo_game.play()[0]
    print(get_winner_score(first_winner))


def part_2():
    bingo_game = BingoGame(path="input.txt")

    last_winner = bingo_game.play()[-1]
    print(last_winner[0].show())
    print(get_winner_score(last_winner))


part_2()
