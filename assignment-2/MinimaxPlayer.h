/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */

//Structure for holding coordinates for a move
struct Move {
	int row;
	int col;
};

class MinimaxPlayer : public Player {
public:

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 * Calls minimax_decision to generate an optimal move and changes row and col accordingly
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();

private:

	/**
	 * @param s The character symbol for the player whose successors we are generating
	 * @param b The board object for the current state of the board whose successors we are generating
	 * @return A vector of move-board pairs that are one valid move from the current board state
	 * Generates all the move-board pairs that can be reached in one move from the current board state for the current player
	 */
	std::vector<std::pair<Move, OthelloBoard>> get_successors(char s, OthelloBoard b);

	/**
	 * @param s The character symbol for the player whose successors we are generating
	 * @param b The board object for the current state of the board whose successors we are generating
	 * @return A vector of boards that are one valid move from the current board state
	 * Generates all the boards that can be reached in one move from the current board state for the current player
	 */
	std::vector<OthelloBoard> get_succ_state(char s, OthelloBoard b);

	/**
	 * @param b The board object for the current state of the board
	 * @return The optimal move that minimax found
	 * Generates the successor states for the current board state then uses the minimax algorithm to determine which successor is optimal.
	 */
	Move minimax_decision(OthelloBoard b);

	/**
	 * @param b The board object for the current state of the board where it is player 1's turn
	 * @return The maximum utility value of the successive move-board states generated
	 * Generates successors for the current state of player 1's moves and finds the maximum utility value of its successors from min's moves.
	 */
	int max_value(OthelloBoard b);

	/**
	 * @param b The board object for the current state of the board where it is player 2's turn
	 * @return The minimum utility value of the successive move-board states generated
	 * Generates successors for the current state of player 2's moves and finds the minimum utility value of its successors from max's moves.
	 */
	int min_value(OthelloBoard b);

	/**
	 * @param b A terminal board state
	 * @return The utility value of the board state
	 * Utility value is player 1's score minus player 2's score
	 */
	int utility(OthelloBoard b);

	/**
	 * @param b Board state for terminal state evaluation
	 * @return True if the board is a terminal state else false
	 * Checks if there are no legal moves remaining for player 1 and player 2
	 */
	bool terminal_test(OthelloBoard b);
};


#endif
