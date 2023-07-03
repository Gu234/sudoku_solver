from solver.sudoku_solver import SudokuSolver
import pytest


@pytest.fixture
def simple_sudoku():
    return {
        "initial": "090060100030201004200080000500103900000006000009000008300509800040000070000020000",
        "solution": "794365182835271694216984753582143967473896521169752438327519846941638275658427319",
    }


@pytest.fixture
def hard_sudoku():
    return {
        "initial": "004300209005009001070060043006002087190007400050083000600000105003508690042910300",
        "solution": "864371259325849761971265843436192587198657432257483916689734125713528694542916378",
    }


def test_solve_simple_sudoku(simple_sudoku):
    solver = SudokuSolver(simple_sudoku["initial"])
    solution = solver.solve()
    assert solution == simple_sudoku["solution"]


def test_solve_hard_sudoku(hard_sudoku):
    solver = SudokuSolver(hard_sudoku["initial"])
    solution = solver.solve()
    assert solution == hard_sudoku["solution"]
