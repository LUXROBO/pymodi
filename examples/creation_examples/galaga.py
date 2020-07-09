import modi
import time

from playscii.games.galaga import GalagaManager

"""
HOW TO PLAY

   $ pip install pyplayscii --user
   $ python galaga.py

   Make your terminal screen big enough to play the game...
   Use the gyro to control the jet!
   Press the button to shoot down enemies!
"""
if __name__ == "__main__":
    bundle = modi.MODI()
    button = bundle.buttons[0]
    led = bundle.leds[0]
    gyro = bundle.gyros[0]
    game_manager = GalagaManager(gyro, button, led)
    game_manager.start()
    time.sleep(3)
