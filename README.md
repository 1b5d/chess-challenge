# chess-challenge

The problem is to find all unique configurations of a set of normal chess pieces on a chess board with dimensions M×N where none of the pieces is in a position to take any of the others. Assuming the colour of the piece does not matter, and that there are no pawns among the pieces.

The program takes as input:
  - The dimensions of the board: M, N
  - The number of pieces of each type (King, Queen, Bishop, Rook and Knight) to try and place on the board.

As output, the program returns all the unique configurations for which all of the pieces can be placed on the board without threatening each other.

# The algorithm

- Initialize pieces on the board starting from the lap position, the lap position starts from the left-upper cell of the board and increases on each lap (a new lap occurs when there are no more available moves).
- Calculate the attacks for all the positions of the initial placement of the pieces.
- For each piece do the following 4 steps:
- Find the appropriate spot that is under attack from the minimum number of piecs (if there are several such spots chose all of them).
- Move the piece in that spot.
- Calculate the attacked positions.
- Check if there are remaining attacks. If there are not the algorithm has found a solution.
- Loop to find other solutions.
