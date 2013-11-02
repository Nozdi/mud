#!/usr/bin/env python3.3

import curses
import Pyro4

hardcoded_fire = u"""
 (                     )  (    (                )       (    (   (
 )\ )       *   )   ( /(  )\ ) )\ )    *   ) ( /(       )\ ) )\ ))\ )
(()/(   ( ` )  /(   )\())(()/((()/(  ` )  /( )\())(    (()/((()/(()/((
 /(_))  )\ ( )(_)) ((_)\  /(_))/(_))  ( )(_)|(_)\ )\    /(_))/(_))(_))\\
(_)) _ ((_|_(_())    ((_)(_))_(_))_| (_(_()) _((_|(_)  (_))_(_))(_))((_)
| _ \ | | |_   _|   / _ \| |_ | |_   |_   _|| || | __| | |_ |_ _| _ \ __|
|  _/ |_| | | |    | (_) | __|| __|    | |  | __ | _|  | __| | ||   / _|
|_|  \___/  |_|     \___/|_|  |_|      |_|  |_||_|___| |_|  |___|_|_\___|
ZMIENIC NA PUT OUT THE FIRE - od gościa z samolotu.
"""

print(hardcoded_fire)

class Player:
    """
    The player
    """
    def __init__(self, name, room, items = []):
        self.name = name
        self.room = room
        self.items = items

    def drop(self, index):
        self.items.pop(index)

