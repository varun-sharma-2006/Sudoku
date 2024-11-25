import pygame

# Initialize the pygame font system
pygame.font.init()

# Defining pygame window dimensions
screen = pygame.display.set_mode((650, 750))

# Title and Icon 
pygame.display.set_caption("SUDOKU SOLVER")

# x and y are current cell positions
x = -1  # Start with invalid position for x
y = -1  # Start with invalid position for y
# diff is size of each grid cell
dif = 500 / 9  # 500px is the board's total size
val = 0  # current value in cell

# Default Sudoku Board; will import it later and make it user interactive
grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
default_grid=grid

# Load test fonts size for future use
font1 = pygame.font.SysFont("cambriacambriamath", 40)  # for numbers in cells
font2 = pygame.font.SysFont("cambriacambriamath", 25)  # for instructions and messages

# x_offset and y_offset to center the grid
x_offset = (650 - 500) // 2  # Horizontally center the grid (650 is window width, 500 is board width)
y_offset = 100  # Move grid down below the instructions (100px down, leaving room for text)

# Get mouse position
def get_cord(pos):  # pos is tuple(x, y)
    global x, y
    x = (pos[0] - x_offset) // dif  # Adjust for the x_offset of the grid
    y = (pos[1] - y_offset) // dif  # Adjust for the y_offset of the grid

# Highlight the cell selected (with updated offsets)
def draw_box():
    if x >= 0 and y >= 0:  # Only draw box if x, y are valid
        for i in range(2):
            pygame.draw.line(screen, (255, 0, 0), (x_offset + x * dif - 3, y_offset + (y + i) * dif),
                             (x_offset + x * dif + dif + 3, y_offset + (y + i) * dif), 7)
            pygame.draw.line(screen, (255, 0, 0), (x_offset + (x + i) * dif, y_offset + y * dif),
                             (x_offset + (x + i) * dif, y_offset + y * dif + dif), 7)

# Function to draw the required lines for making Sudoku grid
def draw():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # Fill blue color in already numbered grid
                pygame.draw.rect(screen, (0, 153, 153), (x_offset + i * dif, y_offset + j * dif, dif + 1, dif + 1))

                # Fill grid with default numbers specified
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
                screen.blit(text1, (x_offset + i * dif + 15, y_offset + j * dif + 15))  # placing the text on the screen

    # Draw lines horizontally and vertically to form grid
    for i in range(10):  # Loop from 0 to 9 to draw both horizontal and vertical lines
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
       # Draw vertical lines (columns)
        pygame.draw.line(screen, (0, 0, 0), (x_offset + i * dif , y_offset), 
                         (x_offset + i * dif , y_offset + 500), thick)
        
        # Draw horizontal lines (rows)
        pygame.draw.line(screen, (0, 0, 0), (x_offset - 3, y_offset + i * dif), 
                         (x_offset + 500 + 3, y_offset + i * dif), thick)


def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x_offset + x * dif + 15, y_offset + y * dif + 15))

# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (255, 0, 0))
    screen.blit(text1, (x_offset + 20, y_offset + 520))  # Adjust position for error message

def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (255, 0, 0))
    screen.blit(text1, (x_offset + 20, y_offset + 520))  # Adjust position for error message

# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    # To reach the starting cell of sub-grid
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True

# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()  # Ensures event queue in Pygame is updated
    for it in range(1, 10):
        if valid(grid, i, j, it) == True:
            grid[i][j] = it
            global x, y  # Updates the global variables to the current cell coordinates
            x = i
            y = j
            # White color background
            screen.fill((255, 255, 255))  # Clears the screen
            draw()  # Draws the updated grid
            draw_box()  # Highlights the current cell
            pygame.display.update()
            pygame.time.delay(20)  # Adds a slight delay
            if solve(grid, i, j) == 1:  # Recursion call
                return True
            else:
                grid[i][j] = 0  # Backtracking
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False

# Display instruction for the game
def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY BOARD", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (x_offset + 20, 20))  # Adjust position based on the offset
    screen.blit(text2, (x_offset + 35, 50))  # Adjust position based on the offset

# Display options when solved
def result():
    text1 = font1.render("FINISHED!! PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (x_offset + 80, y_offset + 570)) 
    pygame.display.update()


run = True
flag1 = 0  # set to 1 when there’s active interaction with a cell and reset to 0 after the interaction is processed
flag2 = 0  # controls whether the program should attempt to solve the Sudoku puzzle using the backtracking algorithm
rs = 0     # acts as an indicator of whether the puzzle has been solved
error = 0  # used to track if there was an invalid action

# The loop that keeps the window running
while run:
    screen.fill((255, 255, 255))
    instruction()  # Display the instructions above the grid
    draw()  # Draw the Sudoku grid
    draw_box()  # Highlight the current selected cell (only if clicked)
    pygame.display.update()  # Update display after every action

    # Loop through the events stored in event.get()
    for event in pygame.event.get():   # pygame.event.get() is a list of all the user-actions
        # Quit the game window
        if event.type == pygame.QUIT:
            run = False
        # Get the mouse position to insert number 
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()   # function that returns the (x, y) coordinates of the mouse cursor on the screen at the time the function is called
            get_cord(pos)   # gets cell number based on mouse position
        # Get the number to be inserted if key pressed 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                flag2 = 1  # indicating triggering of solving function
            # If R pressed clear the sudoku board
            if event.key == pygame.K_r:
                rs = 0  # suggests that a reset or new game action is taking place
                error = 0  # clears any previous errors
                flag2 = 0
                grid = [[0] * 9 for x in range(9)]  # create a sudoku grid of all values = 0
            # If D is pressed reset the board to default 
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                grid = default_grid  # default_grid was missing, using grid here

    if flag2 == 1:   # to check if solving action was triggered
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1  # sudoku solved if rs = 1
        flag2 = 0

    if val != 0:         
        draw_val(val)
        if valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_error2() 
        val = 0
    
    if error == 1:
        raise_error1() 
    if rs == 1:
        result()
    draw() 
    if flag1 == 1:
        draw_box()     
        instruction() 
        pygame.display.update()


pygame.quit()
