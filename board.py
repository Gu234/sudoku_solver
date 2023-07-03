from time import sleep
import os


class Board:
    def __init__(self, cells) -> None:
        self.cells = cells
        empty_cells = []
        for cell in cells:
            self.setup_possible_cell_states(cell)
            if cell.value is None:
                empty_cells.append(cell)
        self.sorted_empty_cells = sorted(empty_cells, key=lambda cell: len(cell.candidates))

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
        return self.sorted_empty_cells[0]

    def yield_connected_cells(self, target_cell):
        box_indexes = get_indexes_from_box_id(target_cell.box_id)
        row_indexes = [target_cell.row * 9 + i for i in range(9)]
        column_indexes = [target_cell.column + i * 9 for i in range(9)]
        
        indexes_set = set(box_indexes + row_indexes + column_indexes)
        indexes_set.remove(target_cell.index)

        for index in indexes_set:
            yield self.cells[index]

    def updated_board(self, cell):
        new_cells = []
        for c in self.cells:
            new_cell = Cell(c.row, c.column, c.value)
            new_cells.append(new_cell)
        new_cells[cell.index] = cell
        return Board(new_cells)

    @property
    def is_solved(self):
        return self.sorted_empty_cells == []

    @property
    def empty_cells(self):
        return self.sorted_empty_cells

    
    def setup_possible_cell_states(self, target_cell):
        ''' given the current sudoku state, setup candidate values for a given cell '''
        for cell in self.yield_connected_cells(target_cell):
            if cell.value in target_cell.candidates:
                target_cell.candidates.discard(cell.value)

            cell.validate()

      

class CellException(Exception):
    pass


class InvalidCellException(CellException):
    pass


class NoCandidateException(CellException):
    pass


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
        raise NoCandidateException

    def remove_candidate(self, value):
        self.candidates.discard(value)

    def validate(self):
        if self.value is None and len(self.candidates) == 0:
            raise InvalidCellException


corner_box_ids = {
    1: 0,
    2: 3,
    3: 6,
    4: 27,
    5: 30,
    6: 33,
    7: 54,
    8: 57,
    9: 60
}


def get_indexes_from_box_id(box_id):
    corner_index = corner_box_ids[box_id]
    indexes = []
    for i in range(3):
        for j in range(3):
            indexes.append(corner_index + j + i * 9)
    return indexes
