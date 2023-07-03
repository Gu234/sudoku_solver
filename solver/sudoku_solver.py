from solver.board import Cell, Board, InvalidCellException, NoCandidateException


class SudokuSolver:
    def __init__(self, sudoku) -> None:
        """sudoku input is expected in a common form of a string with zeros as empty values"""
        self.sudoku = sudoku
        self.prepare_board()

    def prepare_board(self):
        cells = []
        for row in range(9):
            for column in range(9):
                value = int(self.sudoku[row * 9 + column])
                value = value if value != 0 else None
                cell = Cell(row, column, value)
                cells.append(cell)
        self.board = Board(cells)

    def solve(self):
        new_board = self.board
        candidate_cell = new_board.get_cell_with_min_candidates()
        solution_stack = SolutionStack(self.board, None, candidate_cell)

        while not new_board.is_solved:
            try:
                candidate_cell = new_board.get_cell_with_min_candidates()
                candidate_value = candidate_cell.get_next_candidate()
                new_cell = Cell(
                    candidate_cell.row, candidate_cell.column, candidate_value
                )

                solution_stack = solution_stack.put(new_cell)
                new_board = solution_stack.board

            except InvalidCellException:
                candidate_cell.remove_candidate(candidate_value)

            except NoCandidateException:
                invalid_cell = solution_stack.cell
                solution_stack = solution_stack.root
                new_board = solution_stack.board
                old_cell = new_board.cells[invalid_cell.index]
                old_cell.remove_candidate(invalid_cell.value)

        return new_board.to_string_format()


class SolutionStack:
    def __init__(self, board, root, candidate_cell) -> None:
        self.board = board
        self.root = root
        self.cell = candidate_cell

    def put(self, new_cell):
        new_board = self.board.updated_board(new_cell)
        new_branch = SolutionStack(new_board, self, new_cell)
        return new_branch
