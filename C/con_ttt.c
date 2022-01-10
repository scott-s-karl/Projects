// Steven Karl
// 12/8/2021
// Tic Tac Toe - C
// Console Version
// End Header


// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
// Globals
int conv_board[9] = {6,7,8,11,12,13,16,17,18};

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

int boardHasEmpty(){

  // Loop through the board looking for empty squares
  for(int i = 0; i < 9; i++){
    if(board[conv_board[i]] == EMPTY){
      return 1;
    }
  }
  
  return 0;
}

void makeMove(int *board, const int loc, const player){
  board[loc] = player;
}

void gameLoop(){
  // Define local variables before the start of the game
  int game_over = 0;
  int cur_player = NOUGHTS;
  int last_move = 0;
  int board[25];

  // Initialize and print the starting board
  boardInit(&board[0]);
  boardPrint(&board[0]);

  // Start the game loop
  while(!game_over){
    if(cur_player == NOUGHTS){
      
    }
    else {
      boardPrint(&board[0]);
    }

    // Check if there are 3 in a row -- Win

    // Check if there is no spots left -- Draw

    game_over = 1;
  }
  
}

int main(int argc, const char *argv[]){
  // Seed random number generator for computer moves
  srand(time(NULL));

  // Run the Game
  gameLoop();
  
  return 0;
}
