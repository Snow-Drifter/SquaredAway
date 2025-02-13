import pygame
from pygame import Event
from collections import deque

from animation import Animation

ANIMATION_DURATION = 500  # millis


class Player:
    def __init__(self, board_width: int, board_height: int) -> None:
        self.x = 0
        self.y = 0
        self.animations: deque[Animation] = deque()
        self.board_width = board_width
        self.board_height = board_height

    def handle_input(self, event: Event):
        # early return if already in animation
        if len(self.animations) != 0:
            return
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_LEFT: self.move_left()
                case pygame.K_UP: self.move_up()
                case pygame.K_RIGHT: self.move_right()
                case pygame.K_DOWN: self.move_down()

    def update(self, delta_time):
        if len(self.animations) > 0:
            first_animation = self.animations[0]
            movement = first_animation.apply(delta_time)
            if movement:
                self.x = max(0, min(movement[0], self.board_width - 1))
                self.y = max(0, min(movement[1], self.board_height - 1))
            else:
                # animation is over, discard it
                self.animations.popleft()
                # run update again (pick up next animation?)
                self.update(delta_time)

    def move_left(self):
        if self.x > 0:
            self.animations = self.animate([-1, 0])

    def move_up(self):
        if self.y > 0:
            self.animations = self.animate([0, -1])

    def move_right(self):
        if self.x < self.board_width - 1:
            self.animations = self.animate([1, 0])

    def move_down(self):
        if self.y < self.board_height - 1:
            self.animations = self.animate([0, 1])

    def animate(self, distance) -> deque[Animation]:
        return deque([Animation([self.x, self.y], distance, ANIMATION_DURATION)])
