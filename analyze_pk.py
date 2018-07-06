#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : zlq16
# date   : 2018/7/6
from game import Game
from mcts import MCTS
from minimax import AlphaBeta
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
RESULT = {0: "mcts player",1: "minimax player",2: "end in draw"}

def simulation(game, players, turn = 0) -> int:
    """
    模拟ai vs ai 对弈过程，返回模拟结果
    :param game: 游戏
    :param players: 游戏玩家
    :param turn: 开始轮次号
    :return: 模拟结果0 表示mcts_player 1 表示 minimax_player 2 表示平局
    """
    result = 2
    while True:
        current_state = game.state
        action = players[turn].take_action(current_state)
        game.step(action)
        game.render()
        print("###{0}在{1}落子###".format(players[turn], action))

        is_over, winner = game.game_result() # 判断结果

        if is_over:
            if winner:
                result = turn
                print("winner {0}".format(players[turn]))
            else:
                print("平局")
            break

        turn = (turn + 1) % 2 # 更新执棋方

    return result

if __name__ == "__main__":
    game = Game()
    mcts_player = MCTS()
    minimax_player = AlphaBeta()
    players = {0: mcts_player, 1: minimax_player}
    simulation_number = 10 # 博弈模拟的次数
    # 记录结果记录0 表示mcts_player 1 表示 minimax_player 2 表示平局
    trace = pd.Series(data=[0]*3, index=RESULT.values())

    for round in range(simulation_number):
        game.reset()
        print("in {0} round simulation".format(round+1))
        result = simulation(game, players, 1)
        trace[RESULT[result]] += 1
    x = range(3)
    plt.bar(x, height = trace.data)
    plt.xticks(x , trace.index)
    plt.show()




