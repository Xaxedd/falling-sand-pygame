from dataclasses import dataclass
from enum import Enum
from typing import List

import pygame

from utils.technical_utils import Tech, Obstacles


@dataclass
class Colors:
    black = [0, 0, 0]
    white = [255, 255, 255]
    yellow = [230, 172, 37]


@dataclass
class ScreenInfo:
    sand_width_in_pixels: int
    sand_height_in_pixels: int
    padding: int


class XXX(Enum):
    CLEAR = 0
    DRAW = 1


class Pygame:
    @classmethod
    def draw_obstacles(cls, screen, screen_info: ScreenInfo, points: List[Obstacles]):
        for point in points:
            if point.material.value == 1:
                pygame.draw.rect(screen,
                                 Colors.black,
                                 pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                             point.y * screen_info.sand_height_in_pixels,
                                             screen_info.sand_width_in_pixels,
                                             screen_info.sand_height_in_pixels))
            elif point.material.value == 2:
                pygame.draw.rect(screen,
                                 Colors.yellow,
                                 pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                             point.y * screen_info.sand_height_in_pixels,
                                             screen_info.sand_width_in_pixels,
                                             screen_info.sand_height_in_pixels))
        pygame.display.flip()

    @staticmethod
    def get_padding(screen, points, sand_width):
        max_x = Tech.get_max_x(points) * sand_width
        screen_width = screen.get_width()
        return (screen_width - max_x) / 2

    @classmethod
    def draw_falling_sand(cls, screen, screen_info, sand_list):
        cls.falling_sand(screen, screen_info, sand_list, xxx=XXX.DRAW)

    @classmethod
    def clear_falling_sand(cls, screen, screen_info, sand_list):
        cls.falling_sand(screen, screen_info, sand_list, xxx=XXX.CLEAR)

    @staticmethod
    def falling_sand(screen, screen_info, sand_list, xxx: XXX):
        for point in sand_list:
            if xxx is XXX.CLEAR:
                pygame.draw.rect(screen,
                                 Colors.white,
                                 pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                             point.y * screen_info.sand_height_in_pixels,
                                             screen_info.sand_width_in_pixels,
                                             screen_info.sand_height_in_pixels))
            elif xxx is XXX.DRAW:
                pygame.draw.rect(screen,
                                 Colors.yellow,
                                 pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                             point.y * screen_info.sand_height_in_pixels,
                                             screen_info.sand_width_in_pixels,
                                             screen_info.sand_height_in_pixels))
        pygame.display.flip()

    @staticmethod
    def setup_screen(width, height):
        size = [width, height]
        screen = pygame.display.set_mode(size)
        screen.fill(Colors.white)
        return screen
