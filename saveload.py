import globals1
import time
import create_face as f12
import walker as walk
import Player as pl
import item as it
time1=time.time()
time2=time.time()
def save(k):
    f=open('saves/save'+str(k)+'/field.txt','w')
    t=str((globals1.W,globals1.H,globals1.L,globals1.K2,globals1.CELL_WID,len(globals1.FACE[0][0]),len(globals1.FACE[0]),globals1.RWID,globals1.OFFSET))
    f.write(t)
    f.write('\nDIVISION\n')
    time1=time.time()
    rs=[]
    for i in range(len(globals1.R_GRID)):
        for j in range(len(globals1.R_GRID[i])):
            for u in range(len(globals1.R_GRID[i][j])):
                r=globals1.R_GRID[i][j][u]
                t=((u,j,i),(r.x1,r.y1,r.x2,r.y2,r.vis))
                rs.append(t)
    f.write(str(rs))
    rs=0
    f.write('\nDIVISION\n')
    time2=time.time()
    #print('time spended to save rooms --> '+str(time2-time1))
    time1=time.time()
    r=globals1.COR_GRID
    t=str(r)
    f.write(t)
    f.write('\nDIVISION\n')
    time2=time.time()
    #print('time spended to save corridor_grid --> '+str(time2-time1))
    time1=time.time()
    t=str(globals1.MAP)
    f.write(t)
    time2=time.time()
    f.close()




    f=open('saves/save'+str(k)+'/items.txt','w')
    t=str((len(globals1.ITEM_GRID[0][0]),len(globals1.ITEM_GRID[0]),len(globals1.ITEM_GRID)))
    f.write(t)
    f.write('\nDIVISION\n')
    time1=time.time()
    mons=[]
    for w in globals1.MONSTERS:
        if w!=0:
            t=((w.x,w.y,w.l),w.cellp,w.mhp,w.atk,w.name)
        else:
            t=0
        mons.append(t)
    f.write(str(mons))
    mons=0
    f.write('\nDIVISION\n')
    time2=time.time()
    #print('time spended to save mons --> '+str(time2-time1))

    time1=time.time()
    its=[]
    for w in globals1.ITEMS:
        if w!=0:
            t=((w.x,w.y,w.l),w.cellp,w.typ,w.subtype,w.name,w.platk,w.plrange)
        else:
            t=0
        its.append(t)
    f.write(str(its))
    its=0
    time2=time.time()
    #print('time spended to save items --> '+str(time2-time1))
    f.close()




    f=open('saves/save'+str(k)+'/player.txt','w')
    p=globals1.P
    t=str(((p.x,p.y,p.l),p.name,p.hp,p.mhp,p.xp,p.lxp,p.lvl,p.atk,p.batk))
    f.write(t)
    f.write('\nDIVISION\n')

    eq=[]
    for m in p.equip:
        if m==0:
            t=0
        else:
            t=(m.typ,m.subtype,m.name,m.platk,m.plrange)
        eq.append(t)
    f.write(str(eq))
    eq=0
    f.write('\nDIVISION\n')

    bag=[]
    for m in p.bag:
        t=(m.typ,m.subtype,m.name,m.platk,m.plrange)
        bag.append(t)
    f.write(str(bag))
    bag=0
    f.close()




def load(k):
    globals1.clear()

    f1=open('saves/save'+str(k)+'/field.txt','r')
    f=f1.read()
    f=f.split('\nDIVISION\n')
    globals1.W,globals1.H,globals1.L,globals1.K2,globals1.CELL_WID,w5,h5,globals1.RWID,globals1.OFFSET=eval(f[0])
    time1=time.time()
    rooms=eval(f[1])
    globals1.R_GRID=[]
    for i in range(globals1.L):
        globals1.R_GRID.append([])
        for j in range(globals1.H):
            globals1.R_GRID[i].append([0]*globals1.W)

    for i in range(len(rooms)):
        t=rooms[i]
        tr=f12.room(t[1][0],t[1][1],t[1][2],t[1][3],t[0][2])
        tr.vis=t[1][4]
        globals1.R_GRID[t[0][2]][t[0][1]][t[0][0]]=tr
    time2=time.time()
    #print('time spended to load rooms --> '+str(time2-time1))

    globals1.COR_GRID=eval(f[2])
    corridors=[[]]*globals1.L
    f12.countstair=-1
    for u in range(globals1.L):
        for i in range(globals1.H):
            for j in range(globals1.W):
                t1,t2=f12.cor1(globals1.R_GRID[globals1.COR_GRID[u][i][j][2]][globals1.COR_GRID[u][i][j][1]][globals1.COR_GRID[u][i][j][0]],globals1.R_GRID[u][i][j])
                for i5 in t1:
                    corridors[u].append(i5)
                if t2!=None:
                    globals1.STAIRS.append(t2)
    time2=time.time()
    globals1.MAP=eval(f[3])
    #print('time spended to create corridors and stairs --> '+str(time2-time1))
    time1=time.time()
    globals1.FACE=f12.draw_map(w5,h5,globals1.L,globals1.R_GRID,corridors,globals1.STAIRS,False)
    corridors=0
    time2=time.time()
    #print('time spended to create face --> '+str(time2-time1))
    f1.close()



    f1=open('saves/save'+str(k)+'/items.txt','r')
    f=f1.read()
    f=f.split('\nDIVISION\n')
    time1=time.time()
    w,h,z=eval(f[0])
    for u in range(z):
        globals1.ITEM_GRID.append([])
        for i in range(h):
            globals1.ITEM_GRID[u].append([])
            for j in range(w):
                globals1.ITEM_GRID[u][i].append([[],[]])

    for i in range(len(globals1.STAIRS)):
        st=globals1.STAIRS[i]

        x1,y1,z1=st.p1[0]//globals1.CELL_WID,st.p1[1]//globals1.CELL_WID,st.p1[2]
        x2,y2,z2=st.p2[0]//globals1.CELL_WID,st.p2[1]//globals1.CELL_WID,st.p2[2]

        if len(globals1.ITEM_GRID[z1][y1][x1])<3:
            globals1.ITEM_GRID[z1][y1][x1].append([])
            globals1.ITEM_GRID[z1][y1][x1][2].append(st.num)
        else:
            globals1.ITEM_GRID[z1][y1][x1][2].append(st.num)

        if len(globals1.ITEM_GRID[z2][y2][x2])<3:
            globals1.ITEM_GRID[z2][y2][x2].append([])
            globals1.ITEM_GRID[z2][y2][x2][2].append(st.num)
        else:
            globals1.ITEM_GRID[z2][y2][x2][2].append(st.num)
    time2=time.time()
    #print('time spended for item_grid and stairs  --> '+str(time2-time1))
    time1=time.time()
    mons=eval(f[1])
    tcount=-1#temperal counter for items
    for t in mons:
        if t!=0:
            tcount+=1
            temp=walk.walker(t[0][0],t[0][1],t[0][2],t[2],t[4],t[1],tcount)
            temp.atk=t[3]
            globals1.ITEM_GRID[t[0][2]][t[1][1]][t[1][0]][0].append(tcount)
            globals1.MONSTERS.append(temp)
    mons=0
    time2=time.time()
    #print('time spended to load monsters  --> '+str(time2-time1))
    time1=time.time()
    its=eval(f[2])
    tcount=-1#temperal counter for items
    for t in its:
        if t!=0:
            tcount+=1
            temp=it.item(t[0][0],t[0][1],t[0][2],t[2],t[3],t[4],t[1],tcount)
            temp.platk=t[5]
            temp.plrange=t[6]
            globals1.ITEM_GRID[t[1][2]][t[1][1]][t[1][0]][1].append(tcount)
            globals1.ITEMS.append(temp)
    its=0
    time2=time.time()
    #print('time spended to load items  --> '+str(time2-time1))
    f1.close()


    f1=open('saves/save'+str(k)+'/player.txt','r')
    f=f1.read()
    f=f.split('\nDIVISION\n')
    t=eval(f[0])
    globals1.P=pl.player(t[0][0],t[0][1],t[0][2],t[3],t[1])
    globals1.P.hp=t[2]
    globals1.P.xp=t[4]
    globals1.P.lxp=t[5]
    globals1.P.lvl=t[6]
    globals1.P.atk=t[7]
    globals1.P.batk=t[8]
    equip=eval(f[1])
    #(m.typ,m.subtype,m.name,m.platk,m.plrange)
    globals1.P.equip=[]
    for t in equip:
        #self,x,y,l,type,subtype,name,cellp,num
        #(0,0,0,0,0,'|',(0,0,0),0)
        temp=it.item(0,0,0,t[0],t[1],t[2],(0,0,0),0)
        temp.platk=t[3]
        temp.plrange=t[4]
        globals1.P.equip.append(temp)
    equip=0
    bag=eval(f[2])
    globals1.P.bag=[]
    for t in bag:
        temp=it.item(0,0,0,t[0],t[1],t[2],(0,0,0),0)
        temp.platk=t[3]
        temp.plrange=t[4]
        globals1.P.bag.append(temp)
    bag=0
    f1.close()
