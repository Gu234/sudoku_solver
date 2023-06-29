import csv 

sudokus = {}

# load database from csv into memory
print('Initializing database ...')
with open('./archive/sudoku.csv', newline='') as csvfile:

    sudoku_csv = csv.DictReader(csvfile)
    index = 0
    for row in sudoku_csv:
        index += 1
        initial_table = [[0] * 9 for i in range(9)]
        solution_table = [[0] * 9 for i in range(9)]

        for i in range(81):
            initial_value = int(row['quizzes'][i])
            initial_table[i // 9][i % 9] = initial_value if initial_value else None

            solution_value = int(row['solutions'][i])
            solution_table[i // 9][i % 9] = solution_value if solution_value else None
        
        if index > 1000:
            break

        sudoku = {
            'id': index,
            'initial': initial_table,
            'solution': solution_table
        }
        sudokus[index] = sudoku

print('Database initialized.')
