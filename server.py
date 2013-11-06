#!/usr/bin/env python3.3
from yaml import safe_load
from networkx import connected_watts_strogatz_graph as graph_gen
import Pyro4
import random

class Room:
    """
    The room is on fire (maybe)
    """
    def __init__(self, name, description, items = [], water_source=False):
        self.name = name
        self.description = description
        self.items = items
        self.water_source = water_source
        self.players = []

    def is_here(name):
        return name in [player.name for player in self.players]


class Player:
    """
    The player
    """
    def __init__(self, name, items = []):
        self.name = name
        self.items = items

    def drop(self, index):
        self.items.pop(index)


class Item:
    """
    Item class
    """
    def __init__(self, name, description, capacity=0):
        self.name = name
        self.description = description
        self.capacity = capacity

    def __repr__(self):
        return self.name



class Game:
    def __init__(self, connections_amount=2, connection_propability=0.2):
        self.fire = 1000
        with open("items.yaml") as data_file:
            items_data = safe_load(data_file)
            self.items = [ Item(elem['name'], elem['description'], elem['capacity'])
                          for elem in items_data ]

        with open("rooms.yaml") as data_file:
            rooms_data = safe_load(data_file)
            self.rooms = [ Room(
                            elem['name'],
                            elem['description'],
                            random.sample(self.items, random.randint(0,2)),
                            bool(elem.get('water_source', 0))
                                ) for elem in rooms_data ]

        self.graph = graph_gen(len(self.rooms), connections_amount,\
                               connection_propability)
        random.shuffle(self.rooms)
        for no, room in enumerate(self.rooms):
            room.id = no
            room.neighbors = self.graph.neighbors(no)

        for p in self.rooms:
            print(p.id, p.name, p.neighbors, p.items)

        self.fired_room = random.randint(1, len(rooms))

    def get_rooms():
        return self.rooms

    def where_is(name):
        for room in self.rooms:
            if room.is_here(name):
                return room


if __name__ == '__main__':
    with open("rooms.yaml") as data_file:
        rooms_data = safe_load(data_file)
    room_number = len(rooms_data)
    room_order = list(range(room_number))
    random.shuffle(room_order)
    print(room_order)
    #graph = connected_watts_strogatz_graph(room_number+1, 2,0.2) #so called small world graph
    print(rooms_data)
    print(Room(1, 3, 4).description)
    print(Item(1, 2).capacity)
    # initializator()
    Game()