import pygame
from pygame import Vector2, Surface, Color
import constants

class Alien:
    def __init__(self, type_input: str, x: int, y: int, hitbox_x: int, hitbox_y: int, wave: int) -> None:
        self.type = type_input
        self.hitbox: Vector2 = Vector2(hitbox_x, hitbox_y)
        self.pos: Vector2 = Vector2(x, y)
        self.color: Color = Color(255, 255, 255)
        self.images: list = get_alien_images(f"alien_images/{self.type}", self.hitbox)
        # managing death animation
        self.is_dead: bool = False
        self.death_timer: float = 0.25

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def kill(self) -> None:
        self.is_dead = True

    def death_animation_over(self, dt: float) -> bool:
        self.death_timer -= dt
        return self.death_timer < 0

    def has_died(self) -> bool:
        return self.is_dead

    def update_pos(self, new_x: int, new_y: int) -> None:
        self.pos.x = new_x
        self.pos.y = new_y

    def get_score(self) -> int:
        alien_score: int = 0
        match self.type:
            case "shooter":
                alien_score = 40
            case "brute":
                alien_score = 20
            case "tank":
                alien_score = 10
            case _:
                print("alien has no score")
        return alien_score

    def draw(self, screen: Surface, swarm_tic: int) -> None:
        idx: int = 0
        if self.is_dead:
            idx = len(self.images) - 1
        else:
            idx = swarm_tic % 2
        screen.blit(self.images[idx], (self.pos.x, self.pos.y))
        
def get_alien_images(file_path: str, hitbox: Vector2) -> list:
    images: list = []
    # add images for alien to list
    for i in range(1, 3):
        total_file_path: str = file_path+str(i)+".png"
        image: Surface = pygame.image.load(total_file_path)
        image = pygame.transform.scale(image, (hitbox.x, hitbox.y))
        image.convert_alpha()
        images.append(image)
    # insert death image at end of list
    image: Surface = pygame.image.load("alien_images/alien_dead.png")
    image = pygame.transform.scale(image, (hitbox.x, hitbox.y))
    image.convert_alpha()
    images.append(image)
    return images

