// Steven Karl
// con_ttt header file
// --------------------

// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Function Declaration
int min_max(int *board,
	    int side);

void board_init(int *board);

void board_print(int *board);

int board_has_empty(int *board);

void make_move(int *board,
	       const int loc,
	       const int player);

int get_human_move(const int *board);

int get_best_move(const int *board);


int get_winning_move(int *board,
		     const int side);

int get_computer_move(int *board,
		      int side);


int
check_win_dir(const int *board,
	      int cur_square,
	      int dir,
	      int cur_player_type);

int find_three_in_a_row_all_board(const int *board,
				  const int us);
int
evaluate_for_win(const int *board,
		 const int us);
int
find_three_in_a_row(const int *board,
		    int cur_square,
		    int cur_player_type);
void game_loop();  

