"""
Includes test classes for the board type.
"""

import unittest
from pieces import Rook, King
from board import Board


class BoardCell(unittest.TestCase):
    """
    Testing board functionality.
    """
    def setUp(self):
        """
        setup the test with Board class.
        :return: None.
        """
        self.rook = Rook()
        self.king1 = King()
        self.king2 = King()
        self.board = Board(3, 3, [self.rook, self.king1, self.king2])

    def test_setup(self):
        """
        test the board setup.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.rook.move(2, 1)
        self.king2.move(2, 2)
        self.board.calculate_attacks()

        attacks = []
        for row in self.board.matrix:
            for cell in row:
                attacks.append(cell.attacks)

        for piece in self.board.pieces:
            self.assertEqual(piece, self.board[piece.row, piece.column].piece)
        self.assertEqual(attacks, [0, 1, 0, 1, 3, 1, 1, 2, 1])

    def test_getitem(self):
        """
        test getting a board cell.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.assertEqual(self.board[2, 0].piece, self.king1)
        self.assertEqual(self.board[2, 0].row, self.king1.row)
        self.assertEqual(self.board[2, 0].column, self.king1.column)

    def test_setitem(self):
        """
        test setting a board cell.
        :return: None.
        """
        self.setUp()
        self.board[2, 0] = self.king1
        self.assertEqual(self.board[2, 0].piece, self.king1)
        self.assertEqual(self.board[2, 0].row, self.king1.row)
        self.assertEqual(self.board[2, 0].column, self.king1.column)

    def test_gethash(self):
        """
        test getting the hash of a certain configuration of the board.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.rook.move(2, 1)
        self.king2.move(2, 2)
        self.board.calculate_attacks()
        self.assertEqual(self.board.get_hash(), 3567L)
        self.assertEqual(self.board.get_hash(0, 0, 0), 1503L)

    def test_get_next_available_pos(self):
        """
        test getting the next available position on the board.
        :return: None.
        """
        self.assertEqual(self.board.get_next_available_position(), (1, 0))

    def test_get_available_postions(self):
        """
        test getting all the available positions on the board.
        :return: None.
        """
        self.assertEqual(self.board.get_available_postions(),
                         [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def test_calculate_attacks(self):
        """
        test calculating the attacks for all the cells on the board.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.rook.move(2, 1)
        self.king2.move(2, 2)
        self.board.calculate_attacks()

        attacks = []
        for row in self.board.matrix:
            for cell in row:
                attacks.append(cell.attacks)

        self.assertEqual(attacks, [0, 1, 0, 1, 3, 1, 1, 2, 1])

    def test_has_attacked_piece(self):
        """
        test checking if the board has an attacked piece.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.rook.move(2, 1)
        self.king2.move(2, 2)
        self.board.calculate_attacks()
        self.assertEqual(self.board.has_attacked_piece(), 3)

        self.king1.move(0, 0)
        self.rook.move(2, 1)
        self.king2.move(0, 2)
        self.board.calculate_attacks()
        self.assertEqual(self.board.has_attacked_piece(), False)

    def reset_position(self):
        """
        test resetting the board pieces.
        :return: None.
        """
        self.setUp()
        self.king1.move(2, 0)
        self.rook.move(2, 1)
        self.king2.move(2, 2)
        self.board.calculate_attacks()
        self.board.reset_position()

        self.assertEqual(self.board.get_available_postions(),
                         [(1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

    def test_find_independent_confs(self):
        """
        test finding all the unique configurations of the pieces
        on the board where none of the pieces
        is in a position to take any of the others.
        :return: None.
        """
        self.setUp()
        solutions = self.board.find_independent_configurations()
        self.assertEqual(sorted(solutions), [1406L, 1469L, 1759L, 1951L])
