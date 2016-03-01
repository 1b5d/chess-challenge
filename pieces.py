"""
Includes classes that represent the different types
of pieces that can be placed on the board, like:
King, Queen, Bishop, Rook, Knight.
"""


class Piece(object):
    """
    Represents the base class of pieces.
    """
    def __init__(self):
        """
        Initializes a new instance of the Piece class.
        :return: A new instance of Piece class.
        """
        self._row = None
        self._column = None
        self.board = None
        super(Piece, self).__init__()

    @property
    def row(self):
        """
        Gets the current row of the piece.
        :return: An integer that represents the row of the piece.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")
        return self._row

    @row.setter
    def row(self, value):
        """
        Sets the row value of the piece.
        :param value: An integer that represents the row of the piece.
        :return: None.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")
        if value >= self.board.rows:
            raise RuntimeError("Error: piece row number is bigger than board row capacity")
        self._row = value

    @property
    def column(self):
        """
        Gets the current column of the piece.
        :return: An integer that represents the column of the piece.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")
        return self._column

    @column.setter
    def column(self, value):
        """
        Sets the column value of the piece.
        :param value: An integer that represents the column of the piece.
        :return: None.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")
        if value >= self.board.columns:
            raise RuntimeError("Error: piece column number is bigger than board column capacity")
        self._column = value

    def set_position(self, row, column):
        """
        Sets the row and the column values of the piece.
        :param row: An integer that represents the row of the piece.
        :param column: An integer that represents the column of the piece.
        :return: None.
        """
        self.row = row
        self.column = column

    def get_moves(self):
        """
        Returns the legal moves of the piece.
        :return: A list of tuples that represent the legal available moves.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")
        return []

    def update_column_status(self, taken=True):
        """
        Updates the `taken` properties of all the cells of the piece's column.
        :param taken: A boolean that decides whether the column's
        cells will be set as taken or not.
        :return: None.
        """
        pass

    def can_move(self, index, row, column):
        """
        Decides whether if the piece can be moved to the passed position.
        :param index: An integer that represents the index
        of the piece in the board piece set.
        :param row: An integer that represents the row of the tested position.
        :param column: An integer that represents the column of the tested position.
        :return: A boolean.
        """
        cell = self.board[row, column]
        if not cell.available:
            return False
        if self.board.cache.get(self.board.get_hash(index, row, column), None):
            return False
        return True

    def move(self, row, column):
        """
        Moves the piece to the passed position.
        :param row: An integer that represents the destination position's row.
        :param column: An integer that represents the destination position's column.
        :return: None.
        """
        if not self.board:
            raise RuntimeError("Error: piece is not set to a board")

        self.update_column_status(False)
        if not [self.row, self.column].count(None):
            self.board[self.row, self.column] = None
        self.board[row, column] = self
        self.update_column_status()


class King(Piece):
    """
    Represents the King piece.
    """
    def __init__(self):
        """
        Initializes a new instance of the King class.
        :return: A new instance of King class.
        """
        super(King, self).__init__()

    def __str__(self):
        """
        :return: Returns a string representation that differentiate the piece's type.
        """
        return "K"

    def get_moves(self):
        """
        Returns the legal moves of the King's piece.
        :return: A list of tuples that represent the legal available moves.
        """
        moves = super(King, self).get_moves()
        row = self.row
        column = self.column

        rows = self.board.rows
        columns = self.board.columns

        # add all the cells surrounding the piece
        if row - 1 >= 0 and column - 1 >= 0:
            moves.append((row - 1, column - 1))
        if row - 1 >= 0:
            moves.append((row - 1, column))
        if row - 1 >= 0 and column + 1 < columns:
            moves.append((row - 1, column + 1))
        if column + 1 < columns:
            moves.append((row, column + 1))
        if row + 1 < rows and column + 1 < columns:
            moves.append((row + 1, column + 1))
        if row + 1 < rows:
            moves.append((row + 1, column))
        if row + 1 < rows and column - 1 >= 0:
            moves.append((row + 1, column - 1))
        if column - 1 >= 0:
            moves.append((row, column - 1))
        return moves


class Queen(Piece):
    """
    Represents the Queen piece.
    """
    def __init__(self):
        """
        Initializes a new instance of the Queen class.
        :return: A new instance of Queen class.
        """
        super(Queen, self).__init__()

    def __str__(self):
        """
        :return: Returns a string representation that differentiate the piece's type.
        """
        return "Q"

    def get_moves(self):
        """
        Returns the legal moves of the Queen's piece.
        :return: A list of tuples that represent the legal available moves.
        """
        moves = super(Queen, self).get_moves()
        row = self.row
        column = self.column

        rows = self.board.rows
        columns = self.board.columns

        # add all the cells in the piece's column
        for y_axis in xrange(rows):
            if y_axis == row:
                continue
            moves.append((y_axis, column))

        # add all the cells in the piece's row
        for x_axis in xrange(columns):
            if x_axis == column:
                continue
            moves.append((row, x_axis))

        # add all the cells in the piece's diagonals
        for x_axis in xrange(0, row + column + 1):
            y_axis = row + column - x_axis
            if x_axis < columns and y_axis < rows and x_axis != column and y_axis != row:
                moves.append((y_axis, x_axis))

        for y_axis in xrange(row - column, max(rows, columns)):
            x_axis = y_axis - row + column
            if 0 <= x_axis < columns and 0 <= y_axis < rows and x_axis != column and y_axis != row:
                moves.append((y_axis, x_axis))

        return moves

    def update_column_status(self, taken=True):
        """
        Updates the `taken` properties of all the cells of the piece's column.
        :param taken: A boolean that decides whether the column's
        cells will be set as taken or not.
        :return: None.
        """
        for index in xrange(self.board.rows):
            self.board[index, self.column].taken = taken

    def can_move(self, index, row, column):
        """
        Decides whether if the piece can be moved to the passed position.
        :param index: An integer that represents the index
        of the piece in the board piece set.
        :param row: An integer that represents the row of the tested position.
        :param column: An integer that represents the column of the tested position.
        :return: A boolean.
        """
        if column != self.column and self.board[row, column].taken:
            return False
        return super(Queen, self).can_move(index, row, column)


class Bishop(Piece):
    """
    Represents the Bishop piece.
    """
    def __init__(self):
        """
        Initializes a new instance of the Bishop class.
        :return: A new instance of Bishop class.
        """
        super(Bishop, self).__init__()

    def __str__(self):
        """
        :return: Returns a string representation that differentiate the piece's type.
        """
        return "B"

    def get_moves(self):
        """
        Returns the legal moves of the Bishop's piece.
        :return: A list of tuples that represent the legal available moves.
        """
        moves = super(Bishop, self).get_moves()
        row = self.row
        column = self.column

        rows = self.board.rows
        columns = self.board.columns

        # add all the cells in the piece's diagonals
        for x_axis in xrange(0, row + column + 1):
            y_axis = row + column - x_axis
            if x_axis < columns and y_axis < rows and x_axis != column and y_axis != row:
                moves.append((y_axis, x_axis))

        for y_axis in xrange(row - column, max(rows, columns)):
            x_axis = y_axis - row + column
            if 0 <= x_axis < columns and 0 <= y_axis < rows and x_axis != column and y_axis != row:
                moves.append((y_axis, x_axis))

        return moves


class Rook(Piece):
    """
    Represents the Rook piece.
    """
    def __init__(self):
        """
        Initializes a new instance of the Rook class.
        :return: A new instance of Rook class.
        """
        super(Rook, self).__init__()

    def __str__(self):
        """
        :return: Returns a string representation that differentiate the piece's type.
        """
        return "R"

    def get_moves(self):
        """
        Returns the legal moves of the Rook's piece.
        :return: A list of tuples that represent the legal available moves.
        """
        moves = super(Rook, self).get_moves()
        row = self.row
        column = self.column

        rows = self.board.rows
        columns = self.board.columns

        # add all the cells in the piece's column
        for y_axis in xrange(rows):
            if y_axis == row:
                continue
            moves.append((y_axis, column))

        # add all the cells in the piece's row
        for x_axis in xrange(columns):
            if x_axis == column:
                continue
            moves.append((row, x_axis))

        return moves

    def update_column_status(self, taken=True):
        """
        Updates the `taken` properties of all the cells of the piece's column.
        :param taken: A boolean that decides whether the column's
        cells will be set as taken or not.
        :return: None.
        """
        for index in xrange(self.board.rows):
            self.board[index, self.column].taken = taken

    def can_move(self, index, row, column):
        """
        Decides whether if the piece can be moved to the passed position.
        :param index: An integer that represents the index
        of the piece in the board piece set.
        :param row: An integer that represents the row of the tested position.
        :param column: An integer that represents the column of the tested position.
        :return: A boolean.
        """
        if column != self.column and self.board[row, column].taken:
            return False
        return super(Rook, self).can_move(index, row, column)


class Knight(Piece):
    """
    Represents the Rook piece.
    """
    def __init__(self):
        """
        Initializes a new instance of the Knight class.
        :return: A new instance of Knight class.
        """
        super(Knight, self).__init__()

    def __str__(self):
        """
        :return: Returns a string representation that differentiate the piece's type.
        """
        return "N"

    def get_moves(self):
        """
        Returns the legal moves of the Knight's piece.
        :return: A list of tuples that represent the legal available moves.
        """
        moves = super(Knight, self).get_moves()
        row = self.row
        column = self.column

        rows = self.board.rows
        columns = self.board.columns

        if row - 2 >= 0 and column - 1 >= 0:
            moves.append((row - 2, column - 1))
        if row - 1 >= 0 and column - 2 >= 0:
            moves.append((row - 1, column - 2))
        if row + 1 < rows and column - 2 >= 0:
            moves.append((row + 1, column - 2))
        if row + 2 < rows and column - 1 >= 0:
            moves.append((row + 2, column - 1))
        if row + 2 < rows and column + 1 < columns:
            moves.append((row + 2, column + 1))
        if row + 1 < rows and column + 2 < columns:
            moves.append((row + 1, column + 2))
        if row - 1 >= 0 and column + 2 < columns:
            moves.append((row - 1, column + 2))
        if row - 2 >= 0 and column + 1 < columns:
            moves.append((row - 2, column + 1))

        return moves
