// Steven Karl
// 12/8/2021
// Tic Tac Toe - C
// Console Version
// ----------------------


// Includes
#include "../hdr/con_ttt.h"

// Globals
int conv_board[9] = {6,7,8,11,12,13,16,17,18}; // Array that shows the playable squares
const int MIDDLE = 4;
const int CORNERS[4] = {0,2,6,8};
const int win_directions[4] = {1, 5, 4, 6}; // Array that has the increments to step by for different wins

int ply = 0; // How many moves deep into the search tree
int positions; // How many actual positions were searched
int max_ply = 0; // Used to keep track of how many moves deep we are

// Enumerated Constants 0, 1, 2, 3 etc...
enum {NOUGHTS, CROSSES, BORDER, EMPTY};
enum {HUMANWIN, COMPWIN, DRAW};


// Board Layout - Size of 25
/*
  0,1,2,3,4, 5, 6,7,8, 9,10, 11,12,13, 14,15, 16,17,18, 19,20, 21,22,23,24
  :,:,:,:,:
  :,6,7,8,:
  :,11,12,13,:
  :,16,17,18,:
  :,:,:,:,:

  0,1,2,3,4,
  5,6,7,8,9,
  10,11,12,13,14,
  15,16,17,18,19,
  20,21,22,23,24
*/

int
min_max(int *board, int side){
  // Check for a win

  // Generate all moves for the side

  // Loop through moves, make move and then call minmax to get the move score

  // Asses move

  // End by returning the best score move

  // Define local variables
  int move_list[9]; // possible moves
  int move_count = 0; // Moves made
  int best_score = -2; // Current best score of the moves
  int score = -2; // Current temp score for a move
  int best_move = -1; // current best move location
  int move; // current move

  // Update max depth to look for move if we have gone farther
  if(ply > max_ply){
    max_ply = ply;
  }
  // Update the positions taken because we have covered another option
  positions++;

  if(ply > 0){
    score = evaluate_for_win(board, side);
    if(score != 0){
      return score;
    }
  }
  // Fill the move list
  for(int i = 0; i < 9; ++i){
    if(board[conv_board[i]] == EMPTY){
      move_list[move_count++] = conv_board[i];
    }
  }

  // Loop through all moves available
  for(int i = 0; i < move_count; ++i){
    move = move_list[i];
    board[move] = side;

    ply++;
    score = -min_max(board, side^1);
    if(score > best_score){
      best_score = score;
      best_move = move;
    }
    board[move] = EMPTY;
    ply--;
  }
  if(move_count == 0){
    best_score = find_three_in_a_row_all_board(board, side);
  }
  if(ply !=0){
    return best_score;
  }
  else{
    return best_move;
  }
}

void
board_init(int *board){
  // Fill the board with walls
  for(int i = 0; i < 25; i++){
    board[i] = BORDER;
  }

  // Replace the walls with empties
  for(int i = 0; i < 9; i++){
    board[conv_board[i]] = EMPTY;
  }
}

void
board_print(int *board){
  // Define local variables
  char print_chars[] = "OX|-";

  // Print out the header
  printf("\n\nBoard:\n\n");

  // Loop and print the board
  for(int i = 0; i < 9; i++){

    if(i != 0 && i % 3 == 0){
      printf("\n\n");
    }
    printf("%4c",print_chars[board[conv_board[i]]]);
  }
  printf("\n");
}

int
board_has_empty(int *board){

  // Loop through the board squares
  for(int i = 0; i < 9; i++){
    // Check for an empty square
    if(board[conv_board[i]] == EMPTY){
      return 1;
    }
  }
  // Return False/0 if no empty was found
  return 0;
}

void
make_move(int *board, const int loc, const int player){
  board[loc] = player;
}

int
get_human_move(const int *board){
  // Make an array of chars for the user input
  char user_input[4];

  // Define local variables
  int move_valid = 0;
  int move = -1;

  // Loop to the get the user input
  while(move_valid == 0){
    // Message asking user for input
    printf("Please enter a move from 1 to 9: ");

    // Use fgets to the get the input
    // store in - user input
    // read from - stdin
    // max length - 3
    // fflush stdin
    fgets(user_input, 3, stdin);

    // This is to make sure that if the user enters a string like
    // asbasdfbsadfb
    /*
    This way we flush stdin to get rid of remaining characters so we don't
    keep looking for inputs
    */
    fflush(stdin);

    // Check for a single number and a return character
    if(strlen(user_input) != 2){
      printf("Invalid input - too long. Must be number from 1 - 9.\n");
      continue;
    }
    // Use sscanf to format the string and make sure that it matches our format of 1 number
    if(sscanf(user_input, "%d", &move) != 1){
      move = -1;
      printf("Invalid input. Must be a number from 1 - 9.\n");
      continue;
    }
    // Check that the move integer is in the right range
    if(move < 1 || move > 9){
      move = -1;
      printf("Invalid input. Must be a number from 1 - 9. Number out of bounds\n");
      continue;
    }

    // Move is valid but we need to scale it down to the 0 - 8 range we use
    move--;

    // Check if the square is available to use
    if(board[conv_board[move]] != EMPTY){
      move = -1;
      printf("Invalid input. The location chosen is already occupied\n");
      continue;
    }
    move_valid = 1;
  }
  // Print out the move being made
  printf("Making move -> %d\n", (move+1));

  // Return the integer location of the move on the conversion board
  return conv_board[move];
}

int
get_best_move(const int *board){
  // Get the middle
  int our_move = conv_board[MIDDLE];
  if(board[our_move] == EMPTY){
    return our_move;
  }

  // Get open corner
  our_move = -1;
  for(int i = 0; i < 4; i++){
    our_move = conv_board[CORNERS[i]];
    if(board[our_move] == EMPTY){
      break;
    }
    our_move = -1;
  } // End For
  return our_move;
}

int
get_winning_move(int *board,
		 const int side){
  int our_move = -1;
  int win_found = 0;

  for(int i = 0; i < 9; ++i){
    if(board[conv_board[i]] == EMPTY){
      our_move = conv_board[i];
      board[conv_board[i]] = side;
      if(find_three_in_a_row(board,
			     our_move,
			     side) == 3){

	win_found = 1;
      }
      board[our_move] = EMPTY;
      if(win_found == 1){
	break;
      }
      our_move = -1;
    }
  }
  return our_move;
}

int
get_computer_move(int *board,
		  const int side){
  ply = 0;
  positions = 0;
  max_ply = 0;
  int best = min_max(board, side);
  printf("Finished searching\nPosition: %d\nMax Depth: %d\nBest Move: %d\n\n", positions, max_ply, best);
  return best;
}

int
check_win_dir(const int *board,
	      int cur_square,
	      int dir,
	      int cur_player_type){

  int cur_player_count = 0;
  while(board[cur_square] != BORDER){
    if(board[cur_square] != cur_player_type){
      break;
    }
    cur_player_count++;
    cur_square+=dir;
  }
  return cur_player_count;
}

int
find_three_in_a_row(const int *board,
		    int cur_square,
		    int cur_player_type){
  // Define locals
  int cur_player_count = 1;

  // Loop for all win directions pos an neg
  for(int i = 0; i < 4; i++){
    cur_player_count += check_win_dir(board,
				     cur_square + win_directions[i],
				     win_directions[i],
				     cur_player_type);
    cur_player_count += check_win_dir(board,
				     cur_square - win_directions[i],
				     (-1*win_directions[i]),
				     cur_player_type);
    if(cur_player_count == 3){
      break;
    }
    cur_player_count = 1;
  }
  return cur_player_count;
}

int
find_three_in_a_row_all_board(const int *board, const int us){
  // Define locals
  int win_found = 0;

  // Check board
  for(int i = 0; i < 9; ++i){
    if(board[conv_board[i]] == us){
      if(find_three_in_a_row(board, conv_board[i], us) == 3){
	win_found = 1;
	break;
      }
    }
  }
  return win_found;
}

int
evaluate_for_win(const int *board, const int us){
  if(find_three_in_a_row_all_board(board, us) != 0){
    return 1;
  }
  if(find_three_in_a_row_all_board(board, us^1) !=0){
    return -1;
  }

  return 0;

}

void
game_loop(){
  // Define local variables before the start of the game
  int game_over = 0;
  int cur_player = CROSSES;
  int last_move = 0;
  int board[25];

  // Initialize and print the starting board
  board_init(&board[0]);
  board_print(&board[0]);

  // Start the game loop
  while(!game_over){

    // Check what player made the move
    if(cur_player == NOUGHTS){
      // Get the move from the player
      last_move = get_human_move(&board[0]);

      // Make the move
      make_move(&board[0], last_move, cur_player);

      // Change the side
      cur_player = CROSSES;

    }
    else {
      // Get the move from the computer
      last_move = get_computer_move(&board[0], cur_player);

      // Make the move
      make_move(&board[0], last_move, cur_player);

      // Change the side
      cur_player = NOUGHTS;
      board_print(&board[0]);
    }

    // Check if there are 3 in a row -- Win
    if(find_three_in_a_row(board, last_move, cur_player ^ 1) == 3){
      game_over = 1;
      if(cur_player == NOUGHTS){
	printf("Crosses Wins! -> Game Over\n");
      }
      else{
	printf("Noughts Wins! -> Game Over\n");
      }
      board_print(&board[0]);
    }
    // Check if there is no spots left -- Draw
    if(!game_over && !board_has_empty(board)){
      printf("Draw -> Game Over\n");
      game_over = 1;
      board_print(&board[0]);
    }
  } // End While
}

int main(int argc, const char *argv[]){
  // Seed random number generator for computer moves
  srand(time(NULL));

  // Run the Game
  game_loop();

  return 0;
}
