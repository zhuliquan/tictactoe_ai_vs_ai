#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author : Administrator
# date   : 2018/6/26
import numpy as np
import pandas as pd
from game import State
from game import get_opponent
from typing import Tuple


class MiniMax:

    def __init__(self):
        pass

    def __str__(self):
        return "minimax ai"

    def take_action(self, current_state: State):

        def recurse(state: State) -> Tuple[int, object]:
            """
            根据当前状态返回一个当前最佳效应和所对应的动作
            :param state: 当前的状态
            :return: 返回一个元组 (utility action)
            """
            is_over, winner = state.get_state_result()
            if is_over:
                if winner == state.player:
                    return 1, None
                elif winner == get_opponent(state.player):
                    return -1, None
                else:
                    return 0, None

            available_actions = state.get_available_actions()
            values = [- recurse(state.get_next_state(action))[0] for action in available_actions]
            kws = pd.Series(data=values, index=available_actions)
            action = kws.idxmax()
            return kws[action], action

        _, action = recurse(current_state)
        return action


class AlphaBeta:

    def __init__(self):
        pass

    def __str__(self):
        return "minimax ai with alpha-beta purning"

    def take_action(self, current_state: State):
        ### 这个问题比较特殊可以这样剪枝
        # def recurse(state: State) -> Tuple[int, object]:
        #     """
        #     根据当前状态返回一个当前最佳效应和所对应的动作
        #     :param state: 当前的状态
        #     :return: 返回一个元组 (utility action)
        #     """
        #     is_over, winner = state.get_state_result()
        #     if is_over:
        #         if winner == state.player:
        #             return 1, None
        #         elif winner == get_opponent(state.player):
        #             return -1, None
        #         else:
        #             return 0, None
        #     available_actions = state.get_available_actions()
        #     final_value = -1
        #     final_action = available_actions[0]
        #     for action in available_actions:
        #         value = - recurse(state.get_next_state(action))[0]  # 由于下手是对手对于我的利益是负数
        #         if value == 1:  # 如果是已经可以胜利则返回
        #             final_value, final_action = value, action
        #             break
        #         elif value == 0:  # 如果是平局则有待观察
        #             final_value, final_action = value, action
        #     return final_value, final_action
        #
            ### 更加一般化alpha-beta剪枝

        self.player = current_state.player
        def recurse(state: State, alpha, beta) -> Tuple[int, object]:
            """
            根据当前状态返回一个当前最佳效应和所对应的动作
            :param state: 当前的状态
            :param alpha: 到当前状态的最开始玩家的收益下界
            :param beta:  到结束状态的最对手玩家的收益上界
            :return: 返回一个元组 (utility action)
            """
            is_over, winner = state.get_state_result()
            if is_over:
                if winner == self.player:
                    return 1, None
                elif winner == get_opponent(self.player):
                    return -1, None
                else:
                    return 0, None

            available_actions = state.get_available_actions()
            if state.player == self.player:
                max_value = (float("-inf"), None)
                for action in available_actions:
                    max_value = max(max_value, (recurse(state.get_next_state(action), alpha, beta)[0], action), key=lambda x:x[0])
                    alpha = max(alpha, max_value[0])
                    if beta <= alpha:
                        break
                return max_value
            elif state.player == get_opponent(self.player):
                min_value = (float("inf"), None)
                for action in available_actions:
                    min_value = min(min_value, (recurse(state.get_next_state(action), alpha, beta)[0], action), key=lambda x:x[0])
                    beta = min(beta, min_value[0])
                    if beta <= alpha:
                        break
                return min_value

        _, action = recurse(current_state, float("-inf"), float("inf"))
        return action


