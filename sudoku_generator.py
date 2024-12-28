import numpy as np
import random
import matplotlib.pyplot as plt
import time

def grid_sudoku(param=10):
    grid = np.array([[0]*9]*9)
    #construct the matrix 
    vector = list(np.arange(1,10))
    for i in range(3):
        grid[i*3] = random.sample(vector, len(vector))
    # PrintGrid(grid)
    iter = 0
    while chek0inGrid(grid):
        for _ in range(param):
            c = random.choice(range(9))
            r = random.choice(range(9))
            grid[r][c] = 0
        iter += 1
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    grid[i][j] = random.choice(ChoiceInSubGridAndLines(grid, i, j))
        if iter == 10000:
            chek0inGrid(grid)
            break
    return grid, iter

def chek0inGrid(grid):
    number0 = 0
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                number0 += 1
    if number0 != 0:
        return True
    return False

def ChoiceInSubGridAndLines(grid, row, column):
    #based on a cell, we will check the subgrid, the row and the column
    subgrid = grid[(row//3)*3:(row//3)*3+3,(column//3)*3:(column//3)*3+3]
    vector = list(np.arange(1,10))
    #check the subgrid
    for i in range(3):
        for j in range(3):
            if subgrid[i][j] in vector:
                vector.remove(subgrid[i][j])
    #check the row
    for c in range(9):
        if grid[row][c] in vector:
            vector.remove(grid[row][c])
    for r in range(9):
        if grid[r][column] in vector:
            vector.remove(grid[r][column])
            
    if len(vector) == 0 or len(vector) == 2:
        vector = [0]
    return vector
    
def PrintGrid(grid):
    for i in range(9):
        print(grid[i])


#remove cells form the grid to get an unsolved grid
def unsolved_grid(grid, level):
    if level == 1:
        for _ in range(40):
            c = random.choice(range(9))
            r = random.choice(range(9))
            grid[r][c] = 0
    elif level == 2:
        for _ in range(50):
            c = random.choice(range(9))
            r = random.choice(range(9))
            grid[r][c] = 0
    elif level == 3:
        for _ in range(65):
            c = random.choice(range(9))
            r = random.choice(range(9))
            grid[r][c] = 0
    elif level == 4:
        return grid
    return grid
            
PrintGrid(unsolved_grid(grid_sudoku()[0], 3))

#check if a cell is valid
def check_cell(grid, row, column, number):
    #check the row
    for c in range(9):
        if grid[row][c] == number and c != column and grid[row][c] != 0:
            print("problem in row", grid[row])
            return "row", False
    #check the column
    for r in range(9):
        if grid[r][column] == number and r != row and grid[r][column] != 0:
            print("problem in column", grid[:][column])
            return "column", False
    #check the subgrid
    subgrid = grid[(row//3)*3:(row//3)*3+3,(column//3)*3:(column//3)*3+3]
    for i in range(3):
        for j in range(3):
            if subgrid[i][j] == number and (i != row%3 or j != column%3) and subgrid[i][j] != 0:
                print("problem in subgrid", subgrid)
                return "Subgrid", False
    return "ok", True

def check_grid(grid):
    for i in range(9):
        for j in range(9):
            if not check_cell(grid, i, j, grid[i][j])[1]:
                return check_cell(grid, i, j, grid[i][j])[0], False
    return "ok", True
    
    
    
#plot the number of iterations for 1000 grids
def plots():
    iter = []
    time_start = time.time()
    for i in range(100):
        grid, it = grid_sudoku(param=8)
        iter.append(it)
    #remove outliers
    iter = [x for x in iter if x < 1500]
    time_end = time.time()
    print('time cost', time_end-time_start, 's')
    print('mean', np.mean(iter))
        
    #plot the mean and the standard deviation
    plt.plot(iter)
    plt.axhline(np.mean(iter), color='r', linestyle='--')
    plt.axhline(np.mean(iter) + np.std(iter), color='g', linestyle='--')
    plt.axhline(np.mean(iter) - np.std(iter), color='g', linestyle='--')
    plt.xlabel('Grids')
    plt.ylabel('Iterations')
    plt.title('Number of iterations for 100 grids')

    plt.show()