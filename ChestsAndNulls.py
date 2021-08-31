from tkinter import Tk, Button, Grid, N, S, E, W, Label

class GUI(Tk):
    def __init__(self):
        super(GUI, self).__init__()
        self.wm_minsize(250, 250)
        self.is_winner = False
        self.who_turn = False # False - X, True - O
        self.add_cells()
        self.configure_grid()
        self.label = Label(master=self, text="Ходят X")
        self.add_bottom_panel()
        self.mainloop()

    def add_cells(self):
        GUI.Cell(master=self).grid(row=1, column=1, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=1, column=2, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=1, column=3, sticky=N+S+E+W)

        GUI.Cell(master=self).grid(row=2, column=1, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=2, column=2, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=2, column=3, sticky=N+S+E+W)

        GUI.Cell(master=self).grid(row=3, column=1, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=3, column=2, sticky=N+S+E+W)
        GUI.Cell(master=self).grid(row=3, column=3, sticky=N+S+E+W)

    def configure_grid(self):
        Grid.columnconfigure(self=self, index=1, weight=1)
        Grid.columnconfigure(self=self, index=2, weight=1)
        Grid.columnconfigure(self=self, index=3, weight=1)

        Grid.rowconfigure(self=self, index=1, weight=1)
        Grid.rowconfigure(self=self, index=2, weight=1)
        Grid.rowconfigure(self=self, index=3, weight=1)
        Grid.rowconfigure(self=self, index=4, weight=1)

    def add_bottom_panel(self):
        self.label.grid(row=4, column=1, columnspan=2, sticky=N+S+E+W)
        Button(master=self, text="R", command=self.reset).grid(row=4, column=3, sticky=N+S+W+E)

    def reset(self):
        for cell in self.grid_slaves():
            if isinstance(cell, GUI.Cell):
                cell.grid_remove()
        self.is_winner = False
        self.who_turn = False # False - X, True - O
        self.label["text"] = "Ходят Х"
        self.add_cells()

    def check_winner(self):
        table = []
        for cell in self.grid_slaves():
            if isinstance(cell, GUI.Cell):
                table.append(cell["text"])
        table.reverse()
        if table[0] == table[1] == table[2] == "X" or table[3] == table[4] == table[5] == "X" or table[6] == table[7] == table[8] == "X" or table[0] == table[3] == table[6] == "X" or table[1] == table[4] == table[7] == "X" or table[2] == table[5] == table[8] == "X" or table[0] == table[4] == table[8] == "X" or table[2] == table[4] == table[6] == "X":
            self.is_winner = True
            self.label["text"] = "Выйграли Х"
        elif table[0] == table[1] == table[2] == "O" or table[3] == table[4] == table[5] == "O" or table[6] == table[7] == table[8] == "O" or table[0] == table[3] == table[6] == "O" or table[1] == table[4] == table[7] == "O" or table[2] == table[5] == table[8] == "O" or table[0] == table[4] == table[8] == "O" or table[2] == table[4] == table[6] == "O":
            self.is_winner = True
            self.label["text"] = "Выйграли O"
        elif not " " in table:
            self.label["text"] = "Ничья"
    class Cell(Button):
        def __init__(self, master):
            super(GUI.Cell, self).__init__(master=master, text=" ", command=self.turn)
            self.master=master
            self.is_clicked = False

        def turn(self):
            if self.is_clicked or self.master.is_winner:
                return
            if not self.master.who_turn:
                self["text"] = "X"
                self.master.label["text"] = "Ходят О"
            else:
                self["text"] = "O"
                self.master.label["text"] = "Ходят X"
            self.master.who_turn = not self.master.who_turn
            self.is_clicked = True
            self.master.check_winner()

gui = GUI()
