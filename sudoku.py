from itertools import product

def solve_sudoku(grid):
    res = [line[:] for line in grid]
    x = ([("rc", rc) for rc in product(range(9), range(9))] +
            [("rn", rn) for rn in product(range(9), range(1, 10))] +
            [("cn", cn) for cn in product(range(9), range(1, 10))] +
            [("bn", bn) for bn in product(range(9), range(1, 10))])
    y = dict()
    for r, c, n in product(range(9), range(9), range(1, 10)):
        b = (r // 3) * 3 + (c // 3)
        y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]

    x = exact_cover(x, y)
    for i, line in enumerate(grid):
        for j, tile in enumerate(line):
            if tile:
                select(x, y, (i, j, tile))

    
    for solution in solve(x, y, []):
        for (r, c, n) in solution:
            res[r][c] = n
    return res

def exact_cover(x, y):
    x = {j: set() for j in x}
    for i, row in y.items():
        for j in row:
            x[j].add(i)
    return x

def solve(x, y, solution):
    if not x:
        yield list(solution)
    else:
        c = min(x, key=lambda c: len(x[c]))
        for r in list(x[c]):
            solution.append(r)
            cols = select(x, y, r)
            for s in solve(x, y, solution):
                yield s
            deselect(x, y, r, cols)
            solution.pop()

def select(x, y, r):
    cols = []
    for j in y[r]:
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].remove(i)
        cols.append(x.pop(j))
    return cols

def deselect(x, y, r, cols):
    for j in reversed(y[r]):
        x[j] = cols.pop()
        for i in x[j]:
            for k in y[i]:
                if k != j:
                    x[k].add(i)

if __name__ == '__main__':
    sudoku = [[0, 0, 0, 9, 0, 5, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 5, 0, 0],
                [0, 5, 0, 0, 4, 0, 0, 3, 0],
                [0, 8, 0, 0, 1, 0, 0, 4, 0],
                [0, 4, 0, 0, 5, 0, 0, 6, 0],
                [0,0,9,0,0,0,3,0,0],
                [0, 0, 0, 6, 7, 2, 0, 0, 0],
                [5, 6, 3, 0, 0, 0, 7, 9, 2],
                [2, 7, 0, 0, 0, 0, 0, 1, 4]]

    s = solve_sudoku(sudoku)
    print(s)