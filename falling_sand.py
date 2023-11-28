import pygame

from utils.pygame_utils import Pygame, ScreenInfo
from utils.technical_utils import State, Sand, Tech, Obstacles, Material


def get_falling_sand_x_coordinate(puzzle_input):
    return abs(Tech.get_min_x_before_normalization(puzzle_input) - 500)


puzzle_input = open("puzzle_input.txt", "r", encoding="utf8").readlines()
whole_sorted_grid = Tech.get_rock_points_list(puzzle_input)
max_y = Tech.get_max_y(whole_sorted_grid)

for x in whole_sorted_grid:
    x.x += max_y+2

falling_sand_x_coordinte = get_falling_sand_x_coordinate(puzzle_input) + max_y + 2
for i in range(falling_sand_x_coordinte-max_y+2, falling_sand_x_coordinte+max_y+2):
    whole_sorted_grid.append(Obstacles(x=i, y=max_y+2, material=Material.ROCK))

pygame.init()
screen = Pygame.setup_screen(1900, 900)
sand_square_pixel_size = 4
screen_info = ScreenInfo(sand_width_in_pixels=sand_square_pixel_size,
                         sand_height_in_pixels=sand_square_pixel_size,
                         padding=Pygame.get_padding(screen, points=whole_sorted_grid, sand_width=sand_square_pixel_size))

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

    if Tech._get_coordinate_material(coordinates_for_sand, x=falling_sand_x_coordinte, y=0) is Material.SAND:
        end = True

    if iteration % 2 == 0:
        falling_sand_list.append(Sand(x=falling_sand_x_coordinte, y=0, state=State.FALLING))

    if iteration % 200 == 0:
        coordinates_for_sand = Tech._delete_unreachable_cords(coordinates_for_sand, whole_sorted_grid)

    sand_index = 0
    while sand_index < len(falling_sand_list):
        sand_cord_rn = falling_sand_list[sand_index]
        sand_cord_rn = Tech.fall_sand(sand_cord_rn, coordinates_for_sand)
        if sand_cord_rn.state is State.STILL:
            whole_sorted_grid.append(Obstacles(x=sand_cord_rn.x, y=sand_cord_rn.y, material=Material.SAND))
            coordinates_for_sand.append(Obstacles(x=sand_cord_rn.x, y=sand_cord_rn.y, material=Material.SAND))

            Pygame.draw_sand(screen, screen_info, sand_cord_rn)

            falling_sand_list.pop(sand_index)
            sand_index -= 1

        if sand_cord_rn.y > Tech.get_max_y(whole_sorted_grid):
            end = True
            break
        sand_index += 1
    iteration += 1
    Pygame.draw_falling_sand(screen, screen_info, falling_sand_list)
    pygame.time.wait(20)

sand_amount = 0
for x in whole_sorted_grid:
    if x.material is Material.SAND:
        sand_amount += 1
print("sand amount:", sand_amount)