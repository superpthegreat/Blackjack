#!/usr/bin/env python3
# Anthony Soriano
# CSPC 386-03
# 2022-4-2
# soriano_anthony473@csu.fullerton.edu
# @anthony10154
#
# Lab 03-01
#
# This is my blackjack game program
#

"""This module is a blackjack game module that runs the game"""

from blackjack import game

if __name__ == "__main__":
    MAINGAME = game.BlackJackGame()
    MAINGAME.run()