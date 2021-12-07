#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 04:21:22 2021

@author: mapc
"""

import itertools
from dataclasses import dataclass
from typing import Iterable, Protocol, runtime_checkable
from zope.interface import Interface, Attribute, implementer, invariant
from zope.interface.verify import verifyObject


class ICollidable(Interface):
    bounding_box = Attribute("Object's bounding box")
    invariant(lambda self: verifyObject(IBBox, self.bounding_box))


@runtime_checkable
class IBox(Protocol):
    x1: float
    y1: float
    x2: float
    y2: float


class IBBox(Interface):
    x1 = Attribute("lower-left x coordinate")
    y1 = Attribute("lower-left y coordinate")
    x2 = Attribute("upper-right x coordinate")
    y2 = Attribute("upper-right y coordinate")


@runtime_checkable
class ICollider(Protocol):
    @property
    def bounding_box(self) -> IBox: ...


def rects_collide(rect1: IBox, rect2: IBox):
    """Check collision between rectangles
    Rectangle coordinates:
        ┌───(x2, y2)
        │       │
      (x1, y1)──┘
    """
    return (
            rect1.x1 < rect2.x2 and
            rect1.x2 > rect2.x1 and
            rect1.y1 < rect2.y2 and
            rect1.y2 > rect2.y1
    )


def find_collisions(objects: Iterable[ICollider]):
    """ Determines collisions
    :parameter objects an iterable with the @ICollider
    :return collision
    usage: find_collision(Square(1,2))
    """
    for item in objects:
        if not isinstance(item, ICollider):
            raise TypeError(f"{item} is not a collider")
    return [
        (item1, item2)
        for item1, item2
        in itertools.combinations(objects, 2)
        if rects_collide(
            item1.bounding_box,
            item2.bounding_box
        )
    ]


@implementer(ICollidable)
@dataclass
class Square:
    x: float
    y: float
    size: float

    @property
    def bounding_box(self):
        """ Creates a bounding box
        :returns Box object """
        return Box(
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size
        )


@implementer(ICollidable)
@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float

    @property
    def bounding_box(self):
        """ Creates a bounding box
        :returns Box object """
        return Box(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height
        )


@implementer(ICollidable)
@dataclass
class Circle:
    x: float
    y: float
    radius: float

    @property
    def bounding_box(self):
        """ Creates a bounding box
        :returns Box object """
        return Box(
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )


@implementer(ICollidable)
@dataclass
class Box:
    x1: float
    y1: float
    x2: float
    y2: float


for collision in find_collisions([
    Square(0, 0, 10),
    Rect(5, 5, 20, 20),
    Square(15, 20, 5),
    Circle(1, 1, 2),
]):
    print(collision)
