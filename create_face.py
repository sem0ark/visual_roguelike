from random import *
import create_maze_of_cors as maze
import time

class room:
    def __init__(self,x1,y1,x2,y2,l):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        self.l=l
        self.vis=0

class stair:
    def __init__(self,p1,p2,num):
        self.p1=p1
        self.p2=p2
        self.num=num

countstair=-1

def cor1(r1,r2):#create corridors
    global countstair
    x1=(r1.x2+r1.x1)//2
    x2=(r2.x2+r2.x1)//2
    y1=(r1.y2+r1.y1)//2
    y2=(r2.y2+r2.y1)//2
    l1=r1.l
    l2=r2.l
    f=[]
    stair1=None
    if l1==l2:
        if y1<y2 and x1<x2:
            cx=room(x1,y1,x2,y1,l1)
            cy=room(x2,y1,x2,y2,l1)
            f.append(cx)
            f.append(cy)
        elif y1<y2 and x1>x2:
            cx=room(x2,y1,x1,y1,l1)
            cy=room(x2,y1,x2,y2,l1)
            f.append(cx)
            f.append(cy)
        elif y1>y2 and x1<x2:
            cx=room(x1,y2,x2,y2,l1)
            cy=room(x1,y2,x1,y1,l1)
            f.append(cx)
            f.append(cy)
        elif y1>y2 and x1>x2:
            cx=room(x2,y2,x1,y2,l1)
            cy=room(x1,y2,x1,y1,l1)
            f.append(cx)
            f.append(cy)
        elif x1==x2:
            if y1<y2:
                cy=room(x1,y1,x1,y2,l1)
                f.append(cy)
            elif y1>y2:
                cy=room(x1,y2,x1,y1,l1)
                f.append(cy)
        elif y1==y2:
            if x1<x2:
                cx=room(x1,y1,x2,y1,l1)
                f.append(cx)
            elif x1>x2:
                cx=room(x2,y1,x1,y1,l1)
                f.append(cx)
        '''
        cx=room(x1,y1,x2,y1,l1)
        cy=room(x2,y1,x2,y2,l1)
        f.append(cx)
        f.append(cy)'''
    if l1!=l2:
        countstair+=1
        stair1=stair((x1,y1,l1),(x2,y2,l2),countstair)
    return(f,stair1)

def create_map_grid(w,h,l,celld,walld,minroomd,offset):#number of rooms by width/height/layers, side of cell, widht of wall (minimal), minimal widht/height of room
    grid=[]
    time1=time.time()
    print('creating rooms')
    for u in range(l):
        grid.append([])
        for i in range(h):
            grid[u].append([])
            for j in range(w):
                w4=randint(minroomd,celld)
                h4=randint(minroomd,celld)
                x1=offset+(walld+celld)*j+randint(0,celld-w4)
                x2=x1+w4
                y1=offset+(walld+celld)*i+randint(0,celld-h4)
                y2=y1+h4
                roo=room(x1,y1,x2,y2,u)
                grid[u][i].append(roo)
    corridors=[[]]*l
    stairs=[]
    time2=time.time()
    #print('time spended for rooms --> '+str(time2-time1))
    time1=time.time()
    labir=maze.generate_maze_grid_prims(w,h,l)#2d array for aka grid of corridors
    print('creating corridors')
    for u in range(l):
        for i in range(h):
            for j in range(w):
                t1,t2=cor1(grid[labir[u][i][j][2]][labir[u][i][j][1]][labir[u][i][j][0]],grid[u][i][j])
                for i5 in t1:
                    corridors[u].append(i5)
                if t2!=None:
                    stairs.append(t2)
                    '''
                    if (i>0 and j>0) and (i<h-1 and j<w-1):
                        temp3=angle(randint(0,3))
                        u5=t2.p1[2]
                        aq1,aq2=cor1(grid[u5][i][j],grid[u5][i+temp3[1]][j+temp3[0]])
                        for i5 in aq1:
                            corridors[u5].append(i5)
                        temp3=angle(randint(0,3))
                        u5=t2.p2[2]
                        aq1,aq2=cor1(grid[u5][i][j],grid[u5][i+temp3[1]][j+temp3[0]])
                        for i5 in aq1:
                            corridors[u5].append(i5)'''
    time2=time.time()
    #print('time spended for corridors --> '+str(time2-time1))
    return(grid,corridors,stairs,labir)

def draw_map(w,h,l,gr,cr,st,draw):#width,height (of map), list of rooms (grid), list of corridors (corridors)
    p=[]
    for u in range(l):
        p.append([])
        for j in range(h):
            p[u].append(['#']*w)
    for u in range(l):
        for i in range(len(gr[u])):
            for j in range(len(gr[u][i])):
                x1=gr[u][i][j].x1
                y1=gr[u][i][j].y1
                x2=gr[u][i][j].x2
                y2=gr[u][i][j].y2
                t1=(x1+x2)//2
                t2=(y1+y2)//2
                for i1 in range(y1,y2+1):
                    for j1 in range(x1,x2+1):
                        p[u][i1][j1]=' '
    for i in range(len(cr)):
        for j in range(len(cr[i])):
            x1=cr[i][j].x1
            y1=cr[i][j].y1
            x2=cr[i][j].x2
            y2=cr[i][j].y2
            l4=cr[i][j].l
            #print(l4)
            for i1 in range(y1,y2+1):
                for j1 in range(x1,x2+1):
                    p[l4][i1][j1]=' '

    for i in range(len(st)):
        st1=st[i]
        p1=st1.p1
        p2=st1.p2

        if p1[2]>p2[2]:
            p2,p1=p1,p2
        #print(p1,p2)
        fp1=p[p1[2]][p1[1]][p1[0]]
        fp2=p[p2[2]][p2[1]][p2[0]]

        if fp1==' ':
            p[p1[2]][p1[1]][p1[0]]='+'
        elif fp1 ==':':
            p[p1[2]][p1[1]][p1[0]]='I'

        if fp2==' ':
            p[p2[2]][p2[1]][p2[0]]=':'
        elif fp2=='+':
            p[p1[2]][p1[1]][p1[0]]='I'
    if draw:
        for u in range(l):
            print()
            for i in range(len(p[u])):
                l=''
                for j in range(len(p[u][i])):
                    l+=p[u][i][j]
                print(l)
    return(p)

def generate_map(w,h,l,celld,walld,minroomd,border_offset):#width,height (of map), side of cell, widht of wall (minimal), minimal widht/height of room
    gr,cr,st,lab=create_map_grid(w,h,l,celld,walld,minroomd,border_offset)
    face=(draw_map((celld+walld)*w+2*border_offset,(celld+walld)*h+2*border_offset,l,gr,cr,st,False))
    return(gr,st,face,lab)

'''
def angle(n):
    if n==0:
        return(1,0)
    elif n==1:
        return(0,-1)
    elif n==2:
        return(-1,0)
    elif n==3:
        return(0,1)'''

if __name__=='__main__':
    w,h,l=12,4,5
    d,wl,min1=6,2,6
    off=4
    gr,cr,st,face,st_c=generate_map(w,h,l,d,wl,min1,off)
