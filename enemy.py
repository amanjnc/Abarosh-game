import pygame
import math
import random
from common import *

class Enemy:
    def __init__(self, pos_x, pos_y, detection_radius) -> None:
        self.animation_direction = load_images('Police')
        self.image_index = 0
        self.enemy_surface = self.animation_direction["up"][self.image_index]

        self.enemy_rect = self.enemy_surface.get_rect(center=(pos_x, pos_y))
        self.orignal_enemy_position = self.enemy_rect.center

        # gradually increase the enemy speed when it passes different phases (Decrease it if you want it's just fun to use stamina)
        self.enemy_speed = 2.2

        self.direction = "up"

        self.moving_up = True
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False

        self.detection_radius = detection_radius
        self.is_detecting_player = False
        self.player_position = None
        self.timeout = 100

        # gradually increase it when the enemy passes different phases
        self.leaving_probability = 0.1
        self.enemy_collision_rect = setup_collision_box(self.enemy_surface, self.enemy_rect)
        self.orignal_enemy_collision_position = self.enemy_collision_rect.center

    def update(self, player_position):

        distance_to_player = math.dist(self.enemy_rect.center, player_position)
        self.is_detecting_player = distance_to_player <= self.detection_radius
        self.image_index = (self.image_index + 0.1) % 2
        self.enemy_animation()

        if self.is_detecting_player:
            enemy_leaves = random.random() < self.leaving_probability

            if enemy_leaves:
                self.is_detecting_player = False
            else:
                self.move_towards_player(player_position)
        else:
            self.move_up_and_down()  # dumb AI here

    def move_towards_player(self, player_position):
        self.go_to_target(player_position)

    def move_up_and_down(self):
        x_distance = int(
            abs(self.orignal_enemy_position[0] - self.enemy_rect.centerx))
        reached_guard_post = x_distance == 0
        if not reached_guard_post:
            if x_distance <= 3:
                self.enemy_rect.centerx = self.orignal_enemy_position[0]
            self.go_to_target(self.orignal_enemy_position)

        else:
            if self.enemy_rect.midtop[1] <= 70:
                self.enemy_rect.centery += self.enemy_speed
                self.enemy_collision_rect.centery += self.enemy_speed
                self.direction = "down"

            elif self.enemy_rect.midbottom[1] >= 580:
                self.direction = "up"
                self.enemy_rect.centery -= self.enemy_speed
                self.enemy_collision_rect.centery -= self.enemy_speed

            else:
                if self.direction == "up":
                    self.moving_up = True
                    self.moving_down = False
                    self.enemy_rect.centery -= self.enemy_speed
                    self.enemy_collision_rect.centery -= self.enemy_speed

                elif self.direction == "down":
                    self.moving_down = True
                    self.moving_up = False
                    self.enemy_rect.centery += self.enemy_speed
                    self.enemy_collision_rect.centery += self.enemy_speed

    def go_to_target(self, target_position):
        dx = target_position[0] - self.enemy_rect.centerx
        dy = target_position[1] - self.enemy_rect.centery

        distance = math.hypot(dx, dy)

        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance

            self.enemy_rect.centerx += int(direction_x * self.enemy_speed)
            self.enemy_rect.centery += int(direction_y * self.enemy_speed)
            self.enemy_collision_rect.centerx += int(
                direction_x * self.enemy_speed)
            self.enemy_collision_rect.centery += int(
                direction_y * self.enemy_speed)
        if abs(dy) > abs(dx) and dy > 0:
            self.moving_up = False
            self.moving_left = False
            self.moving_right = False
            self.moving_down = True
        elif abs(dy) > abs(dx) and dy <= 0:
            self.moving_up = True
            self.moving_down = False
            self.moving_left = False
            self.moving_right = False

        else:
            if dx > 0:
                self.moving_right = True
                self.moving_down = False
                self.moving_left = False
                self.moving_up = False
            
            elif dx < 0:
                self.moving_left = True
                self.moving_down = False
                self.moving_up = False
                self.moving_right = False

    def draw(self, screen):
        screen.blit(self.enemy_surface, self.enemy_rect)

    def get_position(self):
        return self.enemy_collision_rect

    def draw_collision_box(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.enemy_collision_rect, 2)

    def increase_difficulty(self):
        self.enemy_speed *= 1.3
        self.leaving_probability /= 2
        self.detection_radius += 25

    def enemy_animation(self):
        if self.moving_up:
            self.enemy_surface = self.animation_direction["up"][int(
                self.image_index)]
        elif self.moving_down:
            self.enemy_surface = self.animation_direction["down"][int(
                self.image_index)]

        elif self.moving_left:
            self.enemy_surface = self.animation_direction["left"][int(
                self.image_index)]

        elif self.moving_right:
            self.enemy_surface = self.animation_direction["right"][int(
                self.image_index)]

    def send_to_guard_post(self):
        self.enemy_rect.centerx = self.orignal_enemy_position[0]
        self.enemy_collision_rect.centerx = self.orignal_enemy_collision_position[0]