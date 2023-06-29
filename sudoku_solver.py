from time import sleep
import os


class SudokuSolver:
    def __init__(self, sudoku) -> None:
        self.sudoku = sudoku
        self.prepare_board()

    def prepare_board(self):
        cells = []
        for row in range(9): 
            for column in range(9):
                cell = Cell(row, column, self.sudoku[row][column])
                cells.append(cell)
        self.board = Board(cells)

    def solve(self):

        new_board = self.board
        candidate_cell = new_board.get_cell_with_min_candidates()
        solution_tree = SolutionBranch(self.board, None, candidate_cell)

        while not new_board.is_solved:

            candidate_cell = new_board.get_cell_with_min_candidates()
            new_cell = Cell(candidate_cell.row, candidate_cell.column, candidate_cell.get_next_candidate())
            
            try:
                # propagate
                solution_tree = solution_tree.add_leaf(new_cell)
                new_board = solution_tree.board
            except InvalidCellException:
                
                # backtrack
                stable = candidate_cell.remove_candidate(new_cell.value)
                while not stable:
                    solution_tree = solution_tree.root
                    old_cell = solution_tree.candidate_cell
                    new_board = solution_tree.board
                    value = old_cell.get_next_candidate()
                    stable = old_cell.remove_candidate(value)
            
            new_board.draw()

        return new_board


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
        sorted_cells = sorted(self.empty_cells, key=lambda cell: len(cell.candidates))
        return sorted_cells[0]
        # target_cell = self.cells[0]
        # for cell in self.empty_cells:
        #     if len(cell.candidates) < len(target_cell.candidates):
        #         target_cell = cell
        # return target_cell
    
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

    def get_row(self, row):
        return [cell for cell in self.cells if cell.row == row]

    def get_column(self, column):
        return [cell for cell in self.cells if cell.column == column]

    def get_cells_by_box_id(self, box_id):
        ''' return list of cells that reside in the same sudoku box as given cell '''
        return [cell for cell in self.cell if cell.box_id == box_id]

    def setup_possible_cell_states(self, target_cell):
        ''' given the current sudoku state, setup candidate values for a given cell '''
        for cell in self.get_connected_cells(target_cell):
            if cell.value in target_cell.candidates:
                target_cell.candidates.discard(cell.value)

            cell.validate()


class InvalidCellException(Exception): pass


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
    
    # def new_without_candidate(self, value):
    #     ''' return new cell but without one value in candiadates '''
    #     new_cell = Cell(self.row, self.column, None)
    #     new_cell.candidates.discard(value)
    #     return new_cell

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


class SolutionBranch:
    def __init__(self, board, root, candidate_cell) -> None:
        self.board = board
        self.root = root
        self.leaves = {}
        self.cell = candidate_cell
        
        
    def add_leaf(self, new_cell):
        new_board = self.board.updated_board(new_cell)
        new_branch = SolutionBranch(new_board, self, new_cell)
        self.leaves[new_cell] = new_branch
        return new_branch
