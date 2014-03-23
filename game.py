#!/usr/bin/env python3.3

import curses
import Pyro4
from Pyro4 import threadutil
import sys

hardcoded_fire = """
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

sys.excepthook = Pyro4.util.excepthook

class Mud:
    def __init__(self):
        self.commands = {
            'go': self.change_room,
            'take': self.take_item,
            'drop': self.drop_item,
            'splash': self.splash,
            'commands': self.opt,
            'myitems': self.myitems,
            'roomitems': self.roomitems
            }
        self.game = Pyro4.core.Proxy('PYRONAME:game.server')
        self.player = None
        # self.game = Pyro4.core.Proxy('PYRONAME:game.server@150.254.68.89:9090')

    def where_is(self):
        return self.game.where_is(self.player)

    def message(self, msg, nick):
        if nick!=self.player:
            print(msg)

    @property
    def neighbors(self):
        return self.game.get_neighbors(self.current_room)

    def change_room(self, room_name):
        if room_name not in [room for room in self.neighbors]:
            print("There is no such a room")
        else:
            print(self.game.change_room(
                self.player,
                self.current_room,
                room_name
                ))
            self.current_room = self.where_is()
        print("You can go to:", ', '.join(self.neighbors))

    def take_item(self, item_name):
        print(*self.game.player_take_item(
            self.player,
            item_name,
            self.current_room
            ))

    def drop_item(self, item_name):
        print(*self.game.player_drop_item(
            self.player,
            item_name,
            self.current_room
            ))

    def splash(self):
        self.game.splash(self.player, self.current_room)

    def opt(self):
        opt = ", ".join(self.commands)
        print("Commands: " + opt + ", quit")

    def myitems(self):
        print(self.game.describe_player_items(self.player))

    def roomitems(self):
        print(self.game.describe_room_items(self.current_room))

    def start(self):
        print(hardcoded_fire)
        name = input("Type your name soldier: ").strip()
        self.player = self.game.add_player(name, self)
        self.current_room = self.where_is()
        print(self.game.describe_room(self.current_room))
        print("You can go to:",
            ', '.join(self.neighbors)
            )
        self.opt()

        try:
            while self.game.get_fire() > 0:
                print("\nFire level:", self.game.get_fire())
                cmd = input().strip().split(maxsplit=1)

                if cmd:
                    cmd[0] = cmd[0].lower()
                    if cmd[0] in self.commands.keys():
                        if len(cmd) == 1: self.commands[cmd[0]]()
                        else: self.commands[cmd[0]](cmd[1])
                    elif cmd[0] == "quit":
                        break

        except (EOFError, KeyboardInterrupt):
            pass

        finally:
            self.game.leave(self.player)
            self._pyroDaemon.shutdown()

        if(self.game.get_fire()<=0):
            print("FIRE IS GONE, CONGRATS!!")


class DaemonThread(threadutil.Thread):
    def __init__(self, mud):
        threadutil.Thread.__init__(self)
        self.mud=mud
        self.setDaemon(True)
    def run(self):
        with Pyro4.core.Daemon() as daemon:
            daemon.register(self.mud)
            daemon.requestLoop(lambda: self.mud.game.get_fire() > 0)

#"150.254.68.8", port=9090
if __name__ == '__main__':
    mud = Mud()
    daemonthred = DaemonThread(mud)
    daemonthred.start()
    mud.start()

