from tkinter import Canvas, Tk, PhotoImage, Frame, messagebox
 
class Hexapawn(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry('375x375')
        self.configure(background = 'black')

        self.frame = Frame(self,bg = 'red')

        self.p = [0]*3

        self.board = Board()

        self.wpieces = [0]*3
        self.bpieces = [0]*3

        # can = Canvas(self, height = 360, width = 360)
        for i in range(3):
            self.p[i] = [0]*3
            self.wpieces[i] = [0]*3
            self.bpieces[i] = [0]*3
            for j in range(3):
                if i == j or i+j == 2:
                    self.p[i][j] = Canvas(self.frame, bg = '#696969', height = 120, width = 120)
                else:
                    self.p[i][j] = Canvas(self.frame, bg = '#DCDCDC', height = 120, width = 120)
                self.p[i][j].grid(row = i, column = j)

        self.blackp = PhotoImage(file = '.\\blackpawn1.png')
        self.whitep = PhotoImage(file = '.\\whitepawn1.png')

        self.frame.pack()

        for i in range(3):
            self.bpieces[0][i] = self.p[0][i].create_image(60,60,image = self.blackp)

        for i in range(3):
            self.wpieces[2][i] = self.p[2][i].create_image(60,60,image = self.whitep)

        self.wturn = 'w'
        self.turn()

    def turn(self):
        if self.wturn == 'w':
            for i in range(3):
                for j in range(3):
                    if self.wpieces[i][j] >= 1:
                        self.p[i][j].bind("<Button-1>", lambda event, r=i, c=j:self.click(r,c))
                    else:
                        self.p[i][j].bind("<Button-1>", lambda event:self.clear())

        if self.wturn == 'b':
            for i in range(3):
                for j in range(3):
                    if self.bpieces[i][j] >= 1:
                        self.p[i][j].bind("<Button-1>", lambda event, r=i, c=j:self.click(r,c))
                    else:
                        self.p[i][j].bind("<Button-1>", lambda event:self.clear())

    def clear(self):
        for i in range(3):
            for j in range(3):
                if i == j or i+j == 2:
                    self.p[i][j]['bg'] = '#696969'
                else:
                    self.p[i][j]['bg'] = '#DCDCDC'

    def click(self,r,c):
        self.clear()
        options = self.board.showmoves(r,c)
        for i in options:
            self.p[i[0]][i[1]]['bg'] = '#ffe12b'
            self.p[i[0]][i[1]].bind("<Button-1>", lambda event, ro=i[0], co=i[1]: self.move(r,c,ro,co))
 
    def move(self,fr,fc,tr,tc):
        if self.p[tr][tc]['bg'] == 'yellow' or 'orange':
            if self.wpieces[fr][fc] >= 1:
                if self.bpieces[tr][tc] >= 1:
                    self.p[tr][tc].delete(self.bpieces[tr][tc])
                    self.wpieces[tr][tc] = self.p[tr][tc].create_image(60,60,image = self.whitep)
                    self.p[fr][fc].delete(self.wpieces[fr][fc])
                    self.bpieces[tr][tc] = 0
                else:
                    self.wpieces[tr][tc] = self.p[tr][tc].create_image(60,60,image = self.whitep)
                    self.p[fr][fc].delete(self.wpieces[fr][fc])
                    self.wpieces[fr][fc] = 0
                self.wpieces[fr][fc] = 0

                self.clear()
                self.board.makemove(fr,fc,tr,tc)
                t = 1

            elif self.bpieces[fr][fc] >= 1:
                if self.wpieces[tr][tc] >= 1:
                    self.p[tr][tc].delete(self.wpieces[tr][tc])
                    self.bpieces[tr][tc] = self.p[tr][tc].create_image(60,60,image = self.blackp)
                    self.p[fr][fc].delete(self.bpieces[fr][fc])
                    self.wpieces[tr][tc] = 0
                else:
                    self.bpieces[tr][tc] = self.p[tr][tc].create_image(60,60,image = self.blackp)
                    self.p[fr][fc].delete(self.bpieces[fr][fc])
                    self.bpieces[fr][fc] = 0
                self.bpieces[fr][fc] = 0

                self.clear()
                self.board.makemove(fr,fc,tr,tc)
                t = 0

            for i1 in self.p:
                for j1 in i1:
                    j1.bind("<Button-1>", lambda event: self.donothing())

            if t:
                self.wturn = 'b'
                self.turn()
            else:
                self.wturn = 'w'
                self.turn()

        else:
            self.clear()

    def donothing(self):
        pass


class Board():
    def __init__(self):        
        self.board = [0]*3
        for i in range(3):
            self.board[i] = [0]*3

        for i in range(3):
            self.board[0][i] = 'b'
            self.board[2][i] = 'w'

        self.turn = 0

    def showmoves(self,r,c):
        options = []
        if self.board[r][c] == 'w':
            if r-1 in range(3):
                if self.board[r-1][c] == 0:
                    options.append((r-1,c))
                if c-1 in range(3):
                    if self.board[r-1][c-1] == 'b':
                        options.append((r-1,c-1))
                if c+1 in range(3):
                    if self.board[r-1][c+1] == 'b':
                        options.append((r-1,c+1))

        if self.board[r][c] == 'b':
            if r+1 in range(3):
                if self.board[r+1][c] == 0:
                    options.append((r+1,c))
                if c-1 in range(3):
                    if self.board[r+1][c-1] == 'w':
                        options.append((r+1,c-1))
                if c+1 in range(3):
                    if self.board[r+1][c+1] == 'w':
                        options.append((r+1,c+1))
        return options

    def makemove(self,fr,fc,tr,tc):
        self.turn = self.board[fr][fc]
        a = self.board[fr][fc]
        self.board[fr][fc] = 0
        self.board[tr][tc] = a
        self.checkwin()

    def checkwin(self):
        if 'w' in self.board[0]:
            messagebox.showinfo('Game Over','White Wins')
        elif 'b' in self.board[2]:
            messagebox.showinfo('Game Over','Black Wins')
        t = True
        s = True
        for i in range(3):
            if 'b' in self.board[i]:
                s = False
            if 'w' in self.board[i]:
                t = False
        if t:
            messagebox.showinfo('Game Over','Black Wins')
        if s:
            messagebox.showinfo('Game Over','White Wins')

        if self.turn == 'w':
            a = 'b'
        else:
            a = 'w'
        t = True
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == a:
                    if len(self.showmoves(i,j)) > 0:
                        t = False
        if t:
            messagebox.showinfo('Game Over','{} Wins'.format(self.turn))


if __name__ == '__main__':
    gameone = Hexapawn()
    gameone.mainloop()
