import pygame
from pygame import Vector2, Surface
import constants

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos: Vector2 = Vector2(constants.SCREEN_SIZE.x / 4, constants.SCREEN_SIZE.y - 100)
        self.hitbox: Vector2 = Vector2(64, 20) # 32 pixels left and right from self.pos.x, and 20 pixels down from self.pos.y
        self.speed: int = 300 # pixels per second
        self.lives: int = 3
        self.images: list = get_player_images(self.hitbox)
        self.death_animation: int = 0 # frame of death animation, 0 means not playing death animation
        self.death_animation_timer: float = 0.05

    def get_pos(self) -> Vector2:
        return self.pos

    def get_hitbox(self) -> Vector2:
        return self.hitbox

    def get_lives(self) -> int:
        return self.lives

    def increment_lives(self) -> None:
        self.lives += 1

    def kill(self) -> None:
        self.lives -= 1
        self.death_animation = 1
        #self.pos.x = constants.SCREEN_SIZE.x / 4

    def get_death_animation(self) -> int:
        return self.death_animation

    def lost_all_lives(self) -> bool:
        return self.lives == 0

    def move(self, direction: int, dt: float) -> None:
        # update player position
        self.pos.x = self.pos.x + (self.speed * dt * direction)
        # limit left direction
        if self.pos.x < constants.SCREEN_BOUND_X:
            self.pos.x = constants.SCREEN_BOUND_X
        # limit right direction
        if self.pos.x > (constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X - self.hitbox.x): 
            self.pos.x = constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X - self.hitbox.x

    def draw(self, screen: Surface, dt: float) -> None:
        if self.death_animation == 0:
            if self.lost_all_lives():
                screen.blit(self.images[len(self.images)-1], (self.pos.x, self.pos.y - 14))
            else:
                screen.blit(self.images[0], (self.pos.x, self.pos.y - 14))
        else:
            idx: int = ((self.death_animation - 1) % 5) + 1
            screen.blit(self.images[idx], (self.pos.x, self.pos.y - 14))
            self.death_animation_timer -= dt
            if self.death_animation_timer > 0:
                return None
            self.death_animation += 1
            self.death_animation_timer = 0.05
            if self.death_animation > 9:
                self.death_animation = 0
                if not self.lost_all_lives():
                    self.pos.x = constants.SCREEN_SIZE.x / 4

def get_player_images(hitbox: Vector2) -> list:
    file_path: str = "player_images/player"
    images: list = []
    # insert player image
    for i in range(6):
        image: Surface = pygame.image.load(f"{file_path}{i+1}.png")
        image = pygame.transform.scale(image, (hitbox.x, hitbox.y+14))
        image.convert_alpha()
        images.append(image)
    return images