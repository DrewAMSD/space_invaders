import pygame

class Player:
    def __init__(self, screen: pygame.Surface) -> None:
        self.pos: pygame.Vector2 = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 100)
        self.hitbox: pygame.Vector2 = pygame.Vector2(64, 20) # 32 pixels left and right from self.pos.x, and 20 pixels down from self.pos.y
        self.speed: int = 300 # pixels per second
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
        # base (hitbox region)
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 28, self.pos.y, 56, 20))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 32, self.pos.y + 5, 64, 15))
        # barrel
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 5, self.pos.y - 10, 10, 10))
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x - 2, self.pos.y - 14, 4, 4))