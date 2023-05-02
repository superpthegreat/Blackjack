#!/usr/bin/env python3

"""This module holds information about players"""
import pickle
import random


class Player:
    """Example Player class for a game."""

    def __init__(self, name, score=0, cash=10000):
        """Init a player with a name and a score."""
        self._name = name
        self._score = score
        self._id = random.randint(1, 100)
        self._cash = cash
        self._hand = []
        self._bet = 0
        self._dd_flag = False
        self._insurance_flag = False
        self._insurance = 0
        self._bust = False
        self._split = []
        self._split_flag = False
        self._split_bet = 0
        self._split_bust = False
        self._split_score = 0
        self._amHuman = True

    def bet(self):
        """return bet"""
        return self._bet

    def hand_set(self, card):
        """append a card"""
        self._hand.append(card)

    def hand(self):
        """print hand"""
        print(self._hand)

    @property
    def cash(self):
        """return the player's cash"""
        return self._cash

    @property
    def name(self):
        """Return the player's name"""
        return self._name

    @property
    def score(self):
        """Return the player's score."""
        return self._score

    @score.setter
    def score(self, points):
        """Add points to the player's score."""
        self._score += points

    def __str__(self):
        """Convert the Player to a printable string."""
        return f"Hi, my name is {self._name} ({self._id}) and my score is {self._score}"

    def __repr__(self):
        """Python representation."""
        return f"Player(name={self._name}, score={self._score})"

    def amComputer(self):
        """determines if computer"""
        return False


class Dealer(Player):
    """This class holds information about the Computer Player"""

    def __init__(self, name, score=0, cash=10000):
        self._name = name
        self._score = score
        self._id = random.randint(1, 100)
        self._cash = 10000
        self._hand = []
        self._bet = 0
        self._dd_flag = False
        self._insurance_flag = False
        self._insurance = 0
        self._bust = False
        self._split = []
        self._split_flag = False
        self._split_bet = 0
        self._amHuman = False

    def amComputer(self):
        return True


def to_file(pickle_file, players):
    """Write the list players to the file pickle_file."""
    with open(pickle_file, "wb") as file_handle:
        pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)


def from_file(pickle_file):
    """Read the contents of pickle_file, decode it, and return it as players."""
    with open(pickle_file, "rb") as file_handle:
        players = pickle.load(file_handle)
    return players


def main():
    """Main function; entry point."""
    names = [
        "Groucho",
        "Harpo",
        "Chico",
        "Zeppo",
        "Buster",
        "Charlie",
        "Stan",
        "Oliver",
    ]
    player_list = [
        Player(random.choice(names), random.randint(0, 25)) for _ in range(10)
    ]
    print("This is what is going into the pickle file:")
    print("\n".join(map(str, player_list)))
    to_file("players.pckl", player_list)
    # Set to None to prove we are getting the data from the file.
    player_list = None
    player_list = from_file("players.pckl")
    print("This is what we got back out of the pickle file:")
    print("\n".join(map(str, player_list)))


if __name__ == "__main__":
    main()
