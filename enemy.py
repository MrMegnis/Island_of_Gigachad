import pygame
from base_classes.creature import Creature


class Enemy(Creature):
    def __init__(self, left: int, top: int, settings_path: str, on_death_func, weapon=None, move_speed: int = 150, hp: int = 50,
                 damage: int = 10, detection_radius: int = 300, minimum_range: int = 100, attack_radius=200,
                 attack_interval: int = 1000, name: str = "aboba_warrior") -> None:
        super(Enemy, self).__init__(left, top, settings_path, on_death_func, weapon, move_speed, hp, damage, attack_interval, "enemy",
                                    name)
        self.hb.lock_hb_on_owner(self.hitbox.bottomleft)
        self.detection_radius = detection_radius
        self.minimum_range = minimum_range
        self.attack_radius = attack_radius
        self.distance_to_player = 0
        self.spawn_point = (self.left, self.top)

    def set_spawn_point(self, cords: tuple):
        self.spawn_point = cords

    def try_attack(self, enemies):
        if self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_attack_time >= self.attack_interval:
                self.attack()
        if "attack" in self.animator.status and self.animator.frame_index == len(
                self.animator.animation[self.animator.status]) - 2:
            self.apply_damage(enemies)
        else:
            self.can_apply_damage = True
        super(Enemy, self).try_attack()

    def apply_damage(self, enemies):
        current_time = pygame.time.get_ticks()
        self.last_attack_time = current_time
        super(Enemy, self).apply_damage(enemies)

    def draw(self, screen) -> None:
        if self.distance_to_player <= max(pygame.display.get_window_size()):
            super(Enemy, self).draw(screen)


    def update_direction(self, player):
        if player.hitbox.x < self.hitbox.x:
            self.direction.x = -1
        else:
            self.direction.x = 1
        super(Enemy, self).update_direction()

    def update_distance_to_player(self, player):
        self.distance_to_player = abs(player.hitbox.x - self.hitbox.x)

    def update(self, player, screen) -> None:
        self.update_distance_to_player(player)

        if self.distance_to_player <= max(pygame.display.get_window_size()):
            if "attack" not in self.animator.get_status():
                self.normalize_weapon()
            if self.detection_radius >= self.distance_to_player:
                self.update_direction(player)
            else:
                self.direction.x = 0
            if self.distance_to_player < self.minimum_range:
                self.direction.x = -self.direction.x
            else:
                if self.attack_radius >= abs(self.distance_to_player):
                    self.direction.x = 0
                    self.try_attack([player])
            # self.weapon.draw_weapon_range()
            super(Enemy, self).update(screen)
            self.hb.update_lock_point(self.hitbox.bottomleft)
        # print(self.can_attack, self.can_move)
