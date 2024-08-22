from itertools import chain
from os import system
from random import choice
from time import sleep
from typing import List, Tuple
from keyboard import read_event, KEY_DOWN

colors = ["\033[95m" "\033[94m" "\033[96m" "\033[92m" "\033[93m" "\033[91m" "\033[1m"]
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

    def width(self):
        return len(self.pattern[0])

    def height(self):
        return len(self.pattern)

    def rotate(self):
        self.pattern = [
            [self.pattern[j][i] for j in range(len(self.pattern))]
            for i in range(len(self.pattern[0]) - 1, -1, -1)
        ]

    def inbounds(self, point: Tuple[int, int]):
        x, y = self.coordinates
        return x <= point[0] <= x + self.width() and y <= point[1] <= y + self.height()

    def intersects(self, coords: Tuple[int, int]):
        x, y = self.coordinates
        if not self.inbounds(coords):
            return False

        i, j = [coords[1] - y, coords[0] - x]

        if i >= len(self.pattern) or j >= len(self.pattern[0]):
            return False

        return self.pattern[i][j]

    def colides(self, arena: List[List[int]]):
        x, y = self.coordinates
        sample = [row[x : x + self.width()] for row in arena][y : y + self.height()]
        return any(f and b for f, b in zip(chain(*self.pattern), chain(*sample)))


def display(arena: List[List[int]], block: Entity):
    for i in range(len(arena)):
        for j in range(len(arena[0])):
            if arena[i][j]:
                print("#", end=" ")
                continue
            if block.intersects((j, i)):
                print(f"{block.color}@{RESET}", end=" ")
            else:
                print(".", end=" ")
        print("")


def solidify(arena: List[List[int]], block: Entity):
    x, y = block.coordinates
    for i in range(block.height()):
        for j in range(block.width()):

            arena[y + i][x + j] = arena[y + i][x + j] or block.pattern[i][j]


def get_key() -> str:
    while True:
        event = read_event()
        if event.event_type == KEY_DOWN:
            return event.name


if __name__ == "__main__":
    width = 6
    height = 12
    arena = [[0 for _ in range(width)] for _ in range(height)]
    arena.append([1 for _ in range(width)])
    block = Entity(patterns["T"], choice(colors))

    while True:
        display(arena, block)
        print(block.coordinates)
        sleep(0.25)
        match get_key():
            case "left":
                if block.coordinates[0] > 0:
                    block.coordinates[0] -= 1
            case "right":
                if block.coordinates[0] + block.width() < width:
                    block.coordinates[0] += 1
            case "space":
                block.coordinates[1] = height - 1
                display(arena, block)
            case "r":
                block.rotate()
            case "q":
                print("GAME OVER")
                break

        block.coordinates[1] += 1
        if block.colides(arena) or block.coordinates[1] == height:
            block.coordinates[1] -= 1
            solidify(arena, block)
            block = Entity(choice(list(patterns.values())), choice(colors), [0, 0])

        system("cls")


# TODO: ganhar o jogo (depois de 99999999 pontos)
# TODO: excluir linhas
# TODO: acumular pontos
# TODO: preview dos próximos blocos
# TODO: sortear cor para os blocos
# TODO: perder o jogo
