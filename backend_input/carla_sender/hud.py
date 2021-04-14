# ==============================================================================
# -- HUD -----------------------------------------------------------------------
# ==============================================================================


class HUD():
    def __init__(self, width, height):
        self.dim = (width, height)

    def on_world_tick(self, timestamp):
        pass

    def notification(self, text, seconds=2.0):
        pass

    def tick(self, world, clock):
        pass
