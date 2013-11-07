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
        print(hardcoded_fire)
        name = input("Type your name soldier: ").strip()
        self.game = Game()
        self.player = self.game.add_player(name)
        self.rooms = tuple(self.game.get_rooms())
        self.current_room = self.where_is()
        self.max_capacity = 80

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
        self.game.change_room(
            self.player,
            self.current_room,
            self.get_object(self.rooms, room_name)
            )
        self.current_room = self.where_is()
        print(self.current_room.describe_me())
        print("You can go to:",
            ', '.join([room.name for room in self.neighbors]))

    def take_item(self, item_name):
        item = self.current_room.get_item(item_name)
        if item is not None:
            print(item)
            if self.player.items_capacity() + item.capacity > self.max_capacity:
                print("Item is to big, if you really want it, drop some items")
                self.current_room.drop_item(item)
            else:
                self.player.take(item)
        else:
            print("There is no such an item")

    def drop_item(self, item_name):
        item = self.get_object(self.player.items, item_name)
        self.player.drop(item)
        self.current_room.drop_item(item)


def run_game():
    game = Mud()
    commands = {
        'go': game.change_room,
        'take': game.take_item,
        'drop': game.drop_item,
        'splash': None
        }

    while True:
        cmd = input().strip().split(maxsplit=1)
        if cmd[0] in commands.keys():
            if len(cmd) == 1: commands[cmd[0]]()
            else: commands[cmd[0]](cmd[1])




if __name__ == '__main__':
    run_game()