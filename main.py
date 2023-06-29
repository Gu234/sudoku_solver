from database import sudokus
from sudoku_solver import SudokuSolver
from itertools import product

def main():
    for i in range(1, 1000):
        print(f'Solving for sudoku: {i}')
        solver = SudokuSolver(sudokus[i]['initial'])
        solution = solver.solve()

        if test_solution(solution, sudokus[i]['solution']):
            continue
        else:
            raise Exception(f'Failed solution for id: {i}')


def test_solution(attempt, solution):
    for i, j in product(range(9), range(9)):
        if attempt[i][j] != solution[i][j]:
            return False
    return True
    

if __name__ == "__main__":
    main()
