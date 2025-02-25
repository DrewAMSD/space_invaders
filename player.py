import pygame
from pygame import Vector2, Surface, Color
import constants

class Player:
    def __init__(self) -> None:
        self.pos: Vector2 = Vector2((constants.SCREEN_SIZE.x / 2) - 32, constants.SCREEN_SIZE.y - 100)
        self.hitbox: Vector2 = Vector2(64, 20) # 32 pixels left and right from self.pos.x, and 20 pixels down from self.pos.y
        self.speed: int = 300 # pixels per second
        self.color: Color = Color(0, 255, 0)
        self.lives: int = 3

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def get_lives(self) -> int:
        return self.lives

    def move(self, direction: int, dt: float) -> None:
        # update player position
        self.pos.x = self.pos.x + (self.speed * dt * direction)
        # limit left direction
        if self.pos.x < constants.SCREEN_BOUND_X:
            self.pos.x = constants.SCREEN_BOUND_X
        # limit right direction
        if self.pos.x > (constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X - self.hitbox.x): 
            self.pos.x = constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X - self.hitbox.x

    def draw(self, screen: Surface) -> None:
        # base (hitbox region)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x + 4, self.pos.y, self.hitbox.x - 8, self.hitbox.y))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y + 5, self.hitbox.x, self.hitbox.y - 5))
        # barrel
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x + 27, self.pos.y - 10, 10, 10))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x + 30, self.pos.y - 14, 4, 4))