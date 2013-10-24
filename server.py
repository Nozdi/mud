#!/usr/bin/env python3.3
from utils import initializer
import Pyro4

class Gamer:
    """
    The player
    """
    @initializer
    def __init__(self, name, items, room):
        """
        Da init
        """
        pass
    def pick_up(self):
        pass

    def drop(self):
        pass


class Room:
    """
    The room is on fire(maybe)
    """
    @initializer
    def __init__(self, name, description, items):
        """
        Da init2
        """
        pass

class Item:
    """
    For example bucket, cup or sandwich
    """
    @initializer
    def __init__(self, name, description):
        pass



if __name__ == '__main__':
    print(Room(1, 3, 4).description)