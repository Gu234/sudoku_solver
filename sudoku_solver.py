from board import Cell, Board, InvalidCellException


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
        solution_stack = SolutionStack(self.board, None, candidate_cell)

        while not new_board.is_solved:

            candidate_cell = new_board.get_cell_with_min_candidates()
            new_cell = Cell(candidate_cell.row, candidate_cell.column,
                            candidate_cell.get_next_candidate())

            try:
                # propagate
                solution_stack = solution_stack.add_leaf(new_cell)
                new_board = solution_stack.board
            except InvalidCellException:

                # backtrack
                stable = candidate_cell.remove_candidate(new_cell.value)
                while not stable:
                    solution_stack = solution_stack.root
                    old_cell = solution_stack.candidate_cell
                    new_board = solution_stack.board
                    value = old_cell.get_next_candidate()
                    stable = old_cell.remove_candidate(value)

            new_board.draw()

        return new_board


class SolutionStack:
    def __init__(self, board, root, candidate_cell) -> None:
        self.board = board
        self.root = root
        self.cell = candidate_cell

    def add_leaf(self, new_cell):
        new_board = self.board.updated_board(new_cell)
        new_branch = SolutionStack(new_board, self, new_cell)
        return new_branch
