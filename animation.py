from typing import Callable


BASE_DISTANCE = 100000 / 3
BASE_DURATION = 100

class Animation:
    def __init__(self, initial_position: list[float | int, float | int], translation: list[float | int, float | int], duration: float | int) -> None:
        self.duration = duration  # millis
        self.lifetime = 0
        self.initial_x = initial_position[0]
        self.initial_y = initial_position[1]
        self.x_function = self.scaled(translation[0], self.duration)
        self.y_function = self.scaled(translation[1], self.duration)
        self.target = initial_position[0] + translation[0], initial_position[1] + translation[1]

    def base(self, x) -> float:
        # f(x) = -x^3 / 15 + 10x^2
        # approximates an S shaped curve on [0 to 100]
        return -x**3 / 15 + 10 * x ** 2

    def scaled(self, distance: float | int, duration: float | int) -> Callable[[float | int], float]:
        if distance == 0:
            return lambda x: 0
        distance_scale = distance / BASE_DISTANCE
        duration_scale = BASE_DURATION / duration
        return lambda x: self.base(x * duration_scale) * distance_scale

    def apply(self, delta) -> list[float, float] | None:
        if self.lifetime >= self.duration:
            return None
        self.lifetime = min(self.lifetime + delta, self.duration)
        if self.lifetime == self.duration:
            return self.target
        else:
            return self.initial_x + self.x_function(self.lifetime), self.initial_y + self.y_function(self.lifetime)
