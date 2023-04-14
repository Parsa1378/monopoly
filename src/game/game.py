from models.player import Player
from agent.agent import Agent

# class Game:
    
#     def __init__(self,player:Player,agent:Agent) -> None:
#         self.player = player
#         self.agent = agent
#         self.current_palyer =  player
#         self.other_player = agent
    
#     def swap_turn(self) -> None:
#         self.current_palyer,self.other_player = self.other_player,self.current_palyer
    
#     def is_game_over(self) -> bool:
#         if len(self.player.properties)==0 and self.player.balance<1:
#             return True
#         return False
from copy import deepcopy
from board import Board
from models.cell import *
from math import ceil
import pandas as pd

# Define the Monopoly game class
class MonopolyGame:
    def __init__(self) -> None:
        # Initializing the game state
        self.current_player = 0  # Index of the current player in the players list
        self.other_player = 1
        self.game_over = False  # Boolean flag to indicate if the game is over
        self.board:Board = Board()


    def initialize_players(self,p1:str,p2:str) -> None:
        # Initializing two players with their starting positions, money, and other attributes
        player1 = Player(p1)
        player2 = Player(p2)
        self.players = [player1, player2]

    def take_action(self, action: int):
        # Updating the game state based on the action taken by the current player
        new_players = deepcopy(self.players)
        new_board = deepcopy(self.board)
        curr_player = new_players[self.current_player]
        curr_position = curr_player.position
        curr_prop = new_board[curr_position]
        # Do the appropriate changes for the action
        if action == 0:
            pass
        elif action == 1:
            curr_player.pay_money(curr_prop.price)
            curr_player.properties.append(curr_position)
            curr_prop.owner = self.current_player    
        elif action == 2:
            curr_player.pay_money(curr_prop.rent)
            new_players[curr_prop.owner].get_money(curr_prop.rent)
        elif action == 3:
            curr_prop.rent *= 1.5
            curr_prop.rent = ceil(curr_prop.rent)
            curr_prop.level += 1
        elif action == 4:
            curr_player.position = 10
            curr_player.is_in_jail = True
            curr_player.turns_in_jail += 1
        elif action == 5:
            curr_player.turns_in_jail += 1
        elif action == 6:
            curr_player.pay_money(50)
            curr_player.is_in_jail = False
            curr_player.turns_in_jail = 0
        elif action == 7:
            curr_player.is_in_jail = False
            curr_player.turns_in_jail = 0       
        return MonopolyGame(new_board, new_players, self.current_player, self.game_over)
    
    def get_possible_actions(self) -> list:
        # Get the possible actions available to the current player
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        curr_prop = self.board[curr_position]
        if curr_player.is_in_jail:
            if curr_player.rolled_doubles:
                return [7]
            if curr_player.turns_in_jail >= 3:
                return [6]
            return [5, 6]
        if curr_prop.ownable:
            if curr_prop.owner == self.current_player and curr_prop.upgradable:
                if curr_player.money > curr_prop.build_price:
                    return [3, 0]
                return [0]
            elif curr_prop.owner == None:
                if curr_player.money > curr_prop.price:
                    return [1, 0]
                return [0]
            else:
                return [2]
        if curr_prop.space == "GoToJail":
                return [4]
        return [0]
    
    def move_player(self, dice_result:int) -> None:
        # Pass if the player is in jail
        if self.players[self.current_player].is_in_jail:
            return
        curr_player = self.players[self.current_player]
        curr_position = curr_player.position
        # Update the player's position based on the dice roll result
        curr_position = (curr_position + dice_result) % len(self.board)
        curr_player.position = curr_position

    def is_terminal(self) -> bool:
        # Check if the game has reached a terminal state
        curr_player = self.players[self.current_player]
        if curr_player.money <= 0:
            return True
        return False
    
    def evaluate_utility(self) -> int:
        curr_player = self.players[self.current_player]
        curr_net_worth = curr_player.net_worth(self.board)
        # Evaluate the utility of the current game state for the current player
        return curr_net_worth

    def switch_player(self):
        # Switch to the next player's turn
        self.current_player += 1
        self.current_player %= 2
