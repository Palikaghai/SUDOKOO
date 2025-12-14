import tkinter as tk
from tkinter import messagebox
import random, copy, time

N = 9, BOX = 3 # for making a good small board( its demensions)
def is_valid(board, r, c, val):
    if any(board[r][i] == val for i in range(N)): return False
    if any(board[i][c] == val for i in range(N)): return False
    br, bc = (r // BOX) * BOX, (c // BOX) * BOX
    for i in range(br, br+BOX):
        for j in range(bc, bc+BOX):
            if board[i][j] == val: return False
    return True

def find_empty(board):
    for r in range(N):
        for c in range(N):
            if board[r][c] == 0: return r, c
    return None

def solve(board):
    empty = find_empty(board)
    if not empty: 
        return True
    r, c = empty
    for val in range(1, 10):
        if is_valid(board, r, c, val):
            board[r][c] = val
            if solve(board): 
                return True
            board[r][c] = 0
    return False

def generate_full_board():
    board = [[0]*N for _ in range(N)]
    def fill():
        empty = find_empty(board)
        if not empty: return True
        r, c = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for val in nums:
            if is_valid(board, r, c, val):
                board[r][c] = val
                if fill(): return True
                board[r][c] = 0
        return False
fill()
    return board

def generate_puzzle(clues=35):
    full = generate_full_board()
    puzzle = copy.deepcopy(full)
    cells = [(r, c) for r in range(N) for c in range(N)]
    random.shuffle(cells)
    removed = 0
    target_removed = N*N - clues
    for (r, c) in cells:
        if removed >= target_removed: break
        backup = puzzle[r][c]
        puzzle[r][c] = 0
        test = copy.deepcopy(puzzle)
        if not solve(test):  # ensure solvable
            puzzle[r][c] = backup
        else:
            removed += 1
    return puzzle, full

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ Sudoku Game with Timer")
        self.puzzle, self.solution = generate_puzzle(35)
        self.entries = [[None]*N for _ in range(N)]
        self.start_time = time.time()

        frame = tk.Frame(root, bg="black")
        frame.pack(padx=10, pady=10)

        colors = ["#f0f8ff", "#ffe4e1", "#e6ffe6"]

        for r in range(N):
            for c in range(N):
                box_color = colors[((r//BOX)+(c//BOX)) % len(colors)]
                e = tk.Entry(frame, width=2, font=("Arial", 18, "bold"),
                             justify="center", bg=box_color, relief="solid")
                e.grid(row=r, column=c, padx=(0 if c%3 else 2, 2),
                       pady=(0 if r%3 else 2, 2))
                if self.puzzle[r][c] != 0:
                    e.insert(0, str(self.puzzle[r][c]))
                    e.config(state="disabled", disabledforeground="black")
                else:
                    # Bind event to check correctness immediately
                    e.bind("<KeyRelease>", lambda ev, rr=r, cc=c: self.check_cell(rr, cc))
                self.entries[r][c] = e

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="✅ Check All", bg="#90ee90",
                  command=self.check_all).pack(side="left", padx=5)
        tk.Button(btn_frame, text="💡 Solve", bg="#add8e6",
                  command=self.solve).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔄 Reset", bg="#ffcccb",
                  command=self.reset).pack(side="left", padx=5)

        # Timer label
        self.timer_label = tk.Label(root, text="Time: 0s", font=("Arial", 14))
        self.timer_label.pack(pady=5)
        self.update_timer()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Time: {elapsed}s")
        self.root.after(1000, self.update_timer)

    def get_board(self):
        board = [[0]*N for _ in range(N)]
        for r in range(N):
            for c in range(N):
                val = self.entries[r][c].get()
                board[r][c] = int(val) if val.isdigit() else 0
        return board

    def check_cell(self, r, c):
        val = self.entries[r][c].get()
        if not val.isdigit(): 
            self.entries[r][c].config(fg="black")
            return
        val = int(val)
        if val == self.solution[r][c]:
            self.entries[r][c].config(fg="green")
        else:
            self.entries[r][c].config(fg="red")

    def check_all(self):
        board = self.get_board()
        if board == self.solution:
            messagebox.showinfo("Sudoku", "🎉 Congratulations! You solved it!")
        else:
            messagebox.showwarning("Sudoku", "❌ Mistakes present or not complete.")

    def solve(self):
        for r in range(N):
            for c in range(N):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, str(self.solution[r][c]))
                self.entries[r][c].config(fg="black")

    def reset(self):
        self.start_time = time.time()
        for r in range(N):
            for c in range(N):
                self.entries[r][c].delete(0, tk.END)
                if self.puzzle[r][c] != 0:
                    self.entries[r][c].insert(0, str(self.puzzle[r][c]))
                    self.entries[r][c].config(state="disabled", disabledforeground="black")
                else:
                    self.entries[r][c].config(state="normal", fg="white")

if __name__ == "__main__":
    root = tk.Tk()
    SudokuGUI(root)
    root.mainloop()







