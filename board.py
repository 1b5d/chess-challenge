"""
Includes classes that represent the main
elements of the problem: Board and Cell
"""
import random
from chess_exceptions import InvalidSetupException, InvalidArgumentException,\
    InvalidMoveException


class Cell(object):
    """
    Represents a cell of the board.
    """
    def __init__(self, row, column):
        """
        Initializes a new instance of the Cell class.
        :param row: An integer that represents the row of the cell.
        :param column: An integer that represents the column of the cell.
        :return: A new instance of the Cell class.
        """
        self.attacks = 0
        self.piece = None
        self.taken = False
        self._row = row
        self._column = column

    def __str__(self):
        """
        :return: A string of the piece type if the cell is occupied,
        otherwise, it returns the number of the attacks the cell has.
        """
        if self.piece:
            return str(self.piece)
        return str(self.attacks)

    @property
    def available(self):
        """
        Indicates whether the cell is occupied with a piece or not.
        :return: A boolean.
        """
        return not self.piece

    @property
    def row(self):
        """
        Gets the current row of the cell.
        :return: An integer that represents the row of the cell.
        """
        return self._row

    @property
    def column(self):
        """
        Gets the current column of the cell.
        :return: An integer that represents the column of the cell.
        """
        return self._column


class Board(object):
    """
    Represents a chess board with MxN dimensions
    and a set of pieces to be placed on it.
    """
    def __init__(self, rows, columns, pieces):
        """
        Initializes A Board instance with MxN dimensions and a list of pieces.

        :param rows: An Integer that represents the
        number of rows of the board.
        :param columns: An Integer that represents the
        number of columns of the board.
        :param pieces: A list that holds the chess pieces on the board.
        :return: A new instance of Board class.
        """
        self.rows = rows
        self.columns = columns
        self.pieces = pieces
        self.matrix = [[Cell(row, column) for column in xrange(self.columns)]
                       for row in xrange(self.rows)]
        for piece in self.pieces:
            piece.board = self
            row, column = self.get_next_available_position()
            if row is None or column is None:
                raise InvalidSetupException(
                    "pieces number exceed the board capacity"
                )
            self[row, column] = piece
        self._cache = {self.get_hash(): True}
        self.reset_position()
        self.calculate_attacks()
        super(Board, self).__init__()

    @property
    def cache(self):
        """
        Returns the caching hash table that stores the
        past configurations on the board.
        :return: a dict that stores the past configurations on the board.
        """
        return self._cache

    def __getitem__(self, pos):
        """
        Returns the cell in the passed position.
        :param pos: a tuple that represents the position (row, column).
        :return: An instance of the Cell class.
        """
        row, column = pos
        if row >= self.rows or abs(row) > self.rows:
            raise InvalidArgumentException(
                "piece row number is bigger than board row capacity"
            )
        if column >= self.columns or abs(column) > self.columns:
            raise InvalidArgumentException(
                "piece column number is bigger than board column capacity"
            )
        return self.matrix[row][column]

    def __setitem__(self, pos, value):
        """
        Sets a piece in a certain position on the board.
        :param pos: a tuple that represents the position (row, column).
        :param value: an instance of the Piece class or one of its children.
        :return: None.
        """
        row, column = pos
        if row >= self.rows:
            raise InvalidMoveException(
                "piece row number is bigger than board row capacity"
            )
        if column >= self.columns:
            raise InvalidMoveException(
                "piece column number is bigger than board column capacity"
            )
        cell = self.matrix[row][column]
        if value and not cell.available:
            raise InvalidMoveException(
                "cannot place the piece, spot already occupied"
            )
        cell.piece = value
        if value:
            value.set_position(row, column)

    def __str__(self):
        """
        Prints the board with its pieces and all the
        attacks on boards different positions.
        :return: A string.
        """
        parts = []
        for row in self.matrix:
            parts.append(' '.join([str(cell) for cell in row]))
        return '\n'.join(parts) + '\n'

    def print_board(self):
        """
        Prints the board with its pieces in a Friendly way.
        :return: A string.
        """
        parts = []
        for row in self.matrix:
            parts.append(' '.join(
                [str(cell.piece)
                 if not cell.available
                 else "0" for cell in row]))
        return '\n'.join(parts) + '\n'

    def get_hash(self, index=None, row=None, column=None):
        """
        Returns a signature that represents a certain
        distribution of the pieces on the board.
        It allows overriding a certain piece by passing the
        index, row, column parameters.
        :param index: An integer that represents the piece
        that needs to replaced by the (row, column) piece.
        :param row: An integer that represents the
        row of the replacing piece.
        :param column: An integer that represents the
        column of the replacing piece.
        :return: a Long value that represents the
        distribution of the pieces on the board.
        """
        result = 0L
        step = max(self.rows, self.columns).bit_length()
        test = None
        if index is not None:
            test = self.pieces[index]
        for y_axis in self.matrix:
            for cell in y_axis:
                if not cell.available or\
                        (cell.row == row and cell.column == column):
                    if test is not None and\
                            cell.row == row and cell.column == column:
                        result <<= step
                        result |= row + 1
                        result <<= step
                        result |= column + 1
                    elif not test or\
                            cell.row != test.row or\
                            cell.column != test.column:
                        result <<= step
                        result |= cell.row + 1
                        result <<= step
                        result |= cell.column + 1
        return result

    def get_next_available_position(self, lap=0):
        """
        Returns the first non-occupied position on the board after the offset.
        :param lap: An offset to start from.
        :return: A tuple that represents the first available position.
        """
        row_lap = lap / self.columns
        for y_axis in xrange(row_lap, self.rows):
            column_lap = lap % self.columns if y_axis == row_lap else 0
            row = self.matrix[y_axis]
            for x_axis in xrange(column_lap, self.columns):
                cell = row[x_axis]
                if cell.available:
                    return cell.row, cell.column
        return None, None

    def get_available_postions(self):
        """
        Returns all the non-occupied positions on the board.
        :return: A list of tuples that represents all the available positions.
        """
        moves = []
        for row in self.matrix:
            for cell in row:
                if cell.available:
                    moves.append((cell.row, cell.column))
        return moves

    def calculate_attacks(self):
        """
        Calculates the attacks from other pieces for every piece on the board.
        :return: None.
        """
        for row in self.matrix:
            for cell in row:
                cell.attacks = 0
        for piece in self.pieces:
            piece.update_column_status()
            moves = piece.get_moves()
            for move in moves:
                if not move.count(None):
                    self[move[0], move[1]].attacks += 1

    def has_attacked_piece(self):
        """
        Checks if the any of the pieces on the board has any attacks.
        :return: A boolean.
        """
        attacked = 0
        for piece in self.pieces:
            if self[piece.row, piece.column].attacks:
                attacked += 1
        return attacked

    def reset_position(self, lap=0):
        """
        Resets the positions of the pieces on the board.
        :param lap: the position to start placing the pieces.
        :return: None.
        """
        if lap > self.rows * self.columns - len(self.pieces):
            return False
        for piece in self.pieces:
            self[piece.row, piece.column] = None
        pieces = self.pieces[:]
        random.shuffle(pieces)
        for piece in pieces:
            row, column = self.get_next_available_position(lap)
            if row is None or column is None:
                raise InvalidSetupException(
                    "pieces number exceed the board capacity"
                )
            self[row, column] = piece
        self._cache[self.get_hash()] = True
        return True

    def find_independent_configurations(self, verbose=False):
        """
        Finds all the unique configurations of the pieces
        on the board where none of the pieces
        is in a position to take any of the others.

        :param verbose: decides whether to print execution
        information while finding the configurations or not.
        :return: A list of all the unique configurations.
        """
        solutions = []
        lap = 0
        while True:
            any_moved = False
            for index, piece in enumerate(self.pieces):
                # use get_moves() instead of get_available_postions()
                # to use only legal moves which can make the algorithm faster
                # but it can miss more solutions

                moves = piece.get_moves()
                # moves = self.get_available_postions()
                destinations = []
                for move in moves:
                    if not piece.can_move(index, *move):
                        continue

                    if not len(destinations) or\
                            self[move[0], move[1]].attacks <\
                            self[destinations[0][0],
                                 destinations[0][1]].attacks:
                        destinations = [move]
                    elif len(destinations) and\
                            self[move[0], move[1]].attacks ==\
                            self[destinations[0][0],
                                 destinations[0][1]].attacks:
                        destinations.append(move)

                for destination in destinations:
                    any_moved = True
                    piece.move(*destination)
                    self.calculate_attacks()
                    self._cache[self.get_hash()] = True
                    board_hash = self.get_hash()
                    if not self.has_attacked_piece() and\
                            board_hash not in solutions:
                        if verbose:
                            print self.print_board()
                        solutions.append(board_hash)
            if not any_moved:
                lap += 1
                self._cache = {}
                if not self.reset_position(lap):
                    break
                self.calculate_attacks()
        return solutions
