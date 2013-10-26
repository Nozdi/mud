#!/usr/bin/env python3.3
from utils import initializer
from yaml import safe_load
from networkx import connected_watts_strogatz_graph
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
    def __init__(self, name, description, capacity=None):
        self.capacity = capacity



if __name__ == '__main__':
    with open("rooms.yaml") as data_file:
        rooms_data = safe_load(data_file)
    graph = connected_watts_strogatz_graph(5, 2,0.2) #so called small world graph
    print(rooms_data)
    print(Room(1, 3, 4).description)
    print(Item(1, 2).capacity)
