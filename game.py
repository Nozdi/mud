#!/usr/bin/env python3.3

import curses
import Pyro4
from server import Game

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

#print(hardcoded_fire)

class Mud:
    def __init__(self):
        name = input("Type your name soldier: ").strip()
        self.game = Game()
        self.player = self.game.add_player(name)
        self.rooms = tuple(self.game.get_rooms())
        self.current_room = self.where_is()
        print(self.current_room.describe_me())
        print("You can go to:",
            ', '.join([room.name for room in self.neighbors]))

    def where_is(self):
        return self.game.where_is(self.player)

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
            self.player,
            self.current_room,
            self.get_object(self.rooms, room_name)
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
            if (self.player.items_capacity() + item.capacity
                > self.player.max_capacity):
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


def run_game():
    print(hardcoded_fire)
    mud = Mud()
    commands = {
        'go': mud.change_room,
        'take': mud.take_item,
        'drop': mud.drop_item,
        'splash': mud.splash
        }

    while mud.game.get_fire() > 0:
        print(mud.game.get_fire())
        cmd = input().strip().split(maxsplit=1)
        if cmd[0] in commands.keys():
            if len(cmd) == 1: commands[cmd[0]]()
            else: commands[cmd[0]](cmd[1])




if __name__ == '__main__':
    run_game()