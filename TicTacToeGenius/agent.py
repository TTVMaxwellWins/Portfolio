from typing import List, Any

import nielNetwork
import ttt
import numpy as np
import random as rand
from copy import deepcopy


class Agent:

    def __init__(s, eta, player, epsilon=.1, gamma=1, N=36):
        s.tieReward = -.1
        s.net = nielNetwork.Network([18, N, 9])
        s.eta = eta
        s.gamma = gamma
        s.epsilon = epsilon
        s.episode = []
        s.player = player

    def makeMove(s, state):
        copyState = deepcopy(state)
        action = s.policy(state)
        r = s.reward(state, action)
        s.episode.append((copyState, action, r))
        return action

    def succ(s, state, action):
        board, player = state
        assert board[action] == 0, "illegal move dingus!"
        succBoard = deepcopy(board)
        succBoard[action] = player
        return (succBoard, -player)

    def q(s, state):
        isEnd, winner = ttt.isEnd(state)
        if (isEnd):
            return np.zeros(len(state[0]))
        NNoutput = s.net.feedforward(NNinput(state))
        actualOutput = [NNoutput[j][0] for j in range(len(NNoutput))]
        return actualOutput

    def qtar(s, state, action, reward):
        if ttt.isEnd(state)[0]:
            return reward
        oppState = s.succ(state, action)
        isEnd, winner = ttt.isEnd(oppState)
        if isEnd:
            return winner*s.player
        oppMoves = s.actions(oppState)
        nextStates = [s.succ(oppState, move) for move in oppMoves]
        values = [np.max(s.q(nextState)) for nextState in nextStates]
        return reward + s.gamma * np.min(values)

    def actions(s, state):
        board, player = state
        actions = []
        j = 0
        while j < len(board):
            if board[j] == 0:
                actions.append(j)
            j += 1
        return actions

    def reward(s, state, action):
        isEnd, winner = ttt.isEnd(state)
        if isEnd:
            if winner == 0:
                return s.tieReward
            else:
                return float(winner * s.player)
        isEnd, winner = ttt.isEnd(s.succ(state, action))
        if isEnd:
            if winner == 0:
                return s.tieReward
            else:
                return float(winner * s.player)
        else:
            return 0.0

    def policy(s, state):
        if ttt.isEnd(state)[0]:
            return -1
        actions = s.actions(state)
        q = s.q(state)
        x = rand.random()
        if x < s.epsilon:
            j = rand.randint(0, len(actions) - 1)
            return actions[j]
        else:
            action = -1
            currMax = -1
            for j in actions:
                if q[j] > currMax:
                    currMax = q[j]
                    action = j
            return action

    def learn(s):
        while len(s.episode) > 0:
            state, action, reward = s.episode.pop()
            q = s.q(state)
            qtar = s.qtar(state, action, reward)
            q[action] = qtar
            s.net.update_mini_batch([(NNinput(state), q)], s.eta)


def NNinput(state):
    board, agent = state
    NNinput = []
    for x in board:
        if x == agent:
            NNinput = np.concatenate((NNinput, [1, 0]))
        elif x == -agent:
            NNinput = np.concatenate((NNinput, [0, 1]))
        elif x == 0:
            NNinput = np.concatenate((NNinput, [0, 0]))
        else:
            return "ya fucked up"
    return NNinput
