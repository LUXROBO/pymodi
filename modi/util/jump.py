import time
from playscii import GameObject, GameManager
from playscii.input import Input


class JumpManager(GameManager):
    def __init__(self):
        super().__init__((100, 6))
        self.dino = MODIDino()
        self.obstacle = Obstacle(self)
        self.game_over = False
        self.status = ""
        self.score = 0
        self.scoreboard = GameObject(pos=(50, 5), render='0')

    def setup(self):
        self.add_object(self.dino)
        self.add_object(self.obstacle)
        self.add_object(self.scoreboard)

    def update(self):
        if Input.get_key_down('q'):
            self.quit()
        self.scoreboard.render = str(self.score)
        if self.game_over:
            self.set_title("Game Over!!")
            time.sleep(3)
            self.game_over = False
            self.score = 0
            self.obstacle.speed = 30
            self.obstacle.x = 160
        self.set_title(self.status)
        if self.obstacle.on_collision(self.dino):
            self.dino.vel = 0
            self.obstacle.speed = 0
            self.dino.y = 0
            self.game_over = True


class MODIDino(GameObject):
    def __init__(self):
        super().__init__(pos=(10, 0), render='MODI', size=(4, 1))
        self.touch_ground = True
        self.vel = 0

    def update(self):
        if Input.get_key_down('space'):
            if self.touch_ground:
                self.vel = 15
                self.touch_ground = False
        if not self.touch_ground:
            self.y += self.vel * self.delta_time
            self.vel -= 20 * self.delta_time
        if self.y < 0:
            self.y = 0
            self.touch_ground = True


class Obstacle(GameObject):
    def __init__(self, parent):
        super().__init__(pos=(100, 2), render='D\nD\nD', size=(1, 3))
        self.speed = 30
        self.manager = parent

    def update(self):
        self.x -= self.speed * self.delta_time
        if self.x < 0:
            self.x = 100
            self.manager.score += 1
            self.speed += 1


if __name__ == '__main__':
    JumpManager().start()
