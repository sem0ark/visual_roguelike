from random import *
import pygame as pg
import time

import create_face as facegen
import walker as walk
import Player as pl
import item as it
import globals1


#-----------------------------#
# INITIALISATION OF VARIABLES #

globals1.clear()

globals1.W,globals1.H,globals1.L = 20,20,4
#number of rooms by width/height
c_wid,wl_wid,min_w = 4,3,2#side of cell (of room), widht of wall (minimal), minimal widht and height of room
globals1.CELL_WID = 20
border_offset=5
globals1.RWID=c_wid+wl_wid
globals1.OFFSET=border_offset
globals1.ITEM_GRID=[]
#creation of 2d array of two lists index 0 --> monsters ,index 1 --> globals1.ITEMS
for u in range(globals1.L):
    globals1.ITEM_GRID.append([])
    for i in range(((c_wid+wl_wid)*globals1.H+2*border_offset)//globals1.CELL_WID+1):
        globals1.ITEM_GRID[u].append([])
        for j in range(((c_wid+wl_wid)*globals1.W+2*border_offset)//globals1.CELL_WID+1):
            globals1.ITEM_GRID[u][i].append([[],[]])

globals1.R_GRID, globals1.STAIRS, globals1.FACE, globals1.COR_GRID = facegen.generate_map(globals1.W,globals1.H,globals1.L,c_wid,wl_wid,min_w,border_offset)#2d array of rooms, list of corridors, generation of map

globals1.MAP=[]
for u in range(globals1.L):
    globals1.MAP.append([])
    for i in range(globals1.H*2-1):
        globals1.MAP[u].append([])
        for j in range(globals1.W*2-1):
            globals1.MAP[u][i].append(' ')

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

#-----------------------------#




#--------------------------#
# INITIALISATION OF PLAYER #

rx,ry,rl=randint(0,globals1.W-1),randint(0,globals1.H-1),randint(0,globals1.L-1)

x,y,l=(globals1.R_GRID[rl][ry][rx].x1+globals1.R_GRID[rl][ry][rx].x2)//2,(globals1.R_GRID[rl][ry][rx].y1+globals1.R_GRID[rl][ry][rx].y2)//2,rl

hp=1000

globals1.P=pl.player(x,y,l,hp,'@')
#--------------------------#



#----------------------------#
# INITIALISATION OF MONSTERS #

#x,y,hp,name,cellp,num
def generate_monster(x,y,l,cellp,name,hp=10,atk=0):
    w=walk.walker(x,y,l,hp,name,cellp,len(globals1.MONSTERS))
    w.atk=atk
    return(w)

def spawn_monster():
    global k_monster
    x,y,z=randint(0,globals1.W-1),randint(0,globals1.H-1),randint(0,globals1.L-1)
    ro=globals1.R_GRID[z][y][x]
    x1=randint(ro.x1,ro.x2)
    y1=randint(ro.y1,ro.y2)
    if globals1.FACE[z][y1][x1]==' ':
        temp_p=(x1//globals1.CELL_WID, y1//globals1.CELL_WID)
        globals1.ITEM_GRID[z][temp_p[1]][temp_p[0]][0].append(len(globals1.MONSTERS))
        alf=choice(globals1.ALPHABET)
        globals1.FACE[z][y1][x1]=alf
        mon=generate_monster(x1,y1,z,temp_p,alf,10+globals1.K2//30,globals1.K2//40)
        globals1.MONSTERS.append(mon)

#----------------------------#



#-------------------------#
# INITIALISATION OF ITEMS #

its=[['|','/'], [')',']']]

def spawn_item():#type1 0 --> [0(subtype)->sword,1->spear], 1 --> [0->short_bow,1->long_bow]
    global its
    type1,subtype=randint(0,1),randint(0,1)
    name=its[type1][subtype]
    x,y,z=randint(0,globals1.W-1),randint(0,globals1.H-1),randint(0,globals1.L-1)
    ro=globals1.R_GRID[z][y][x]
    x1=randint(ro.x1,ro.x2)
    y1=randint(ro.y1,ro.y2)
    if globals1.FACE[z][y1][x1]==' ':
        temp_p=(x1//globals1.CELL_WID, y1//globals1.CELL_WID, z)
        globals1.ITEM_GRID[z][temp_p[1]][temp_p[0]][1].append(len(globals1.ITEMS))
        globals1.FACE[z][y1][x1]=name
        item1=it.item(x1,y1,z,type1,subtype,name,temp_p,len(globals1.ITEMS))
        item1.platk=globals1.K2//100
        if subtype==1 and type1==0:
            item1.plrange=1
        if subtype==1 and type1==1:
            item1.plrange=globals1.K2//1000
        globals1.ITEMS.append(item1)

#-------------------------#



#---------------------------#
# INITIALISESATION OF TILES #
cw,ch=48*16+16*8,48*16
globals1.disp=pg.display
globals1.C=globals1.disp.set_mode((cw,ch))

globals1.item_tiles=[pg.image.load('tiles/bow1.png'),pg.image.load('tiles/bow2.png'),pg.image.load('tiles/spear.png'),pg.image.load('tiles/sword1.png')]
globals1.field_tiles=[pg.image.load('tiles/floor1.png'),pg.image.load('tiles/wall1.png'),pg.image.load('tiles/stair_down.png'),pg.image.load('tiles/stair_up.png'),pg.image.load('tiles/stair_updown.png')]
globals1.live_tiles=[pg.image.load('tiles/player.png'),pg.image.load('tiles/walker.png')]
globals1.map_tiles=[pg.image.load('tiles/map_room.png'),pg.image.load('tiles/map_room_down.png'),pg.image.load('tiles/map_room_up.png'),pg.image.load('tiles/map_room_updown.png'),pg.image.load('tiles/map_road_vert.png'),pg.image.load('tiles/map_road_horiz.png'),pg.image.load('tiles/map_mask1.png'),pg.image.load('tiles/map_player.png')]

#---------------------------#





#-------------------------#
#------- FOR DEBUG -------#

def draw_face():
    for u in range(len(globals1.FACE)):
        print()
        for i in range(len(globals1.FACE[u])):
            l=''
            for j in range(len(globals1.FACE[u][i])):
                l+=globals1.FACE[u][i][j]
            print(l)

def watch():
    print('face w,h -->',len(globals1.FACE[0][0]),len(globals1.FACE[0]))
    print('item_grid w,h,CELL_WID -->',len(globals1.ITEM_GRID[0][0]),len(globals1.ITEM_GRID[0]) , globals1.CELL_WID)
    print('stairs -->',len(globals1.STAIRS))
#-------------------------#








#------#
# MAIN #
globals1.K2=0#TURN COUNTER
#globals1.W*globals1.H*globals1.L
for i in range(globals1.W*globals1.H*globals1.L):
    spawn_monster()
time1=time.time()
time2=time.time()
#print('time spended for mons --> '+str(time2-time1))
for i in range(4):
    spawn_item()
    print()

#draw_face()
watch()
f1=open('Help.txt','r')
print(f1.read())
input('press enter to continue')
print()
#print()

temp=globals1.P.find_items_around(0,2)
for i in range(len(temp)):
        globals1.MONSTERS[temp[i]].whattodo()
def iteration():
    globals1.K2+=1
    pg.display.update()
    globals1.P.whattodo(True)
    temp=globals1.P.find_items_around(0,2)
    #print((temp,ascii(globals1.MONSTERS)))
    #print(globals1.ITEM_GRID)
    pg.display.update()
    for i in range(len(temp)):
        globals1.MONSTERS[temp[i]].whattodo()
    if globals1.K2%100==0:
        spawn_item()
    if globals1.K2%40==0:
        spawn_monster()
run = True
while run:
    pg.time.delay(10)
    for ev in pg.event.get():
        if ev.type==pg.QUIT:
            run=False
    '''
    keys=pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        x-=vel
        if x<-w:
            x=500+w
    if keys[pg.K_RIGHT]:
        x+=vel
        if x>500:
            x=-w
    if keys[pg.K_DOWN]:
        y+=vel
        if y>500:
            y=-h
    if keys[pg.K_UP]:
        y-=vel
        if y<-h:
            y=500+h'''
    iteration()


#------#
