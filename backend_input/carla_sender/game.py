import logging
import carla

from .world import World
from .hud import HUD
from .keyboard_control import KeyboardControl
from .clock import Clock


# ==============================================================================
# -- Game ---------------------------------------------------------------
# ==============================================================================


class Game:
    def __init__(self, args):
        self.args = args

    def start(self):
        self.client = carla.Client(self.args.carla_host, self.args.carla_port)
        self.client.set_timeout(2.0)
        logging.info(f'Listetning to Carla server on {self.args.carla_host}:{self.args.carla_port}')

        self.hud = HUD(self.args.width, self.args.height)
        self.world = World(self.client.get_world(), self.hud, self.args)
        self.controller = KeyboardControl(self.world, self.args.autopilot)

        self.clock = Clock()
    
    def handle_input(self, key):
        try:
            # self.clock.tick_busy_loop(60)

            if self.controller.parse_keys(self.client, self.world, key, self.clock):
                return
            self.world.tick(self.clock)
        except Exception as e:
            logging.error(e)
    
    def end(self):
        if (self.world and self.world.recording_enabled):
            self.client.stop_recorder()

        if self.world is not None:
            self.world.destroy()

        logging.info('Game ended.')


# ==============================================================================
# -- game_loop() ---------------------------------------------------------------
# ==============================================================================


def game_loop(args, keys):
    world = None

    try:
        client = carla.Client(args.carla_host, args.carla_port)
        client.set_timeout(2.0)

        hud = HUD(args.width, args.height)
        world = World(client.get_world(), hud, args)
        controller = KeyboardControl(world, args.autopilot)

        clock = Clock()
        while True:
            # clock.tick_busy_loop(60)

            if controller.parse_keys(client, world, keys, clock):
                return
            world.tick(clock)

    finally:
        if (world and world.recording_enabled):
            client.stop_recorder()

        if world is not None:
            world.destroy()

