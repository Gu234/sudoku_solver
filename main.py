from database import sudokus
from sudoku_solver import SudokuSolver
from itertools import product
from time import time
def main():
    avrg_time = 0
    avrg_loops = 0
    for i in range(1, 101):
        time_delta = time()
        # print(f'Solving for sudoku: {i}')
        solver = SudokuSolver(sudokus[i]['initial'])
        solution, loop_counter = solver.solve()
        time_delta = time() - time_delta
        avrg_time += time_delta
        avrg_loops += loop_counter

    avrg_time /= 100
    avrg_loops /= 100 

    print('Average time: ', avrg_time, 'Average loops: ', avrg_loops)

if __name__ == "__main__":
    main()
