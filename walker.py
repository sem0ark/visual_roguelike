from random import *
from math import *
import globals1

class walker:
    def __init__(self,x,y,l,hp,name,cellp,num):
        self.x=x
        self.y=y
        self.l=l

        self.hp=hp
        self.mhp=hp
        self.name=name
        self.number=num
        self.cellp=cellp

        self.floor=' '

        self.stack=['w1']

        #add. atk
        self.atk=0
        #range of detection
        self.arange=8
        #range of running
        self.rrange=12
        #range of attack
        self.at=1.1
        #percent of hp for running away
        self.rrate=0.4

    def go(self,h):
        x1,y1=angle(h)
        x , y = self.y+y1 , self.x+x1
        o=False
        if globals1.FACE[self.l][self.y+y1][self.x+x1] in [' ','|','/',')',']']:
            globals1.FACE[self.l][self.y][self.x]=self.floor
            self.floor=globals1.FACE[self.l][self.y+y1][self.x+x1]
            globals1.FACE[self.l][self.y+y1][self.x+x1]=self.name
            self.y+=y1
            self.x+=x1
            if (self.x//globals1.CELL_WID,self.y//globals1.CELL_WID)!=self.cellp:
                globals1.ITEM_GRID[self.l][self.cellp[1]][self.cellp[0]][0].remove(self.number)
                self.cellp=(self.x//globals1.CELL_WID,self.y//globals1.CELL_WID)
                globals1.ITEM_GRID[self.l][self.cellp[1]][self.cellp[0]][0].append(self.number)
            o=True
        return(o)

    def go1(self,r,fh):#
        #fh=0 >>> attack
        #fh=1 >>> run away
        d1x,d1y=r[1],r[2]
        if fh==0:
            if r[0]<=self.at:
                return(0)
        o=False
        if d1x!=0:
            if d1x>0:
                o=o or self.go([0,2][fh])
            else:
                o=o or self.go([2,0][fh])
        if d1y!=0:
            if d1y>0:
                o=o or self.go([3,1][fh])
            else:
                o=o or self.go([1,3][fh])
        if not(o) and (d1y==0 and d1x!=0):
            o1=self.go([1,3][randint(0,1)])
            if not(o1):
                self.go([3,1][randint(0,1)])
        if not(o) and (d1y!=0 and d1x==0):
            o1=self.go([0,2][randint(0,1)])
            if not(o1):
                self.go([2,0][randint(0,1)])

    def w1(self):
        h=randint(0,3)
        self.go(h)
        r=dist(self)
        if self.hp<self.mhp:
            t=randint(0,1)
            self.hp+=t
        if globals1.P.hp>0:
            if r[0]<=self.arange:
                if self.hp<self.rrate*self.mhp:
                    self.stack.pop()
                    self.stack.append('w3')
                    print(self.name+' wants to run away')
                    #runaway
                else:
                    self.stack.pop()
                    self.stack.append('w2')
                    print(self.name+' detected player')

    def w2(self):
        if globals1.P.hp>0:
            r=dist(self)
            self.go1(r,0)
            #print(self.name+'>>>hp'+str(self.hp)+' / '+str(self.mhp))
            #print('distance to '+self.name+' is '+str(round(r[0],3)))
            if r[0]<self.at:
                self.stack.append('a1')
                print(self.name+' want to attack')
            if r[0]>self.arange:
                self.stack.pop()
                self.stack.append('w1')
                print(self.name+' missed player')
            if r[0]<self.rrange and self.hp<self.rrate*self.mhp:
                self.stack.append('w3')
                print(self.name+' wants to run away')

        else:
            self.stack.pop()
            self.stack.append('w1')

    def w3(self):
        #print(self.name+'>>>hp'+str(self.hp)+' / '+str(self.mhp))
        r=dist(self)
        self.go1(r,1)
        if r[0]>self.rrange:
            self.stack.pop()
            self.stack.append('w1')
            print(self.name+' missed player')
        if self.hp<self.rrate*self.mhp:
            t=randint(0,1)
            self.hp+=t
            print(self.name+' restored '+str(t)+' hp')
        else:
            self.stack.pop()
            self.stack.append('w1')

    def a1(self):
        r=dist(self)
        print(self.name+'>>>hp'+str(self.hp)+' / '+str(self.mhp))
        if r[0]<=self.at:
            t6=randint(0+self.atk,2+self.atk)
            globals1.P.hp-=t6
            if self.hp<self.rrate*self.mhp:
                self.stack.pop()
                self.stack.append('w3')
                print(self.name+' wants to run away')
            if globals1.P.hp<=0:
                globals1.FACE[self.l][globals1.P.y][globals1.P.x]=' '
                print('game_over')
                print(self.name+' missed player')
                self.stack.pop()
            print(self.name+' attacked >> '+globals1.P.name+' by '+str(t6)+' hp '+str(z(globals1.P.hp))+'/'+str(z(globals1.P.mhp)))
        else:
            self.stack.pop()

    def whattodo(self):
        if self.hp>0:
            eval('self.'+self.stack[len(self.stack)-1]+'()')

def dist(w):
    x=globals1.P.x-w.x
    y=globals1.P.y-w.y
    d=sqrt(x**2+y**2)
    return((d,x,y))

def z(x):
    if x<0: return(0)
    else: return(x)

def angle(n):
    if n==0:
        return(1,0)
    elif n==1:
        return(0,-1)
    elif n==2:
        return(-1,0)
    elif n==3:
        return(0,1)
