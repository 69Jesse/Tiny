import json
import pygame
import random
import time

from typing import (
    Any,
    Optional,
)
from typing_extensions import (
    Self,
)


COLORS: dict[str, int] = {
    'background1': 0xFFFFFF,
    'from_start_background1': 0xFFC9DB,
    'background2': 0xCCCCCC,
    'from_start_background2': 0xCDA1B0,
    'border': 0x000000,
    'text': 0x000000,
    'subtext': 0x000000,
    'selected': 0xADD8FD,
    'selected_editing_subvalues': 0xADD8A0,
    'same_as_selected': 0xFFF200,
}
SIZE: tuple[int, int] = (
    750,
    750,
)
CELL_SIZE: tuple[int, int] = (SIZE[0] // 9, SIZE[1] // 9)
SIZE = (CELL_SIZE[0] * 9, CELL_SIZE[1] * 9)
BORDER_PERCENTAGE: float = 0.025


def jsonify(obj: Any) -> dict[str, Any]:
    return {attr: getattr(obj, attr) for attr in getattr(obj, 'saving_attributes', [])}

def hex8(n: int) -> int:
    return int(f'{hex(n)[2:]:06}FF', 16)


class Cell:
    saving_attributes: tuple[str, ...] = ('position', 'value', 'subvalues', 'from_start')
    def __init__(self, position: tuple[int, int], value: Optional[int] = None, subvalues: Optional[list[int]] = None, from_start: bool = False) -> None:
        self.position = position
        self.value = value
        self.subvalues = subvalues or []
        self.from_start = from_start
        self.invalid: list[int] = []


class Grid:
    saving_attributes: tuple[str, ...] = ('cells_as_list', 'started', 'saved_at')
    def __init__(self, cells: Optional[dict[tuple[int, int], Cell]] = None, started: Optional[float] = None) -> None:
        self.groups = self.generate_groups()
        self.cells = cells or self.generate_cells()
        self.started = started or time.time()
        self.selected: Optional[Cell] = None

    @property
    def cells_as_list(self) -> list[Cell]:
        return list(self.cells.values())

    def filled(self, cells: Optional[dict[tuple[int, int], Cell]] = None) -> bool:
        cells = cells or self.cells
        return all(cell.value is not None for cell in cells.values())

    def valid(self, cells: Optional[dict[tuple[int, int], Cell]] = None) -> bool:
        cells = cells or self.cells
        for group in self.groups:
            values = [v for v in (cells[x, y].value for x, y in group) if v is not None]
            if not len(set(values)) == len(values):
                return False
        return True

    def solve(self, cells: Optional[dict[tuple[int, int], Cell]] = None, randomly: bool = False) -> None:
        cells = cells or self.cells
        if randomly:
            values = lambda: random.sample(range(1, 10), 9)
        else:
            values = lambda: range(1, 10)

        def recursive(cells: dict[tuple[int, int], Cell]) -> None:
            for cell in cells.values():
                if cell.value is not None:
                    continue

                for value in values():
                    cell.value = value
                    if self.valid(cells=cells):
                        recursive(cells=cells)
                        if self.filled(cells=cells):
                            return
                    cell.value = None
                return

        recursive(cells=cells)

    def generate_cells(self) -> dict[tuple[int, int], Cell]:
        cells: dict[tuple[int, int], Cell] = {}
        for y in range(9):
            for x in range(9):
                cells[(x, y)] = Cell((x, y))
        self.solve(cells, randomly=True)

        for _ in range(random.randrange(30, 51)):
            cell = random.choice([c for c in cells.values() if c.value is not None])
            cell.value = None

        for cell in cells.values():
            if cell.value is not None:
                cell.from_start = True

        return cells

    def generate_groups(self) -> list[list[tuple[int, int]]]:
        groups: list[list[tuple[int, int]]] = []
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                groups.append([(x + i, y + j) for i in range(3) for j in range(3)])
        for i in range(9):
            groups.append([(i, j) for j in range(9)])
            groups.append([(j, i) for j in range(9)])

        return groups

    def won(self) -> bool:
        return self.filled() and self.valid()

    @classmethod
    def new(cls) -> Self:
        return cls()

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        cells: dict[tuple[int, int], Cell] = {}
        for c in data.pop('cells_as_list'):
            c['position'] = tuple(c.get('position'))
            cells[c.get('position')] = Cell(**c)
        data['started'] = time.time() - (data.pop('saved_at') - data['started'])
        return cls(cells=cells, **data)

    @classmethod
    def from_save(cls, fp: Optional[str] = None) -> Self:
        fp = fp or 'save.json'
        with open(fp, 'r') as f:
            return cls.from_json(json.load(f))

    @property
    def saved_at(self) -> float:
        return time.time()

    def to_json(self) -> str:
        return json.dumps(self, default=jsonify, indent=4)

    def save(self, fp: Optional[str] = None) -> None:
        fp = fp or 'save.json'
        with open(fp, 'w') as f:
            f.write(self.to_json())
        print(f'Saved game as {fp}!')

    def caption(self) -> str:
        filled = sum(cell.value is not None for cell in self.cells.values())
        m, s = divmod(int(time.time() - self.started), 60)
        return f'Sudoku - {filled}/{len(self.cells)} - {m:02}:{s:02}'


def main() -> None:
    try:
        grid = Grid.from_save()
        print('Successfully loaded game from save!')
    except Exception:
        grid = Grid.new()
        print('Could not load game from save, starting new game!')

    pygame.init()
    pygame.display.set_caption(grid.caption())
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial Black', int(min(CELL_SIZE) * 0.8))
    subfont = pygame.font.SysFont('Arial Black', int(min(CELL_SIZE) * 0.2))
    editing_subvalues: bool = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                grid.save()
                pygame.quit()
                print('Successfully saved game and quit!')
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    grid = Grid.new()
                    print('Successfully started new game!')
                elif event.key in (pygame.K_l, pygame.K_RSHIFT):
                    try:
                        grid = Grid.from_save()
                        print('Successfully loaded game from save!')
                    except Exception:
                        print('Could not load game from save!')
                elif event.key in (pygame.K_s, pygame.K_RETURN):
                    grid.save()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    if grid.selected is not None and not grid.selected.from_start:
                        num = event.key - pygame.K_0
                        if not editing_subvalues:
                            if grid.selected.value == num:
                                grid.selected.value = None
                            else:
                                grid.selected.value = num
                                grid.selected.subvalues = []
                        else:
                            if num in grid.selected.subvalues:
                                grid.selected.subvalues.remove(num)
                            else:
                                grid.selected.value = None
                                grid.selected.subvalues.append(num)
                                grid.selected.subvalues = grid.selected.subvalues[-4:]
                elif event.key == pygame.K_SLASH:
                    """debug"""
                    grid.solve()
                    if not grid.won():
                        print('There is no possible solution for the current grid!')

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x, y = x // CELL_SIZE[0], y // CELL_SIZE[1]
                if (x, y) not in grid.cells:
                    continue
                cell = grid.cells[(x, y)]
                if event.button in (1, 3):
                    right_click = {1: False, 3: True}[event.button]
                    if cell is grid.selected and right_click == editing_subvalues:
                        grid.selected = None
                    else:
                        grid.selected = cell
                    editing_subvalues = right_click
                if event.button == 2:
                    """debug"""
                    possible = list(range(1, 10))
                    for group in grid.groups:
                        if cell.position in group:
                            values = [grid.cells[p].value for p in group if cell.position != p]
                            for value in values:
                                if value in possible:
                                    possible.remove(value)
                    print(f'Possible values for {cell.position}: {possible}')

        screen.fill(COLORS['border'])
        for cell in grid.cells.values():
            pygame.draw.rect(
                screen,
                COLORS[(
                    ('selected' + '_editing_subvalues' * editing_subvalues) if cell is grid.selected else
                    'same_as_selected' if grid.selected is not None and cell.value == grid.selected.value and cell.value is not None else
                    'from_start_' * cell.from_start + ('background1' if (cell.position[0] // 3 + cell.position[1] // 3) % 2 == 0 else 'background2')
                )],
                pygame.Rect(
                    cell.position[0] * CELL_SIZE[0] + BORDER_PERCENTAGE * CELL_SIZE[0],
                    cell.position[1] * CELL_SIZE[1] + BORDER_PERCENTAGE * CELL_SIZE[1],
                    CELL_SIZE[0] * (1 - 2 * BORDER_PERCENTAGE),
                    CELL_SIZE[1] * (1 - 2 * BORDER_PERCENTAGE),
                ),
            )
            if cell.value is not None:
                text = font.render(str(cell.value), True, hex8(COLORS['text']))
                screen.blit(
                    text,
                    (
                        cell.position[0] * CELL_SIZE[0] + CELL_SIZE[0] // 2 - text.get_width() // 2,
                        cell.position[1] * CELL_SIZE[1] + CELL_SIZE[1] // 2 - text.get_height() // 2,
                    ),
                )
            if len(cell.subvalues) > 0:
                text = subfont.render(' '.join(str(v) for v in cell.subvalues), True, hex8(COLORS['subtext']))
                screen.blit(
                    text,
                    (
                        cell.position[0] * CELL_SIZE[0] + CELL_SIZE[0] // 2 - text.get_width() // 2,
                        cell.position[1] * CELL_SIZE[1],
                    ),
                )

        pygame.display.set_caption(grid.caption())
        if grid.won():
            text = font.render('YOU WIN!', True, hex8(COLORS['border']), hex8(COLORS['selected']))
            screen.blit(
                source=text,
                dest=(SIZE[0] // 2 - text.get_width() // 2, SIZE[1] // 2 - text.get_height() // 2),
            )
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
