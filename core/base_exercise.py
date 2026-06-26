import math 
from abc import ABC, abstractmethod

# in python, we make a class abstract by inheriting it from the abc module and using the @abstractmethod decorator on the methods that we want to make abstract. abc module = abstract base class module. 


class BaseExercise(ABC):
    def __init__(self):
        self.reps = 0
        self.stage = None

# function to calculate the angle between three points a, b, and c. The angle is calculated at point b using the coordinates of points a and c. The function returns the angle in degrees. If the magnitude of either vector is zero (which would result in a division by zero), it returns 0.0 degrees. Example: we have to calculate the angle at the knee joint (point b) formed by the hip (point a) and ankle (point c). The angle is calculated using the dot product formula and the arccosine function, which gives us the angle in radians. We then convert it to degrees for easier interpretation.

    def calculate_angle(self, a, b, c):
        ax, ay = a[0] - b[0], a[1] - b[1]
        cx, cy = c[0] - b[0], c[1] - b[1]

        dot = ax * cx + ay * cy

        mag_a = math.sqrt(ax ** 2 + ay ** 2)
        mag_c = math.sqrt(cx ** 2 + cy ** 2)

        if mag_a * mag_c == 0:
            return 0.0

        cos_angle = max(-1.0, min(1.0, dot / (mag_a * mag_c)))

        return math.degrees(math.acos(cos_angle))

    def get_point(self, landmarks, idx):
        p = landmarks[idx]

        return (p.x, p.y)

    @abstractmethod
    def process(self, landmarks):
        pass

    @abstractmethod
    def reset(self):
        pass