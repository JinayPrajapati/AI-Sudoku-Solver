import tkinter as tk
from tkinter import ttk
import random
import time

N = 9
CELL = 50
SIZE = CELL * N

puzzle = [[0]*9 for _ in range(9)]
original_puzzle = [[0]*9 for _ in range(9)]
solution = [[0]*9 for _ in range(9)]

# ---------- Constraint Check ----------

def is_safe(board,row,col,num):

    for i in range(9):
        if board[row][i] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3

    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False

    return True


# ---------- Backtracking ----------

def backtracking(board):

    for row in range(9):
        for col in range(9):

            if board[row][col] == 0:

                nums = list(range(1,10))
                random.shuffle(nums)

                for num in nums:

                    if is_safe(board,row,col,num):

                        board[row][col] = num

                        if backtracking(board):
                            return True

                        board[row][col] = 0

                return False

    return True


# ---------- CSP Solver ----------

def find_empty(board):

    for i in range(9):
        for j in range(9):

            if board[i][j] == 0:
                return i,j

    return None


def get_domain(board,row,col):

    return [n for n in range(1,10) if is_safe(board,row,col,n)]


def csp_solver(board):

    cell = find_empty(board)

    if not cell:
        return True

    row,col = cell

    for num in get_domain(board,row,col):

        board[row][col] = num

        if csp_solver(board):
            return True

        board[row][col] = 0

    return False


# ---------- Generate Full Sudoku ----------

def generate_full_board():

    board = [[0]*9 for _ in range(9)]
    backtracking(board)
    return board


# ---------- Generate Puzzle ----------

def generate_puzzle():

    global puzzle, original_puzzle

    board = generate_full_board()

    difficulty = diff.get()

    if difficulty == "Easy":
        clues = 40
    elif difficulty == "Medium":
        clues = 25
    else:
        clues = 15

    cells = [(r,c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for r,c in cells[:81-clues]:
        board[r][c] = 0

    puzzle = [row[:] for row in board]
    original_puzzle = [row[:] for row in board]

    draw_board(puzzle)
    time_label.config(text="Solving Time:")


# ---------- Clear Solution ----------

def clear_solution():

    global puzzle

    puzzle = [row[:] for row in original_puzzle]

    draw_board(puzzle)
    time_label.config(text="Solving Time:")


# ---------- Draw Grid ----------

def draw_grid():

    for i in range(N+1):

        width = 4 if i % 3 == 0 else 1

        canvas.create_line(i*CELL,0,i*CELL,SIZE,width=width)
        canvas.create_line(0,i*CELL,SIZE,i*CELL,width=width)

    canvas.create_rectangle(2,2,SIZE-2,SIZE-2,width=4)


# ---------- Draw Board ----------

def draw_board(board):

    canvas.delete("all")

    # Draw cell backgrounds
    for i in range(9):
        for j in range(9):

            if original_puzzle[i][j] != 0:
                color = "#D3D3D3"
            else:
                color = "white"

            canvas.create_rectangle(j*CELL,
                                    i*CELL,
                                    j*CELL+CELL,
                                    i*CELL+CELL,
                                    fill=color,
                                    outline="")

    draw_grid()

    # Draw numbers
    for i in range(9):
        for j in range(9):

            if board[i][j] != 0:

                color = "black" if original_puzzle[i][j] != 0 else "blue"

                canvas.create_text(j*CELL + CELL/2,
                                   i*CELL + CELL/2,
                                   text=str(board[i][j]),
                                   font=("Arial",20,"bold"),
                                   fill=color)


# ---------- Animation ----------

def animate_solution():

    for i in range(9):
        for j in range(9):

            if puzzle[i][j] == 0:

                puzzle[i][j] = solution[i][j]

                draw_board(puzzle)
                root.update()
                root.after(80)


# ---------- Solve ----------

def solve_selected():

    for i in range(9):
        for j in range(9):
            solution[i][j] = puzzle[i][j]

    method = algo.get()

    start = time.time()

    if method == "Backtracking":
        backtracking(solution)
    else:
        csp_solver(solution)

    end = time.time()

    solving_time = round(end-start,4)

    time_label.config(text=f"Solving Time: {solving_time} sec")

    animate_solution()


# ---------- GUI ----------

root = tk.Tk()
root.title("AI Sudoku Solver")
root.geometry("520x650")
root.configure(bg="#E8F0F2")

controls = tk.Frame(root,bg="#E8F0F2")
controls.pack(pady=10)

tk.Label(controls,text="Difficulty",bg="#E8F0F2",
         font=("Arial",11,"bold")).grid(row=0,column=0,padx=10)

diff = ttk.Combobox(controls,
                    values=["Easy","Medium","Hard"],
                    state="readonly",
                    width=10)

diff.current(0)
diff.grid(row=0,column=1,padx=10)

tk.Label(controls,text="Algorithm",bg="#E8F0F2",
         font=("Arial",11,"bold")).grid(row=0,column=2,padx=10)

algo = ttk.Combobox(controls,
                    values=["Backtracking","CSP"],
                    state="readonly",
                    width=12)

algo.current(0)
algo.grid(row=0,column=3,padx=10)

btn_frame = tk.Frame(root,bg="#E8F0F2")
btn_frame.pack(pady=10)

generate_btn = tk.Button(btn_frame,
                         text="Generate Puzzle",
                         width=15,
                         bg="#4CAF50",
                         fg="white",
                         font=("Arial",10,"bold"),
                         command=generate_puzzle)

generate_btn.grid(row=0,column=0,padx=10)

solve_btn = tk.Button(btn_frame,
                      text="Solve Sudoku",
                      width=15,
                      bg="#2196F3",
                      fg="white",
                      font=("Arial",10,"bold"),
                      command=solve_selected)

solve_btn.grid(row=0,column=1,padx=10)

clear_btn = tk.Button(btn_frame,
                      text="Clear Solution",
                      width=15,
                      bg="#F44336",
                      fg="white",
                      font=("Arial",10,"bold"),
                      command=clear_solution)

clear_btn.grid(row=0,column=2,padx=10)

canvas = tk.Canvas(root,
                   width=SIZE,
                   height=SIZE,
                   bg="white",
                   highlightthickness=0)

canvas.pack(pady=10)

draw_board(puzzle)

time_label = tk.Label(root,
                      text="Solving Time:",
                      bg="#E8F0F2",
                      font=("Arial",12,"bold"))

time_label.pack(pady=10)

root.mainloop()