

# ----------------------------------------------------------------------
# MemoryGame.py
# Jacob Reppeto
# 10/15/2024
# ----------------------------------------------------------------------

from typing import List, Optional
from random import shuffle
from graphics import GraphWin, Point
from CardButton import CardButton

import time

class MemoryGame:

    """
    class for playing the memory game
    """

    def __init__(self, window: GraphWin):
        """
        creates two copies of each card and stores them in a list in a random order
        :param window: GraphWin for drawing board
        """
        self._cards: List[CardButton] = []
        self._window: GraphWin = window
        # nested for loops for each of the three options
        for style in CardButton.styles: # ("circle", "square"):
            for color in CardButton.colors: # ("red", "blue"):
                for count in CardButton.counts: # (1, 2):
                    # create two cards of the specified style
                    c = CardButton(style, color, count, 1, window)
                    self._cards.append(c)
                    c = CardButton(style, color, count, 1, window)
                    self._cards.append(c)
        # shuffle the cards
        shuffle(self._cards)

    def createUI(self):
        """
        positions the cards on the screen and draws each one with the back side up
        :return: None
        """
        rows = len(self._cards) // 4
        # set coords for width 1
        self._window.setCoords(0, 0, 11, rows * 3 - 1)
        # position of first card
        x, y = 1.75, 1
        for i in range(len(self._cards)):
            card = self._cards[i]
            card.move(x, y)
            card.draw()
            # move over for next card
            x += 2
            # ever fourth card, move down and back to first card column
            if i % 4 == 3:
                x = 1.75
                y += 2.5

    def removeCard(self, card: CardButton):
        """
        removes the specified CardButton from the screen and from the remaining cards to match
        :param card: CardButton to remove
        :return: None
        """
        for cards in self._cards:
            if cards == card:
                self._cards.remove(card)
        card.undraw()

    def processClick(self, click: Point) -> Optional[CardButton]:
        """
        Returns the CardButton that was clicked or None if click is not inside any CardButton.
        """
        for card in self._cards:
            if card.clicked(click):
                return card
        return None

    def selectCard(self) -> CardButton:
        """
        Keeps getting mouse clicks in the GraphWin until a remaining CardButton is clicked.
        :return: The CardButton that was clicked.
        """
        while True:
            selectedCards = self.processClick(self._window.getMouse())
            if selectedCards is not None:
                return selectedCards

    def processCards(self, card1: CardButton, card2: CardButton):
        """
        processes the two selected cards;
        if they match, wait 0.5 seconds and then remove them
        if they don't match, wait 1.5 seconds and then flip both of them
        :param card1: a CardButton that was selected/flipped
        :param card2: a CardButton that was selected/flipped
        :return: True if the cards matched, False if they do not match
        """

        if card1 == card2:
            time.sleep(0.5)
            self.removeCard(card1)
            self.removeCard(card2)
            return True

        else:
            time.sleep(1.5)
            card1.flipCard()
            card2.flipCard()
            return False

    def play(self):
        """
        Repeatedly get two selected cards until the user has matched all the cards.
        :return: None
        """
        while len(self._cards) > 0:
            card1 = self.selectCard()
            card1.flipCard()

            while True:
                card2 = self.selectCard()
                if card1 is not card2: # checks to make sure they dont click the same card
                    card2.flipCard()
                    break

            self.processCards(card1, card2)


        self._window.getMouse()
        self._window.close()


def main():
    window = GraphWin("Memory", 600, 600)
    view = MemoryGame(window)
    view.createUI()
    view.play()


# ----------------------------------------------------------------------


if __name__ == "__main__":
    main()