import pygame
from pygame import Event
from collections import deque

ANIMATION_STEPS = 10


class Player:
    def __init__(self, board_width, board_height) -> None:
        self.x = 0
        self.y = 0
        self.movement_frames = deque()
        self.board_width = board_width
        self.board_height = board_height

    def handle_input(self, event: Event):
        # early return if already in animation
        if len(self.movement_frames) != 0:
            return
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT: self.move_left()
                case pygame.K_UP: self.move_up()
                case pygame.K_RIGHT: self.move_right()
                case pygame.K_DOWN: self.move_down()

    def update(self):
        if len(self.movement_frames) > 0:
            last = self.movement_frames.popleft()
            self.x = max(0, min(self.x + last[0], self.board_width - 1))
            self.y = max(0, min(self.y + last[1], self.board_height - 1))

    def move_left(self):
        if self.x > 0:
            self.movement_frames = subdivide_movement([-1, 0], ANIMATION_STEPS)

    def move_up(self):
        if self.y > 0:
            self.movement_frames = subdivide_movement([0, -1], ANIMATION_STEPS)

    def move_right(self):
        if self.x < self.board_width - 1:
            self.movement_frames = subdivide_movement([1, 0], ANIMATION_STEPS)

    def move_down(self):
        if self.y < self.board_height - 1:
            self.movement_frames = subdivide_movement([0, 1], ANIMATION_STEPS)


def subdivide_movement(distance, steps) -> deque:
    return deque([[distance[0] / steps, distance[1] / steps] for _ in range(steps)])
