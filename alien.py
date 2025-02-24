import pygame
from pygame import Vector2, Surface, Color

class Alien:
    def __init__(self, type_input: str, row: int, col: int, wave: int) -> None:
        self.type = type_input
        self.hitbox: Vector2 = Vector2(50, 40)
        self.pos: Vector2 = Vector2(col * (self.hitbox.x + 15) + 40, row * (self.hitbox.y + 22) + 40)
        self.color: Color = Color(255, 255, 255)

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        