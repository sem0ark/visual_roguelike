from random import *
from math import *
import pygame as pg
import item as it1
import saveload as sl
import globals1

class player:
    def __init__(self,x,y,l,hp,name):
        #coordinates on map
        self.x=x
        self.y=y
        self.l=l

        self.xp=0
        self.lvl=1
        self.lxp=int(sqrt(self.lvl**2.2)+20)

        self.name=name#name showed on map
        self.floor=globals1.FACE[l][y][x]
        globals1.FACE[l][y][x]=name

        self.rpos=(self.l,(self.y-globals1.OFFSET)//globals1.RWID,(self.x-globals1.OFFSET)//globals1.RWID)
        self.prev_rpos=self.rpos

        self.hp=hp#current HP
        self.mhp=hp#maximal HP
        self.atk=0
        self.batk=0

        self.a1_attack_range=1#attack range of first type of weapon
        self.b1_attack_range=6#attack range of second type of weapon

        self.throw_range=4#item throw range

        self.bag=[]
        self.equip=[it1.item(0,0,0,0,0,'|',(0,0,0),0),it1.item(0,0,0,1,0,')',(0,0,0),0)]

    def go(self,h):
        if self.hp>0:
            x1,y1=angle(h)
            if globals1.FACE[self.l][self.y+y1][self.x+x1] in [' ',':','+','I','|','/',')',']']:
                globals1.FACE[self.l][self.y][self.x]=self.floor
                self.floor=globals1.FACE[self.l][self.y+y1][self.x+x1]
                globals1.FACE[self.l][self.y+y1][self.x+x1]=self.name
                self.y+=y1
                self.x+=x1
                trpos=(self.l,(self.y-globals1.OFFSET)//globals1.RWID,(self.x-globals1.OFFSET)//globals1.RWID)
                if trpos!=self.rpos:
                    self.prev_rpos=self.rpos
                    self.rpos=trpos
                # print(self.x,self.y,self.floor)


    def find_items_around(self,ind,radius):#ind: 0 --> monsters, 1 --> items, 2 --> stairs
        cell_p=(self.x//globals1.CELL_WID, self.y//globals1.CELL_WID)
        temp=[]
        x1,x2=cell_p[0]-radius,cell_p[0]+radius
        y1,y2=cell_p[1]-radius,cell_p[1]+radius
        for i in range(y1,y2+1):
            for j in range(x1,x2+1):
                if (i>=0 and j>=0) and (i<len(globals1.ITEM_GRID[self.l]) and j<len(globals1.ITEM_GRID[self.l][0])):
                    if ind!=2:
                        temp+=globals1.ITEM_GRID[self.l][i][j][ind]
                    else:
                        if len(globals1.ITEM_GRID[self.l][i][j])>2:
                            temp+=globals1.ITEM_GRID[self.l][i][j][ind]
        return(temp)

    def find_items_ahead(self,ind,heading,lenght):#ind: 0 --> monsters, 1 --> items, 2 --> stairs
        x1,y1=self.x//globals1.CELL_WID, self.y//globals1.CELL_WID
        x2,y2=(self.x+heading[0]*lenght)//globals1.CELL_WID, (self.y+heading[1]*lenght)//globals1.CELL_WID
        temp=[]
        if x1>x2:
            x1,x2=x2,x1
        if y1>y2:
            y1,y2=y2,y1
        fg=False
        for i in range(y1,y2+1):
            for j in range(x1,x2+1):
                if (i>=0 and j>=0) and (i<len(globals1.ITEM_GRID[self.l]) and j<len(globals1.ITEM_GRID[self.l][0])):
                    temp+=globals1.ITEM_GRID[self.l][i][j][ind]
                else:
                    fg=True
                    break
            if fg:
                break
        return(temp)

    # def find_tiles(x,y,r):
    #     x1=z(x-r)
    #     y1=z(y-r)
    #     x2=x+r
    #     y2=y+r
    #     if x2>=len(globals1.FACE[self.l][0]):
    #         x2=len(globals1.FACE[self.l][0])-1
    #     if y2>=len(globals1.FACE[self.l]):
    #         y2=len(globals1.FACE[self.l])-1
    def wait(self):
        t=0
        if self.hp<self.mhp:
            t=randint(0,1)
            self.hp+=t
        print(self.name+' waited and restored '+str(t)+' hp '+str(z(self.hp))+'/'+str(z(self.mhp)))

    def tp(self,p):#teleport (for stairs)
        globals1.FACE[self.l][self.y][self.x]=self.floor
        self.floor=globals1.FACE[p[2]][p[1]][p[0]]
        globals1.FACE[p[2]][p[1]][p[0]]=self.name
        self.x,self.y,self.l=p
        self.prev_rpos=self.rpos
        self.rpos=(self.l,(self.y-globals1.OFFSET)//globals1.RWID,(self.x-globals1.OFFSET)//globals1.RWID)
    def get_xp(self,hp,at):
        self.xp+=hp+int(sqrt(hp+at))
        while(self.xp>=self.lxp):
            self.xp-=self.lxp
            self.lvl+=1
            self.lxp=int(sqrt(self.lvl**2.2)+20)
            print(self.name + ' leveled up, now it`s --> '+str(self.lvl))
            self.mhp+=self.lvl*2
            self.hp=self.mhp
            self.atk=int(self.lvl/2)
            self.batk=int(sqrt(self.lvl/2))
    def a1(self,h):#attack by first weapon by h heading
        if self.hp>0:
            xp,yp=angle(h)
            t=[]
            for i in range(self.a1_attack_range+self.equip[0].plrange):
                dtx,dty=self.x+xp*(i+1),self.y+yp*(i+1)
                if globals1.FACE[self.l][dty][dtx] in globals1.ALPHABET:
                    if (dtx>=0 and dty>=0) and (dtx<len(globals1.FACE[self.l]) and dty<len(globals1.FACE[self.l])):
                        t.append((dtx,dty))
                else:
                    if globals1.FACE[self.l][self.y+yp*(i+1)][self.x+xp*(i+1)]!=' ': break
            temp_mons_ind=self.find_items_ahead(0,(xp,yp),(self.a1_attack_range+self.equip[0].plrange))
            counter=0
            temp_mons=[]
            for i in range(len(temp_mons_ind)):
                it=globals1.MONSTERS[temp_mons_ind[i]]
                if (it.x,it.y) in t:
                    counter+=1
                    temp_mons.append(temp_mons_ind[i])
                    if counter == len(t):
                        break
            for i in range(len(temp_mons)):
                it=globals1.MONSTERS[temp_mons[i]]
                if self.equip[0]!=0:
                    t5=randint(2+self.equip[0].platk+self.atk,4+self.equip[0].platk+self.atk)
                else: t5=randint(2+self.atk,4+self.atk)
                it.hp-=t5
                #self.get_xp(t5,0)
                print(self.name+' hit by '+self.equip[0].name+' >> '+it.name+' by '+str(t5)+' hp '+str(z(it.hp))+'/'+str(z(it.mhp)))
                if it.hp<=0:
                    cell_p=it.cellp
                    globals1.FACE[self.l][it.y][it.x]=' '
                    print(self.name+' killed '+it.name)
                    ta,tb=it.mhp,it.atk
                    self.get_xp(ta,tb)
                    txp=ta+int(sqrt(ta+tb))
                    print('acquired '+str(txp)+' xp')
                    globals1.ITEM_GRID[self.l][cell_p[1]][cell_p[0]][0].remove(temp_mons[i])
                    globals1.MONSTERS[temp_mons[i]]=0

    def b1(self,h):#attack by second weapon by h heading
        itdic=['|',')','/',']',' ']
        if self.hp>0:
            xp,yp=angle(h)
            t=[]
            for i in range(self.b1_attack_range+self.equip[1].plrange):
                if globals1.FACE[self.l][self.y+yp*(i+1)][self.x+xp*(i+1)] in globals1.ALPHABET:
                    t.append((self.x+xp*(i+1),self.y+yp*(i+1)))
                    break
                else:
                    if not(globals1.FACE[self.l][self.y+yp*(i+1)][self.x+xp*(i+1)] in itdic): break

            temp_mons_ind=self.find_items_ahead(0,(xp,yp),(self.a1_attack_range+self.equip[0].plrange))
            counter=0
            temp_mons=[]
            for i in range(len(temp_mons_ind)):
                it=globals1.MONSTERS[temp_mons_ind[i]]
                if (it.x,it.y) in t:
                    counter+=1
                    temp_mons.append(temp_mons_ind[i])
                    if counter == len(t):
                        break

            for i in range(len(temp_mons)):
                it=globals1.MONSTERS[temp_mons[i]]
                if self.equip[1]!=0:
                    t5=randint(self.equip[1].platk+self.batk,2+self.equip[1].platk+self.batk)
                else: t5=randint(0+self.batk,2+self.batk)
                it.hp-=t5
                #self.get_xp(t5,0)
                print(self.name+' hit by '+self.equip[1].name+' >> '+it.name+' by '+str(t5)+' hp '+str(z(it.hp))+'/'+str(z(it.mhp)))
                if it.hp<=0:
                    cell_p=it.cellp
                    globals1.FACE[self.l][it.y][it.x]=' '
                    print(self.name+' killed '+it.name)
                    ta,tb=it.mhp,it.atk
                    self.get_xp(ta,tb)
                    txp=ta+int(sqrt(ta+tb))
                    print('acquired '+str(txp)+' xp')
                    globals1.ITEM_GRID[self.l][cell_p[1]][cell_p[0]][0].remove(temp_mons[i])
                    globals1.MONSTERS[temp_mons[i]]=0

    def g1(self,h):#pick up item from floor
        itdic=['|',')','/',']']
        if self.hp>0:
            x1,y1=angle(h)
            if globals1.FACE[self.l][self.y+y1][self.x+x1] in itdic:
                temp_items_ind=self.find_items_ahead(1,(x1,y1),1)
                temp_items=[]
                for i in range(len(temp_items_ind)):
                    it=globals1.ITEMS[temp_items_ind[i]]
                    #print(it.name,it.x,it.y,it.cellp)
                    if (it.x,it.y) == (self.x+x1,self.y+y1):
                        temp_items.append(temp_items_ind[i])
                for i in range(len(temp_items)):
                    it=globals1.ITEMS[temp_items[i]]
                    self.bag.append(it)
                    globals1.ITEMS[temp_items[i]]=0
                    globals1.FACE[self.l][it.y][it.x]=' '
                    globals1.ITEM_GRID[self.l][it.cellp[1]][it.cellp[0]][1].remove(it.num)
                    it.name=it.name+'+'+str(it.platk)
                    print('acquired '+it.name)

    def climb(self):
        st=['I','+',':']
        if self.hp>0:
            if self.floor in st:
                temp_st_ind=self.find_items_around(2,0)
                down=None
                up=None
                for i in range(len(temp_st_ind)):
                    tst=globals1.STAIRS[temp_st_ind[i]]
                    if tst.p1==(self.x,self.y,self.l):
                        if tst.p2[2]-tst.p1[2]==1:
                            if down==None:
                                down=(tst,1)
                        elif tst.p2[2]-tst.p1[2]==-1:
                            if up==None:
                                up=(tst,1)
                    if tst.p2==(self.x,self.y,self.l):
                        if tst.p1[2]-tst.p2[2]==1:
                            if down==None:
                                down=(tst,2)
                        elif tst.p1[2]-tst.p2[2]==-1:
                            if up==None:
                                up=(tst,2)
                if up!=None and down!=None:
                    a=input('climb 1>up 2>down? >>> ')
                    if a !='c':
                        if a in ['1','2']:
                            if a=='1':
                                if up[1]==1:
                                    self.tp(up[0].p2)
                                elif up[1]==2:
                                    self.tp(up[0].p1)
                            if a=='2':
                                if down[1]==1:
                                    self.tp(down[0].p2)
                                elif down[1]==2:
                                    self.tp(down[0].p1)
                        else:
                            print('wrong key, please retry')
                            self.whattodo(False)
                            return(0)
                    else:
                        print('action canceled')
                        return(0)
                elif up!=None:
                    a=input('climb 1>up? >>> ')
                    if a !='c':
                        if a=='1':
                            if up[1]==1:
                                self.tp(up[0].p2)
                            elif up[1]==2:
                                self.tp(up[0].p1)
                        else:
                            print('wrong key, please retry')
                            self.whattodo(False)
                            return(0)
                    else:
                        print('action canceled')
                        return(0)
                elif down!=None:
                    a=input('climb 1>down? >>> ')
                    if a !='c':
                        if a=='1':
                            if down[1]==1:
                                self.tp(down[0].p2)
                            elif down[1]==2:
                                self.tp(down[0].p1)
                        else:
                            print('wrong key, please retry')
                            self.whattodo(False)
                            return(0)
                    else:
                        print('action canceled')
                        return(0)

    def e1(self):#equip item from bag
        if len(self.bag)>0:
            for i in range(len(self.bag)):
                print(str(i+1)+'> '+self.bag[i].name)
            print('choose number of item you want to equip')
            a1=input('>>>')
            if a1 !='c':
                try:
                    a1=int(a1)-1
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
            else:
                print('action canceled')
                return(0)
            try:
                it=self.bag[a1]
            except:
                print('wrong key, please retry')
                self.whattodo(False)
                return(0)
            self.bag.remove(it)
            if self.equip[it.typ]!=0:
                it12=self.equip[it.typ]
                self.bag.append(it12)
                self.equip[it.typ]=it
            else:
                self.equip[it.typ]=it
            print('equipped '+it.name)
        else:
            print('there is nothing to equip')

    def t1(self):#throw away item from bag
        if len(self.bag)>0:
            for i in range(len(self.bag)):
                print(str(i+1)+'> '+self.bag[i].name)
            print('choose number of item you want to throw away')
            a1=input('>>>')
            if a1 !='c':
                try:
                    a1=int(a1)-1
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
            else:
                print('action canceled')
                return(0)
            try:
                item_t=self.bag[a1]
            except:
                print('wrong key, please retry')
                self.whattodo(False)
                return(0)
            t14=input('Are you sure(item will be lost), y/n ?')
            if t14=='y':
                self.bag.remove(item_t)
                print(item_t.name+' was trowed')
                print(item_t.name+' broke out')
            else:
                print('action canceled')
        else:
            print('there is nothing to throw')

    def save(self):
        a=input('choose number of save (1..5) ...')
        sl.save(a)

    def load(self):
        a=input('choose number of save (1..5) ...')
        sl.load(a)

    def draw_view(self,vx,vy):
        x1=z(self.x-vx)
        y1=z(self.y-vy)
        x2=self.x+vx
        y2=self.y+vy
        print(' ')
        if x2>=len(globals1.FACE[self.l][0]):
            x2=len(globals1.FACE[self.l][0])
        if y2>=len(globals1.FACE[self.l]):
            y2=len(globals1.FACE[self.l])
        for i in range(y1,y2):
            p=''
            for j in range(x1,x2):
                p+=globals1.FACE[self.l][i][j]
            print(p)
        print(' ')

    def except_view(self,vx,vy):
        globals1.C.fill((144,144,171))
        x1=z(self.x-vx)
        y1=z(self.y-vy)
        x2=self.x+vx
        y2=self.y+vy
        m=2# additional border of view
        m1=2
        if x2>=len(globals1.FACE[self.l][0]):
            x2=len(globals1.FACE[self.l][0])
        if y2>=len(globals1.FACE[self.l]):
            y2=len(globals1.FACE[self.l])
        roo=globals1.R_GRID[self.l][self.rpos[1]][self.rpos[2]]

        if roo.vis==0:
            roo.vis=1
            globals1.MAP[self.l][self.rpos[1]*2][self.rpos[2]*2]='#'
            if self.rpos[1]!=self.prev_rpos[1]:
                globals1.MAP[self.l][self.rpos[1]*2+(self.prev_rpos[1]-self.rpos[1])][self.rpos[2]*2]='|'

            if self.rpos[2]!=self.prev_rpos[2]:
                globals1.MAP[self.l][self.rpos[1]*2][self.rpos[2]*2+(self.prev_rpos[2]-self.rpos[2])]='-'

            if self.rpos[0]<self.prev_rpos[0]:
                if globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]in ['#',' ']:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]=':'
                else:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='I'
                if globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]in ['#',' ']:
                    globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='+'
                else:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='I'

            if self.rpos[0]>self.prev_rpos[0]:
                if globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]in ['#',' ']:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='+'
                else:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='I'
                if globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]in ['#',' ']:
                    globals1.MAP[self.rpos[0]][self.rpos[1]*2][self.rpos[2]*2]=':'
                else:
                    globals1.MAP[self.prev_rpos[0]][self.rpos[1]*2][self.rpos[2]*2]='I'
        p12=[]
        for i in range(y2-y1):
            p12.append([])
            for j in range(x2-x1):
                p12[i].append(' ')
        for i in range(y1,y2):
            for j in range(x1,x2):
                if (j>=z(roo.x1-m) and j<=roo.x2+m) and (i>=z(roo.y1-m) and i<=roo.y2+m):
                    if globals1.FACE[self.l][i][j]!=' ':
                        p12[i-y1][j-x1]=globals1.FACE[self.l][i][j]
                    else:
                        p12[i-y1][j-x1]='.'
                    fg2=1
                if (j>=z(self.x-m1) and j<=self.x+m1) and (i>=z(self.y-m1) and i<=self.y+m1):
                    if globals1.FACE[self.l][i][j]!=' ':
                        p12[i-y1][j-x1]=globals1.FACE[self.l][i][j]
                    else:
                        p12[i-y1][j-x1]='.'
        for i in range(len(p12)):
            for j in range(len(p12[i])):
                if p12[i][j] in ['#','.','+',':','I']:
                    if p12[i][j]=='#':
                        globals1.C.blit(globals1.field_tiles[1],(j*48,i*48))
                    if p12[i][j]=='.':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                    if p12[i][j]=='+':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.field_tiles[2],(j*48,i*48))
                    if p12[i][j]==':':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.field_tiles[3],(j*48,i*48))
                    if p12[i][j]=='I':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.field_tiles[4],(j*48,i*48))
                if p12[i][j] in globals1.ALPHABET:
                    globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                    globals1.C.blit(globals1.live_tiles[1],(j*48,i*48))
                if p12[i][j] in [')','|','/',']']:
                    if p12[i][j]==')':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.item_tiles[0],(j*48,i*48))
                    if p12[i][j]==']':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.item_tiles[1],(j*48,i*48))
                    if p12[i][j]=='/':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.item_tiles[2],(j*48,i*48))
                    if p12[i][j]=='|':
                        globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                        globals1.C.blit(globals1.item_tiles[3],(j*48,i*48))
                if p12[i][j]=='@':
                    globals1.C.blit(globals1.field_tiles[0],(j*48,i*48))
                    globals1.C.blit(globals1.live_tiles[0],(j*48,i*48))
        map=self.show_map(4,4)
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j]=='#':
                    globals1.C.blit(globals1.map_tiles[0],(j*16+48*16,i*16))
                if map[i][j]=='|':
                    globals1.C.blit(globals1.map_tiles[4],(j*16+48*16,i*16))
                if map[i][j]=='-':
                    globals1.C.blit(globals1.map_tiles[5],(j*16+48*16,i*16))
                if map[i][j]=='+':
                    globals1.C.blit(globals1.map_tiles[1],(j*16+48*16,i*16))
                if map[i][j]==':':
                    globals1.C.blit(globals1.map_tiles[2],(j*16+48*16,i*16))
                if map[i][j]=='I':
                    globals1.C.blit(globals1.map_tiles[3],(j*16+48*16,i*16))
                if map[i][j]=='@':
                    globals1.C.blit(globals1.map_tiles[7],(j*16+48*16,i*16))
        globals1.C.blit(globals1.map_tiles[6],(48*16,0))
        globals1.disp.update()
    def show_map(self,vx,vy):
        x1=z(self.rpos[2]*2-vx)
        y1=z(self.rpos[1]*2-vy)
        if self.rpos[2]*2-vx<0:
            x2=2*vx
        else:
            x2=self.rpos[2]*2+vx
        if self.rpos[1]*2-vx<0:
            y2=2*vy
        else:
            y2=self.rpos[1]*2+vy

        y2=self.rpos[1]*2+vy
        if x2>=len(globals1.MAP[self.l][0]):
            x2=len(globals1.MAP[self.l][0])
        if y2>=len(globals1.MAP[self.l]):
            y2=len(globals1.MAP[self.l])
        p=[]
        for i in range(y1,y2):
            p.append('')
            for j in range(x1,x2):
                if i==self.rpos[1]*2 and j==self.rpos[2]*2:
                    p[i-y1]+='@'
                else:
                    p[i-y1]+=globals1.MAP[self.l][i][j]
        return(p)
    def whattodo(self,fg):
        print(' ')
        key=1#keybilding
        if fg:
            self.except_view(8,8)
        a=str(input('turn n'+str(globals1.K2)+'>'))
        if self.hp>0:

            if a=='':
                self.wait()
            elif a in [['6','8','4','2'],['1','2','3','4']][key]:
                try:
                    a=chnum(a,key)
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
                self.go(a)
            elif a[0]=='a':
                try:
                    a=chnum(a[1],key)
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
                self.a1(a)
            elif a[0]=='b':
                try:
                    a=chnum(a[1],key)
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
                self.b1(a)
            elif a[0]=='g':
                try:
                    a=chnum(a[1],key)
                except:
                    print('wrong key, please retry')
                    self.whattodo(False)
                    return(0)
                self.g1(a)
            elif a[0]=='e':
                self.e1()
            elif a[0]=='t':
                self.t1()
            elif a=='cl':
                self.climb()
            elif a=='save':
                self.save()
            elif a=='load':
                self.load()
            elif a=='help':
                f1=open('Help.txt','r')
                print(f1.read())
                input('press enter to continue')
            else:
                print('wrong key, please retry')
                self.whattodo(False)
                return(0)
            print('')
def angle(n):
    if n==0:
        return(1,0)
    elif n==1:
        return(0,-1)
    elif n==2:
        return(-1,0)
    elif n==3:
        return(0,1)

def dist(p,w):
    x=p.x-w.x
    y=p.y-w.y
    d=sqrt(x**2+y**2)
    return((d,x,y))

def z(x):
    if x<0: return(0)
    else: return(x)

def chnum(a,i):
    if a==['6','1'][i]:
        a=0
    if a==['8','2'][i]:
        a=1
    if a==['4','3'][i]:
        a=2
    if a==['2','4'][i]:
        a=3
    return(a)
def draw_face():
    for u in range(len(globals1.FACE)):
        print()
        for i in range(len(globals1.FACE[u])):
            l=''
            for j in range(len(globals1.FACE[u][i])):
                l+=globals1.FACE[u][i][j]
            print(l)
