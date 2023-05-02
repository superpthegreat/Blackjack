#!/usr/bin/env python3

"""This module holds blackjack game mechanics"""

import time
import random

from .cards import Deck, card_value
from .player import Player, Dealer, to_file, from_file


class BlackJackGame:
    """this class holds information about the game"""

    def __init__(self):
        self._players = []

    """runs game"""

    def run(self):
        """get number of players"""
        ans = input("Would you like to import a file?[y/n]")
        if ans == "y":
            player_list = from_file("players.pckl")
            self._players.extend(player_list)
        else:
            num_players = int(input("How many players? [1-4] "))
            for i in range(num_players):
                name = input("What is your name? ")
                time.sleep(0.5)
                self._players.append(Player(name, 0))
            self._players.append(Dealer("Dealer"))

        print(self._players)
        current_player_index = 0
        print("All new players start with $10,000 ")
        d = Deck()
        for x in range(7):
            b = Deck()
            d.merge(b)
        d.shuffle(7)
        d.cut()

        first_deal = 0
        length = len(self._players) * 2
        end_flag = False
        insurance = False
        bet_flag = True

        while True:
            turn_up = True
            split_hand_flag = False
            if first_deal != length:
                print(d.__len__())
                cp = self._players[current_player_index]
                print("")
                print("Player {} is up!".format(cp.name))
                if cp._cash < 1:
                    print("A donor has given you $10,000. Be gracious")
                    cp._cash = 10000
                isPlayer = cp.amComputer()
                if isPlayer is False:
                    if bet_flag is True:
                        print("Current Cash: {}".format(cp._cash))
                        bet = int(input("How much would you like to bet? "))
                        cp._bet = bet
                        print("You betted: {}".format(cp._bet))
                time.sleep(1)
                cp.hand_set(d.deal(1))
                isPlayer = cp.amComputer()
                if isPlayer is True:
                    print(cp._hand[0])
                    insur = card_value(cp._hand[0].__getitem__(0))
                    if insur == 10 or cp._hand[0].__getitem__(0).rank == "Ace":
                        insurance = True
                    bet_flag = False
                else:
                    cp.hand()
            else:
                cp = self._players[current_player_index]
                time.sleep(1)
                print("")
                print("Player {} is up!".format(cp.name))
                print("Current hand is ")
                cp.hand()
                print("Adds up to:")
                hand_total = 0
                for x in cp._hand:
                    if x.__getitem__(0).rank == "Ace":
                        if (card_value(x.__getitem__(0)) + hand_total) < 21:
                            hand_total += 11
                    else:
                        hand_total += card_value(x.__getitem__(0))
                print(hand_total)
                isPlayer = cp.amComputer()
                if cp._split_flag is False and isPlayer is False:
                    card_rank = cp._hand[0].__getitem__(0).rank
                    card_rank2 = cp._hand[1].__getitem__(0).rank
                    if card_rank == card_rank2:
                        answer = input("Would you like to split?[y/n]")
                        if answer == "y":
                            cp._split_flag = True
                            cp._split.extend(cp._hand)
                            del cp._hand[1]
                            del cp._split[1]
                            print("I have two hands now!")
                            print("Hand 1")
                            cp.hand()
                            print("Hand 2")
                            print(cp._split)
                isPlayer = cp.amComputer()
                if isPlayer is False:
                    if insurance is True:
                        answer = input("Would you like to buy insurance?[y/n]")
                        if answer == "y":
                            cp._insurance_flag = True
                            answer = int(input("How much would you like to bet? "))
                            cp._insurance = answer
                    answer = input("Would you like to double down?[y/n]")
                    if answer == "y":
                        cp._dd_flag = True
                        cp._bet = cp._bet * 2
                        print("Current Bet Total: {}".format(cp._bet))
                        cp.hand_set(d.deal(1))
                        cp.hand()
                        total = 0
                        for x in cp._hand:
                            if x.__getitem__(0).rank == "Ace":
                                if (card_value(x.__getitem__(0)) + total) < 21:
                                    total += 11
                            else:
                                total += card_value(x.__getitem__(0))
                        print("Total: {}".format(total))
                        if total > 21:
                            cp._bust = True
                            print("Bust")
                    if cp._split_flag is True:
                        answer = input(
                            "Would you like to double down on split hand?[y/n]"
                        )
                        if answer == "y":
                            cp._bet = cp._bet * 2
                            cp._split.append(d.deal(1))
                            print(cp._split)
                            total = 0
                            for x in cp._split:
                                if x.__getitem__(0).rank == "Ace":
                                    if (card_value(x.__getitem__(0)) + total) < 21:
                                        total += 11
                                else:
                                    total += card_value(x.__getitem__(0))
                            print("Total: {}".format(total))
                            if total > 21:
                                cp._bust = True
                                print("Bust")

                else:
                    print("i am dealer")
                while turn_up is True:
                    if cp._dd_flag is True:
                        break
                    isPlayer = cp.amComputer()
                    if isPlayer is True:
                        total = 0
                        for x in cp._hand:
                            if x.__getitem__(0).rank == "Ace":
                                if (card_value(x.__getitem__(0)) + total) < 21:
                                    total += 11
                            else:
                                total += card_value(x.__getitem__(0))
                        cp.hand()
                        print("Total: {}".format(total))
                        if total == 21:
                            print("Dealer has a natural 21")
                            print("All players who made insurance bet has won")
                            for x in self._players:
                                if x._insurance_flag is True:
                                    x._cash = x._cash + x._insurance
                                    print("Player: {}".format(x._name))
                                    print("Current Cash: {}".format(x._cash))
                        if total != 21:
                            print("Dealer does not have a natural 21")
                            print("All players who made insurance bet has lost")
                            for x in self._players:
                                if x._insurance_flag is True:
                                    x._cash = x._cash - x._insurance
                                    print("Player: {}".format(x._name))
                                    print("Current Cash: {}".format(x._cash))

                        while total < 17:
                            cp.hand_set(d.deal(1))
                            cp.hand()
                            total = 0
                            for x in cp._hand:
                                if x.__getitem__(0).rank == "Ace":
                                    if (card_value(x.__getitem__(0)) + total) < 21:
                                        total += 11
                                else:
                                    total += card_value(x.__getitem__(0))
                        if total > 21:
                            cp._bust = True
                            print("Bust")
                            end_flag = True

                        total = 0
                        for x in cp._hand:
                            if x.__getitem__(0).rank == "Ace":
                                if (card_value(x.__getitem__(0)) + total) < 21:
                                    total += 11
                            else:
                                total += card_value(x.__getitem__(0))
                        print("Total: {}".format(total))
                        for x in self._players:
                            if x._amHuman is True:
                                print("Player: {}".format(x._name))
                                if cp._bust is True:
                                    print("Dealer has busted")
                                    if x._bust is True:
                                        x._cash = x._cash - x._bet
                                    else:
                                        x._cash = x._cash + x._bet
                                else:
                                    if x._split_flag is True:
                                        if x._split_score == total:
                                            print(
                                                "A push has occured with this player's split hand"
                                            )
                                            x._cash = x._cash + x._split_bet
                                        if (
                                            x._split_score > total
                                            and x._split_score <= 21
                                        ):
                                            print(
                                                "Dealer has lost to this player's split hand"
                                            )
                                            x._cash = x._cash + x._split_bet
                                        else:
                                            print(
                                                "Dealer has won against this player's split hand"
                                            )
                                            x._cash = x._cash - x._split_bet
                                    if x._score == total:
                                        print("A push has occured")
                                        x._cash = x._cash + x._bet
                                    if x._score > total and x._score <= 21:
                                        print("Dealer has lost to this player")
                                        x._cash = x._cash + x._bet
                                    else:
                                        print("Dealer has won against this player")
                                        x._cash = x._cash - x._bet
                                print("Current Cash: {}".format(x._cash))

                        end_flag = True
                        break
                    else:
                        answer = input("Would you like to hit or stand? [hit/stand]")
                        if answer == "hit" and split_hand_flag is False:
                            turn_up = True
                            cp.hand_set(d.deal(1))
                            total = 0
                            for x in cp._hand:
                                if x.__getitem__(0).rank == "Ace":
                                    if (card_value(x.__getitem__(0)) + total) < 21:
                                        total += 11
                                else:
                                    total += card_value(x.__getitem__(0))
                            print("Total: {}".format(total))
                            if total > 21:
                                cp._bust = True
                                print("Bust")
                                turn_up = False
                                if cp._split_flag is True:
                                    turn_up = True
                                    split_hand_flag = True
                            if total == 21:
                                print("You have gotten 21!")
                                turn_up = False
                                if cp._split_flag is True:
                                    turn_up = True
                                    split_hand_flag = True
                        if answer == "stand" and split_hand_flag is False:
                            total = 0
                            for x in cp._hand:
                                if x.__getitem__(0).rank == "Ace":
                                    if (card_value(x.__getitem__(0)) + total) < 21:
                                        total += 11
                                else:
                                    total += card_value(x.__getitem__(0))
                            print("Total: {}".format(total))
                            cp._score = total
                            turn_up = False
                            if cp._split_flag is True:
                                turn_up = True
                                split_hand_flag = True
                        if split_hand_flag is True:
                            print("This works")
                            time.sleep(1)
                            split_ans = input(
                                "Would you like to hit or stand? For your split hand? [hit/stand]"
                            )
                            if split_ans == "hit":
                                cp._split.append(d.deal(1))
                                split_total = 0
                                for x in cp._split:
                                    if x.__getitem__(0).rank == "Ace":
                                        if (
                                            card_value(x.__getitem__(0)) + split_total
                                        ) < 21:
                                            split_total += 11
                                    else:
                                        split_total += card_value(x.__getitem__(0))
                                print("Split Total: {}".format(split_total))
                                cp._split_score = split_total
                                if split_total > 21:
                                    cp._split_bust = True
                                    cp._cash = cp._cash - cp._split_bet
                                    print("Split Hand Bust")
                                    print("Curent Cash: {}".format(cp._cash))
                                    turn_up = False
                                    split_hand_flag = False
                                    break
                                if split_total == 21:
                                    print("You have gotten 21!")
                                    turn_up = False
                                    split_hand_flag = False
                                    break
                            if split_ans == "stand":
                                split_total = 0
                                for x in cp._split:
                                    if x.__getitem__(0).rank == "Ace":
                                        if (
                                            card_value(x.__getitem__(0)) + split_total
                                        ) < 21:
                                            split_total += 11
                                    else:
                                        split_total += card_value(x.__getitem__(0))
                                print("Split Total: {}".format(split_total))
                                cp._split_score = split_total
                                turn_up = False
                                split_hand_flag = False

            if end_flag is True:
                answer = input("Do you want to play again?[y/n]")
                if answer == "y":
                    bet_flag = True
                    first_deal = -1
                    end_flag = False
                    turn_up = True
                    for x in self._players:
                        x._hand.clear()
                        x._bust = False
                        x._dd_flag = False
                else:
                    for x in self._players:
                        x._hand.clear()
                        x._split.clear()
                        x._split_score = 0
                        x._bust = False
                        x._dd_flag = False
                        x._insurance_flag = False
                        x._split_flag = False
                        x._score = 0
                    player_list = []
                    player_list.extend(self._players)
                    to_file("players.pckl", player_list)
                    break
            if first_deal == length:
                print("End of turn")
            else:
                first_deal += 1
            current_player_index = (current_player_index + 1) % len(self._players)
            if d.__len__() == 80:
                d = Deck()
                for x in range(7):
                    b = Deck()
                    d.merge(b)
                d.shuffle(7)
                d.cut()
