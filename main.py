from ortools.sat.python import cp_model

def solve_queens(n, color_groups):
    model = cp_model.CpModel()

    # Variables
    x = {}
    for i in range(n):
        for j in range(n):
            x[(i, j)] = model.NewIntVar(0, 1, f'x_{i}_{j}')

    # Row constraints
    for i in range(n):
        model.Add(sum(x[(i, j)] for j in range(n)) == 1)

    # Column constraints
    for j in range(n):
        model.Add(sum(x[(i, j)] for i in range(n)) == 1)

    # Color constraints
    color_to_cells = {}
    for i in range(n):
        for j in range(n):
            color = color_groups[i][j]
            if color not in color_to_cells:
                color_to_cells[color] = []
            color_to_cells[color].append(x[(i, j)])
    for color, cells in color_to_cells.items():
        model.Add(sum(cells) == 1)

    # Diagonal constraints (linearized)
    for i1 in range(n):
        for j1 in range(n):
            for i2 in range(n):
                for j2 in range(n):
                    if abs(i1 - i2) == abs(j1 - j2) and (i1 != i2 or j1 != j2):
                        # Auxiliary variable for x[(i1, j1)] * x[(i2, j2)]
                        y = model.NewIntVar(0, 1, f'y_{i1}_{j1}_{i2}_{j2}')
                        # Linearization constraints
                        model.Add(y <= x[(i1, j1)])
                        model.Add(y <= x[(i2, j2)])
                        model.Add(y >= x[(i1, j1)] + x[(i2, j2)] - 1)
                        # Enforce y = 0 (no two queens on the same diagonal)
                        model.Add(y == 0)

    # Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        solution = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                solution[i][j] = solver.Value(x[(i, j)])
        return solution
    else:
        return None


n = 9
color_groups = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0],
    [4, 4, 4, 1, 2, 2, 3, 0, 3],
    [5, 5, 4, 1, 1, 2, 3, 0, 3],
    [5, 4, 4, 1, 1, 2, 3, 3, 3],
    [5, 5, 4, 1, 1, 2, 7, 7, 3],
    [4, 4, 4, 6, 2, 2, 2, 7, 3],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 8],
]

solution = solve_queens(n, color_groups)
if solution:
    for row in solution:
        print(row)
else:
    print("No solution exists.")