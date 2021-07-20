## GLOBAL VARIABLES ##

W,H,L=0,0,0
P=0
K2=0
CELL_WID=0
RWID=0
OFFSET=0
ITEM_GRID=[]
COR_GRID=[]
R_GRID=[]
FACE=[]
STAIRS=[]
MONSTERS=[]
ITEMS=[]
MAP=[]
ALPHABET = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

item_tiles=[]
field_tiles=[]
live_tiles=[]
map_tiles=[]

C=0
disp=0

#--------------------#

def clear():
    global W,H,L,P,CELL_WID,R_GRID,FACE,MONSTERS,ITEMS,K2,COR_GRID,STAIRS,ITEM_GRID,RWID,OFFSET,MAP
    W,H,L=0,0,0
    P=0
    K2=0
    RWID=0
    OFFSET=0
    CELL_WID=0
    ITEM_GRID=[]
    COR_GRID=[]
    R_GRID,FACE,STAIRS=[],[],[]
    MONSTERS=[]
    ITEMS=[]
    MAP=[]
