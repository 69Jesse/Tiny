import pygame
import sys
import random
import time


GRID_SIZE: tuple[int, int] = (256, 256)
CELL_SIZE: int = 4

TWO_AND_THREE: set[int] = {2, 3}
THREE: int = 3


class Grid:
    width: int
    height: int
    cells: list[bool]
    last_cells: list[bool]
    checks: dict[int, tuple[bool, bool, bool, bool, bool, bool, bool, bool]]
    adds: tuple[int, int, int, int, int, int, int, int]
    def __init__(
        self,
        size: tuple[int, int],
    ) -> None:
        self.width, self.height = size
        self.cells = [random.choice((True, False)) for _ in range(self.width * self.height)]
        self.last_cells = [not cell for cell in self.cells]
        self.checks = {
            y * self.width + x: (
                x > 0 and y > 0,
                y > 0,
                x < self.width - 1 and y > 0,
                x > 0,
                x < self.width - 1,
                x > 0 and y < self.height - 1,
                y < self.height - 1,
                x < self.width - 1 and y < self.height - 1,
            ) for y in range(self.height) for x in range(self.width)
        }
        self.adds = (
            -self.width - 1,
            -self.width,
            -self.width + 1,
            -1,
            1,
            self.width - 1,
            self.width,
            self.width + 1,
        )

    def get_count(self, index: int) -> int:
        return sum(
            check and self.last_cells[index + add]
            for add, check in zip(self.adds, self.checks[index])
        )

    def update(self) -> None:
        self.last_cells = self.cells.copy()
        for i in range(self.width * self.height):
            count = self.get_count(i)
            if self.last_cells[i]:
                self.cells[i] = count in (2, 3)
            else:
                self.cells[i] = count == 3


ON: int = 0xFFFFFF
OFF: int = 0x000000
COLOUR: dict[bool, int] = {True: ON, False: OFF}


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((GRID_SIZE[0] * CELL_SIZE, GRID_SIZE[1] * CELL_SIZE))
    screen.fill(OFF)
    clock = pygame.time.Clock()
    grid = Grid(GRID_SIZE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        grid.update()
        for i in range(grid.width * grid.height):
            cell = grid.cells[i]
            if grid.last_cells[i] is not cell:
                x, y = i % grid.width, i // grid.width
                pygame.draw.rect(screen, COLOUR[cell], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.set_caption(f'Game of Life - {clock.get_fps():.2f} FPS')
        pygame.display.flip()
        clock.tick()


if __name__ == '__main__':
    main()
