#!/usr/bin/env python3.3
from utils import initializer
from yaml import safe_load
from networkx import connected_watts_strogatz_graph
import Pyro4
import random

class Gamer:
    """
    The player
    """
    @initializer
    def __init__(self, name, room, items = []):
        """
        Da init
        """
        self.items = items
    def pick_up(self, item):
        self.items.append(item)

    def drop(self, index):
        self.items.pop(index)


class Room:
    """
    The room is on fire(maybe)
    """
    @initializer
    def __init__(self, name, description, items = []):
        """
        Da init2
        """
        self.items = items

class Item:
    """
    For example bucket, cup or sandwich
    """
    @initializer
    def __init__(self, name, description, capacity=None):
        self.capacity = capacity


FIRE = 1000

if __name__ == '__main__':
    with open("rooms.yaml") as data_file:
        rooms_data = safe_load(data_file)
    room_number = len(rooms_data)
    room_order = list(range(room_number))
    random.shuffle(room_order)
    print(room_order)
    graph = connected_watts_strogatz_graph(room_number+1, 2,0.2) #so called small world graph
    print(rooms_data)
    print(Room(1, 3, 4).description)
    print(Item(1, 2).capacity)
