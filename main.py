from database import sudoku
from sudoku_solver import SudokuSolver
from itertools import product

def main():
    solver = SudokuSolver(sudoku['initial'])
    solution = solver.solve()
    table_solution = solution.to_table_format()
    print(table_solution)

    success = True
    for i, j  in product(range(9), range(9)):
        if table_solution[i][j] != sudoku['solution'][i][j]:
            success = False
    
    if success:
        print('poprawne rozwiazanie')
    else:
        print('Failed solution')


if __name__ == "__main__":
    main()
