/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include "MinimaxPlayer.h"

using std::vector;

/*THE MINIMAX ALGORITHM
 	function MINIMAX_DECISION(state) returns an action
 		inputs: state, current state in game
 		v = MAX_VALUE(state)
 		return the action in SUCCESSORS(state) with value v
 		
 	function MAX_VALUE(state) returns a utility value
 		if TERMINAL_TEST(state) then return UTILITY(state)
 		v = -InfinitySUCCESSORS(state)
 		for a, s in  do
 			v = MAX(v, MIN_VALUE(s)) //The maximum value of the bunch
 			return v
 
 	function MIN_VALUE(state) returns a utility value
 		if TERMINAL_TEST(state) then return UTILITY(state)
 		v = Infinity
 		for a, s in SUCCESSORS(state) do
 			v = MIN(v, MAX_VALUE(s)) //The minimum value of the bunch
 		return v
*/

/*
 Does a depth first exploration of the game tree
*/

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) {
    Move move = minimax_decision(*b);
    col = move.col;
    row = move.row;
}

Move MinimaxPlayer::minimax_decision(OthelloBoard b)
{
	Move v; //Optimal move that will be returned
	int minimax_util, util_min, util_max; //Integer buffers for temporary minimax, largest and smallest utility values
	util_min = 0x7FFFFFFF; //Largest value for a 32 bit signed integer buffer
	util_max = 0x80000000; //Smallest value for a 32 bit signed integer buffer

	//Generate the move-board successor states from the current board state
	std::vector<std::pair<Move, OthelloBoard>> succ = get_successors(symbol, b);
	std::vector<std::pair<Move, OthelloBoard>>::iterator it;

	bool is_p1 = (symbol == b.get_p1_symbol()); //Is true if the current player is player 1

	//Iterate through this state's possible moves and choose the one with the best minimax value depending on who the player is
	for(it = succ.begin(); it != succ.end(); it++)
	{
		if(is_p1) //If we are player one and are maximizing
		{
			//We are checking player two's move here so we call the min function
			minimax_util = min_value((*it).second);
			if(minimax_util >= util_max) //If the minimax value we obtained here is greater than our current utility max, update util_max
			{
				util_max = minimax_util;
				v = (*it).first;
			}
		}
		else //If we are player two and are minimizing
		{
			//We are checking player one's move here so we call the max function
			minimax_util = max_value((*it).second);
			if(minimax_util < util_min) //If the minimax value we obtained here is less than our current utility min, update util_min
			{
				util_min = minimax_util;
				v = (*it).first;
			}
		}
	}

	return v;
}

int MinimaxPlayer::max_value(OthelloBoard b)
{
	//If the current state is a terminal state then evaluate it with the utility funciton.
	if(terminal_test(b))
		return utility(b);

	int util_val = (signed int)0x80000000, temp; //Smallest number in a 32 bit signed integer buffer

	//Get the successor states from the current board state for minimax evaluation
	std::vector<OthelloBoard> succ = get_succ_state(b.get_p1_symbol(), b);
	std::vector<OthelloBoard>::iterator it;

	//Iterate through the successor states
	for(it = succ.begin(); it != succ.end(); it++)
	{
		temp = min_value(*it); //Get the utility values that minimum returns
		if (util_val < temp) //Get the maximum value of min's utility values
		{
			util_val = temp;
		}
	}

	//If there are no successors then check min's moves on the current unchanged board state
	if(succ.empty())
	{
		util_val = min_value(b);
	}
	
	return util_val; //Return the maximum utility value obtained from this state
}

int MinimaxPlayer::min_value(OthelloBoard b)
{
	//If the current state is a terminal state then evaluate it with the utility funciton.
	if(terminal_test(b))
		return utility(b);

	int util_val = (signed int)0x7FFFFFFF, temp; //Largest number in a 32 bit signed integer buffer

	//Get the successor states from the current board state for minimax evaluation
	std::vector<OthelloBoard> succ = get_succ_state(b.get_p2_symbol(), b);
	std::vector<OthelloBoard>::iterator it;

	//Iterate through the successor states
	for(it = succ.begin(); it != succ.end(); it++)
	{
		temp = max_value(*it); //Get the utility values that maximum returns
		if (util_val >= temp) //Get the minimum value of max's utility values
		{
			util_val = temp;
		}
	}

	//If there are no successors then check max's moves on the current unchanged board state
	if(succ.empty())
	{
		util_val = max_value(b);
	}
	
	return util_val; //Return the minimum utility value obtained from this state
}

int MinimaxPlayer::utility(OthelloBoard b)
{
	//Get the player scores
	int p1_score = b.count_score(b.get_p1_symbol());
	int p2_score = b.count_score(b.get_p2_symbol());

	return p1_score - p2_score; //A greater margin of victory indicates a better utility. Will be negative if p2 wins and positive if p1 wins
}

std::vector<std::pair<Move, OthelloBoard>> MinimaxPlayer::get_successors(char s, OthelloBoard b) {

	//4x4 board exhaustive search for valid moves
	std::vector<std::pair<Move, OthelloBoard>> successors;
	for(int i = 0; i < 4; i++) {
		for(int j = 0; j < 4; j++) {
			if(b.is_legal_move(j, i, s)) {
				//If the move is legal, generate the state and add to the vector of states
				OthelloBoard state = b;
				Move move = {i, j};
				state.play_move(j, i, s); //Set the successor board to the new valid state
				successors.push_back(std::pair<Move, OthelloBoard>(move, state)); //Add successor to the vector of successors
			}
		}
	}
	return successors;

}

std::vector<OthelloBoard> MinimaxPlayer::get_succ_state(char s, OthelloBoard b) {

	//4x4 board exhaustive search for valid moves
	std::vector<OthelloBoard> successors;
	for(int i = 0; i < 4; i++) {
		for(int j = 0; j < 4; j++) {
			if(b.is_legal_move(j, i, s)) {
				//If the move is legal, generate the state and add to the vector of states
				OthelloBoard state = b;
				state.play_move(j, i, s); //Set the successor board to the new valid state
				successors.push_back(state); //Add successor to the vector of successors
			}
		}
	}
	return successors;
}

bool MinimaxPlayer::terminal_test(OthelloBoard b)
{
	return !(b.has_legal_moves_remaining(b.get_p1_symbol()) || b.has_legal_moves_remaining(b.get_p2_symbol()));
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
