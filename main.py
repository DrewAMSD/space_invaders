import pygame
from pygame import Vector2, Surface, Color
import constants
from player import *
from projectile import *
from alien import *
import Text
import random

def main() -> None:
    # setup
    pygame.init()
    screen: Surface = pygame.display.set_mode((constants.SCREEN_SIZE.x, constants.SCREEN_SIZE.y))
    pygame.display.set_caption("Space Invaders")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Game variables
    game_data: dict = new_game_data()
    # player state
    player: Player = Player()
    player_projectiles: list = [None]
    # alien swarm state
    swarm_data: dict = new_swarm_data()
    swarm: list = generate_new_swarm(game_data, swarm_data)
    alien_projectiles: list = []

    # event loop
    while game_data["running"]:
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # end game if user clicked X to close window
                game_data["running"] = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_data["game_over"] and mouse_over_play_again():
                # reset state
                game_data = new_game_data()
                player = Player()
                player_projectiles = [None]
                swarm_data = new_swarm_data()
                swarm = generate_new_swarm(game_data, swarm_data)
                alien_projectiles = []

        # run game
        if not game_data["game_over"]:
            update_physics(screen, game_data, player, player_projectiles, swarm, swarm_data, alien_projectiles)
        fill_frame(screen, player, player_projectiles, swarm, game_data, alien_projectiles)

        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        game_data["dt"] = clock.tick(60) / 1000

    # end game
    pygame.quit()

def new_game_data() -> dict:
    return {
        "running": True,
        "game_over": False,
        "dt": 0,
        "wave": 1,
        "score": 0,
    }

def new_swarm_data() -> dict:
    return {
        "location": Vector2((constants.SCREEN_SIZE.x / 2) - (constants.SWARM_LENGTH / 2), 120), # northwest (top-left) of swarm location
        "timer": constants.SWARM_TIMER, # time until swarm can move in seconds
        "direction": 1,
        "col_has_aliens": [True for i in range(constants.SWARM_COLS)]
    }

def generate_new_swarm(game_data: dict, swarm_data: dict) -> list:
    wave = game_data["wave"] - 1
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

def update_physics(screen: Surface, game_data: dict, player: Player, player_projectiles: list, swarm: list, swarm_data: dict, alien_projectiles: list) -> None:
    # check player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, game_data["dt"]) # move left
    if keys[pygame.K_RIGHT]:
        player.move(1, game_data["dt"]) # move right
    if keys[pygame.K_SPACE]:
        player_shoot(screen, player, player_projectiles) # shoot laser
    
    # check if enough time has passed for swarm to move
    swarm_data["timer"] -= game_data["dt"]
    if swarm_data["timer"] <= 0:
        move_swarm(swarm, swarm_data)
    # move projectiles
    move_alien_projectiles(alien_projectiles, game_data)
    move_player_projectile(player_projectiles, game_data)
    # generate enemy projectiles
    for c in range(constants.SWARM_COLS):
        if len(alien_projectiles) > constants.ALIEN_MAX_PROJECTILES:
            break
        random_int: int = random.randint(1, 10000)
        if random_int <= get_chance_to_shoot(len(alien_projectiles)):
            alien_shoot(screen, swarm[0][c], alien_projectiles)
    # check for collisions
    check_collisions(screen, game_data, player, player_projectiles, swarm, alien_projectiles)
    # check if game is over
    if player.is_dead():
        game_data["game_over"] = True

def get_chance_to_shoot(n: int):
    return constants.SWARM_COLS - n + 5

def move_swarm(swarm: list, swarm_data: dict) -> None:
    for c in range(constants.SWARM_COLS):
        swarm_data["col_has_aliens"][c] = has_aliens(swarm, c)

    # check if you need to move swarm vertically or horizontally
    if swarm_reached_edge(swarm, swarm_data):
        # move swarm vertically
        swarm_data["direction"] *= -1
        swarm_data["location"].y += constants.SWARM_MOV_Y
    else:
        # move swarm horizontally
        swarm_data["location"].x = swarm_data["location"].x + (constants.SWARM_MOV_X * swarm_data["direction"])

    swarm_data["timer"] = constants.SWARM_TIMER
    update_alien_locations(swarm, swarm_data)

def move_alien_projectiles(alien_projectiles: list, game_data: dict) -> None:
    for i in range(len(alien_projectiles)):
        alien_projectiles[i].move(game_data["dt"])

def move_player_projectile(player_projectiles: list, game_data: dict) -> None:
    if player_projectiles[0] is not None:
        player_projectiles[0].move(game_data["dt"])

def has_aliens(swarm: list, c: int) -> bool:
    for r in range(constants.SWARM_ROWS):
        if swarm[r][c] is not None:
            return True
    return False

def swarm_reached_edge(swarm: list, swarm_data: dict) -> bool:
    loc_left: int = swarm_data["location"].x
    loc_right: int = swarm_data["location"].x + constants.SWARM_LENGTH
    # update left and right depending on col_has_aliens bool array
    for c in range(constants.SWARM_COLS):
        if swarm_data["col_has_aliens"][c]:
            break
        loc_left += constants.ALIEN_HITBOX_X + constants. ALIEN_OFFSET_X
    for c in range(constants.SWARM_COLS - 1, 0, -1):
        if swarm_data["col_has_aliens"][c]:
            break
        loc_right -= (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X)

    return (loc_left <= constants.SCREEN_BOUND_X and swarm_data["direction"] == -1) or (loc_right >= constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X and swarm_data["direction"] == 1)

def update_alien_locations(swarm: list, swarm_data: dict) -> None:
    for r in range(constants.SWARM_ROWS):
        for c in range(constants.SWARM_COLS):
            if swarm[r][c] is None:
                continue
            x: int = c * (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X) + swarm_data["location"].x
            y: int = r * (constants.ALIEN_HITBOX_Y + constants.ALIEN_OFFSET_Y) + swarm_data["location"].y
            swarm[r][c].update_pos(x, y)

def check_collisions(screen: Surface, game_data: dict, player: Player, player_projectiles: list, swarm: list, alien_projectiles: list) -> None:
    # remove player projectile if it collides with end of screen
    if player_projectiles[0] is not None and player_projectiles[0].off_screen():
        player_projectiles[0] = None
    
    # remove alien projectiles if it collides with end of screen
    for alien_projectile in alien_projectiles:
        if alien_projectile.off_screen():
            alien_projectiles.remove(alien_projectile)

    # check for collisions between player and alien projectiles
    for alien_projectile in alien_projectiles:
        if rect_collision(player.get_pos(), player.get_hitbox(), alien_projectile.get_pos(), alien_projectile.get_hitbox()):
            alien_projectiles.remove(alien_projectile)
            player.kill()
    
    # check for collisions between aliens and player projectile
    for r in range(len(swarm)):
        if player_projectiles[0] is None: 
            break
        for c in range(len(swarm[r])):
            if swarm[r][c] is None: 
                continue
            if rect_collision(player_projectiles[0].get_pos(), player_projectiles[0].get_hitbox(), swarm[r][c].get_pos(), swarm[r][c].get_hitbox()):
                game_data["score"] += swarm[r][c].get_score()
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

def alien_shoot(screen: Surface, alien: Alien, alien_projectiles: list) -> None:
    if alien is None:
        return None
    alien_pos: Vector2 = alien.get_pos()
    alien_hitbox: Vector2 = alien.get_hitbox()
    alien_projectiles.append(Projectile("cross", 1, alien_pos.x + alien_hitbox.x / 2 - 2, alien_pos.y + alien_hitbox.y / 2))

def fill_frame(screen: Surface, player: Player, player_projectiles: list, swarm: list, game_data: dict, alien_projectiles: list) -> None:
    # fill background wiping away previous frame
    screen.fill("black")
    # bottom boundary rectangle
    pygame.draw.rect(screen, Color(0, 255, 0), pygame.Rect(68, constants.SCREEN_SIZE.y - 20, constants.SCREEN_SIZE.x - 136, 5))
    # draw text
    Text.text_to_screen(screen, "Score", 0, 0, 30, (255, 255, 255))
    Text.text_to_screen(screen, game_data["score"], 90, 0, 30, (0, 255, 0))
    Text.text_to_screen(screen, "Lives", constants.SCREEN_SIZE.x - 130, 0, 30, (255, 255, 255))
    Text.text_to_screen(screen, player.get_lives(), constants.SCREEN_SIZE.x - 50, 0, 30, (0, 255, 0))
    # if game over show loss screen, else continue to draw all objects
    if game_data["game_over"]:
        # text for game over screen
        # Game Over
        Text.text_to_screen(screen, "Game Over", constants.SCREEN_SIZE.x / 2 - 160, constants.SCREEN_SIZE.y / 2 - 140, 80, (255, 255, 255))
        # Play Again?
        play_again_color: Color = None
        if mouse_over_play_again():
            play_again_color = Color(0, 255, 0)
        else:
            play_again_color = Color(255, 255, 255)
        Text.text_to_screen(screen, "Play Again?", constants.SCREEN_SIZE.x / 2 - 80, constants.SCREEN_SIZE.y / 2, 40, play_again_color)
        return None
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
    # alien projectiles
    for i in range(len(alien_projectiles)):
        alien_projectiles[i].draw(screen)

def mouse_over_play_again():
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    return mouse_pos_x >= 562 and mouse_pos_x <= 780 and mouse_pos_y >= 462 and mouse_pos_y <= 496

if __name__ == "__main__":
    main()