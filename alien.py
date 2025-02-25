import pygame
from pygame import Vector2, Surface, Color
import constants

class Alien:
    def __init__(self, type_input: str, x: int, y: int, hitbox_x: int, hitbox_y: int, wave: int) -> None:
        self.type = type_input
        self.hitbox: Vector2 = Vector2(hitbox_x, hitbox_y)
        self.pos: Vector2 = Vector2(x, y)
        self.color: Color = Color(255, 255, 255)
        # START remove later
        match self.type:
            case "shooter":
                self.color.g = 0
                self.color.b = 0
            case "brute":
                self.color.r = 0
                self.color.b = 0
            case "tank":
                self.color.r = 0
                self.color.g = 0
            case _:
                print("Alien created without a type")
        # END remove later

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def update_pos(self, new_x: int, new_y: int) -> None:
        self.pos.x = new_x
        self.pos.y = new_y

    def draw(self, screen: Surface) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        