import pygame
from pygame import Vector2, Surface, Color
import constants

class Projectile(pygame.sprite.Sprite):
    def __init__(self, projectile_type: str, direction_input: int, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.projectile_type: str = projectile_type
        self.pos: Vector2 = Vector2(x, y)
        self.hitbox: Vector2 = Vector2(10, 10)
        self.speed: int = 10
        self.color: Color = Color(255, 255, 255)
        self.direction: int = direction_input
        self.tic: int = 1

        match self.projectile_type:
            case "laser":
                self.hitbox.x = 4
                self.hitbox.y = 20
                self.speed = 700
            case "cross":
                self.hitbox.x = 3
                self.hitbox.y = 18
                self.speed = 350
            case "wiggle":
                self.hitbox.x = 12
                self.hitbox.y = 20
                self.speed = 450
            case _:
                print("Projectile created without a type")

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def move(self, dt: float) -> None:
        self.pos.y = self.pos.y + (self.speed * dt * self.direction)
        self.tic += 1

    def off_screen(self):
        return self.pos.y < 0 or self.pos.y + self.hitbox.y > constants.SCREEN_SIZE.y - 50

    def draw(self, screen: pygame.Surface) -> None:
        match self.projectile_type:
            case "laser":
                pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
            case "cross":
                # vertical bar
                pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
                # horizontal bar
                offset: int = self.tic % 10
                if int(self.tic / 10) % 2 == 1:
                    offset = 10 - offset
                pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - self.hitbox.x * 1.5, self.pos.y + 3 + offset , self.hitbox.x * 4.5, 3))
            case "wiggle":
                mod: int = 20
                left: bool = (self.tic % mod) < (mod / 2)
                x_pos: list = []
                if left:
                    x_pos = [4, 0, 4, 8, 4]
                else:
                    x_pos = [4, 8, 4, 0, 4]
                for i in range(5):
                    h: int = i * 4
                    pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x + x_pos[i], self.pos.y + h, 4, 4))
            case _:
                print("Projectile created without a type")
