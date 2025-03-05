import pygame
from pygame import Vector2, Surface, Color
import constants

class Alien:
    def __init__(self, type_input: str, x: int, y: int, hitbox_x: int, hitbox_y: int, wave: int) -> None:
        self.type = type_input
        self.hitbox: Vector2 = Vector2(hitbox_x, hitbox_y)
        self.pos: Vector2 = Vector2(x, y)
        self.color: Color = Color(255, 255, 255)
        self.sprites: list = get_sprites(f"alien_sprites/{self.type}", self.hitbox) # replace with self.type

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

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
        screen.blit(self.sprites[swarm_tic % 2], (self.pos.x, self.pos.y))
        
def get_sprites(file_path: str, hitbox: Vector2) -> list:
    sprites: list = []
    for i in range(1, 3):
        total_file_path: str = file_path+str(i)+".png"
        sprite: Surface = pygame.image.load(total_file_path)
        sprite = pygame.transform.scale(sprite, (hitbox.x, hitbox.y))
        sprite.convert_alpha()
        sprites.append(sprite)
    return sprites

