import unittest
from pieces import Piece, King, Queen, Bishop, Rook, Knight
from board import Board
from chess_exceptions import InvalidSetupException,\
    InvalidMoveException


class TestPieceNoBoard(unittest.TestCase):
    """
    Testing piece functionality without a board set to it.
    """
    def setUp(self):
        """
        setup the test with Piece class.
        :return: None.
        """
        self.piece = Piece()

    def test_row(self):
        """
        test the row getter.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.row

    def test_set_row(self):
        """
        test the row setter.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.row = 1

    def test_column(self):
        """
        test the column getter.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.column

    def test_set_column(self):
        """
        test the column setter.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.column = 1

    def test_set_position(self):
        """
        test the position setting functionality.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.set_position(1, 1)

    def test_get_moves(self):
        """
        test getting the available moves of a piece.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.get_moves()

    def test_update_column_status(self):
        """
        test updating the column `taken` value.
        :return: None.
        """
        self.assertEqual(self.piece.update_column_status(), None)

    def test_can_move(self):
        """
        test the can_move functionality of a piece.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.can_move(1, 1, 1)

    def test_move(self):
        """
        test the move functionality of a piece.
        :return: None.
        """
        with self.assertRaises(InvalidSetupException):
            self.piece.move(1, 1)


class TestPiece(unittest.TestCase):
    """
    Testing a piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 piece on a board.
        :return: None.
        """
        self.piece = Piece()
        self.piece.board = Board(4, 4, [self.piece])

    def test_row(self):
        """
        test the row getter.
        :return: None.
        """
        self.assertEqual(self.piece.row, 0)

    def test_set_row(self):
        """
        test the row setter.
        :return: None.
        """
        self.setUp()
        self.piece.row = 2
        self.assertEqual(self.piece.row, 2)

        with self.assertRaises(InvalidMoveException):
            self.piece.row = -1

        with self.assertRaises(InvalidMoveException):
            self.piece.row = 4

    def test_column(self):
        """
        test the column getter.
        :return: None.
        """
        self.assertEqual(self.piece.column, 0)

    def test_set_column(self):
        """
        test the column setter.
        :return: None.
        """
        self.setUp()
        self.piece.column = 2
        self.assertEqual(self.piece.column, 2)

        with self.assertRaises(InvalidMoveException):
            self.piece.column = -1

        with self.assertRaises(InvalidMoveException):
            self.piece.column = 4

    def test_set_position(self):
        """
        test the position setting functionality.
        :return: None.
        """
        self.setUp()
        self.piece.set_position(2, 2)

        self.assertEqual(self.piece.row, 2)
        self.assertEqual(self.piece.column, 2)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(-1, 2)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(2, -1)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(-1, -1)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(4, 2)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(2, 4)

        with self.assertRaises(InvalidMoveException):
            self.piece.set_position(4, 4)

    def test_get_moves(self):
        """
        test getting the available moves of a piece.
        :return: None.
        """
        self.assertEqual(self.piece.get_moves(), [])

    def test_update_column_status(self):
        """
        test updating the column `taken` value.
        :return: None.
        """
        self.setUp()
        self.piece.update_column_status()

        self.assertEqual(self.piece.board[0, 1].taken, False)

    def test_can_move(self):
        """
        test the can_move functionality of a piece.
        :return: None.
        """
        self.assertEqual(self.piece.can_move(0, 0, 1), True)

    def test_move(self):
        """
        test the move functionality of a piece.
        :return: None.
        """
        self.setUp()
        self.piece.move(0, 1)

        self.assertEqual(self.piece.row, 0)
        self.assertEqual(self.piece.column, 1)

        self.assertEqual(self.piece.board[0, 1].piece, self.piece)


class TestKing(TestPiece):
    """
    Testing a King piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 King on a board.
        :return: None.
        """
        self.piece = King()
        self.piece.board = Board(4, 4, [self.piece])

    def test_get_moves(self):
        """
        test getting the available moves of a King piece.
        :return: None.
        """
        self.setUp()

        moves = self.piece.get_moves()
        moves_should_be = [(0, 1), (1, 1), (1, 0)]
        self.assertEqual(moves, moves_should_be)

        self.piece.move(2, 2)

        moves = self.piece.get_moves()
        moves_should_be = [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3),
                           (3, 2), (3, 1), (2, 1)]
        self.assertEqual(moves, moves_should_be)


class TestQueen(TestPiece):
    """
    Testing a Queen piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 Queen on a board.
        :return: None.
        """
        self.piece = Queen()
        self.piece.board = Board(4, 4, [self.piece])

    def test_get_moves(self):
        """
        test getting the available moves of a Queen piece.
        :return: None.
        """
        self.setUp()

        moves = self.piece.get_moves()
        moves_should_be = [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2),
                           (0, 3), (1, 1), (2, 2), (3, 3)]
        self.assertEqual(moves, moves_should_be)

        self.piece.move(2, 2)

        moves = self.piece.get_moves()
        moves_should_be = [(0, 2), (1, 2), (3, 2), (2, 0), (2, 1),
                           (2, 3), (3, 1), (1, 3), (0, 0), (1, 1),
                           (3, 3)]

        self.assertEqual(moves, moves_should_be)

    def test_update_column_status(self):
        """
        test updating the column `taken` value of a Queen piece.
        :return: None.
        """
        self.setUp()
        self.piece.move(2, 2)

        for index in xrange(self.piece.board.rows):
            self.assertEqual(self.piece.board[index, 2].taken, True)

        for index in xrange(self.piece.board.rows):
            self.assertEqual(self.piece.board[index, 0].taken, False)

    def test_can_move(self):
        """
        test the can_move functionality of a Queen piece.
        :return: None.
        """
        self.piece = Queen()
        second_piece = Queen()
        self.piece.board = Board(4, 4, [self.piece, second_piece])

        self.piece.move(2, 2)
        second_piece.move(1, 1)

        self.assertEqual(self.piece.can_move(0, 2, 1), False)
        self.assertEqual(self.piece.can_move(0, 3, 2), True)
        self.assertEqual(self.piece.can_move(0, 2, 3), True)


class TestBishop(TestPiece):
    """
    Testing a Bishop piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 Bishop on a board.
        :return: None.
        """
        self.piece = Bishop()
        self.piece.board = Board(4, 4, [self.piece])

    def test_get_moves(self):
        """
        test getting the available moves of a Bishop piece.
        :return: None.
        """
        self.setUp()

        moves = self.piece.get_moves()
        moves_should_be = [(1, 1), (2, 2), (3, 3)]
        self.assertEqual(moves, moves_should_be)

        self.piece.move(2, 2)

        moves = self.piece.get_moves()
        moves_should_be = [(3, 1), (1, 3), (0, 0), (1, 1), (3, 3)]

        self.assertEqual(moves, moves_should_be)


class TestRook(TestPiece):
    """
    Testing a Rook piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 Rook on a board.
        :return: None.
        """
        self.piece = Rook()
        self.piece.board = Board(4, 4, [self.piece])

    def test_get_moves(self):
        """
        test getting the available moves of a Rook piece.
        :return: None.
        """
        self.setUp()

        moves = self.piece.get_moves()
        moves_should_be = [(1, 0), (2, 0), (3, 0), (0, 1), (0, 2), (0, 3)]
        self.assertEqual(moves, moves_should_be)

        self.piece.move(2, 2)

        moves = self.piece.get_moves()
        moves_should_be = [(0, 2), (1, 2), (3, 2), (2, 0), (2, 1), (2, 3)]

        self.assertEqual(moves, moves_should_be)

    def test_can_move(self):
        """
        test the can_move functionality of a Rook piece.
        :return: None.
        """
        self.piece = Rook()
        second_piece = Rook()
        self.piece.board = Board(4, 4, [self.piece, second_piece])

        self.piece.move(2, 2)
        second_piece.move(1, 1)

        self.assertEqual(self.piece.can_move(0, 2, 1), False)
        self.assertEqual(self.piece.can_move(0, 3, 2), True)
        self.assertEqual(self.piece.can_move(0, 2, 3), True)


class TestKnight(TestPiece):
    """
    Testing a Knight piece functionality with a board set to it.
    """
    def setUp(self):
        """
        setup the test with 1 Knight on a board.
        :return: None.
        """
        self.piece = Knight()
        self.piece.board = Board(4, 4, [self.piece])

    def test_get_moves(self):
        """
        test getting the available moves of a Knight piece.
        :return: None.
        """
        self.setUp()

        moves = self.piece.get_moves()
        moves_should_be = [(2, 1), (1, 2)]
        self.assertEqual(moves, moves_should_be)

        self.piece.move(2, 2)

        moves = self.piece.get_moves()
        moves_should_be = [(0, 1), (1, 0), (3, 0), (0, 3)]

        self.assertEqual(moves, moves_should_be)
