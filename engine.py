from os import system
from time import sleep
from typing import List
from keyboard import read_event, KEY_DOWN

RED = "\033[91m"
RESET = "\033[0m"

patterns = {
    "I": [
        [1, 1, 1, 1],
    ],
    "O": [
        [1, 1],
        [1, 1],
    ],
    "T": [
        [0, 1, 0],
        [1, 1, 1],
    ],
    "J": [
        [1, 0, 0],
        [1, 1, 1],
    ],
    "L": [
        [0, 0, 1],
        [1, 1, 1],
    ],
    "S": [
        [0, 1, 1],
        [1, 1, 0],
    ],
    "Z": [
        [1, 1, 0],
        [0, 1, 1],
    ],
}


class Entity:
    def __init__(self, pattern, color, coords=[0, 0]) -> None:
        self.coordinates = coords
        self.pattern = pattern
        self.color = color

    def rotate(self):
        pass


def display(arena: List[List[int]], block: Entity):
    for i in range(len(arena)):
        for j in range(len(arena[0])):
            if [i, j] == block.coordinates:
                print(f"{block.color}@{RESET}", end=" ")
            else:
                print(".", end=" ")
        print("")


def get_key() -> str:
    while True:
        event = read_event()
        if event.event_type == KEY_DOWN:
            return event.name


if __name__ == "__main__":
    width = 6
    height = 12
    arena = [[0 for _ in range(width)] for _ in range(height)]
    block = Entity(patterns["T"], RED)

    for tick in range(height):
        display(arena, block)
        sleep(0.5)
        key = get_key()
        match key:
            case "left":
                block.coordinates[1] -= 1
            case "right":
                block.coordinates[1] += 1
            case "space":
                block.coordinates[0] = height - 1
                system("cls")
                display(arena, block)
                break
            case "up":
                block.rotate()
            case _:
                print(key)

        block.coordinates[0] += 1
        system("cls")
