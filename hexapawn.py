from tkinter import Canvas, Tk, PhotoImage, Frame, messagebox, Button

 
class Hexapawn(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry('475x375')

        self.frame = Grid(self)
        self.frame.grid(row = 0, column = 0)

        self.playagainb = Button(self, text = "Play Again", command = lambda:self.playagain())
        self.playagainb.grid(row = 0, column = 1)

    def playagain(self):
        self.frame.destroy()
        self.frame = Grid(self)
        self.frame.grid(row = 0, column = 0)

class Grid(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.parent = parent

        self.p = [0]*3

        self.board = Board(self)

        self.pieces = {'w':[0]*3, 'b':[0]*3}
        # self.wpieces = [0]*3
        # self.bpieces = [0]*3

        # can = Canvas(self, height = 360, width = 360)
        for i in range(3):
            self.p[i] = [0]*3
            self.pieces['w'][i] = [0]*3
            self.pieces['b'][i] = [0]*3
            for j in range(3):
                if i == j or i+j == 2:
                    self.p[i][j] = Canvas(self, bg = '#696969', height = 120, width = 120)
                else:
                    self.p[i][j] = Canvas(self, bg = '#DCDCDC', height = 120, width = 120)
                self.p[i][j].grid(row = i, column = j)

        self.images = {}
        self.images['b'] = PhotoImage(file = '.\\blackpawn1.png')
        self.images['w'] = PhotoImage(file = '.\\whitepawn1.png')

        for i in range(3):
            self.pieces['w'][2][i] = self.p[2][i].create_image(60,60,image = self.images['w'])
            self.pieces['b'][0][i] = self.p[0][i].create_image(60,60,image = self.images['b'])

        self.wturn = 'w'
        self.nturn = 'b'
        self.turn()

    def turn(self):
        for i in range(3):
            for j in range(3):
                if self.pieces[self.wturn][i][j] >= 1:
                    self.p[i][j].bind("<Button-1>", lambda event, r=i, c=j:self.click(r,c))
                else:
                    self.p[i][j].bind("<Button-1>", lambda event:self.clear())

    def clear(self):
        for i in range(3):
            for j in range(3):
                if i == j or i+j == 2:
                    self.p[i][j]['bg'] = '#696969' #light
                else:
                    self.p[i][j]['bg'] = '#DCDCDC' #dark

    def click(self,r,c):
        self.clear()
        options = self.board.showmoves(r,c)
        for i in options:
            self.p[i[0]][i[1]]['bg'] = '#ffe12b' #pinapple color
            self.p[i[0]][i[1]].bind("<Button-1>", lambda event, ro=i[0], co=i[1]: self.move(r,c,ro,co))
 
    def move(self,fr,fc,tr,tc):
        if self.p[tr][tc]['bg'] == '#ffe12b':
            if self.pieces[self.nturn][tr][tc] >= 1:
                self.p[tr][tc].delete(self.pieces[self.nturn][tr][tc])
                self.pieces[self.wturn][tr][tc] = self.p[tr][tc].create_image(60,60,image = self.images[self.wturn])
                self.p[fr][fc].delete(self.pieces[self.wturn][fr][fc])
                self.pieces[self.nturn][tr][tc] = 0
            else:
                self.pieces[self.wturn][tr][tc] = self.p[tr][tc].create_image(60,60,image = self.images[self.wturn])
                self.p[fr][fc].delete(self.pieces[self.wturn][fr][fc])
                self.pieces[self.wturn][fr][fc] = 0
            self.pieces[self.wturn][fr][fc] = 0

            self.clear()
            self.board.makemove(fr,fc,tr,tc)

            for i1 in self.p:
                for j1 in i1:
                    j1.bind("<Button-1>", lambda event: self.donothing())

            a = self.wturn
            self.wturn = self.nturn
            self.nturn = a
            self.turn()

        else:
            self.clear()

    def donothing(self):
        pass

class Board():
    def __init__(self, parent): 
        self.parent = parent

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
            self.parent.parent.playagain()
        elif 'b' in self.board[2]:
            messagebox.showinfo('Game Over','Black Wins')
            self.parent.parent.playagain()
        t = True
        s = True
        for i in range(3):
            if 'b' in self.board[i]:
                s = False
            if 'w' in self.board[i]:
                t = False
        if t:
            messagebox.showinfo('Game Over','Black Wins')
            self.parent.parent.playagain()
        if s:
            messagebox.showinfo('Game Over','White Wins')
            self.parent.parent.playagain()

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
            self.parent.parent.playagain()


if __name__ == '__main__':
    gameone = Hexapawn()
    gameone.mainloop()
