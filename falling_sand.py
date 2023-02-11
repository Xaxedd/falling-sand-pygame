import time

import pygame

from utils.pygame_utils import Pygame, ScreenInfo, Colors
from utils.technical_utils import State, Sand, Tech, Obstacles, Material

pygame.init()
screen = Pygame.setup_screen(600, 900)
puzzle_input = open("puzzle_input.txt", "r", encoding="utf8").readlines()
whole_sorted_grid = Tech.get_rock_points_list(puzzle_input)

screen_info = ScreenInfo(sand_width_in_pixels=5,
                         sand_height_in_pixels=5,
                         padding=Pygame.get_padding(screen, points=whole_sorted_grid, sand_width=5))
Pygame.draw_obstacles(screen, screen_info, whole_sorted_grid)
pygame.display.flip()

end = False
falling_sand_list = []
iteration = 0
coordinates_for_sand = whole_sorted_grid
coordinates_for_sand = Tech._delete_unreachable_cords(coordinates_for_sand, whole_sorted_grid)
print("good cords", coordinates_for_sand)
while not end:
    Pygame.clear_falling_sand(screen, screen_info, falling_sand_list)

    if iteration % 2 == 0:
        falling_sand_list.append(Sand(x=42, y=0, state=State.FALLING))

    if iteration % 200 == 0:
        coordinates_for_sand = Tech._delete_unreachable_cords(coordinates_for_sand, whole_sorted_grid)

    sand_index = 0
    while sand_index < len(falling_sand_list):
        sand_cord_rn = falling_sand_list[sand_index]
        sand_cord_rn = Tech.fall_sand(sand_cord_rn, coordinates_for_sand)
        if sand_cord_rn.state is State.STILL:
            whole_sorted_grid.append(Obstacles(x=sand_cord_rn.x, y=sand_cord_rn.y, material=Material.SAND))
            coordinates_for_sand.append(Obstacles(x=sand_cord_rn.x, y=sand_cord_rn.y, material=Material.SAND))
            drawn_sand = pygame.draw.rect(screen,
                                          Colors.yellow,
                                          pygame.Rect(sand_cord_rn.x * screen_info.sand_width_in_pixels + screen_info.padding,
                                                      sand_cord_rn.y * screen_info.sand_height_in_pixels,
                                                      screen_info.sand_width_in_pixels,
                                                      screen_info.sand_height_in_pixels))
            pygame.display.update(drawn_sand)
            falling_sand_list.pop(sand_index)
            sand_index -= 1

        if sand_cord_rn.y > Tech.get_max_y(whole_sorted_grid):
            end = True
            break
        sand_index += 1
    iteration += 1
    Pygame.draw_falling_sand(screen, screen_info, falling_sand_list)
    pygame.time.wait(20)
