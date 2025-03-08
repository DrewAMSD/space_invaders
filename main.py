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
    player_projectiles: list[Projectile] = [None]
    # alien swarm state
    swarm_data: dict = new_swarm_data(game_data)
    swarm: list[list[Alien]] = generate_new_swarm(game_data, swarm_data)
    alien_projectiles: list[Projectile] = []

    # event loop
    while game_data["running"]:
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # end game if user clicked X to close window
                game_data["running"] = False
            if event.type == pygame.MOUSEBUTTONDOWN and game_data["game_over"] and mouse_over_play_again(): # user clicked on play again
                # reset state
                game_data = new_game_data()
                player = Player()
                player_projectiles = [None]
                swarm_data = new_swarm_data(game_data)
                swarm = generate_new_swarm(game_data, swarm_data)
                alien_projectiles = []

        # run game
        if swarm_empty(swarm): # player cleared swarm/wave
            game_data["wave"] += 1
            swarm_data = new_swarm_data(game_data)
            swarm = generate_new_swarm(game_data, swarm_data)
            player.increment_lives()
        if not game_data["game_over"]:
            update_physics(screen, game_data, player, player_projectiles, swarm, swarm_data, alien_projectiles)
        
        # check if game is over
        if player.lost_all_lives() or swarm_reached_player(swarm_data):
            game_data["game_over"] = True

        # fill display frame
        fill_frame(screen, player, player_projectiles, swarm, game_data, alien_projectiles, swarm_data)
        # flip display to put new frame onto screen
        pygame.display.flip()

        # limit FPS to 60
        # keep track of delta time since last frame in seconds for physics calculations
        game_data["tic"] += 1
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
        "tic": 0,
    }

def new_swarm_data(game_data: dict) -> dict:
    wave: int = game_data["wave"]
    # swarm data variables
    location: Vector2 = Vector2((constants.SCREEN_SIZE.x / 2) - (constants.SWARM_LENGTH / 2), 120)
    location.y += (constants.SWARM_MOV_Y) * min(wave-1, 4)
    timer: int = constants.SWARM_TIMER - (0.05 * (8 if wave-1 > 8 else wave-1))
    direction: int = 1 if (wave - 1) % 2 == 0 else -1
    col_has_aliens: list[bool] = [True for c in range(constants.SWARM_COLS)]
    row_has_aliens: list[bool] = [True for r in range(constants.SWARM_ROWS)]
    return {
        "location": location, # northwest (top-left) of swarm location
        "max_timer": timer,
        "timer": timer, # time until swarm can move in seconds
        "direction": direction,
        "col_has_aliens": col_has_aliens,
        "row_has_aliens": row_has_aliens,
        "tic": 0,
    }

def generate_new_swarm(game_data: dict, swarm_data: dict) -> list[list[Alien]]:
    wave = game_data["wave"] - 1
    swarm: list[list[Alien]] = []
    for r in range(constants.SWARM_ROWS):
        row: list[Alien] = []
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

def swarm_empty(swarm: list[list[Alien]]) -> bool:
    for r in range(constants.SWARM_ROWS):
        for c in range(constants.SWARM_COLS):
            if swarm[r][c] is not None:
                return False
    return True

def update_physics(screen: Surface, game_data: dict, player: Player, player_projectiles: list[Projectile], swarm: list[list[Alien]], swarm_data: dict, alien_projectiles: list[Projectile]) -> None:
    # remove dead aliens who have finished death animation
    remove_dead_aliens(game_data, swarm, swarm_data)
    
    # if player is in death animation pause all physics updates exluding removing aliens that have finished death animation(line above)
    if player.get_death_animation() != 0:
        return None
    
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
        if random_int <= get_chance_to_shoot(len(alien_projectiles), swarm_data):
            alien_shoot(screen, swarm[0][c], alien_projectiles)
    # check for collisions
    check_collisions(screen, game_data, player, player_projectiles, swarm, swarm_data, alien_projectiles)

def remove_dead_aliens(game_data: dict, swarm: list[list[Alien]], swarm_data: dict) -> None:
    for r in range(constants.SWARM_ROWS):
        for c in range(constants.SWARM_COLS):
            if swarm[r][c] is None:
                continue
            if not swarm[r][c].has_died(): # continue if alien is not playing dead and playing death animation
                continue
            if swarm[r][c].death_animation_over(game_data["dt"]):
                swarm[r][c] = None

def get_chance_to_shoot(n: int, swarm_data: dict) -> int:
    return constants.SWARM_COLS - n + 5

def move_swarm(swarm: list[list[Alien]], swarm_data: dict) -> None:
    # check if you need to move swarm vertically or horizontally
    if swarm_reached_edge(swarm, swarm_data):
        # move swarm vertically
        swarm_data["direction"] *= -1
        swarm_data["location"].y += constants.SWARM_MOV_Y
    else:
        # move swarm horizontally
        swarm_data["location"].x = swarm_data["location"].x + (constants.SWARM_MOV_X * swarm_data["direction"])

    swarm_data["timer"] = swarm_data["max_timer"]
    swarm_data["tic"] += 1
    update_alien_locations(swarm, swarm_data)

def move_alien_projectiles(alien_projectiles: list[Projectile], game_data: dict) -> None:
    for i in range(len(alien_projectiles)):
        alien_projectiles[i].move(game_data["dt"])

def move_player_projectile(player_projectiles: list[Projectile], game_data: dict) -> None:
    if player_projectiles[0] is not None:
        player_projectiles[0].move(game_data["dt"])

def swarm_reached_edge(swarm: list[list[Alien]], swarm_data: dict) -> bool:
    loc_left: int = swarm_data["location"].x
    loc_right: int = swarm_data["location"].x + constants.SWARM_LENGTH
    # update left and right depending on col_has_aliens bool array
    for c in range(constants.SWARM_COLS):
        if swarm_data["col_has_aliens"][c]:
            break
        loc_left += constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X
    for c in range(constants.SWARM_COLS - 1, 0, -1):
        if swarm_data["col_has_aliens"][c]:
            break
        loc_right -= (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X)

    return (loc_left <= constants.SCREEN_BOUND_X and swarm_data["direction"] == -1) or (loc_right >= constants.SCREEN_SIZE.x - constants.SCREEN_BOUND_X and swarm_data["direction"] == 1)

def swarm_reached_player(swarm_data: dict) -> bool:
    loc_bot: int = swarm_data["location"].y + constants.SWARM_HEIGHT
    for r in range(constants.SWARM_ROWS - 1, 0, -1):
        if swarm_data["row_has_aliens"][r]:
            break
        loc_bot -= (constants.ALIEN_HITBOX_Y + constants.ALIEN_OFFSET_Y)
    return loc_bot >= constants.SCREEN_SIZE.y - 200

def update_alien_locations(swarm: list[Projectile], swarm_data: dict) -> None:
    for r in range(constants.SWARM_ROWS):
        for c in range(constants.SWARM_COLS):
            if swarm[r][c] is None:
                continue
            if swarm[r][c].has_died():
                continue
            x: int = c * (constants.ALIEN_HITBOX_X + constants.ALIEN_OFFSET_X) + swarm_data["location"].x
            y: int = r * (constants.ALIEN_HITBOX_Y + constants.ALIEN_OFFSET_Y) + swarm_data["location"].y
            swarm[r][c].update_pos(x, y)

def check_collisions(screen: Surface, game_data: dict, player: Player, player_projectiles: list[Projectile], swarm: list[list[Alien]], swarm_data: dict, alien_projectiles: list[Projectile]) -> None:
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
            if swarm[r][c].has_died():
                continue
            if rect_collision(player_projectiles[0].get_pos(), player_projectiles[0].get_hitbox(), swarm[r][c].get_pos(), swarm[r][c].get_hitbox()):
                game_data["score"] += swarm[r][c].get_score()
                swarm[r][c].kill() # queue to draw death animation
                player_projectiles[0] = None
                swarm_data["col_has_aliens"][c] = col_has_aliens(swarm, c)
                swarm_data["row_has_aliens"][r] = row_has_aliens(swarm, r)
                break

def col_has_aliens(swarm: list[list[Alien]], c: int) -> bool:
    for r in range(constants.SWARM_ROWS):
        if swarm[r][c] is not None:
            if swarm[r][c].has_died():
                continue
            return True
    return False

def row_has_aliens(swarm: list[list[Alien]], r: int) -> bool:
    for c in range(constants.SWARM_COLS):
        if swarm[r][c] is not None:
            if swarm[r][c].has_died():
                continue
            return True
    return False

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

def player_shoot(screen: Surface, player: Player, player_projectiles: list[Projectile]) -> None:
    if player_projectiles[0] is not None:
        return None
    player_pos: Vector2 = player.get_pos()
    player_projectiles[0] = Projectile("laser", -1, player_pos.x + 30, player_pos.y - 34,)

def alien_shoot(screen: Surface, alien: Alien, alien_projectiles: list[Projectile]) -> None:
    if alien is None:
        return None
    alien_pos: Vector2 = alien.get_pos()
    alien_hitbox: Vector2 = alien.get_hitbox()
    rand: int = random.randint(1, 100)
    if rand < 20:
        alien_projectiles.append(Projectile("wiggle", 1, alien_pos.x + alien_hitbox.x / 2 - 3, alien_pos.y + alien_hitbox.y / 2))
    else:
        alien_projectiles.append(Projectile("cross", 1, alien_pos.x + alien_hitbox.x / 2 - 2, alien_pos.y + alien_hitbox.y / 2))

def fill_frame(screen: Surface, player: Player, player_projectiles: list[Projectile], swarm: list[list[Alien]], game_data: dict, alien_projectiles: list[Projectile], swarm_data: dict) -> None:
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
        player.draw(screen, game_data["dt"])
        return None
    # draw all objects
    # player
    player.draw(screen, game_data["dt"])
    # aliens
    for row in swarm:
        for alien in row:
            if alien is None: 
                continue
            alien.draw(screen, swarm_data["tic"])
    # player projectile
    if player_projectiles[0] is not None:
        player_projectiles[0].draw(screen)
    # alien projectiles
    for i in range(len(alien_projectiles)):
        alien_projectiles[i].draw(screen)

def mouse_over_play_again() -> bool:
    mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
    return mouse_pos_x >= 562 and mouse_pos_x <= 780 and mouse_pos_y >= 462 and mouse_pos_y <= 496

if __name__ == "__main__":
    main()