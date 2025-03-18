import pygame
from pygame import Vector2, Surface
import constants
import Text
import random

class Alien(pygame.sprite.Sprite):
    def __init__(self, type_input: str, x: int, y: int, hitbox_x: int, hitbox_y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.type = type_input
        self.hitbox: Vector2 = Vector2(hitbox_x, hitbox_y)
        self.pos: Vector2 = Vector2(x, y)
        self.images: list = get_alien_images(self.type, self.hitbox)
        self.score: int = self.calculate_score()
        # managing death animation
        self.is_dead: bool = False
        self.death_timer: float = 0.4 if self.type == "spaceship" else 0.25

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

    def calculate_score(self) -> int:
        alien_score: int = 0
        match self.type:
            case "shooter":
                alien_score = 40
            case "brute":
                alien_score = 20
            case "tank":
                alien_score = 10
            case "spaceship":
                alien_score = random.randint(1, 5) * 50
                if alien_score == 250:
                    alien_score = 300
            case _:
                print("alien has no score")
        return alien_score

    def get_score(self) -> int:
        return self.score

    def draw(self, screen: Surface, swarm_tic: int) -> None:
        idx: int = 0
        if self.is_dead:
            idx = len(self.images) - 1
        else:
            idx = swarm_tic % 2
        
        if self.type == "spaceship" and self.is_dead:
            Text.text_to_screen(screen, self.score, self.pos.x, self.pos.y, 30, (255, 255, 255)) 
            return None
        screen.blit(self.images[idx], (self.pos.x, self.pos.y))
        
def get_alien_images(alien_type: str, hitbox: Vector2) -> list:
    images: list = []
    # if spaceship only add image of spaceship
    if alien_type == "spaceship":
        image: Surface = pygame.image.load("alien_images/spaceship.png")
        image = pygame.transform.scale(image, (80, 35))
        image.convert_alpha()
        images.append(image)
        return images
    # add images for alien to list
    for i in range(1, 3):
        total_file_path: str = "alien_images/"+alien_type+str(i)+".png"
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

