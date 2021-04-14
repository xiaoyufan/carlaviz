import carla


KEYS = {
    'K_W': 'w',
    'K_A': 'a',
    'K_S': 's',
    'K_D': 'd',
    'K_UP': 'ArrowUp',
    'K_DOWN': 'ArrowDown',
    'K_LEFT': 'ArrowLeft',
    'K_RIGHT': 'ArrowRight',
    'K_SPACE': ' ',
}


# ==============================================================================
# -- KeyboardControl -----------------------------------------------------------
# ==============================================================================


class KeyboardControl():
    """Class that handles keyboard input."""
    def __init__(self, world, start_in_autopilot):
        self._autopilot_enabled = start_in_autopilot

        if isinstance(world.player, carla.Vehicle):
            self._control = carla.VehicleControl()
            self._lights = carla.VehicleLightState.NONE
            world.player.set_autopilot(self._autopilot_enabled)
            world.player.set_light_state(self._lights)
        else:
            raise NotImplementedError("Actor type not supported")

        self._steer_cache = 0.0
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

    def validate_keys(self, key):
        return key in KEYS.values()

    def parse_keys(self, client, world, key, clock):
        if not self.validate_keys(key):
            return

        if self._autopilot_enabled:
            return

        if isinstance(self._control, carla.VehicleControl):
            current_lights = self._lights
            self._parse_vehicle_keys(key, clock.get_time())
            self._control.reverse = self._control.gear < 0

            # Set automatic control-related vehicle lights
            if self._control.brake:
                current_lights |= carla.VehicleLightState.Brake
            else: # Remove the Brake flag
                current_lights &= ~carla.VehicleLightState.Brake
            if self._control.reverse:
                current_lights |= carla.VehicleLightState.Reverse
            else: # Remove the Reverse flag
                current_lights &= ~carla.VehicleLightState.Reverse
            if current_lights != self._lights: # Change the light state only if necessary
                self._lights = current_lights
                world.player.set_light_state(carla.VehicleLightState(self._lights))

        world.player.apply_control(self._control)

    def _parse_vehicle_keys(self, key, milliseconds):
        if key == KEYS['K_UP'] or key == KEYS['K_W']:
            self._control.throttle = min(self._control.throttle + 0.01, 1)
        else:
            self._control.throttle = 0.0

        if key == KEYS['K_DOWN'] or key == KEYS['K_S']:
            self._control.brake = min(self._control.brake + 0.2, 1)
        else:
            self._control.brake = 0

        milliseconds = 100.0
        steer_increment = 5e-4 * milliseconds
        if key == KEYS['K_LEFT'] or key == KEYS['K_A']:
            if self._steer_cache > 0:
                self._steer_cache = 0
            else:
                self._steer_cache -= steer_increment
        elif key == KEYS['K_RIGHT'] or key == KEYS['K_D']:
            if self._steer_cache < 0:
                self._steer_cache = 0
            else:
                self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0
        self._steer_cache = min(0.7, max(-0.7, self._steer_cache))
        self._control.steer = round(self._steer_cache, 1)
        self._control.hand_brake = key == KEYS['K_SPACE']

