import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.height, self.width = self.life.rows * cell_size, self.life.cols * cell_size
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, x), (self.height, x))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (y, 0), (y, self.width))

    def draw_grid(self) -> None:
        y = 0
        for row in self.life.curr_generation:
            x = 0
            for cell in row:
                color = pygame.Color("green") if cell else pygame.Color("white")
                pygame.draw.rect(self.screen, color, (y, x, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        paused = clicked = False
        while running and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # пауза
                    paused = not paused

                if not self.life.is_changing:
                    paused = True

                if paused and event.type == pygame.MOUSEBUTTONDOWN:  # нажатие кнопки
                    clicked = True
                    click_y, click_x = pygame.mouse.get_pos()

            if paused:
                if clicked:
                    prev_cell_state = self.life.curr_generation[click_y // self.cell_size][
                        click_x // self.cell_size
                        ]
                    self.life.curr_generation[click_y // self.cell_size][
                        click_x // self.cell_size
                        ] = (0 if prev_cell_state == 1 else 1)
                    clicked = False
            else:
                self.life.step()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


gui = GUI(GameOfLife((100, 100), max_generations=100))
gui.run()
