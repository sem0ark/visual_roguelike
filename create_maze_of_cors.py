from random import *
import heapq as hq

def generate_maze_grid_backtracer(w,h,l):
    cells=[]
    for u in range(l):
        cells.append([])
        for i in range(h):
            cells[u].append([])
            for j in range(w):
                cells[u][i].append(0)
    stack=[]
    y1=randint(0,h-1)
    x1=randint(0,w-1)
    z1=randint(0,l-1)
    #print(x1,y1)
    cells[z1][y1][x1]=(x1,y1,z1)
    stack.append((x1,y1,z1))
    while len(stack)>0:
        x,y,z=stack[len(stack)-1]
        f=[]
        if x>0:
            if cells[z][y][x-1]==0:
                f.append((x-1,y,z))
        if x+1<w:
            if cells[z][y][x+1]==0:
                f.append((x+1,y,z))
        if y>0:
            if cells[z][y-1][x]==0:
                f.append((x,y-1,z))
        if y+1<h:
            if cells[z][y+1][x]==0:
                f.append((x,y+1,z))
        if z+1<l:
            if cells[z+1][y][x]==0:
                f.append((x,y,z+1,z))
        if z>0:
            if cells[z-1][y][x]==0:
                f.append((x,y,z-1))
        if len(f)!=0:
            aim=choice(f)
            x,y,z=stack[len(stack)-1]
            cells[aim[2]][aim[1]][aim[0]]=(x,y,z)
            stack.append(aim)
        else:
            if len(stack)>0:
                stack.pop()
    return(cells)

def generate_maze_grid_prims(w,h,l):
    cells=[]
    for u in range(l):
        cells.append([])
        for i in range(h):
            cells[u].append([])
            for j in range(w):
                cells[u][i].append(0)

    jk=200#additional weight
    y1=randint(1,h-2)
    x1=randint(1,w-2)
    z1=randint(0,l-1)
    f=[(0,((x1,y1,z1),(x1+1,y1,z1)))]
    cells[z1][y1][x1]=(x1,y1,z1)
    while len(f)>0:
        item=hq.heappop(f)
        item=item[1]
        pos=item[0]
        aim=item[1]
        if cells[aim[2]][aim[1]][aim[0]]==0:
            cells[aim[2]][aim[1]][aim[0]]=pos
            x,y,z=aim
            if x-1>=0:
                if cells[z][y][x-1]==0:
                    weight=randint(w*2,w*2+jk)
                    hq.heappush(f, (weight,(aim,(x-1,y,z))) )
            if x+1<w:
                if cells[z][y][x+1]==0:
                    weight=randint(w*2,w*2+jk)
                    hq.heappush(f, (weight,(aim,(x+1,y,z))) )
            if y-1>=0:
                if cells[z][y-1][x]==0:
                    weight=randint(w*2,w*2+jk)
                    hq.heappush(f, (weight,(aim,(x,y-1,z))) )
            if y+1<h:
                if cells[z][y+1][x]==0:
                    weight=randint(w*2,w*2+jk)
                    hq.heappush(f, (weight,(aim,(x,y+1,z))) )
            if z+1<l:
                if cells[z+1][y][x]==0:
                    weight=randint(w*2,w*2+jk)*2
                    hq.heappush(f, (weight,(aim,(x,y,z+1))) )
            if z-1>=0:
                if cells[z-1][y][x]==0:
                    weight=randint(w*2,w*2+jk)*2
                    hq.heappush(f, (weight,(aim,(x,y,z-1))) )
    return(cells)

if __name__=='__main__':
    gr=generate_maze_grid_prims(10,10,6)
    for i in range(len(gr)):
        print(' ')
        for j in range(len(gr[i])):
            print(gr[i][j])
