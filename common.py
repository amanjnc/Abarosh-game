from collections import defaultdict
import pygame


def setup_collision_box(surface, rect, width=48, height=48):
    collision_box_width = width
    collision_box_height = height
    collision_box_offset_x = (
        surface.get_width() - collision_box_width) // 2
    collision_box_offset_y = (
        surface.get_height() - collision_box_height) // 2

    collision_rect = pygame.Rect(
        rect.left + collision_box_offset_x,
        rect.top + collision_box_offset_y,
        collision_box_width,
        collision_box_height
    )

    return collision_rect


def load_images(image_name: str):
    image_folder_path = './assets/sprites/' + image_name + "_sprite"
    animation_direction = defaultdict(list)
    image_number = 2
    directions = ["down", "up", "right", "left"]

    for direction in directions:
        for _ in range(2):
            image = f'{image_folder_path}/{image_name}-{image_number}.png.png'
            loaded_image = pygame.image.load(image)
            scaled_image = pygame.transform.scale(loaded_image, (96, 96))
            animation_direction[direction].append(scaled_image)
            image_number += 1
    print(animation_direction)
    return animation_direction
