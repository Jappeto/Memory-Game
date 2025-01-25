#!/usr/bin/env python3

# ----------------------------------------------------------------------
# CardButton.py
# Dave Reed
# 10/14/2024
# ----------------------------------------------------------------------

from __future__ import annotations
from typing import List
from graphics import Point, Circle, Rectangle, GraphWin, GraphicsObject

class CardButton:

    """
    a button for displaying either the back of a card or a card with various shapes
    """

    styles = ("circle", "square")
    colors = ("blue", "red")
    counts = (1, 2)
    shapeYOffsets = ((0,), (-0.25, 0.25))

    def __init__(self, style: str, color: str, count: int, width: float, window: GraphWin):
        """
        create CardButton with specified parameters
        :param style: either "square" or "circle" indicating shape(s) to display on the card
        :param color: color for the shapes
        :param count: number of shapes on a card (currently should be 1 or 2)
        :param width: width of the button (the height used is 1.5 * width)
        :param window: GraphWin the card is to be drawn in
        """
        self._style: str = style
        self._color: str = color
        self._count: int = count
        self._window: GraphWin = window
        height = width * 1.5

        rect = Rectangle(Point(0, 0), Point(width, height))
        rect.setFill("gray")
        rect.setOutline("gray")
        self._shapes: List[GraphicsObject] = [rect]
        self._backShown = True

        yOffsets = CardButton.shapeYOffsets[count - 1]
        cx = width / 2.0
        cy = height / 2.0
        shapeWidth = height / 6
        offsetScale = height
        for y in yOffsets:
            shape = self._makeShape(self._style, Point(cx, cy + y * offsetScale), shapeWidth)
            self._shapes.append(shape)

    def _makeShape(self, style: str, center: Point, halfWidth: float) -> GraphicsObject:
        """
        helper method to create the shape pattern for the front of the card
        :param style: either "square" or "circle" indicating shape(s) to display on the card
        :param center: center Point for the shape
        :param halfWidth: half the width of the Card
        :return: the Circle or Rectangle created for the shape
        """
        if style == "circle":
            shape = Circle(center, halfWidth)
        # if add more styles, update this code to a series of elif for each shape
        else: # elif style == "square":
            x, y = center.getX(), center.getY()
            p1 = Point(x - halfWidth, y - halfWidth)
            p2 = Point(x + halfWidth, y + halfWidth)
            shape = Rectangle(p1, p2)

        shape.setOutline(self._color)
        shape.setFill(self._color)
        return shape

    def move(self, dx: float, dy: float):
        """
        move all the shapes for the card by the specified amounts
        :param dx: x amount to move all the shapes in the card
        :param dy: y amount to move all the shapes in the card
        :return: None
        """
        for shape in self._shapes:
            shape.move(dx, dy)

    def draw(self):
        """
        for initially drawing the card - just draws the rectangle for the back of the card
        :return: None
        """
        self._shapes[0].draw(self._window)

    def flipCard(self):
        """
        flip the card over by drawing/undrawing the appropriate shapes
        :return: None
        """
        if self._backShown:
            # draw the shapes for the front on top of the Rectangle for the card
            for shape in self._shapes[1:]:
                shape.draw(self._window)
            # draw the front of the card as white
            self._shapes[0].setFill("white")
        else:
            # remove all the shapes for the front of the card
            for shape in self._shapes[1:]:
                shape.undraw()
            # draw the back as gray
            self._shapes[0].setFill("gray")
        self._backShown = not self._backShown

    def undraw(self):
        """
        undraw all the shapes (including the back for the card); used when card is removed from screen
        :return: None
        """
        # first undraw all the shapes so they aren't visible briefly before undrawing the back of card Rectangle
        if not self._backShown:
            for shape in self._shapes[1:]:
                shape.undraw()
        # undraw the first shape that is the back of card Rectangle
        self._shapes[0].undraw()

    def bounds(self) -> (Point, Point):
        """
        :return: tuple containing the min and max corner Points for the
        current location of the CardButton
        """
        rect: Rectangle = self._shapes[0]
        rectP1 = rect.getP1()
        rectP2 = rect.getP2()
        # get the min and max points of the rectangle
        x1, x2 = rectP1.getX(), rectP2.getX()
        minX, maxX = min(x1, x2), max(x1, x2)
        y1, y2 = rectP1.getY(), rectP2.getY()
        minY, maxY = min(y1, y2), max(y1, y2)
        return Point(minX, minY), Point(maxX, maxY)

    def center(self) -> Point:
        """
        :return: current center Point for the CardButton
        """
        rect: Rectangle = self._shapes[0]
        return rect.getCenter()

    def clicked(self, pt: Point) -> bool:
        """
        :param pt: the Point to check if its inside the CardButton's current location on the screen
        :return: True if the point is inside the CardButton's current location or False otherwise
        """
        p1, p2 = self.bounds()
        return p1.getX() <= pt.getX() <= p2.getX() and p1.getY() <= pt.getY() <= p2.getY()

    def isFlipped(self) -> bool:
        """
        :return: True if the card is currently flipped to show the front, False otherwise
        """
        return not self._backShown

    def __eq__(self, other: CardButton):
        """
        :param other: CardButton to compare
        :return: True if both CardButton's have the same style, color, and number of shapes; False otherwise
        """
        return self._style == other._style and self._color == other._color and self._count == other._count

    def __ne__(self, other: CardButton):
        """
        :param other: CardButton to compare
        :return: False if both CardButton's have the same style, color, and number of shapes; True otherwise
        """
        return self._style != other._style or self._color != other._color or self._count != other._count
        # return not (self == other)

# ----------------------------------------------------------------------

def main():
    win = GraphWin("CardButton", 400, 400)
    b1 = CardButton("square", "red", 2, 100, win)
    b1.move(150, 100)
    b1.draw()
    count = 0
    while count < 3:
        pt = win.getMouse()
        if b1.clicked(pt):
            b1.flipCard()
            count += 1
    win.getMouse()
    b1.undraw()
    win.getMouse()

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
