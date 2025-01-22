import pygame

class Player:
    def __init__(self, screen: pygame.Surface) -> None:
        self.pos: pygame.Vector2 = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 80)
        self.hitbox: pygame.Vector2 = pygame.Vector2(70, 30)
        self.speed: int = 200 # distance to move per second
        self.color: pygame.Color = pygame.Color(0, 255, 0)

    def move(self, screen: pygame.Surface, direction: int, dt: float) -> None:
        # update player position
        self.pos.x = self.pos.x + (self.speed * dt * direction)
        # limit left direction
        if self.pos.x < 100:
            self.pos.x = 100
        # limit right direction
        if self.pos.x > (screen.get_width() - 100): 
            self.pos.x = screen.get_width() - 100

    def draw(self, screen: pygame.Surface) -> None:
        # base
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 30, self.pos.y-5, 60, 20))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 35, self.pos.y, 70, 15))
        # barrel
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 5, self.pos.y - 15, 10, 10))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x-2, self.pos.y-19, 4, 4))