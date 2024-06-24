import tkinter as tk


class GrilleFront:
    def __init__(self, parent, label_text, row_offset, click_handler):
        self.buttons = []
        self.frame = None
        self.parent = parent
        self.label_text = label_text
        self.row_offset = row_offset
        self.click_handler = click_handler
        self.create_grille()

    def create_grille(self):
        self.frame = tk.Frame(self.parent)
        if self.row_offset == 0:
            self.frame.grid(row=self.row_offset, column=0, padx=20, pady=20)

        elif self.row_offset == 1:
            self.frame.grid(row=self.row_offset, column=0, padx=20, pady=20, rowspan=10)

        tk.Label(self.frame, text=self.label_text).grid(row=0, columnspan=11)

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for col, letter in enumerate(letters):
            tk.Label(self.frame, text=letter).grid(row=1, column=col+1)

        for row in range(10):
            tk.Label(self.frame, text=str(row+1)).grid(row=row+2, column=0)

        self.buttons = [[tk.Button(self.frame, text=' ', width=2, height=1, bg='light blue', command=lambda r=row, c=col: self.click_handler(self, r, c)) for col in range(10)] for row in range(10)]
        for row in range(10):
            for col in range(10):
                self.buttons[row][col].grid(row=row+2, column=col+1)

    def update_button(self, row, col, color):
        button = self.buttons[row][col]
        button.config(bg=color)

    def disable_button(self, row, col):
        button = self.buttons[row][col]
        button.config(state="disabled")
