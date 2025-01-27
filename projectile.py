import pygame

class Projectile:
    def __init__(self, projectile_type: str, x: int, y: int, dir: int) -> None:
        self.projectile_type: str = projectile_type
        self.pos: pygame.Vector2 = pygame.Vector2(x, y)
        self.hitbox: pygame.Vector2 = pygame.Vector2(10, 10)
        self.speed: int = 10
        self.color: pygame.Color = pygame.Color(255, 255, 255)
        self.direction = dir

        match self.projectile_type:
            case "laser":
                self.hitbox.x = 4
                self.hitbox.y = 20
                self.speed = 700
            case _:
                print("uh oh!")

    def move(self, screen: pygame.Surface, dt: int) -> bool:
        self.pos.y = self.pos.y + (self.speed * dt * self.direction)
        if self.pos.y < 0: return False
        if self.pos.y > screen.get_height() - 50: return False
        return True

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
