import modi
from playscii import GameManager, GameObject
from random import randint
import time

"""
This example requires you to install playascii package
"""

PLAYER_RENDER = " O    \n" \
                "/|\\   \n" \
                "/ \\"
MODI_RENDER = "------\n" \
              "|MODI|\n" \
              "______"


class DodgeManager(GameManager):

    def __init__(self, controller):
        super().__init__((50, 20))

        self.player = self.GameObject(
            pos=(25, 2),
            render=PLAYER_RENDER)
        self.fire = self.GameObject(render=MODI_RENDER)
        self.gyro = controller.gyros[0]
        self.button = controller.buttons[0]

    def setup(self):
        self.set_title("PyMODI Dodge")
        self.add_object(self.player)
        self.add_object(self.fire)
        self.fire.x, self.fire.y = 25, 20

    def update(self):
        pitch = self.gyro.get_pitch()
        if pitch < -5 and self.player.x < 48:
            self.player.x += 30 * self.delta_time
        elif pitch > 5 and self.player.x > 0:
            self.player.x -= 30 * self.delta_time
        self.fire.y -= 15 * self.delta_time
        if self.fire.y < 0:
            self.fire.x, self.fire.y = randint(0, 40), 25
        if self.fire.y < 3 and (self.fire.x - 4 <= self.player.x <=
                                self.fire.x + 4):
            self.set_title("GAME OVER")
            self.set_flag('quit', True)

    class GameObject(GameObject):
        def update(self):
            pass


if __name__ == "__main__":
    bundle = modi.MODI(3)
    game_manager = DodgeManager(bundle)
    game_manager.start()
    time.sleep(3)
