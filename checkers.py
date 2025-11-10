import random
import time
from tkinter import *
from tkinter import messagebox
from functools import partial
from tkmacosx import Button


class Checkers:
    def __init__(self):
        self.root = Tk()
        self.root.title('Checkers')

        self.frame = Frame(self.root)
        self.frame.grid(row=0)

        self.x = Button(
            self.frame, width=75, height=50, bd=8, bg='green', relief=RAISED,
            text='1-Player', font=('Arial', 18), command=self.yes
        )
        self.y = Button(
            self.frame, width=75, height=50, bd=8, bg='red', relief=RAISED,
            text='2-Player', font=('Arial', 18), command=self.initGame
        )

        self.x.pack(padx=5, pady=5, side=LEFT)
        self.y.pack(padx=5, pady=5)

    def yes(self):
        self.x['bg'] = 'red'
        self.x['text'] = 'First'
        self.x['command'] = partial(self.initGame, 'white')

        self.y['bg'] = 'white'
        self.y['text'] = 'Second'
        self.y['command'] = partial(self.initGame, 'red')

    def initGame(self, botColor=False):
        self.frame.destroy()

        self.bot = botColor
        self.colors = [[] for _ in range(8)]
        self.highlighted = [0, 0]
        self.squares = [[] for _ in range(8)]
        self.king = [[False for _ in range(8)] for _ in range(8)]
        self.players = ['red', 'white']
        self.chips = [12, 12]
        self.player = 0
        self.verts = [
            15.0, 22.5, 22.5, 22.5, 25.0, 15.0, 27.5, 22.5,
            35.0, 22.5, 28.75, 27.5, 31.25, 35.0, 25.0, 30.0,
            18.75, 35.0, 21.25, 27.5
        ]

        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    self.squares[i].append(Canvas(
                        self.root, bg='blanched almond', width=50, height=50,
                        highlightthickness=0, highlightbackground='black'
                    ))
                    self.colors[i].append('bruh')
                else:
                    self.squares[i].append(Canvas(
                        self.root, bg='dark green', width=50, height=50,
                        highlightthickness=0, highlightbackground='black'
                    ))

                    if j in [0, 1, 2]:
                        self.squares[i][-1].create_oval(10, 10, 40, 40, fill='red')
                        self.colors[i].append('red')
                    elif j in [5, 6, 7]:
                        self.squares[i][-1].create_oval(10, 10, 40, 40, fill='white')
                        self.colors[i].append('white')
                    else:
                        self.colors[i].append('bruh')

                    self.squares[i][-1].bind('<Button-1>', partial(self.select, i, j))

                self.squares[i][-1].grid(row=j, column=i)

        self.turn = Label(self.root, text='Turn:', font=('Arial', 14))
        self.turn.grid(row=8, column=1)

        self.color = Canvas(self.root, bg='light gray', width=42, height=42, highlightthickness=4)
        self.color.create_oval(10, 10, 40, 40, fill='red')
        self.color.grid(row=8, column=2)

        if self.bot == 'red':
            self.botMove()

        self.root.mainloop()

    def change_turn(self):
        self.color.create_oval(10, 10, 40, 40, fill=self.players[1 - self.player])
        self.player = 1 - self.player

        if self.chips[0] == 0 or self.chips[1] == 0 or not self.check_moves():
            self.endgame()
        elif self.players[self.player] == self.bot:
            self.botMove()

    def check_moves(self):
        for a in range(8):
            for b in range(8):
                if (
                    self.players[self.player] == 'red'
                    and self.colors[a][b] == 'red'
                    and (
                        (0 <= b + 1 < 8 and (
                            (0 <= a + 1 < 8 and self.colors[a + 1][b + 1] == 'bruh') or
                            (0 <= a - 1 < 8 and self.colors[a - 1][b + 1] == 'bruh')
                        )) or
                        (self.king[a][b] and 0 <= b - 1 < 8 and (
                            (0 <= a + 1 < 8 and self.colors[a + 1][b - 1] == 'bruh') or
                            (0 <= a - 1 < 8 and self.colors[a - 1][b - 1] == 'bruh')
                        ))
                    )
                ) or (
                    self.players[self.player] == 'white'
                    and self.colors[a][b] == 'white'
                    and (
                        (0 <= b - 1 < 8 and (
                            (0 <= a + 1 < 8 and self.colors[a + 1][b - 1] == 'bruh') or
                            (0 <= a - 1 < 8 and self.colors[a - 1][b - 1] == 'bruh')
                        )) or
                        (self.king[a][b] and 0 <= b + 1 < 8 and (
                            (0 <= a + 1 < 8 and self.colors[a + 1][b + 1] == 'bruh') or
                            (0 <= a - 1 < 8 and self.colors[a - 1][b + 1] == 'bruh')
                        ))
                    )
                ):
                    return True

        return self.check_takes()

    def check_takes(self, array=None):
        if array is None:
            array = [[a, b] for a in range(8) for b in range(8)]

        for a, b in array:
            if self.colors[a][b] == self.players[self.player]:
                for i in (-1, 1):
                    for j in (-1, 1):
                        if (
                            -1 < a + 2 * i < 8 and -1 < b + 2 * j < 8 and
                            self.colors[a + 2 * i][b + 2 * j] == 'bruh' and (
                                (self.players[self.player] == 'red' and
                                 ((not self.king[a][b] and j == 1) or self.king[a][b]) and
                                 self.colors[a + i][b + j] == 'white') or
                                (self.players[self.player] == 'white' and
                                 ((not self.king[a][b] and j == -1) or self.king[a][b]) and
                                 self.colors[a + i][b + j] == 'red')
                            )
                        ):
                            return True
        return False

    def move(self, a, b, c, d):
        self.squares[a][b].delete('all')
        self.squares[c][d].create_oval(10, 10, 40, 40, fill=self.colors[a][b])

        self.colors[a][b], self.colors[c][d] = 'bruh', self.colors[a][b]

        if self.king[a][b]:
            self.king[a][b], self.king[c][d] = False, True
            self.squares[c][d].create_polygon(self.verts, fill='black', outline='black')

        self.squares[a][b]['width'] = 50
        self.squares[a][b]['height'] = 50
        self.squares[a][b]['highlightthickness'] = 0

        self.squares[c][d]['width'] = 42
        self.squares[c][d]['height'] = 42
        self.squares[c][d]['highlightthickness'] = 4

        self.highlighted = [c, d]

        if (
            (d == 0 and self.colors[c][d] == 'white' and not self.king[c][d]) or
            (d == 7 and self.colors[c][d] == 'red' and not self.king[c][d])
        ):
            self.squares[c][d].create_polygon(self.verts, fill='black', outline='black')
            self.king[c][d] = True
            return True

        return False

    def take(self, a, b, c, d, e, f):
        self.squares[e][f].delete('all')
        self.colors[e][f] = 'bruh'
        self.chips[1 - self.player] -= 1
        return self.move(a, b, c, d)

    def endgame(self):
        winner = self.players[1 - self.player].capitalize()
        messagebox.showinfo('Checkers', f'Congratulations, {winner}-Player, you won!')

        self.color.destroy()
        self.turn.config(text='Game Over', font=('Arial', 18))
        self.turn.grid(row=8, column=2, columnspan=4)

        for i in range(8):
            for j in range(8):
                self.squares[i][j].unbind('<Button-1>')

    def select(self, i, j, _):
        if self.colors[i][j] == self.players[self.player]:
            self.squares[self.highlighted[0]][self.highlighted[1]].config(
                width=50, height=50, highlightthickness=0
            )
            self.squares[i][j].config(width=42, height=42, highlightthickness=4)
            self.highlighted = [i, j]

        elif (
            len(self.highlighted) == 2 and
            self.colors[self.highlighted[0]][self.highlighted[1]] == self.players[self.player]
        ):
            moves = [
                [self.highlighted[0] + i, self.highlighted[1] + j]
                for i in (-1, 1)
                for j in (-1, 1)
                if (
                    -1 < self.highlighted[0] + i < 8 and
                    -1 < self.highlighted[1] + j < 8 and
                    self.colors[self.highlighted[0] + i][self.highlighted[1] + j] == 'bruh' and
                    (
                        (self.players[self.player] == 'red' and
                         ((not self.king[self.highlighted[0]][self.highlighted[1]] and j == 1) or
                          self.king[self.highlighted[0]][self.highlighted[1]])) or
                        (self.players[self.player] == 'white' and
                         ((not self.king[self.highlighted[0]][self.highlighted[1]] and j == -1) or
                          self.king[self.highlighted[0]][self.highlighted[1]]))
                    )
                )
            ]

            eat = [
                [self.highlighted[0] + 2 * i, self.highlighted[1] + 2 * j]
                for i in (-1, 1)
                for j in (-1, 1)
                if (
                    -1 < self.highlighted[0] + 2 * i < 8 and
                    -1 < self.highlighted[1] + 2 * j < 8 and
                    self.colors[self.highlighted[0] + 2 * i][self.highlighted[1] + 2 * j] == 'bruh' and (
                        (self.players[self.player] == 'red' and
                         self.colors[self.highlighted[0] + i][self.highlighted[1] + j] == 'white' and
                         ((not self.king[self.highlighted[0]][self.highlighted[1]] and j == 1) or
                          self.king[self.highlighted[0]][self.highlighted[1]])) or
                        (self.players[self.player] == 'white' and
                         self.colors[self.highlighted[0] + i][self.highlighted[1] + j] == 'red' and
                         ((not self.king[self.highlighted[0]][self.highlighted[1]] and j == -1) or
                          self.king[self.highlighted[0]][self.highlighted[1]]))
                    )
                )
            ]

            if [i, j] in eat and (
                self.take(self.highlighted[0], self.highlighted[1], i, j,
                          (self.highlighted[0] + i) // 2, (self.highlighted[1] + j) // 2)
                or not self.check_takes([[i, j]])
            ):
                self.change_turn()

            elif [i, j] in moves and not self.check_takes():
                self.move(self.highlighted[0], self.highlighted[1], i, j)
                self.change_turn()

    def botMove(self):
        eat = [
            [a, b, a + 2 * i, b + 2 * j]
            for a in range(8)
            for b in range(8)
            for i in (-1, 1)
            for j in (-1, 1)
            if (
                self.colors[a][b] == self.players[self.player] and
                -1 < a + 2 * i < 8 and -1 < b + 2 * j < 8 and (
                    (self.players[self.player] == 'red' and
                     self.colors[a + i][b + j] == 'white' and
                     self.colors[a + 2 * i][b + 2 * j] == 'bruh' and
                     ((not self.king[a][b] and j == 1) or self.king[a][b])) or
                    (self.players[self.player] == 'white' and
                     self.colors[a + i][b + j] == 'red' and
                     self.colors[a + 2 * i][b + 2 * j] == 'bruh' and
                     ((not self.king[a][b] and j == -1) or self.king[a][b]))
                )
            )
        ]

        if eat:
            x = random.choice(eat)
            self.root.update()
            time.sleep(0.5)
            self.select(x[0], x[1], None)
            self.root.update()
            time.sleep(0.5)
            self.select(x[2], x[3], None)

            if self.players[self.player] == self.bot:
                self.botMove()

        else:
            x = random.choice([
                [a, b, a + i, b + j]
                for a in range(8)
                for b in range(8)
                for i in (-1, 1)
                for j in (-1, 1)
                if (
                    self.colors[a][b] == self.players[self.player] and
                    -1 < a + i < 8 and -1 < b + j < 8 and
                    self.colors[a + i][b + j] == 'bruh' and (
                        (self.players[self.player] == 'red' and
                         ((not self.king[a][b] and j == 1) or self.king[a][b])) or
                        (self.players[self.player] == 'white' and
                         ((not self.king[a][b] and j == -1) or self.king[a][b]))
                    )
                )
            ])
            self.root.update()
            time.sleep(0.5)
            self.select(x[0], x[1], None)
            self.root.update()
            time.sleep(0.5)
            self.select(x[2], x[3], None)


if __name__ == "__main__":
    Checkers()

