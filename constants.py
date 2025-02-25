import pygame
from pygame import Vector2

# screen constants
SCREEN_SIZE: Vector2 = Vector2(1280, 900)
SCREEN_BOUND_X: int = 68
# alien constants
ALIEN_HITBOX_X: int = 50
ALIEN_HITBOX_Y: int = 40
ALIEN_OFFSET_X: int = 15
ALIEN_OFFSET_Y: int = 22
# swarm constants
SWARM_ROWS: int = 5
SWARM_COLS: int = 11
SWARM_LENGTH: int = SWARM_COLS * (ALIEN_HITBOX_X + ALIEN_OFFSET_X) - ALIEN_OFFSET_X
SWARM_HEIGHT: int = SWARM_ROWS * (ALIEN_HITBOX_Y + ALIEN_OFFSET_Y) - ALIEN_OFFSET_Y
SWARM_MOV_X: int = 12
SWARM_MOV_Y: int = 30
SWARM_TIMER: float = 0.75