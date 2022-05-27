# Make File Setup
# Jacob Sorber tutorials referenced

# Setup complier
CC=gcc
CFLAGS=-g -Wall
SRC=src
OBJ=obj
BINDIR=bin
BIN= $(BINDIR)/TicTacToe
HDR=hdr
SUBMITNAME=TicTacToe.zip
SRCS=$(wildcard $(SRC)/*.c)
OBJS=$(patsubst $(SRC)/%.c, $(OBJ)/%.o, $(SRCS))

all: $(BIN)

release: CFLAGS=-Wall -O2 -DNDEBUG
release: clean
release: $(BIN)

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

$(OBJ)/%.o: $(SRC)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) -r $(BINDIR)/* $(OBJ)/* 
submit:
	$(RM) $(SUBMITNAME)
	zip $(SUBMITNAME) $(BIN)
