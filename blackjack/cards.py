#!/usr/bin/env python3

"""This module is used to hold information about cards"""

from collections import namedtuple
from random import shuffle, randrange
from math import ceil

Card = namedtuple("Card", ["rank", "suit"])


def _str_card(card):
    """Convert a card to a nicely formatted string"""
    return f"{card.rank} of {card.suit}"


# redefine Card's __str__ to _str_card()
Card.__str__ = _str_card


class Deck:
    """Deck class to hold 52 French suited playing cards."""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Clubs Hearts Spades Diamonds".split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self):
        """Create one whole deck of cards."""
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

    def __len__(self):
        """Return the number of cards in the deck."""
        return len(self._cards)

    def __getitem__(self, position):
        """Return the card at the given position."""
        return self._cards[position]

    def shuffle(self, n_shuffles=1):
        """Shuffle the deck n times. Default is 1 time."""
        for _ in range(n_shuffles):
            shuffle(self._cards)

    def cut(self):
        """Cut the deck at approximately the half way point of the cards."""
        extra = ceil(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-extra, extra)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, n_cards=1):
        """Deal n cards. Default is 1 card."""
        return [self._cards.pop(0) for x in range(n_cards)]

    def merge(self, other_deck):
        """Merge the current deck with the deck passed as a parameter."""
        # Yes, we are accessing a protected member _cards of a client class.
        # We're breaking the rules. The alternative is to add an option to
        # remove the cards from the other_deck and via a method (i.e. deal())
        # and then add the cards to self._cards.
        # self._cards = self._cards + other_deck._cards
        self._cards = self._cards + other_deck.deal(len(other_deck))

    def __str__(self):
        """Convert the deck to a string."""
        return ", ".join(map(str, self._cards))


def card_value(card):
    """Return the numerical value of the rank of a given card."""
    return Deck.value_dict[card.rank]


# Methods to lookup a card's value or convert to an integer value
Card.value = card_value
Card.__int__ = card_value
