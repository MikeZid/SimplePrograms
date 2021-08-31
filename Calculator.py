from tkinter import *

class Story_frame(Frame):
    def __init__(self, master=None):
        super(Story_frame, self).__init__(master=master)
        self.current_row = 0
        self["background"] = "grey"

    def add(self, text):
        Label(self, text=text).grid(row=self.current_row, sticky=E)
        self.current_row += 1

class Calculator_frame(Frame):
    def __init__(self, master=None):
        super(Calculator_frame, self).__init__(master=master)
        self.STORY_MODE = False
        self.master = master
        self.grid(row=0, column=0, sticky=N+S+E+W)
        Grid.rowconfigure(self=master, index=0, weight=1)
        Grid.columnconfigure(self=master, index=0, weight=1)
        self.TEXT_FIELD = Label(master=self)
        self.TEXT_FIELD_2 = Label(master=self)
        self.OPERATION = Label(master=self)
        self.STORY = Story_frame(master=self)

        self.OPERATION.grid(row=1, rowspan=2, column=0, columnspan=3, sticky=E)
        self.TEXT_FIELD.grid(row=2, column=3,columnspan=2, sticky=E)
        self.TEXT_FIELD_2.grid(row=1, column=3,columnspan=2, sticky=E)

        self.add_buttons()


    def show_story(self):
        if self.STORY_MODE is False:
            self.STORY_MODE = True
            self.STORY.grid(row=1, column=0, rowspan=6, columnspan=5, sticky=N+S+E+W)
            for button in self.grid_slaves():
                if isinstance(button, Calculator_button):
                    button.destroy()
        else:
            self.STORY_MODE = False
            self.STORY.grid_remove()
            self.add_buttons()


    def add_buttons(self):
        #Grid.rowconfigure(self=self, index=0, weight=1)
        Grid.rowconfigure(self=self, index=1, weight=1)
        Grid.rowconfigure(self=self, index=2, weight=1)
        Grid.rowconfigure(self=self, index=3, weight=1)
        Grid.rowconfigure(self=self, index=4, weight=1)
        Grid.rowconfigure(self=self, index=5, weight=1)
        Grid.rowconfigure(self=self, index=6, weight=1)
        Grid.columnconfigure(self=self, index=0, weight=1)
        Grid.columnconfigure(self=self, index=1, weight=1)
        Grid.columnconfigure(self=self, index=2, weight=1)
        Grid.columnconfigure(self=self, index=3, weight=1)
        Grid.columnconfigure(self=self, index=4, weight=1)

        Button(master=self, text="", command=self.show_story).grid(row=0, column=0, columnspan=5, sticky=N+S+E+W)

        Calculator_button(master=self, data=9, row=3, column=2)
        Calculator_button(master=self, data=8, row=3, column=1)
        Calculator_button(master=self, data=7, row=3, column=0)

        Calculator_button(master=self, data=6, row=4, column=2)
        Calculator_button(master=self, data=5, row=4, column=1)
        Calculator_button(master=self, data=4, row=4, column=0)

        Calculator_button(master=self, data=3, row=5, column=2)
        Calculator_button(master=self, data=2, row=5, column=1)
        Calculator_button(master=self, data=1, row=5, column=0)

        Calculator_button(master=self, data=0, row=6, column=1)

        Calculator_button(master=self, data=".", row=6, column=2)

        Calculator_button(master=self, data="<-", row=3, column=3)
        Calculator_button(master=self, data="C", row=3, column=4)

        Calculator_button(master=self, data="+", row=4, column=3)
        Calculator_button(master=self, data="-", row=5, column=3)
        Calculator_button(master=self, data="*", row=4, column=4)
        Calculator_button(master=self, data="/", row=5, column=4)
        Calculator_button(master=self, data="^", row=6, column=4)
        Calculator_button(master=self, data="=", row=6, column=3)


class Calculator_button(Button):
    def __init__(self, master, row, column, data):
        super(Calculator_button, self).__init__(master=master, command=self.click)
        self.grid(row=row, column=column, sticky=N+S+E+W)
        self.data = data
        self["text"] = self.data

    def click(self):
        if self.data == "+" or self.data == "-" or self.data == "*" or self.data == "/" or self.data == "^":
            if self.master.TEXT_FIELD["text"] == "":
                return
            if self.master.OPERATION["text"] == "":
                    self.master.TEXT_FIELD_2["text"] = self.master.TEXT_FIELD["text"]
                    self.master.TEXT_FIELD["text"] = ""
                    self.master.OPERATION["text"] = self.data
            else:
                if self.master.TEXT_FIELD["text"] == "":
                    self.master.OPERATION["text"] = self.data
                else:
                    text = self.master.TEXT_FIELD_2["text"] + self.master.OPERATION["text"] + self.master.TEXT_FIELD["text"]
                    self.master.TEXT_FIELD_2["text"] = Ariphmetic.do(self=None, a=self.master.TEXT_FIELD_2["text"], b=self.master.TEXT_FIELD["text"], operation=self.master.OPERATION["text"])
                    text += "=" + self.master.TEXT_FIELD_2["text"]
                    self.master.STORY.add(text=text)
                    self.master.TEXT_FIELD["text"] = ""
                    self.master.OPERATION["text"] = self.data
            return
        if self.data == "C":
            self.master.TEXT_FIELD["text"] = ""
            self.master.TEXT_FIELD_2["text"] = ""
            self.master.OPERATION["text"] = ""
            return
        if self.data == "<-":
            if self.master.TEXT_FIELD["text"] == "" and self.master.OPERATION["text"] != "":
                self.master.OPERATION["text"] = ""
            elif self.master.TEXT_FIELD["text"] != "":
                self.master.TEXT_FIELD["text"] = self.master.TEXT_FIELD["text"][:len(self.master.TEXT_FIELD["text"])-1:]
            return
        if self.data == "=":
            text = self.master.TEXT_FIELD_2["text"] + self.master.OPERATION["text"] + self.master.TEXT_FIELD["text"]
            self.master.TEXT_FIELD["text"] = Ariphmetic.do(self=None, a=self.master.TEXT_FIELD_2["text"], b=self.master.TEXT_FIELD["text"], operation=self.master.OPERATION["text"])
            text += "=" + self.master.TEXT_FIELD["text"]
            self.master.STORY.add(text=text)
            self.master.TEXT_FIELD_2["text"] = ""
            self.master.OPERATION["text"] = ""
            return

        if self.data == ".":
            if self.master.TEXT_FIELD["text"] == "":
                self.master.TEXT_FIELD["text"] += "0"
        self.master.TEXT_FIELD["text"] += str(self.data)


class Ariphmetic:

    def sum(self, a, b):
        if (a == ""):
            a = 0
        if (b == ""):
            b = 0
        return str(float(a)+float(b))

    def sub(self, a, b):
        if (a == ""):
            a = 0
        if (b == ""):
            b = 0
        return str(float(a)-float(b))

    def mul(self, a, b):
        if (a == ""):
            a = 0
        if (b == ""):
            b = 0
        return str(float(a)*float(b))

    def div(self, a, b):
        if (a == ""):
            a = 0
        if (b == ""):
            b = 1
        return str(float(a)/float(b))

    def pow(self, a, b):
        if (a == ""):
            a = 1
        if (b == ""):
            b = 1
        return str(float(a)**float(b))


    def do(self, a, b, operation):
        if operation == "":
            return
        if operation == "+":
            return Ariphmetic.sum(self, a=a, b=b)
        elif operation == "-":
            return Ariphmetic.sub(self, a=a, b=b)
        elif operation == "*":
            return Ariphmetic.mul(self, a=a, b=b)
        elif operation == "/":
            return Ariphmetic.div(self, a=a, b=b)
        elif operation == "^":
            return Ariphmetic.pow(self, a=a, b=b)


window = Tk()
window.wm_minsize(250, 250)

frame = Calculator_frame(master=window)
window.mainloop()