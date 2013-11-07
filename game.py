#!/usr/bin/env python3.3

import curses
import Pyro4
from Pyro4 import threadutil
from server import Room, Player, Item

hardcoded_fire = u"""
 (                     )                           )       (    (   (
 )\ )       *   )   ( /(         *   )    *   ) ( /(       )\ ) )\ ))\ )
(()/(   ( ` )  /(   )\())    ( ` )  /(  ` )  /( )\())(    (()/((()/(()/((
 /(_))  )\ ( )(_)) ((_)\     )\ ( )(_))  ( )(_)|(_)\ )\    /(_))/(_))(_))\\
(_)) _ ((_|_(_())    ((_) _ ((_|_(_())  (_(_()) _((_|(_)  (_))_(_))(_))((_)
| _ \ | | |_   _|   / _ \| | | |_   _|  |_   _|| || | __| | |_ |_ _| _ \ __|
|  _/ |_| | | |    | (_) | |_| | | |      | |  | __ | _|  | __| | ||   / _|
|_|  \___/  |_|     \___/ \___/  |_|      |_|  |_||_|___| |_|  |___|_|_\___|

You start in radom room. You have to find some items with ability to filling
with liquids, then find the source of fire, and PUT OUT THE FIRE.
"""


# Pyro4.config.SERIALIZERS_ACCEPTED.add('json')
# Pyro4.config.SERIALIZER='json'
#print(hardcoded_fire)

class Mud:
    def __init__(self):
        self.commands = {
            'go': self.change_room,
            'take': self.take_item,
            'drop': self.drop_item,
            'splash': self.splash
            }
        self.game = Pyro4.core.Proxy('PYRONAME:game.server')


    def where_is(self):
        return self.game.where_is(self.player.name)

    def get_object(self, container, name):
        for elem in container:
            if elem.name == name:
                return elem

    @property
    def neighbors(self):
        return [self.rooms[index] for index in self.current_room.neighbors]

    def change_room(self, room_name):
        if room_name not in [room.name for room in self.neighbors]:
            print("There is no such a room")
            return

        self.game.change_room(
            self.player.name,
            self.current_room.name,
            room_name
            )
        self.current_room = self.where_is()

        print(self.current_room.describe_me())

        if self.current_room.water_source:
            for item in self.player.items:
                if item.capacity:
                    print(item, "filled with water")
                    item.is_full = True

        if self.current_room.id == self.game.fired_room:
            print("FIIREEE, type splash!")
        print("You can go to:",
            ', '.join([room.name for room in self.neighbors]))




    def take_item(self, item_name):
        item = self.current_room.get_item(item_name)
        if item is not None:
            if (self.player.items_capacity() + item.capacity > 80):
                print("Item is too big, if you really want it, drop some items")
                print("Your items:", self.player.items)
                self.current_room.drop_item(item)
            else:
                self.player.take(item)
                print(item.describe_me())
        else:
            print("There is no such an item")

    def drop_item(self, item_name):
        item = self.get_object(self.player.items, item_name)
        self.player.drop(item)
        self.current_room.drop_item(item)

    def splash(self):
        substruct = sum([ item.capacity for item in self.player.items \
            if item.is_full ])
        self.game.put_out_fire(substruct)

        for item in self.player.items:
            item.is_full = False

    def start(self):
        print(hardcoded_fire)
        name = input("Type your name soldier: ").strip()
        self.player = self.game.add_player(name)
        # print(self.game.where_is(self.player))
        self.rooms = tuple(self.game.get_rooms())
        print(self.player in self.rooms[0].players)
        print(self.rooms[0].players)
        print(self.player)
        self.current_room = self.where_is()
        print(self.current_room.describe_me())
        print("You can go to:",
            ', '.join([room.name for room in self.neighbors]))
        while self.game.get_fire() > 0:
            print(self.game.get_fire())
            cmd = input().strip().split(maxsplit=1)
            if cmd[0] in self.commands.keys():
                if len(cmd) == 1: self.commands[cmd[0]]()
                else: self.commands[cmd[0]](cmd[1])

        print("FIRE IS GONE, CONGRATS!!")


# class DaemonThread(threadutil.Thread):
#     def __init__(self, mud):
#         threadutil.Thread.__init__(self)
#         self.mud=mud
#         self.setDaemon(True)

#     def run(self):
#         with Pyro4.core.Daemon() as daemon:
#             daemon.register(self.mud)
#             daemon.requestLoop(lambda: True)

if __name__ == '__main__':
    mud = Mud()
    # daemonthred = DaemonThread(mud)
    # daemonthred.start()
    mud.start()

