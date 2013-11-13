#!/usr/bin/env python3.3
from yaml import safe_load
from networkx import connected_watts_strogatz_graph as graph_gen #so called small world graph
import Pyro4
import random
from threading import Timer

def get_object(container, name):
    for elem in container:
        if elem.name == name:
            return elem

class Room:
    """
    The room is on fire (maybe)
    """
    def __init__(self, name, description, items = [], water_source=False):
        self.name = name #unique
        self.description = description
        self.items = items
        self.water_source = water_source
        self.players = []

    def is_here(self, player):
        return player in [player.name for player in self.players]

    def remove_player(self, player):
        who = None
        for gamer in self.players:
            if gamer.name == player.name:
                who = gamer
                break
        self.players.remove(who)
        return "\nPlayer %s left the %s" % (player, self.name)

    def add_player(self, player):
        self.players.append(player)
        return "\nPlayer %s join the %s" % (player, self.name)

    def describe_me(self):
        description = "You are in %s. People in room: %s\n%s" % (self.name,\
                      ' '.join(map(str, self.players)), self.description)
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
    def __init__(self, name, callback, items = []):
        self.name = name #unique
        self.items = items
        self.callback = callback

    def items_capacity(self):
        return sum([item.capacity for item in self.items])

    def take(self, item):
        self.items.append(item)

    def drop(self, item):
        self.items.remove(item)

    def __str__(self):
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
            room.neighbors = [self.rooms[index].name for index in \
                                                self.graph.neighbors(no)]

        #we start at 0
        self.fired_room = self.rooms[random.randint(1, len(self.rooms))].name

        self.spread_fire()

    def publish(self, room, msg, nick):
        for player in room.players:        # use a copy of the list
            try:
                player.callback.message(msg, nick)    # oneway call
            except Pyro4.errors.ConnectionClosedError:
                # connection dropped, remove the listener if it's still there
                # check for existence because other thread may have killed it already
                if player in room.players:
                    room.players.remove(player)
                    print('Removed dead player %s %s' % (player.name, player.callback))

    def leave(self, player):
        room = get_object(self.rooms, self.where_is(player))
        gamer = get_object(room.players, player)
        room.players.remove(gamer)
        for item in gamer.items:
            gamer.drop(item)
            room.drop_item(item)
        del gamer

    @property
    def players(self):
        gamer_list = []
        for room in self.rooms:
            gamer_list+=room.players
        return gamer_list

    def get_fire(self):
        return self.__fire

    def put_out_fire(self, quantity):
        self.__fire -= quantity

    def get_neighbors(self, player_room):
        current_room = get_object(self.rooms, player_room)
        return current_room.neighbors

    def spread_fire(self):
        if self.__fire != 0:
            self.__fire += 3
            Timer(3, self.spread_fire).start()

    def get_rooms(self):
        return [room.name for room in self.rooms]

    def where_is(self, player):
        for room in self.rooms:
            if room.is_here(player):
                return room.name

    def add_player(self, name, callback, items=[]):
        callback._pyroOneway.add('message')
        gamer = Player(name, callback, items)
        self.rooms[0].players.append(gamer)
        self.publish(self.rooms[0], "%s joined the game!" % (name,), name)
        return gamer.name

    def change_room(self, player_name, from_room, to_room):
        f = get_object(self.rooms, from_room)
        t = get_object(self.rooms, to_room)
        player = get_object(self.players, player_name)
        msg = f.remove_player(player)
        self.publish(f, msg, player_name)
        msg = t.add_player(player)
        self.publish(t, msg, player_name)
        ret = t.describe_me()
        if t.water_source:
            for item in player.items:
                item.is_full = True
                ret += "\n%s filled with water" % item.name
        if t.name == self.fired_room:
            ret += "\nFIIIREEEEE!!! Type 'splash'!"
        return ret

    def describe_room_items(self, room_name):
        room = get_object(self.rooms, room_name)
        msg = "\n".join(i.describe_me() for i in room.items)
        return msg or "There are no items here!"

    def describe_player_items(self, player_name):
        room_name = self.where_is(player_name)
        room = get_object(self.rooms, room_name)
        player = get_object(room.players, player_name)
        msg = "\n".join(i.describe_me() for i in player.items)
        return msg or "You have no items!"


    def describe_room(self, room_name):
        room = get_object(self.rooms, room_name)
        return room.describe_me()

    def player_take_item(self, player_name, item_name, room_name):
        player = get_object(self.players, player_name)
        room = get_object(self.rooms, room_name)
        item = room.get_item(item_name)
        if item is not None:
            if (player.items_capacity() + item.capacity > 80):
                room.drop_item(item)
                return ("Item is too big, if you really want it" +
                    "drop some items. Your items:",
                    [item.name for item in player.items])
            else:
                player.take(item)
                return ("You just took an item:", item.describe_me())
        else:
            return ("There is no such an item",)

    def player_drop_item(self, player_name, item_name, room_name):
        player = get_object(self.players, player_name)
        room = get_object(self.rooms, room_name)
        item = get_object(player.items, item_name)
        if item in player.items:
            player.drop(item)
            room.drop_item(item)
            return("You just dropped: ", item.name)
        else:
            return("You don't have such an item",)

    def splash(self, player_name, room_name):
        player = get_object(self.players, player_name)
        if player.items:
            substruct = sum([ item.capacity for item in player.items \
                    if item.is_full ])
            for item in player.items:
                item.is_full = False
            if room_name == self.fired_room:
                self.put_out_fire(substruct)


if __name__ == '__main__':
    # with Pyro4.core.Daemon(host="192.168.1.3", port=9092) as daemon:
    with Pyro4.core.Daemon() as daemon:
        with Pyro4.naming.locateNS() as ns:
            uri=daemon.register(Game())
            ns.register("game.server",uri)
        daemon.requestLoop()

