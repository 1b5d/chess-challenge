"""
Includes the different kinds of exception that can occur in the app.
"""


class ChessException(Exception):
    pass


class InvalidSetupException(ChessException):
    pass


class InvalidMoveException(ChessException):
    pass


class InvalidArgumentException(ChessException):
    pass
