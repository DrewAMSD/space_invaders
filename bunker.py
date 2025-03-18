import pygame
from pygame import Vector2, Surface

class Bunker(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.blocks: pygame.sprite.Group = self.generate_blocks(x, y)
        self.pos: Vector2 = Vector2(x, y)

    def update(self):
        for block in self.blocks.sprites():
            if block.is_destroyed():
                self.blocks.remove(block)

    def is_destroyed(self) -> bool:
        return len(self.blocks) == 0

    def get_blocks(self) -> pygame.sprite.Group:
        return self.blocks

    def generate_blocks(self, x: int, y: int) -> pygame.sprite.Group:
        group: pygame.sprite.Group = pygame.sprite.Group()
        group.add(Block(x, y))
        group.add(Block(x, y+30))
        group.add(Block(x, y+60))
        group.add(Block(x+30, y))
        group.add(Block(x+30, y+30))
        group.add(Block(x+60, y))
        group.add(Block(x+60, y+30))
        group.add(Block(x+90, y))
        group.add(Block(x+90, y+30))
        group.add(Block(x+90, y+60))
        return group

    def draw(self, screen: Surface) -> None:
        for block in self.blocks.sprites():
            block.draw(screen)

class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.pos: Vector2 = Vector2(x, y)
        self.images: list = get_block_images("block")
        self.state = 1

    def hit(self) -> None:
        self.state += 1

    def get_pos(self) -> Vector2:
        return self.pos

    def is_destroyed(self) -> bool:
        return self.state > 4

    def draw(self, screen: Surface) -> None:
        if self.is_destroyed():
            return None
        screen.blit(self.images[self.state - 1], self.pos)

def get_block_images(block_type: str) -> list:
    block_images: list = []
    for i in range(1, 5):
        file_path = f"block_images/{block_type}{i}.png"
        image: Surface = pygame.image.load(file_path)
        image = pygame.transform.scale(image, (30, 30))
        image.convert_alpha()
        block_images.append(image)
    return block_images