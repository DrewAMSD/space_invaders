import pygame
from pygame import Vector2, Surface, Color
import constants

class Projectile:
    def __init__(self, projectile_type: str, direction_input: int, x: int, y: int) -> None:
        self.projectile_type: str = projectile_type
        self.pos: Vector2 = Vector2(x, y)
        self.hitbox: Vector2 = Vector2(10, 10)
        self.speed: int = 10
        self.color: Color = Color(255, 255, 255)
        self.direction = direction_input

        match self.projectile_type:
            case "laser":
                self.hitbox.x = 4
                self.hitbox.y = 20
                self.speed = 700
            case _:
                print("Projectile created without a type")

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def move(self, dt: int) -> bool:
        self.pos.y = self.pos.y + (self.speed * dt * self.direction)
        if self.pos.y < 0: return False
        if self.pos.y > constants.SCREEN_SIZE.y: return False
        return True

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
