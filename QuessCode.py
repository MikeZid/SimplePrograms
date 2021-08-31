from tkinter import Tk, Frame, Button, Label, Grid, N, S, E, W, Canvas
from random import randint
from copy import deepcopy

ALL_COLORS = ("black", "white", "yellow", "green", "red", "blue")
TRY = 10

class GUI(Tk):
    def __init__(self):
        super(GUI, self).__init__()
        self.picked = ""
        self.logic = Logic()
        self.win = False
        self.lose = False
        self.game_field = GUI.GameField(master=self)
        Grid.columnconfigure(self=self,index=0, weight=1)
        Grid.rowconfigure(self=self, index=0, weight=1)
        self.game_field.grid(row=0, column=0, sticky=N+S+E+W)


    class GameField(Frame):
        def __init__(self, master):
            super(GUI.GameField, self).__init__(master=master)
            self.master = master
            self.current_row = 0
            self.game_field_grid_configure()
            self.help_field = None
            self.add_bottom_panel()
            self.add_row()

        def game_field_grid_configure(self):
            for column in range(9):
                Grid.columnconfigure(self=self, index=column, weight=1)
            for row in range(TRY+2):
                Grid.rowconfigure(self=self, index=row, weight=1)

        def lose(self):
            self.master.lose = True
            Label(master=self, text="lose").grid(row=self.current_row, column=0, sticky=N+S+E+W)
            column = 1
            for color in self.master.logic.win_combination:
                GUI.Piece(master=self, color=color).grid(row=self.current_row, column = column, sticky=N+S+E+W)
                column += 1

        def add_row(self):
            text_for_label = str(self.current_row+1) + "/" + str(TRY)
            Label(master=self, text=text_for_label).grid(row=self.current_row, column=0, sticky=N+S+E+W)
            for i in range(1, 5, 1):
                GUI.Piece(master=self).grid(row=self.current_row, column=i, sticky=N+S+E+W)
            self.help_field = GUI.HelpField(master=self).grid(row=self.current_row, column=5, sticky=N+S+E+W)
            self.current_row += 1

        def add_bottom_panel(self):
            column = 1
            for color in ALL_COLORS:
                GUI.Piece(master=self, color=color).grid(row=TRY+1, column=column, sticky=N+S+E+W)
                column += 1
            Button(master=self, text="V", command=self.accept).grid(row=TRY+1, column=column, sticky=N+S+E+W)
            column += 1
            Button(master=self, text="R", command=self.reset).grid(row=TRY+1, column=column, sticky=N+S+E+W)

        def accept(self):
            if self.master.win or self.master.lose:
                return
            if self.current_row==TRY+1:
                self.lose()
                return
            current_combination = []
            for current_Piece in self.grid_slaves(row=self.current_row-1):
                if isinstance(current_Piece, GUI.Piece):
                    if current_Piece.color is None:
                        return
                    current_Piece.is_accepted = True
                    current_combination.append(current_Piece.color)
            current_combination.reverse()
            quess = self.master.logic.check_current_combination(current_combination=current_combination)
            if quess[0] == 4:
                self.master.win = True
                Label(master=self, text="you win").grid(row=self.current_row, columnspan=5)
                return

            self.grid_slaves(row=self.current_row-1, column=5)[0].show_help(quess=quess)
            self.add_row()

        def reset(self):
            self.master.logic = Logic()
            current_row = 0
            self.master.win = False
            self.master.lose = False
            while current_row < TRY+1:
                for element in self.grid_slaves(row=current_row):
                    element.grid_remove()
                current_row += 1
            self.current_row = 0
            self.add_row()

    class Piece(Button):
        def __init__(self, master, color=None, is_lost=False):
            super(GUI.Piece, self).__init__(master=master, width=3)
            self.master = master
            self.color = color
            if is_lost is True:
                self["background"] = color
                return
            else:
                self.is_accepted = False
                if color is None:
                    self["command"] = self.set
                else:
                    self["background"] = self.color
                    self["command"] = self.pick

        def pick(self):
            self.master.master.picked = self.color

        def set(self):
            if self.master.master.picked == "" or self.is_accepted:
                return
            self.color = self.master.master.picked
            self["background"] = self.color


    class HelpField(Frame):
        def __init__(self, master):
            super(GUI.HelpField, self).__init__(master=master)
            self.master = master
            Grid.columnconfigure(self=self, index=0, weight=1)
            Grid.columnconfigure(self=self, index=1, weight=1)
            Grid.rowconfigure(self=self, index=0, weight=1)
            Grid.rowconfigure(self=self, index=1, weight=1)
            self.label1 = Label(master=self, borderwidth=3)
            self.label1.grid(row=0, column=0, sticky=N+S+W+E)
            self.label2 = Label(master=self, borderwidth=3)
            self.label2.grid(row=0, column=1, sticky=N+S+W+E)
            self.label3 = Label(master=self, borderwidth=3)
            self.label3.grid(row=1, column=0, sticky=N+S+W+E)
            self.label4 = Label(master=self, borderwidth=3)
            self.label4.grid(row=1, column=1, sticky=N+S+W+E)

        def show_help(self, quess):
            index = 1
            for pos in range(quess[0]):
                self.add_help(index=index, color="grey")
                index += 1
            for color in range(quess[1]):
                self.add_help(index=index, color="yellow")
                index += 1

        def add_help(self, index, color):
            if index == 1:
                self.label1["background"] = color
            elif index == 2:
                self.label2["background"] = color
            elif index == 3:
                self.label3["background"] = color
            elif index == 4:
                self.label4["background"] = color

class Logic:
    def __init__(self):
        self.win_combination = [ALL_COLORS[randint(0, 5)], ALL_COLORS[randint(0, 5)], ALL_COLORS[randint(0, 5)], ALL_COLORS[randint(0, 5)]]
        # TODO combination
        print(self.win_combination)

    def check_current_combination(self, current_combination):
        current_Piece = 0
        quess_pos = 0
        quess_color = 0
        copy_win_combination = deepcopy(self.win_combination)
        while current_Piece < 4:
            if (current_combination[current_Piece] == copy_win_combination[current_Piece]):
                copy_win_combination[current_Piece] = ""
                current_combination[current_Piece] = ""
                quess_pos += 1
            current_Piece += 1

        current_Piece = 0
        while current_Piece < 4:
            current_Piece_in_win_combination = 0
            if current_combination[current_Piece] == "":
                current_Piece += 1
                continue
            while current_Piece_in_win_combination < 4:
                if current_combination[current_Piece] == copy_win_combination[current_Piece_in_win_combination]:
                    quess_color += 1
                    copy_win_combination[current_Piece_in_win_combination] = ""
                current_Piece_in_win_combination += 1

            current_Piece += 1
        return (quess_pos, quess_color)
# log = Logic()
# print(log.win_combination)
# log.check_current_combination(["black", "black", "black", "red"])

gui = GUI()

gui.mainloop()
