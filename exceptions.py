"""
Includes the different kinds of exception that can occur in the app.
"""


class ChessException(Exception):
    """
    Base exception for all the exception that can be caught in the game.
    """
    pass


class InvalidSetupException(ChessException):
    """
    A type of exception that can be raised when
    the setup of the board/pieces is not valid.
    """
    pass


class InvalidMoveException(ChessException):
    """
    A type of exception that can be raised when we try to move
    a piece to a position where it should not be moved into.
    """
    pass


class InvalidArgumentException(ChessException):
    """
    A type of exeption that can be raised upon passing
    invalid arguments to functions inside the game, such as move().
    """
    pass
