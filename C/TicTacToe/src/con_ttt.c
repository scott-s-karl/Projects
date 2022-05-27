// Steven Karl
// 12/8/2021
// Tic Tac Toe - C
// Console Version
// ----------------------


// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Globals
int conv_board[9] = {6,7,8,11,12,13,16,17,18};

// Enumerated Constants 0, 1, 2, 3 etc...
enum {NOUGHTS, CROSSES, BORDER, EMPTY};
enum {HUMANWIN, COMPWIN, DRAW};


// Board Layout
/*
  0,1,2,3,4, 5, 6,7,8, 9,10, 11,12,13, 14,15, 16,17,18, 19,20, 21,22,23,24
  :,:,:,:,:
  :,6,7,8,:
  :,11,12,13,:
  :,16,17,18,:
  :,:,:,:,:

*/


void boardInit(int *board){
  // Fill the board with walls
  for(int i = 0; i < 25; i++){
    board[i] = BORDER;
  }

  // Replace the walls with empties
  for(int i = 0; i < 9; i++){
    board[conv_board[i]] = EMPTY;
  }
}

void boardPrint(int *board){
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

int boardHasEmpty(int *board){

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

void makeMove(int *board, const int loc, const int player){
  board[loc] = player;
}

int getHumanMove(const int *board){
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

int getComputerMove(const int *board){
  // Local Variables
  int index = 0;
  int num_free = 0;
  int available_moves[9];
  int rand_move = 0;

  /* 2,4,8
     availableMoves[0] = 2 numFree++ -> 1
     availableMoves[1] = 4 numFree++ -> 2
     availableMoves[2] = 8 numFree++ -> 3
     
     rand() % numFree gives 0 to 2 
     rand number from 0 to 2 and return availableMoves[rand]
  */

  // Loop through the board squares
  for(index = 0; index < 9; ++index){
    // Check if the current square on the board is empty
    if(board[conv_board[index]] == EMPTY){
      available_moves[num_free++] = conv_board[index];
    }
  }

  // Get a random number from the array of possible moves
  rand_move = (rand() % num_free);

  return available_moves[rand_move];
}

void gameLoop(){
  // Define local variables before the start of the game
  int game_over = 0;
  int cur_player = NOUGHTS;
  int last_move = 0;
  int board[25];
  int move_loc;
  
  // Initialize and print the starting board
  boardInit(&board[0]);
  boardPrint(&board[0]);

  // Start the game loop
  while(!game_over){

    // Check what player made the move
    if(cur_player == NOUGHTS){
      // Get the move from the player
      last_move = getHumanMove(&board[0]);

      // Make the move
      makeMove(&board[0], last_move, cur_player);

      // Change the side
      cur_player = CROSSES;
      
    }
    else {
      // Get the move from the computer
      last_move = getComputerMove(&board[0]);

      // Make the move
      makeMove(&board[0], move_loc, cur_player);

      // Change the side
      cur_player = NOUGHTS;
      
      // Print the board out
      boardPrint(&board[0]);
    }

    // Check if there are 3 in a row -- Win
    
    // Check if there is no spots left -- Draw
    if(!boardHasEmpty(board)){
      printf("Game Over\n");
      game_over = 1;
      printf("The game is a draw\n");
    }
  }
  
}

int main(int argc, const char *argv[]){
  // Seed random number generator for computer moves
  srand(time(NULL));

  // Run the Game
  gameLoop();
  
  return 0;
}
