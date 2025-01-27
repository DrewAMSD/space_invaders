import pygame
from player import *
from projectile import *

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
    player_projectiles: list = [None]

    # event loop
    while running:
        # end game if user clicked X to close window 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # run game
        update_physics(screen, dt, player, player_projectiles)
        fill_frame(screen, player, player_projectiles)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        dt = clock.tick(60) / 1000

    # end game
    pygame.quit()

def update_physics(screen: pygame.Surface, dt: float, player: Player, player_projectiles: list) -> None:
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(screen, -1, dt) # move left
    if keys[pygame.K_RIGHT]:
        player.move(screen, 1, dt) # move right
    if keys[pygame.K_SPACE]:
        player_shoot(screen, player, player_projectiles) # shoot laser

    if player_projectiles[0] is not None:
        player_projectile_on_screen: bool = player_projectiles[0].move(screen, dt)
        if not player_projectile_on_screen:
            player_projectiles[0] = None

def player_shoot(screen: pygame.Surface, player: Player, player_projectiles: list) -> None:
    if player_projectiles[0] is not None: 
        return None
    player_pos: pygame.Vector2 = player.get_pos()
    player_projectiles[0] = Projectile("laser", player_pos.x - 2, player_pos.y - 34, -1)

def fill_frame(screen: pygame.Surface, player: Player, player_projectiles: list) -> None:
    # fill background wiping away previous frame
    screen.fill("black")
    # bottom boundary rectangle
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(68, screen.get_height() - 40, screen.get_width() - 136, 5))

    # draw all objects
    player.draw(screen)
    if player_projectiles[0] is not None:
        player_projectiles[0].draw(screen)

if __name__ == "__main__":
    main()