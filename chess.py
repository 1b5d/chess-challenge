"""
A program that lists all the unique configurations
of a set of normal chess pieces on a chess board
with dimensions MxN where none of the pieces
is in a position to take any of the others.
"""
import optparse
import time
from chess_exceptions import InvalidSetupException, InvalidArgumentException,\
    InvalidMoveException, ChessException
from board import Board
from pieces import King, Queen, Bishop, Rook, Knight


def parse_args():
    """
    Parse the command-line options of the game.
    :return: Tuple (Any, Any)
    """
    parser = optparse.OptionParser("usage: %prog [options] pieces list")
    parser.add_option("-m", "-m", dest="rows", default=8, type="int",
                      help="Number of rows of the board")
    parser.add_option("-n", "-n", dest="columns", default=8, type="int",
                      help="Number of columns on the board")
    parser.add_option("-K", "--kings", dest="kings", default=0, type="int",
                      help="Number of kings on the board")
    parser.add_option("-Q", "--queens", dest="queens", default=0, type="int",
                      help="Number of queens on the board")
    parser.add_option("-B", "--bishop", dest="bishops", default=0, type="int",
                      help="Number of bishops on the board")
    parser.add_option("-R", "--rooks", dest="rooks", default=0, type="int",
                      help="Number of rooks on the board")
    parser.add_option("-N", "--knights", dest="knights", default=0, type="int",
                      help="Number of knights on the board")
    return parser.parse_args()


def main():
    """
    Main function that initializes the program
    :return: None
    """
    (options, _) = parse_args()
    kings = options.kings
    queens = options.queens
    bishops = options.bishops
    rooks = options.rooks
    knights = options.knights
    rows = options.rows
    columns = options.columns
    print "Initializing board with %d rows and %d columns (%dx%d)" %\
          (rows, columns, rows, columns)
    print "Setting kings: %d, queens: %s, " \
          "bishops: %d, rooks: %s, knights: %d" %\
          (kings, queens, bishops, rooks, knights)

    pieces = []
    pieces.extend([King() for _ in xrange(kings)])
    pieces.extend([Queen() for _ in xrange(queens)])
    pieces.extend([Bishop() for _ in xrange(bishops)])
    pieces.extend([Rook() for _ in xrange(rooks)])
    pieces.extend([Knight() for _ in xrange(knights)])

    start_time = time.time()

    try:
        board = Board(rows, columns, pieces)

        solutions = board.find_independent_configurations(True)
        print "%d solutions found!" % len(solutions)

    except InvalidSetupException, exp:
        print "Bad setup of board/pieces, error was: {%s}" % exp.message
    except InvalidMoveException, exp:
        print "Invalid move was initiated, error was: {%s}" % exp.message
    except InvalidArgumentException, exp:
        print "Invalid argument was passed, error was: {%s}" % exp.message
    except ChessException, exp:
        print "Something wrong happened in the game, error was: {%s}" %\
            exp.message
    except BaseException, exp:
        print "Something wrong happened in the game, error was: {%s}" %\
            exp.message

    end_time = time.time()

    print "time: %.2f s" % (end_time - start_time)

if __name__ == '__main__':
    main()
