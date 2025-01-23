import pygame
from player import *

def main() -> None:
    # setup
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((1280, 900))
    pygame.display.set_caption("Space Invaders")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Game variables
    running: bool = True
    dt: float = 0
    player: Player = Player(screen)

    # event loop
    while running:
        # end game if user clicked X to close window 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # run game
        fill_frame(screen, clock, dt, player)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        dt = clock.tick(60) / 1000

    # end game
    pygame.quit()

def fill_frame(screen: pygame.Surface, clock: pygame.time.Clock, dt: float, player: Player) -> None:
    # fill background wiping away previous frame
    screen.fill("black")
    # bottom boundary rectangle
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(68, screen.get_height() - 40, screen.get_width() - 136, 5))
    
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        player.move(screen, -1, dt) # move left
    if keys[pygame.K_RIGHT]:
        player.move(screen, 1, dt) # move right
    # if keys[pygame.K_SPACE]: # shoot laser

    # draw all objects
    player.draw(screen)

if __name__ == "__main__":
    main()