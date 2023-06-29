from time import sleep
import os


class InvalidCellException(Exception):
    pass


class Board:
    def __init__(self, cells) -> None:
        self.cells = cells
        for cell in cells:
            self.setup_possible_cell_states(cell)

    def to_table_format(self):
        table = [[0] * 9 for i in range(9)]
        for cell in self.cells:
            table[cell.row][cell.column] = cell.value
        return table

    def draw(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('#####################')
        for row in range(9):
            str_to_print = ''
            for column in range(9):
                value = self.cells[row * 9 + column].value
                value = str(value) if value else '_'
                str_to_print += value + ' '
            print(str_to_print)
        print('#####################')
        sleep(0.1)

    def get_cell_with_min_candidates(self):
        sorted_cells = sorted(
            self.empty_cells, key=lambda cell: len(cell.candidates))
        return sorted_cells[0]

    def get_connected_cells(self, target_cell):
        return [cell for cell in self.cells if (
                cell.row == target_cell.row or
                cell.column == target_cell.column or
                cell.box_id == target_cell.box_id
                )
                ]

    def updated_board(self, cell):
        new_cells = self.cells.copy()
        new_cells[cell.index] = cell
        return Board(new_cells)

    @property
    def is_solved(self):
        return self.empty_cells == []

    @property
    def empty_cells(self):
        return [cell for cell in self.cells if cell.value is None]

    def get_cells_by_box_id(self, box_id):
        ''' return list of cells that reside in the same sudoku box as given cell '''
        return [cell for cell in self.cell if cell.box_id == box_id]

    def setup_possible_cell_states(self, target_cell):
        ''' given the current sudoku state, setup candidate values for a given cell '''
        for cell in self.get_connected_cells(target_cell):
            if cell.value in target_cell.candidates:
                target_cell.candidates.discard(cell.value)

            cell.validate()


class Cell:
    def __init__(self, row, column, value) -> None:
        self.value = value
        self.row = row
        self.column = column
        self.box_id = ((column // 3) + 1) + ((row // 3) * 3)
        if value is None:
            self.candidates = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:
            self.candidates = {}

    @property
    def index(self):
        return self.row * 9 + self.column

    def get_next_candidate(self):
        for i in range(1, 10):
            if i in self.candidates:
                return i
        raise InvalidCellException

    def remove_candidate(self, value):
        self.candidates.discard(value)
        try:
            self.validate()
            return True
        except InvalidCellException:
            return False

    def validate(self):
        if self.value is None and len(self.candidates) == 0:
            raise InvalidCellException



