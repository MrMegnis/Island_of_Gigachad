import pygame
from base_classes.rectangle import Rectangle
from animator import Animator
from gui.widgets.health_bar import Health_Bar


class Creature(Rectangle):
    def __init__(self, left: int, top: int, image: str = None, size: tuple = None, move_speed: int = 100, hp: int = 50,
                 color="yellow", type_: str = None, name: str = None, gravity_strength: int = 10, jump_height: int = 25) -> None:
        self.stats = {"hp": hp, "gravity_strength": gravity_strength, "speed": move_speed, "type": type_,
                      "color": color, "jump_height": jump_height}
        # надо убрать все переменные-характеристики игрока

        self.direction = pygame.Vector2(0, 0)
        self.move_speed = move_speed
        self.name = name
        self.hp = hp
        self.can_move = True
        self.gravity_strength = gravity_strength
        self.type_ = type_
        self.animator = Animator(self, ["idle", "move_right", "move_left", "attack", "hit", "jump"])
        image = self.animator.get_current_frame()
        super(Creature, self).__init__(left, top, image, size, color)
        self.hitbox = self.rect.copy()
        
        self.jump_count = 0
        self.hb = Health_Bar(self.rect.left, self.rect.bottom, (self.rect.size[0], self.rect.size[1] // 10), self)

    def move(self):
        if self.direction.x == 1 and self.move_speed != 0:
            self.animator.set_bool("move_right", True)
        elif self.direction.x == -1 and self.move_speed != 0:
            self.animator.set_bool("move_left", True)
        else:
            self.animator.set_bool("move_right", False)
            self.animator.set_bool("move_left", False)
        # print(int(self.direction.x), self.move_speed, int(self.direction.x) * self.move_speed / 60)
        x = int(self.direction.x * self.move_speed / 60)
        y = int(self.direction.y * self.move_speed / 60)
        self.rect.x += x
        self.rect.y += y
        self.hitbox.x += x
        self.hitbox.y += y
        # self.rect.topleft = (self.left, self.top)

    def lock_movement(self):
        self.can_move = False

    def unlock_movement(self):
        self.can_move = True

    def next_move(self):
        # print(self.rect.center,"a")
        left = self.rect.left
        left += int(self.direction.x * self.move_speed / 60)
        top = self.rect.top
        top += int(self.direction.y * self.move_speed / 60)
        rect = self.rect.copy()
        rect.topleft = (left, top)
        return rect

    def next_gravity_move(self, gravity_strength=None):
        if not gravity_strength:
            gravity_strength = self.gravity_strength
        left = self.rect.left
        top = self.rect.top
        top += gravity_strength
        rect = self.rect.copy()
        rect.topleft = (left, top)
        return rect

    def gravity_move(self, y):
        self.rect.y += y
        self.hitbox.y += y

    def get_damage(self, attaker, damage):
        self.hp -= damage
        self.hb.get_damage(damage)
        if self.hp <= 0:
            self.kill()
        else:
            self.get_hit(attaker)

    def get_hit(self, attacker):
        self.animator.trigger("hit")

    def make_attack(self):
        self.animator.trigger("attack")

    def do_jump(self):
        self.rect.y -= self.jump_count
        self.hitbox.y -= self.jump_count

    def draw_hitbox(self):
        pygame.draw.rect(pygame.display.get_surface(), "green", self.hitbox, 5)

    def update(self, screen) -> None:
        if self.can_move:
            self.move()
        if self.animator.get_status() == "attack":
            self.lock_movement()
        else:
            self.unlock_movement()
        self.animator.next_frame()
        self.hb.update(screen)
        # self.draw_hitbox()
