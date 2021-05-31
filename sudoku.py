class Sudoku:
    def __init__(self):
        self.grid = [[0 for j in range(9)] for i in range(9)]

    def add_constraint(self, i, j, number):
        self.grid[i][j] = number
    
    def iter_line(self, i):
        res = []
        for e in self.grid[i]:
            if e != 0:
                res.append(e)
        return res

    def iter_col(self, j):
        res = []
        for l in self.grid:
            if l[j] != 0:
                res.append(l[j])
        return res

    def iter_square(self, i0, j0):
        """
        i = 0 -> 0 - 2
        i = 1 -> 0 - 2
        i = 2 -> 0 - 2
        i = 3 -> 3 - 5
        i = 4 -> 3 - 5
        i = 5 -> 3 - 5
        i = 6 -> 6 - 8
        i = 7 -> 6 - 8
        i = 8 -> 6 - 8
        """

        ranges = (range(i, i+3) for i in range(0, 7, 3))
        range_i = None
        range_j = None

        
        for r in ranges:
            if i0 in r:
                range_i = r
            if j0 in r:
                range_j = r

        res = []
        for i in range_i:
            for j in range_j:
                if self.grid[i][j] != 0:
                    res.append(self.grid[i][j])
        return res

    def is_full(self):
        for l in self.grid:
            for e in l:
                if e == 0:
                    return False
        return True

    def backtrack(self, i, j):
        if i == 8 and j == 8:
            return True

        if j == 9:
            i += 1
            j = 0
        
        if self.grid[i][j] > 0:
            return self.solve(i, j + 1)

        taken = self.iter_line(i) + self.iter_col(j) + self.iter_square(i, j)
        for candidat in range(1, 10):
            if candidat in taken:
                continue

            self.grid[i][j] = candidat
            if self.solve(i, j + 1):
                return True
            self.grid[i][j] = 0

        return False
        
def main():
    test = Sudoku()
    test.add_constraint(0, 0, 3)
    test.add_constraint(0, 2, 6)
    test.add_constraint(0, 3, 5)
    test.add_constraint(0, 5, 8)
    test.add_constraint(0, 6, 4)

    test.add_constraint(1, 0, 5)
    test.add_constraint(1, 1, 2)

    test.add_constraint(2, 1, 8)
    test.add_constraint(2, 2, 7)
    test.add_constraint(2, 7, 3)
    test.add_constraint(2, 8, 1)

    test.add_constraint(3, 2, 3)
    test.add_constraint(3, 4, 1)
    test.add_constraint(3, 7, 8)

    test.add_constraint(4, 0, 9)
    test.add_constraint(4, 3, 8)
    test.add_constraint(4, 4, 6)
    test.add_constraint(4, 5, 3)
    test.add_constraint(4, 8, 5)

    test.add_constraint(5, 1, 5)
    test.add_constraint(5, 4, 9)
    test.add_constraint(5, 6, 6)

    test.add_constraint(6, 0, 1)
    test.add_constraint(6, 1, 3)
    test.add_constraint(6, 6, 2)
    test.add_constraint(6, 7, 5)

    test.add_constraint(7, 7, 7)
    test.add_constraint(7, 8, 4)

    test.add_constraint(8, 2, 5)
    test.add_constraint(8, 3, 2)
    test.add_constraint(8, 5, 6)
    test.add_constraint(8, 6, 3)

    test.solve(0, 0)
    print(test.grid)

main()