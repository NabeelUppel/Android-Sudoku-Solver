import numpy as np


class SudokuSolution:
    def __init__(self, board):
        self.board = board
        self.solve()

    def getSolution(self):
        return self.board

    def findNextCell(self, i, j):
        for x in range(i, 9):
            for y in range(j, 9):
                if self.board[x][y] == 0:
                    return x, y

        for x in range(0, 9):
            for y in range(0, 9):
                if self.board[x][y] == 0:
                    return x, y
        return -1, -1

    def isValid(self, e, i, j):
        rowOk = self.checkRows(e, i)
        if rowOk:
            columnOk = self.checkCols(e, j)
            if columnOk:
                return self.checkSquares(e, i, j)
        return False

    def checkCols(self, num, col):
        check = []
        for x in range(9):
            check.append(self.board[x][col])
        if num in check:
            return False
        return True

    def checkRows(self, num, row):
        if num in self.board[row]:
            return False
        return True

    def checkSquares(self, num, rows, cols):
        block = []
        if rows % 3 == 0:

            if cols % 3 == 0:

                block.append(self.board[rows + 1][cols + 1])
                block.append(self.board[rows + 1][cols + 2])
                block.append(self.board[rows + 2][cols + 1])
                block.append(self.board[rows + 2][cols + 2])

            elif cols % 3 == 1:

                block.append(self.board[rows + 1][cols - 1])
                block.append(self.board[rows + 1][cols + 1])
                block.append(self.board[rows + 2][cols - 1])
                block.append(self.board[rows + 2][cols + 1])

            elif cols % 3 == 2:

                block.append(self.board[rows + 1][cols - 2])
                block.append(self.board[rows + 1][cols - 1])
                block.append(self.board[rows + 2][cols - 2])
                block.append(self.board[rows + 2][cols - 1])

        elif rows % 3 == 1:

            if cols % 3 == 0:

                block.append(self.board[rows - 1][cols + 1])
                block.append(self.board[rows - 1][cols + 2])
                block.append(self.board[rows + 1][cols + 1])
                block.append(self.board[rows + 1][cols + 2])

            elif cols % 3 == 1:

                block.append(self.board[rows - 1][cols - 1])
                block.append(self.board[rows - 1][cols + 1])
                block.append(self.board[rows + 1][cols - 1])
                block.append(self.board[rows + 1][cols + 1])

            elif cols % 3 == 2:

                block.append(self.board[rows - 1][cols - 2])
                block.append(self.board[rows - 1][cols - 1])
                block.append(self.board[rows + 1][cols - 2])
                block.append(self.board[rows + 1][cols - 1])

        elif rows % 3 == 2:

            if cols % 3 == 0:

                block.append(self.board[rows - 2][cols + 1])
                block.append(self.board[rows - 2][cols + 2])
                block.append(self.board[rows - 1][cols + 1])
                block.append(self.board[rows - 1][cols + 2])

            elif cols % 3 == 1:

                block.append(self.board[rows - 2][cols - 1])
                block.append(self.board[rows - 2][cols + 1])
                block.append(self.board[rows - 1][cols - 1])
                block.append(self.board[rows - 1][cols + 1])

            elif cols % 3 == 2:

                block.append(self.board[rows - 2][cols - 2])
                block.append(self.board[rows - 2][cols - 1])
                block.append(self.board[rows - 1][cols - 2])
                block.append(self.board[rows - 1][cols - 1])

        if num in block:
            return False
        return True

    def solve(self, i=0, j=0):
        i, j = self.findNextCell(i, j)
        if i == -1:
            return True

        for x in range(1, 10):
            if self.isValid(x, i, j):
                self.board[i][j] = x
                if self.solve(i, j):
                    return True
                self.board[i][j] = 0
        return False


