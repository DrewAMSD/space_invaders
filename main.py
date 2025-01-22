import pygame
from player import *

def main() -> None:
    # setup
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((1280, 720))
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
        
        # fill background wiping away previous frame
        screen.fill("black")

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
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: 
        player.move(screen, -1, dt) # move left
    if keys[pygame.K_RIGHT]:
        player.move(screen, 1, dt) # move right

    # draw all objects
    player.draw(screen)

if __name__ == "__main__":
    main()