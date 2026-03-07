import tkinter as tk
from tkinter import messagebox
import random, copy, time

N = 9
BOX = 3

# Difficulty levels configuration
DIFFICULTY_LEVELS = {
    "Easy": 45,
    "Medium": 35,
    "Difficult": 20
}

# Beautiful color themes
THEMES = {
    "Ocean": {
        "bg": "#0f1419",
        "light_cell": "#1e3a5f",
        "dark_cell": "#0d2540",
        "grid_color": "#2a5aa8",
        "text_given": "#e0f2ff",
        "text_user": "#4db8ff",
        "text_correct": "#00cc44",
        "text_wrong": "#ff4444",
        "button_bg": "#1e3a5f",
        "button_fg": "#00d4ff",
        "header_bg": "#0d1f2d",
        "header_fg": "#00d4ff"
    },
    "Forest": {
        "bg": "#0d2818",
        "light_cell": "#1a4d2e",
        "dark_cell": "#0d2818",
        "grid_color": "#2d6a4f",
        "text_given": "#d1e7dd",
        "text_user": "#52b788",
        "text_correct": "#74c69d",
        "text_wrong": "#ff6b6b",
        "button_bg": "#1a4d2e",
        "button_fg": "#52b788",
        "header_bg": "#0d1f14",
        "header_fg": "#52b788"
    },
    "Sunset": {
        "bg": "#2a1a0f",
        "light_cell": "#5d3a1a",
        "dark_cell": "#3d2415",
        "grid_color": "#8b5a2b",
        "text_given": "#ffe4b5",
        "text_user": "#ffb366",
        "text_correct": "#ffd700",
        "text_wrong": "#ff6347",
        "button_bg": "#5d3a1a",
        "button_fg": "#ffb366",
        "header_bg": "#3d2415",
        "header_fg": "#ffb366"
    },
    "Purple Nights": {
        "bg": "#1a0f2e",
        "light_cell": "#3d2463",
        "dark_cell": "#2a1847",
        "grid_color": "#553399",
        "text_given": "#e6d5ff",
        "text_user": "#cc99ff",
        "text_correct": "#00ff88",
        "text_wrong": "#ff4d94",
        "button_bg": "#3d2463",
        "button_fg": "#cc99ff",
        "header_bg": "#2a1847",
        "header_fg": "#cc99ff"
    }
}

# Sudoku logic
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
            if board[r][c] == 0: 
                return r, c
    return None

def solve(board):
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    for val in range(1, 10):
        if is_valid(board, r, c, val):
            board[r][c] = val
            if solve(board): return True
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
        if not solve(test):
            puzzle[r][c] = backup
        else:
            removed += 1
    return puzzle, full

# Game screen GUI
class SudokuGame:
    def __init__(self, root, difficulty, theme):
        self.root = root
        self.difficulty = difficulty
        self.theme = THEMES[theme]
        self.clues = DIFFICULTY_LEVELS[difficulty]
        self.puzzle, self.solution = generate_puzzle(self.clues)
        self.entries = [[None]*N for _ in range(N)]
        self.start_time = time.time()

        self.root.configure(bg=self.theme["bg"])
        self.root.title(f"🎮 Sudoku Game - {difficulty} ({theme})")

        # Header
        header = tk.Label(self.root, text=f"🎯 SUDOKU - {difficulty.upper()} LEVEL",
                         font=("Arial", 20, "bold"), bg=self.theme["header_bg"],
                         fg=self.theme["header_fg"], pady=15)
        header.pack(fill=tk.X)

        # Timer and difficulty info
        info_frame = tk.Frame(self.root, bg=self.theme["bg"])
        info_frame.pack(pady=10)
        self.timer_label = tk.Label(info_frame, text="⏰ Time: 0s", 
                                   font=("Arial", 14, "bold"), 
                                   bg=self.theme["bg"], fg=self.theme["header_fg"])
        self.timer_label.pack(side=tk.LEFT, padx=20)

        # Sudoku grid
        frame = tk.Frame(self.root, bg=self.theme["grid_color"], padx=3, pady=3)
        frame.pack(padx=20, pady=15)

        for r in range(N):
            for c in range(N):
                is_dark = ((r//BOX) + (c//BOX)) % 2
                cell_color = self.theme["dark_cell"] if is_dark else self.theme["light_cell"]
                
                e = tk.Entry(frame, width=2, font=("Arial", 20, "bold"),
                           justify="center", bg=cell_color, 
                           fg=self.theme["text_given"], relief="flat",
                           bd=1, highlightthickness=1, highlightcolor=self.theme["grid_color"])
                
                padx = (5, 0) if c % 3 == 2 and c != 8 else (0, 0)
                pady = (5, 0) if r % 3 == 2 and r != 8 else (0, 0)
                e.grid(row=r, column=c, padx=padx, pady=pady)

                if self.puzzle[r][c] != 0:
                    e.insert(0, str(self.puzzle[r][c]))
                    e.config(state="disabled", disabledforeground=self.theme["text_given"])
                else:
                    e.bind("<KeyRelease>", lambda ev, rr=r, cc=c: self.check_cell(rr, cc))
                self.entries[r][c] = e

        # Button frame
        btn_frame = tk.Frame(self.root, bg=self.theme["bg"])
        btn_frame.pack(pady=15)

        button_style = {
            "font": ("Arial", 11, "bold"),
            "fg": "white",
            "bd": 0,
            "padx": 15,
            "pady": 10,
            "relief": tk.RAISED,
            "cursor": "hand2"
        }

        tk.Button(btn_frame, text="✅ CHECK", bg="#2ecc71",
                 command=self.check_all, **button_style).pack(side="left", padx=8)
        tk.Button(btn_frame, text="💡 HINT", bg="#3498db",
                 command=self.give_hint, **button_style).pack(side="left", padx=8)
        tk.Button(btn_frame, text="🔍 SOLVE", bg="#9b59b6",
                 command=self.solve, **button_style).pack(side="left", padx=8)
        tk.Button(btn_frame, text="🔄 RESET", bg="#e74c3c",
                 command=self.reset, **button_style).pack(side="left", padx=8)
        tk.Button(btn_frame, text="🏠 MENU", bg="#95a5a6",
                 command=self.back_to_menu, **button_style).pack(side="left", padx=8)

        self.update_timer()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        mins, secs = elapsed // 60, elapsed % 60
        self.timer_label.config(text=f"⏰ Time: {mins}m {secs}s")
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
        if not val or not val.isdigit():
            self.entries[r][c].config(fg=self.theme["text_user"])
            return
        val = int(val)
        if val == self.solution[r][c]:
            self.entries[r][c].config(fg=self.theme["text_correct"])
        else:
            self.entries[r][c].config(fg=self.theme["text_wrong"])

    def give_hint(self):
        for r in range(N):
            for c in range(N):
                if self.puzzle[r][c] == 0 and self.entries[r][c].get() == "":
                    self.entries[r][c].insert(0, str(self.solution[r][c]))
                    self.entries[r][c].config(fg=self.theme["text_correct"], state="disabled")
                    return
        messagebox.showinfo("Hint", "No more hints available!")

    def check_all(self):
        board = self.get_board()
        if board == self.solution:
            elapsed = int(time.time() - self.start_time)
            mins, secs = elapsed // 60, elapsed % 60
            messagebox.showinfo("🎉 VICTORY!", 
                              f"Congratulations! You solved it!\n\nTime: {mins}m {secs}s\nDifficulty: {self.difficulty}")
        else:
            messagebox.showwarning("Check Result", "❌ Some cells are incorrect or incomplete.\nKeep trying!")

    def solve(self):
        for r in range(N):
            for c in range(N):
                self.entries[r][c].config(state="normal")
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, str(self.solution[r][c]))
                self.entries[r][c].config(fg=self.theme["text_correct"], state="disabled")

    def reset(self):
        self.start_time = time.time()
        for r in range(N):
            for c in range(N):
                self.entries[r][c].delete(0, tk.END)
                if self.puzzle[r][c] != 0:
                    self.entries[r][c].insert(0, str(self.puzzle[r][c]))
                    self.entries[r][c].config(state="disabled", 
                                            fg=self.theme["text_given"])
                else:
                    self.entries[r][c].config(state="normal", 
                                            fg=self.theme["text_user"])

    def back_to_menu(self):
        self.root.destroy()
        root = tk.Tk()
        StartScreen(root)
        root.mainloop()

# Start screen GUI
class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Sudoku Game")
        self.root.configure(bg="#000000")
        self.root.geometry("500x600")

        # Title
        title = tk.Label(self.root, text="🎮 SUDOKU", font=("Arial", 40, "bold"),
                        fg="#00d4ff", bg="#000000", pady=30)
        title.pack()

        subtitle = tk.Label(self.root, text="Select Difficulty Level",
                           font=("Arial", 16), fg="#4db8ff", bg="#000000", pady=10)
        subtitle.pack()

        # Difficulty buttons
        button_style = {
            "font": ("Arial", 14, "bold"),
            "fg": "white",
            "width": 20,
            "pady": 12,
            "bd": 0,
            "cursor": "hand2"
        }

        tk.Button(self.root, text="🟢 EASY", bg="#27ae60",
                 command=lambda: self.select_difficulty("Easy"),
                 **button_style).pack(pady=10)
        tk.Button(self.root, text="🟡 MEDIUM", bg="#f39c12",
                 command=lambda: self.select_difficulty("Medium"),
                 **button_style).pack(pady=10)
        tk.Button(self.root, text="🔴 DIFFICULT", bg="#e74c3c",
                 command=lambda: self.select_difficulty("Difficult"),
                 **button_style).pack(pady=10)

        # Theme selection
        theme_label = tk.Label(self.root, text="Select Theme",
                              font=("Arial", 14, "bold"), fg="#00d4ff", bg="#000000", pady=15)
        theme_label.pack()

        self.selected_theme = tk.StringVar(value="Ocean")
        for theme in THEMES.keys():
            tk.Radiobutton(self.root, text=f"🎨 {theme}", variable=self.selected_theme,
                          value=theme, font=("Arial", 12), fg="#00d4ff", bg="#000000",
                          selectcolor="#1e3a5f", bd=0).pack(anchor="w", padx=100, pady=5)

        # Start button
        tk.Button(self.root, text="▶️ START GAME", bg="#2ecc71",
                 font=("Arial", 14, "bold"), fg="white", width=20,
                 pady=12, bd=0, cursor="hand2",
                 command=self.start_game).pack(pady=30)

    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.start_game()

    def start_game(self):
        difficulty = getattr(self, 'difficulty', 'Medium')
        theme = self.selected_theme.get()
        self.root.destroy()
        root = tk.Tk()
        SudokuGame(root, difficulty, theme)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    StartScreen(root)
    root.mainloop()


