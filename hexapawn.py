from tkinter import Canvas, Tk, PhotoImage, Frame, messagebox, Button
import random

 
class Hexapawn(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.geometry('450x375')

        self.frames = [0]
        self.frames[0] = Grid(self)
        self.frames[0].grid(row = 0, column = 0)

        self.ai = AI(self)

        self.playagainb = Button(self, text = "Play Again", command = lambda:self.playagain())
        self.playagainb.grid(row = 0, column = 1)

    def playagain(self):
        if self.frames[0].won != None:
            self.ai.feedback(self.frames[0].won,self.frames[0].moveno)
        self.frames.append(Grid(self))
        self.frames[len(self.frames)-1].grid(row = 0, column = 0)
        del self.frames[0]
        self.ai.refresh()


class Grid(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)
        self.parent = parent

        self.p = [0]*3

        self.board = Board(self)

        self.pieces = {'w':[0]*3, 'b':[0]*3}

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

        self.won = None
        self.wturn = 'w'
        self.nturn = 'b'
        self.moveno = 1
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
        if self.pieces[self.nturn][tr][tc] >= 1:
            self.p[tr][tc].delete(self.pieces[self.nturn][tr][tc])
        self.pieces[self.wturn][tr][tc] = self.p[tr][tc].create_image(60,60,image = self.images[self.wturn])
        self.p[fr][fc].delete(self.pieces[self.wturn][fr][fc])
        self.pieces[self.wturn][fr][fc] = 0

        self.clear()
        self.board.makemove(fr,fc,tr,tc)

        for i1 in self.p:
            for j1 in i1:
                j1.bind("<Button-1>", lambda event: self.donothing())

        self.parent.ai.note(self.moveno,fr,fc,tr,tc)

        b = self.checkwin()
        if b:
            return

        a = self.wturn
        self.wturn = self.nturn
        self.nturn = a
        self.moveno += 1

        if self.wturn == 'b':
            self.parent.ai.turn(self.moveno)
        else:
            self.turn()

    def donothing(self):
        pass

    def checkwin(self):
        if 'w' in self.board.board[0]:
            messagebox.showinfo('Game Over','White Wins')
            self.won = 'w'
            self.parent.playagain()
            return True
        elif 'b' in self.board.board[2]:
            messagebox.showinfo('Game Over','Black Wins')
            self.won = 'b'
            self.parent.playagain()
            return True

        t = True
        s = True
        for i in range(3):
            if 'b' in self.board.board[i]:
                s = False
            if 'w' in self.board.board[i]:
                t = False
        if s:
            messagebox.showinfo('Game Over','White Wins')
            self.won = 'w'
            self.parent.playagain()
            return True
        if t:
            messagebox.showinfo('Game Over','Black Wins')
            self.won = 'b'
            self.parent.playagain()
            return True

        a = self.nturn
        t = True
        for i in range(3):
            for j in range(3):
                if self.board.board[i][j] == a:
                    if len(self.board.showmoves(i,j)) > 0:
                        t = False
        if t:
            messagebox.showinfo('Game Over','{} Wins'.format(self.wturn))
            self.won = self.wturn
            self.parent.playagain()
            return True


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

    def isvalid(self, q):
        if self.board[q[0]][q[1]] == 'b':
            return True
        else:
            return False


class AI():
    def __init__(self,parent):
        self.parent = parent
        self.memory = {1:{(2,0,1,0):[], (2,1,1,1):[], (2,2,1,2):[]}, 3:{}, 5:{}}
        # self.heirarchy = {(2,0,1,0,{}):[(0,1,1,1,{}),(0,1,1,0,{}),(0,2,1,2,{})],(2,1,1,1,{}):[],(2,2,1,2,{}):[]}
        self.one = {(2,0,1,0):[], (2,1,1,1):[], (2,2,1,2):[]}
        self.three = {}
        self.five = {}
        # self.current = self.heirarchy
        self.frame = self.parent.frames[len(self.parent.frames)-1]
        self.notes = {}

    def note(self,no,fr,fc,tr,tc):
        self.notes[no] = (fr,fc,tr,tc)

    def turn(self,n):
        m = n-1
        if m == 1:
            if self.notes[m] in list(self.one.keys()):
                if self.one[self.notes[m]] == []:
                    self.one[self.notes[m]] = self.blackmoves()
            else:
                self.one[self.notes[m]] = self.blackmoves()
            self.randommove(self.one[self.notes[m]])
        elif m == 3:
            if (self.notes[1],self.notes[2],self.notes[3]) in list(self.three.keys()):
                if self.three[(self.notes[1],self.notes[2],self.notes[3])] == []:
                    self.three[(self.notes[1],self.notes[2],self.notes[3])] = self.blackmoves()
            else:
                self.three[(self.notes[1],self.notes[2],self.notes[3])] = self.blackmoves()
            self.randommove(self.three[(self.notes[1],self.notes[2],self.notes[3])])
        elif m == 5:
            if (self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5]) in list(self.five.keys()):
                if self.five[(self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5])] == []:
                    self.five[(self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5])] = self.blackmoves()
            else:
                self.five[(self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5])] = self.blackmoves()
            self.randommove(self.five[(self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5])])

    def blackmoves(self):
        a = []
        possible = self.blacks()
        for i in possible:
            s = self.frame.board.showmoves(i[0], i[1])
            for j in s:
                a.append((i[0],i[1],j[0],j[1]))
        return a

    def blacks(self):
        possible = []
        for i in range(3):
            for j in range(3):
                if self.frame.board.board[i][j] == 'b':
                    possible.append((i,j))
        return possible

    def randommove(self, options):
        s = random.choice(options)
        self.frame.move(s[0],s[1],s[2],s[3])
        self.lastmove = (s[0],s[1],s[2],s[3])

    def feedback(self,who,n):
        if who == 'w':
            #remove lastmove from self.memory's last moveno's(frame.moveno), self.notes's last moveno
            # self.memory[self.frame.moveno-2][self.notes[self.frame.moveno-2]].remove(self.lastmove)
            if n == 3:
                self.one[(self.notes[1])].remove(self.lastmove)
            if n == 5:
                self.three[(self.notes[1],self.notes[2],self.notes[3])].remove(self.lastmove)
            if n == 7:
                self.five[(self.notes[1],self.notes[2],self.notes[3],self.notes[4],self.notes[5])].remove(self.lastmove)


    def refresh(self):
        self.frame = self.parent.frames[len(self.parent.frames)-1]
        self.notes = {}
        

if __name__ == '__main__':
    gameone = Hexapawn()
    gameone.mainloop()
