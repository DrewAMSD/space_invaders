import pygame

def main():
    # setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Space Invaders")
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # event loop
    while running:
        # end game if user clicked X to close window 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # fill background wiping away previous frame
        screen.fill("black")

        # run game
        fill_frame(screen, clock, dt)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        dt = clock.tick(60) / 1000

    # end game
    pygame.quit()

def fill_frame(screen, click, dt: float):
    # what
    return None

if __name__ == "__main__":
    main()