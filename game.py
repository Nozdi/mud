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
        self.rooms = self.game.get_rooms()
        self.current_room = self.where_is()

    def where_is(self):
        return self.game.where_is(self.player)

    def get_room_object(self, room_name):
        for room in self.rooms:
            if room.name == room_name:
                return room

    @property
    def neighbors(self):
        return [self.rooms[index] for index in self.current_room.neighbors]

    def change_room(self, room_name):
        self.game.change_room(
            self.player,
            self.current_room,
            self.get_room_object(room_name)
            )
        self.current_room = self.where_is()

        print("You can go to:",
            ', '.join([room.name for room in self.neighbors]))



if __name__ == '__main__':
    Mud().change_room('kitchen')