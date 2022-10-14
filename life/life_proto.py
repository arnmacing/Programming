import copy
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Первая отрисовка поля
        self.grid = [[]]

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        # список клеток
        self.grid = self.create_grid(randomize=True)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [
            [random.randint(0, 1) if randomize else 0 for j in range(self.cell_width)]
            for i in range(self.cell_height)
        ]
        return grid

    def draw_grid(self) -> None:
        for h in range(self.cell_height):
            for w in range(self.cell_width):
                y = h * self.cell_size
                x = w * self.cell_size
                color = pygame.Color('white') if self.grid[h][w] == 0 else pygame.Color('green')
                # Rect - координаты прямоугольника в формате (x, y, длина стороны a, длина стороны b)
                # Screen - где нужно отрисовать прямоугольник
                pygame.draw.rect(self.screen, color, [x + 1, y + 1, self.cell_size - 1, self.cell_size - 1])

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                h = cell[0] + i
                w = cell[1] + j
                if i == 0 and j == 0:  # мёртвые клетки
                    continue
                if 0 <= w < self.cell_width and 0 <= h < self.cell_height:
                    neighbours.append(self.grid[h][w])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = copy.deepcopy(self.grid)  # полная копия
        for h in range(self.cell_height):
            for w in range(self.cell_width):
                neighbours = self.get_neighbours((h, w))  # получили соседей
                alive_neighbours = sum(neighbours)  # сумма единиц, т.е. живых клеток
                if alive_neighbours != 2 and alive_neighbours != 3:
                    new_grid[h][w] = 0  # мёртвая
                elif alive_neighbours == 3:
                    new_grid[h][w] = 1  # рождается новая

        return new_grid
