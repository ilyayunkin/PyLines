import time
from tkinter import *
from random import *
from tkinter import messagebox


class Lines:
    def play(self):
        self.root.mainloop()

    def __init__(self):
        self.game_name = "PyLines"
        self.lines_count = 9
        self.cells_count = self.lines_count * self.lines_count

        self.root = Tk()
        self.root.title(self.game_name)
        self.cell_width = 30
        self.size = self.lines_count * self.cell_width
        self.canvas = Canvas(self.root, width=self.size, height=self.size)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.action)
        self.clear()

    def clear(self):
        self.cells_list = list()
        self.selected = False
        self.selected_pos = 0
        self.coins = 0

        for i in range(self.cells_count):
            self.cells_list.append('')

        self.step()
        self.update()

    def coord_to_pos(self, x, y):
        pos = y * self.lines_count + x
        return pos

    def update(self):
        self.root.title(self.game_name + " - " + str(self.coins) + " coins")
        self.canvas.delete("all")
        if self.selected:
            x = int(self.selected_pos % self.lines_count)
            y = int(self.selected_pos / self.lines_count)
            colors = 'green'
            x0 = x * self.cell_width
            y0 = y * self.cell_width
            self.canvas.create_rectangle(x0, y0, x0 + self.cell_width, y0 + self.cell_width, fill=colors)

        for i in range(self.cells_count):
            if self.cells_list[i] != '' :
                x = int(i % self.lines_count)
                y = int(i / self.lines_count)
                x0 = x * self.cell_width
                y0 = y * self.cell_width
                self.canvas.create_oval(x0, y0, x0 + self.cell_width, y0 + self.cell_width, fill=self.cells_list[i])

        for i in range(self.lines_count):
            self.canvas.create_line(i * self.cell_width, 0, i * self.cell_width, self.size)
            self.canvas.create_line(0, i * self.cell_width, self.size, i * self.cell_width)
        self.canvas.update()

    @staticmethod
    def random_color():
        return choice(['blue', 'green','black', 'red', 'yellow', 'magenta', 'cyan'])

    def free_list(self):
        free = list()
        for i in range(self.cells_count):
            if self.cells_list[i] == '':
                free.append(i)
        return free

    def step(self):
        free = self.free_list()
        new_balls_count = range(min(free.__len__(), 3))
        for i in new_balls_count:
            pos = choice(free)
            free.remove(pos)
            self.cells_list[pos] = self.random_color()
            self.check(pos)
        self.update()
        free = self.free_list()
        if free.__len__() == 0:
            if messagebox.askquestion(self.game_name, "You got " + str(self.coins) + " coins\nDo you want to restart?") == 'yes':
                self.clear()

    def is_valid(self, x, y):
        return (x >= 0) and (y >= 0) and (x < self.lines_count) and (y < self.lines_count)

    def check_d1(self, pos):
        del_list = list()
        del_list.append(pos)
        x = int(pos % self.lines_count)
        y = int(pos / self.lines_count)
        current_x = x - 1
        current_y = y -1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x - 1
            current_y = current_y - 1
        current_x = x + 1
        current_y = y + 1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x + 1
            current_y = current_y + 1
        return del_list

    def check_d2(self, pos):
        del_list = list()
        del_list.append(pos)
        x = int(pos % self.lines_count)
        y = int(pos / self.lines_count)
        current_x = x - 1
        current_y = y + 1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x - 1
            current_y = current_y + 1
        current_x = x + 1
        current_y = y - 1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x + 1
            current_y = current_y - 1
        return del_list

    def check_horizontal(self, pos):
        del_list = list()
        del_list.append(pos)
        x = int(pos % self.lines_count)
        y = int(pos / self.lines_count)
        current_y = y
        current_x = x - 1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x - 1
        current_x = x + 1
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_x = current_x + 1
        return del_list

    def check_vertical(self, pos):
        del_list = list()
        del_list.append(pos)
        x = int(pos % self.lines_count)
        y = int(pos / self.lines_count)
        current_y = y - 1
        current_x = x
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_y = current_y - 1
        current_y = y + 1
        current_x = x
        while self.is_valid(current_x, current_y) and (self.cells_list[self.coord_to_pos(current_x, current_y)] == self.cells_list[pos]):
            del_list.append(self.coord_to_pos(current_x, current_y))
            current_y = current_y + 1
        return del_list

    def check(self, pos):
        del_list = list()
        r1 = self.check_horizontal(pos)
        r2 = self.check_vertical(pos)
        r3 = self.check_d1(pos)
        r4 = self.check_d2(pos)
        if r1.__len__() >= 5:
            del_list+=r1
        if r2.__len__() >= 5:
            del_list+=r2
        if r3.__len__() >= 5:
            del_list+=r3
        if r4.__len__() >= 5:
            del_list+=r4
        if del_list.__len__() >= 5:
            self.coins += del_list.__len__()
            print("coins="+str(self.coins))
            for i in del_list:
                self.cells_list[i] = ''
        print(str(del_list) + '=' + str(r1) + ' ' + str(r2) + ' ' + str(r3) + ' ' + str(r4))

        return del_list.__len__() >= 5

    def is_nei(self, x, y, pos_to):
        ret = False
        if self.is_valid(x, y):
            if(self.coord_to_pos(x + 1, y) == pos_to) or \
                    (self.coord_to_pos(x + 1, y + 1) == pos_to) or \
                    (self.coord_to_pos(x + 1, y - 1) == pos_to) or \
                    (self.coord_to_pos(x, y + 1) == pos_to) or \
                    (self.coord_to_pos(x, y - 1) == pos_to) or \
                    (self.coord_to_pos(x - 1, y) == pos_to) or \
                    (self.coord_to_pos(x - 1, y + 1) == pos_to) or \
                    (self.coord_to_pos(x - 1, y - 1) == pos_to) :
                ret = True

        return ret

    def is_able_r(self, pos_from, pos_to, list_copy):
        x = int(pos_from % self.lines_count)
        y = int(pos_from / self.lines_count)
        if self.is_nei(x, y, pos_to):
            return True
        list_copy[pos_from] = 'gray'
        x1 = x
        y1 = y - 1
        new_pos = self.coord_to_pos(x1, y1)
        if self.is_valid(x1, y1) and list_copy[new_pos] == '' and self.is_able_r(new_pos, pos_to, list_copy):
            return True
        x1 = x
        y1 = y + 1
        new_pos = self.coord_to_pos(x1, y1)
        if self.is_valid(x1, y1) and list_copy[new_pos] == '' and self.is_able_r(new_pos, pos_to, list_copy):
            return True
        x1 = x + 1
        y1 = y
        new_pos = self.coord_to_pos(x1, y1)
        if self.is_valid(x1, y1) and list_copy[new_pos] == '' and self.is_able_r(new_pos, pos_to, list_copy):
            return True
        x1 = x - 1
        y1 = y
        new_pos = self.coord_to_pos(x1, y1)
        if self.is_valid(x1, y1) and list_copy[new_pos] == '' and self.is_able_r(new_pos, pos_to, list_copy):
            return True

        return False

    def is_able(self, pos_from, pos_to):
        list_copy = self.cells_list.copy()
        return self.is_able_r(pos_from, pos_to, list_copy)

    def action(self, event):
        x = int(event.x / self.cell_width)
        y = int(event.y / self.cell_width)
        pos = x + y * self.lines_count
        if not self.selected:
            if self.cells_list[pos] != '':
                self.selected = True
                self.selected_pos = pos
        else:
            if self.cells_list[pos] == '':
                if self.is_able(pos, self.selected_pos):
                    self.selected = False
                    self.cells_list[pos] = self.cells_list[self.selected_pos]
                    self.cells_list[self.selected_pos] = ''
                    if not self.check(pos):
                        self.step()
            else:
                self.selected_pos = pos
        self.update()
