#!/usr/bin/env python3.3
from yaml import safe_load
from networkx import connected_watts_strogatz_graph as graph_gen #so called small world graph
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

    def is_here(self, player):
        return player in self.players

    def remove_player(self, player):
        self.players.remove(player)

    def add_player(self, player):
        self.players.append(player)


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
        self.__fire = 1000
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

        self.fired_room = random.randint(1, len(self.rooms)) #we start at 0

    def get_rooms(self):
        return self.rooms

    def where_is(self, player):
        for room in self.rooms:
            if room.is_here(player):
                return room

    def add_player(self, name, items=None):
        self.rooms[0].players.append(Player(name, items))

    def change_room(self, player, from_room, to_room):
        from_room.remove_player(player)
        to_room.add_player(player)


if __name__ == '__main__':
    da_game = Game()
    da_game.add_player("John")
    da_game.rooms[0].remove_player("John")
    print(da_game.rooms[0].players)

