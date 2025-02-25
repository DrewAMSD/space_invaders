import pygame
from pygame import Vector2, Surface, Color
import constants
from player import *
from projectile import *
from alien import *

def main() -> None:
    # setup
    pygame.init()
    screen: Surface = pygame.display.set_mode((constants.SCREEN_SIZE.x, constants.SCREEN_SIZE.y))
    pygame.display.set_caption("Space Invaders")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Game variables
    running: bool = True
    dt: float = 0
    wave: int = 1
    # player state
    player: Player = Player()
    player_projectiles: list = [None]
    # alien swarm state
    swarm_data: dict = {
        "location": Vector2((screen.get_width() / 2) - (constants.SWARM_LENGTH / 2), 40), # northwest (top-left) of swarm location
        "timer": constants.SWARM_TIMER, # time until swarm can move in seconds
        "direction": 1,
    }
    swarm: list = generate_new_swarm(wave, swarm_data)

    # event loop
    while running:
        # end game if user clicked X to close window 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # run game
        update_physics(screen, dt, player, player_projectiles, swarm, swarm_data)
        fill_frame(screen, player, player_projectiles, swarm)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        dt = clock.tick(60) / 1000

    # end game
    pygame.quit()

def generate_new_swarm(wave: int, swarm_data: dict) -> list:
    wave -= 1
    swarm: list = []
    for r in range(constants.SWARM_ROWS):
        row: list = []
        for c in range(constants.SWARM_COLS):
            x: int = c * (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X) + swarm_data["location"].x
            y: int = r * (constants.ALIEN_HITBOX_Y + constants.ALIEN_OFFSET_Y) + swarm_data["location"].y
            alien_type: str = ""
            if r == 0:
                alien_type = "shooter"
            elif r == 1 or r == 2:
                alien_type = "brute"
            else:
                alien_type = "tank"
            row.append(Alien(alien_type, x, y, constants.ALIEN_HITBOX_X, constants.ALIEN_HITBOX_Y, wave))
        swarm.append(row)
    return swarm

def update_physics(screen: Surface, dt: float, player: Player, player_projectiles: list, swarm: list, swarm_data: dict) -> None:
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, dt) # move left
    if keys[pygame.K_RIGHT]:
        player.move(1, dt) # move right
    if keys[pygame.K_SPACE]:
        player_shoot(screen, player, player_projectiles) # shoot laser
    
    # check if enough time has passed for swarm to move
    swarm_data["timer"] -= dt
    if swarm_data["timer"] <= 0:
        move_swarm(swarm, swarm_data)
    # check for collisions
    check_collisions(screen, dt, player, player_projectiles, swarm)

def move_swarm(swarm: list, swarm_data: dict) -> None:
    # check if you need to move swarm up or down
    if swarm_reached_edge(swarm_data):
        swarm_data["direction"] *= -1
        swarm_data["location"].y += constants.SWARM_MOV_Y
    else:
        # move swarm left or right
        swarm_data["location"].x = swarm_data["location"].x + (constants.SWARM_MOV_X * swarm_data["direction"])
        if swarm_data["location"].x < constants.SCREEN_BOUND_X:
            swarm_data["location"].x = constants.SCREEN_BOUND_X
        elif swarm_data["location"].x + constants.SWARM_LENGTH > constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X:
            swarm_data["location"].x = constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X - constants.SWARM_LENGTH

    swarm_data["timer"] = constants.SWARM_TIMER
    update_alien_locations(swarm, swarm_data)

def swarm_reached_edge(swarm_data: dict) -> bool:
    return (swarm_data["location"].x == constants.SCREEN_BOUND_X and swarm_data["direction"] == -1) or (swarm_data["location"].x + constants.SWARM_LENGTH == constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X and swarm_data["direction"] == 1)

def update_alien_locations(swarm: list, swarm_data: dict) -> None:
    for r in range(constants.SWARM_ROWS):
        for c in range(constants.SWARM_COLS):
            if swarm[r][c] is None:
                continue
            x: int = c * (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X) + swarm_data["location"].x
            y: int = r * (constants.ALIEN_HITBOX_Y + constants.ALIEN_OFFSET_Y) + swarm_data["location"].y
            swarm[r][c].update_pos(x, y)

def check_collisions(screen: Surface, dt: float, player: Player, player_projectiles: list, swarm: list) -> None:
    # remove player projectile if it collides with end of screen
    if player_projectiles[0] is not None:
        player_projectile_on_screen: bool = player_projectiles[0].move(dt)
        if not player_projectile_on_screen:
            player_projectiles[0] = None
    
    # check for collisions between aliens and player projectile
    for r in range(len(swarm)):
        if player_projectiles[0] is None: break
        for c in range(len(swarm[r])):
            if swarm[r][c] is None: 
                continue
            if rect_collision(player_projectiles[0].get_pos(), player_projectiles[0].get_hitbox(), swarm[r][c].get_pos(), swarm[r][c].get_hitbox()):
                swarm[r][c] = None # replace with death animation later
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
    player_projectiles[0] = Projectile("laser", -1, player_pos.x + 30, player_pos.y - 34,)

def fill_frame(screen: Surface, player: Player, player_projectiles: list, swarm: list) -> None:
    # fill background wiping away previous frame
    screen.fill("black")
    # bottom boundary rectangle
    pygame.draw.rect(screen, Color(0, 255, 0), pygame.Rect(68, screen.get_height() - 40, screen.get_width() - 136, 5))
    # draw all objects
    # player
    player.draw(screen)
    # aliens
    for row in swarm:
        for alien in row:
            if alien is None: 
                continue
            alien.draw(screen)
    # player projectile
    if player_projectiles[0] is not None:
        player_projectiles[0].draw(screen)

if __name__ == "__main__":
    main()