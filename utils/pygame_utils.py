import math
from dataclasses import dataclass
from enum import Enum
from typing import List

import pygame

from utils.technical_utils import Tech, Obstacles, Material, Sand


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


class FALLING_SAND_ACTION(Enum):
    CLEAR = 0
    DRAW = 1


class Pygame:
    @classmethod
    def draw_obstacles(cls, screen, screen_info: ScreenInfo, points: List[Obstacles]):
        for point in points:
            if point.material is Material.ROCK:
                pygame.draw.rect(screen,
                                 Colors.black,
                                 pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                             point.y * screen_info.sand_height_in_pixels,
                                             screen_info.sand_width_in_pixels,
                                             screen_info.sand_height_in_pixels))
            elif point.material is Material.SAND:
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
        min_x = Tech.get_min_x(points) * sand_width
        map_pixel_width = max_x - min_x
        screen_width = screen.get_width()
        padding = math.floor((screen_width - map_pixel_width) / 2)
        return padding

    @classmethod
    def draw_falling_sand(cls, screen, screen_info, sand_list):
        cls.falling_sand(screen, screen_info, sand_list, falling_sand_action=FALLING_SAND_ACTION.DRAW)

    @classmethod
    def clear_falling_sand(cls, screen, screen_info, sand_list):
        cls.falling_sand(screen, screen_info, sand_list, falling_sand_action=FALLING_SAND_ACTION.CLEAR)

    @staticmethod
    def falling_sand(screen, screen_info, sand_list, falling_sand_action: FALLING_SAND_ACTION):
        if falling_sand_action is FALLING_SAND_ACTION.DRAW:
            pixel_color = Colors.yellow
        if falling_sand_action is FALLING_SAND_ACTION.CLEAR:
            pixel_color = Colors.white

        for point in sand_list:
            pygame.draw.rect(screen,
                             pixel_color,
                             pygame.Rect(point.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                         point.y * screen_info.sand_height_in_pixels,
                                         screen_info.sand_width_in_pixels,
                                         screen_info.sand_height_in_pixels))
        pygame.display.flip()

    @staticmethod
    def draw_sand(screen, screen_info, sand_coordinate_rn: Sand):
        drawn_sand = pygame.draw.rect(screen,
                                      Colors.yellow,
                                      pygame.Rect(sand_coordinate_rn.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                                  sand_coordinate_rn.y * screen_info.sand_height_in_pixels,
                                                  screen_info.sand_width_in_pixels,
                                                  screen_info.sand_height_in_pixels))
        pygame.display.update(drawn_sand)

    @staticmethod
    def setup_screen(width, height):
        size = [width, height]
        screen = pygame.display.set_mode(size)
        screen.fill(Colors.white)
        return screen
