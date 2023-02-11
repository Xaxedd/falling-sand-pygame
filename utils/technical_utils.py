import time
from dataclasses import dataclass
from enum import Enum
from typing import List


class Material(Enum):
    AIR = 0
    ROCK = 1
    SAND = 2


class State(Enum):
    FALLING = 0
    STILL = 1


@dataclass
class Cords:
    x: int
    y: int


@dataclass
class Obstacles(Cords):
    material: Material


@dataclass
class Sand(Cords):
    state: State


class Tech:
    @staticmethod
    def _to_str(x):
        return str(x)

    @staticmethod
    def _to_cords(x):
        x = x.replace("<", "")
        x = x.replace(": 1>", "")
        return eval(x)

    @classmethod
    def get_rock_points_list(cls, puzzle_input, max_height: int = 99999) -> List[Obstacles]:
        rock_structure_points_list = []
        for line in puzzle_input:
            line = line.strip()
            starting_points = line.split(" -> ")

            if len(starting_points) >= 2:
                index = 1
                while index < len(starting_points):
                    start_cords = cls._get_cords(starting_points[index - 1])
                    ending_cords = cls._get_cords(starting_points[index])
                    if start_cords.x == ending_cords.x:
                        if start_cords.y >= ending_cords.y:
                            for i in range(ending_cords.y, start_cords.y + 1):
                                if i > max_height:
                                    continue
                                rock_structure_points_list.append(Obstacles(x=start_cords.x, y=i, material=Material.ROCK))
                        else:
                            for i in range(start_cords.y, ending_cords.y + 1):
                                if i > max_height:
                                    continue
                                rock_structure_points_list.append(Obstacles(x=start_cords.x, y=i, material=Material.ROCK))

                    if start_cords.y == ending_cords.y:
                        if start_cords.x >= ending_cords.x:
                            for i in range(ending_cords.x, start_cords.x + 1):
                                if start_cords.y > max_height:
                                    continue
                                rock_structure_points_list.append(Obstacles(x=i, y=start_cords.y, material=Material.ROCK))
                        else:
                            for i in range(start_cords.x, ending_cords.x + 1):
                                if start_cords.y > max_height:
                                    continue
                                rock_structure_points_list.append(Obstacles(x=i, y=start_cords.y, material=Material.ROCK))
                    index += 1
        rock_structure_points_list = cls._delete_duplicates(rock_structure_points_list)
        rock_structure_points_list = cls._change_coordinate_x_values_to_normal(rock_structure_points_list)
        return rock_structure_points_list

    @staticmethod
    def _get_cords(cords: str):
        splitted_cords = cords.split(",")
        return Cords(x=int(splitted_cords[0]),
                     y=int(splitted_cords[1]))

    @classmethod
    def _delete_duplicates(cls, rock_list: List[Cords]):
        stringified = set(map(cls._to_str, rock_list))
        return list(map(cls._to_cords, stringified))

    @classmethod
    def _delete_unreachable_cords(cls, usable_coordinates: List[Obstacles], for_visualization: List[Obstacles]):
        good_cords = []
        for usable_cord in usable_coordinates:
            needed_cord = True
            if cls._get_coordinate_material(for_visualization, x=usable_cord.x, y=usable_cord.y - 1) is not Material.AIR:
                if cls._get_coordinate_material(for_visualization, x=usable_cord.x - 1, y=usable_cord.y) is not Material.AIR and \
                        cls._get_coordinate_material(for_visualization, x=usable_cord.x + 1, y=usable_cord.y) is not Material.AIR:
                    if cls._get_coordinate_material(for_visualization, x=usable_cord.x - 1, y=usable_cord.y - 1) is not Material.AIR and \
                            cls._get_coordinate_material(for_visualization, x=usable_cord.x + 1, y=usable_cord.y - 1) is not Material.AIR:
                        if cls._get_coordinate_material(for_visualization, x=usable_cord.x - 2, y=usable_cord.y) is not Material.AIR and \
                                cls._get_coordinate_material(for_visualization, x=usable_cord.x + 2, y=usable_cord.y) is not Material.AIR:
                            needed_cord = False
            if needed_cord:
                good_cords.append(usable_cord)
        return good_cords

    @classmethod
    def _change_coordinate_x_values_to_normal(cls, rock_point_list):
        min_x = cls.get_min_x(rock_point_list)
        new_list = []
        for cord in rock_point_list:
            cord.x -= min_x
            new_list.append(cord)
        return new_list

    @staticmethod
    def _get_coordinate_material(grid: List[Obstacles], x: int, y: int):
        for cord in grid:
            if cord.x == x and cord.y == y:
                return cord.material
        return Material.AIR

    @staticmethod
    def get_max_y(rock_structure_points_list):
        sort2 = sorted(rock_structure_points_list, key=lambda x: (x.y, x.x))
        return sort2[-1].y

    @staticmethod
    def get_min_x(rock_structure_points_list):
        sort = sorted(rock_structure_points_list, key=lambda x: (x.x, x.y))
        return sort[0].x

    @staticmethod
    def get_max_x(rock_structure_points_list):
        sort = sorted(rock_structure_points_list, key=lambda x: (x.x, x.y))
        return sort[-1].x

    @classmethod
    def fall_sand(cls, sand_cord_rn: Sand, obstacles_list: List[Obstacles]):
        material_under = cls._get_coordinate_material(obstacles_list, x=sand_cord_rn.x, y=sand_cord_rn.y + 1)
        if material_under is Material.AIR:
            sand_cord_rn.y = sand_cord_rn.y + 1
        elif material_under is Material.ROCK or material_under is Material.SAND:
            material_under = cls._get_coordinate_material(obstacles_list, x=sand_cord_rn.x - 1, y=sand_cord_rn.y + 1)
            if material_under is Material.AIR:
                sand_cord_rn.x = sand_cord_rn.x - 1
                sand_cord_rn.y = sand_cord_rn.y + 1
            elif material_under is Material.ROCK or material_under is Material.SAND:
                material_under = cls._get_coordinate_material(obstacles_list, x=sand_cord_rn.x + 1, y=sand_cord_rn.y + 1)
                if material_under is Material.AIR:
                    sand_cord_rn.x = sand_cord_rn.x + 1
                    sand_cord_rn.y = sand_cord_rn.y + 1
                elif material_under is Material.ROCK or material_under is Material.SAND:
                    sand_cord_rn.state = State.STILL
                    return sand_cord_rn
        return sand_cord_rn
