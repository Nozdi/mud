#!/usr/bin/env python3.3
from yaml import safe_load
from networkx import connected_watts_strogatz_graph as graph_gen #so called small world graph
import Pyro4
import random
from threading import Timer

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

    def describe_me(self):
        description = "You are in %s with %s\n%s" % (self.name, ' '.join(self.players), self.description)
        if self.items:
            description += "\nitems: %s" % (self.items,)
        if self.water_source:
            description += "\nYou can take water from here!!"
        return description

    def get_item(self, name):
        number = None
        for no, elem in enumerate(self.items):
            if elem.name == name:
                number = no
                break
        return self.items.pop(number) if number is not None else None

    def drop_item(self, item):
        self.items.append(item)


class Player:
    """
    The player
    """
    def __init__(self, name, items = []):
        Player.max_capacity = 80
        self.name = name
        self.items = items

    def items_capacity(self):
        return sum([item.capacity for item in self.items])

    def take(self, item):
        self.items.append(item)

    def drop(self, item):
        self.items.remove(item)

    def __repl__(self):
        return self.name


class Item:
    """
    Item class
    """
    def __init__(self, name, description, capacity=0):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.is_full = False

    def describe_me(self):
        description = "This is %s. %s" % (self.name, self.description)
        if self.capacity > 0:
            description += "\nThis item has %s capacity." % (self.capacity,)
        if self.is_full:
            description += "\nIt is full of water."
        return description

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
        self.spread_fire()

    def get_fire(self):
        return self.__fire

    def put_out_fire(self, quantity):
        self.__fire -= quantity

    def spread_fire(self):
        if self.__fire != 0:
            self.__fire += 3
            Timer(3, self.spread_fire).start()

    def get_rooms(self):
        return self.rooms

    def where_is(self, player):
        for room in self.rooms:
            if room.is_here(player):
                return room

    def add_player(self, name, items=[]):
        gamer = Player(name, items)
        self.rooms[0].players.append(gamer)
        return gamer

    def change_room(self, player, from_room, to_room):
        from_room.remove_player(player)
        to_room.add_player(player)



if __name__ == '__main__':
    da_game = Game()
    da_game.add_player("John")
    # da_game.rooms[0].remove_player("John")
    print(da_game.rooms[0].describe_me())
    print(da_game.rooms[0].players)
    # import time
    # time.sleep(10)
    # print(da_game.get_fire())

