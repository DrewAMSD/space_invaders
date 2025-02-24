import pygame
from pygame import Vector2, Surface, Color
from player import *
from projectile import *
from alien import *

def main() -> None:
    # setup
    pygame.init()
    screen: Surface = pygame.display.set_mode((1280, 900))
    pygame.display.set_caption("Space Invaders")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Game variables
    running: bool = True
    dt: float = 0
    player: Player = Player(screen)
    player_projectiles: list = [None]
    alien_wave: int = 0
    aliens: list = generate_new_swarm(alien_wave)

    # event loop
    while running:
        # end game if user clicked X to close window 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # run game
        update_physics(screen, dt, player, player_projectiles, aliens)
        fill_frame(screen, player, player_projectiles, aliens)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        dt = clock.tick(60) / 1000

    # end game
    pygame.quit()

def generate_new_swarm(wave: int) -> list:
    swarm: list = []
    for r in range(5):
        row: list = []
        for c in range(11):
            if r == 1:
                row.append(Alien("Shooter", r, c, wave))
            elif r == 2 or r == 3:
                row.append(Alien("Brute", r, c, wave))
            else:
                row.append(Alien("Tank", r, c, wave))
        swarm.append(row)
    return swarm

def update_physics(screen: Surface, dt: float, player: Player, player_projectiles: list, aliens: list) -> None:
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(screen, -1, dt) # move left
    if keys[pygame.K_RIGHT]:
        player.move(screen, 1, dt) # move right
    if keys[pygame.K_SPACE]:
        player_shoot(screen, player, player_projectiles) # shoot laser

    # check for collisions
    check_collisions(screen, dt, player, player_projectiles, aliens)

def check_collisions(screen: Surface, dt: float, player: Player, player_projectiles: list, aliens: list) -> None:
    # remove projectiles if they collide with end of screen/wall
    if player_projectiles[0] is not None:
        player_projectile_on_screen: bool = player_projectiles[0].move(screen, dt)
        if not player_projectile_on_screen:
            player_projectiles[0] = None
    
    # check for collisions between aliens and player projectile
    for r in range(len(aliens)):
        if player_projectiles[0] is None: break
        for c in range(len(aliens[r])):
            if aliens[r][c] is None: 
                continue
            if rect_collision(player_projectiles[0].get_pos(), player_projectiles[0].get_hitbox(), aliens[r][c].get_pos(), aliens[r][c].get_hitbox()):
                aliens[r][c] = None # replace with death animation later
                player_projectiles[0] = None
                break

def rect_collision(obj1_pos: Vector2, obj1_hitbox: Vector2, obj2_pos: Vector2, obj2_hitbox: Vector2) -> bool:
    # n = north, e = east, s = south, w = west
    # ob1 coordinates
    w1 = obj1_pos.x
    e1 = w1 + obj1_hitbox.x
    n1 = obj1_pos.y
    s1 = n1 + obj1_hitbox.y
    # obj2 coordinates
    w2 = obj2_pos.x
    e2 = w2 + obj2_hitbox.x
    n2 = obj2_pos.y
    s2 = n2 + obj2_hitbox.y
    # east side is to the right of the west side of the other object
    # south side is below the north side of the other object 
    return w1 < e2 and w2 < e1 and n1 < s2 and n2 < s1

def player_shoot(screen: Surface, player: Player, player_projectiles: list) -> None:
    if player_projectiles[0] is not None: 
        return None
    player_pos: Vector2 = player.get_pos()
    player_projectiles[0] = Projectile("laser", player_pos.x + 30, player_pos.y - 34, -1)

def fill_frame(screen: Surface, player: Player, player_projectiles: list, aliens: list) -> None:
    # fill background wiping away previous frame
    screen.fill("black")
    # bottom boundary rectangle
    pygame.draw.rect(screen, Color(0, 255, 0), pygame.Rect(68, screen.get_height() - 40, screen.get_width() - 136, 5))

    # draw all objects
    player.draw(screen)
    for row in aliens:
        for alien in row:
            if alien is None: 
                continue
            alien.draw(screen)
    if player_projectiles[0] is not None:
        player_projectiles[0].draw(screen)

if __name__ == "__main__":
    main()