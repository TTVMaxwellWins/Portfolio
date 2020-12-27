import numpy as np
import agent
import ttt

class TicTacToe:

    def __init__(s):
        s.state = (np.zeros(9), 1)
        s.policies = {1: s.agentPolicy, -1: s.humanPolicy}
        s.players = [1,-1]
        s.size = 3
        s.currPlayer = 0
        s.X = s.players[0]
        s.O = s.players[1]
        s.agent = agent.Agent(.69, 1,.1)


        s.printBoard(s.state)
        while True:
            s.gameLoop(s.state)

    def agentPolicy(s, state):
        board, player = state
        action = s.agent.makeMove(state)
        if action == -1:
            s.agent.learn()
            return action
        assert board[action] == 0, "the AI fucked up and picked an illegal move"
        return action
    def humanPolicy(s, state):
        board, player = state
        while True:
            action = int(input("make a move bitch"))
            if board[action] == 0:
                break
        return action

    def printBoard(s, state):
        for row in range(0, s.size):
            print(" {0} | {1} | {2} \n".format(s.squareAsString(row, 0, state), s.squareAsString(row, 1, state),
                                               s.squareAsString(row, 2, state)))
            if (row < s.size - 1):
                print("______________\n")

    def squareAsString(s, x, y, state):
        board, player = state
        z = int(board[3*x + y])
        if z == s.X:
            return "X"
        elif z == s.O:
            return "O"
        else:
            return " "

    def stopGame(s):
        print("Game over!")

    def makeMove(s,state, x):
        board, player = state
        assert board[x] == 0, "woah there, something fucked up"
        if board[x] == 0:
            board[x] = player
            s.state = (board, -player)
            return True
        else:
            print("That square is taken, try again!")
            return False

    def gameLoop(s, state):
        policy = s.policies[s.players[s.currPlayer]]
        action = policy(state)
        s.makeMove(state, action)
        s.printBoard(state)
        s.currPlayer = (s.currPlayer + 1) % len(s.players)
        isEnd, winner = ttt.isEnd(state)
        if isEnd:
            s.stopGame()

#returns 2-tuple (isEndState, player who won / draw = 0)
def isEnd(state):
    board, player = state
    if board[0] == board[4] and board[0] == board[8] and not board[0] == 0:
        return True, board[0]
    elif board[2] == board[4] and board[2] == board[6] and not board[2] == 0:
        return True, board[2]
    for j in range(3):
        if board[j] == board[j+3] and board[j] == board[j+6] and not board[j] == 0:
            return True, board[j]
    for j in [0,3,6]:
        if board[j] == board[j+1] and board[j] == board[j+2] and not board[j] == 0:
            return True, board[j]
    for j in board:
         if j == 0:
             return False, 0
    return True, 0


  # def checkIfPlayerWon(s, player):
    #     for i in range(0, s.size):
    #         if s.board[i][0] == player and s.board[i][1] == player and s.board[i][2] == player:
    #             print("player {0} wins!".format(str(player)))
    #             return True
    #         if s.board[0][i] == player and s.board[1][i] == player and s.board[2][i] == player:
    #             print("player {0} wins!".format(str(player)))
    #             return True
    #     if s.board[0][0] == player and s.board[1][1] == player and s.board[2][2] == player:
    #         print("player {0} wins!".format(str(player)))
    #         return True
    #     if s.board[0][2] == player and s.board[1][1] == player and s.board[2][0] == player:
    #         print("player {0} wins!".format(str(player)))
    #         return True
    #     return False

    # def checkForEnd(s):
    #     #     for player in s.players:
    #     #         if s.checkIfPlayerWon(player):
    #     #             s.stopGame()
    #     #     # check for draw
    #     #     for x in range(0, s.size):
    #     #         for y in range(0, s.size):
    #     #             if s.board[x][y] == 0:
    #     #                 return
    #     #     print("Game is a draw")
    #     #     s.stopGame()