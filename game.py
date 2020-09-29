import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import math
from block import Block
from player import Player
import importlib
from map import Map

def getBlockData():
    folders=[]
    for folder in os.walk("data/blocks"):
        foldername=folder[0][12:]
        if foldername.isnumeric():
            if "block.dat" in folder[2]:
                folders.append(int(foldername))
    folders.sort()
    folders=[str(folder) for folder in folders]
    for folder in folders:
        with open("data/blocks/"+folder+"/block.dat", "r") as f:
            name=f.readline().strip().lower()
            vColorString=f.readline().strip().split(",")
            hColorString=f.readline().strip().split(",")
            vColor=tuple(float(i)*255 for i in vColorString)
            hColor=tuple(float(i)*255 for i in hColorString)
            collidableString=f.readline().strip()
            collidable=bool(int(collidableString))
            f=None
            if os.path.exists("data/blocks/"+folder+"/main.py"):
                with open("data/blocks/"+folder+"/__init__.py", "w") as f:
                    pass
                f=importlib.import_module("data.blocks."+folder+".main")
                print("Found script for block: "+name+" id: "+folder)
            block=Block(int(folder),vColor, hColor, collidable)
            if f != None:
                if hasattr(f, "onCollide"):
                    block.setOnCollision(f.onCollide)
                if hasattr(f, "onLeave"):
                    block.setOnLeave(f.onLeave)
            #blocks.append(block)
            blocks.update({name:block})


def drawMap():
    for x in range(mapX):
        for y in range(mapY):
            color=BLACK
            if(mapP[y*mapX+x]>0):
                color=WHITE
            pygame.draw.rect(screen, color, pygame.Rect(x*mapS+1,y*mapS+1,mapS-1,mapS-1))

def drawPlayer():
    pygame.draw.line(screen, YELLOW, pygame.math.Vector2(px+4,py+4), pygame.math.Vector2(px+pdx*5+4, py+pdy*5+4), 3)
    pygame.draw.rect(screen, YELLOW, pygame.Rect(px,py,8,8))

def dist(ax: float, ay: float, bx: float, by: float, ang: float):
    return math.sqrt((bx-ax)*(bx-ax)+(by-ay)*(by-ay))

def drawRays():
    mx,my,mp,dof,mv,mh=0,0,0,0,0,0
    rx,ry,xo,yo,disT=0.0,0.0,0.0,0.0,0.0
    maxDof=32
    ra=player.getPlayerAngle()-math.radians(35)
    if ra <0:
        ra+=2*math.pi
    if ra > 2*math.pi:
        ra-=2*math.pi
    pygame.draw.rect(screen, ceilingColor, pygame.Rect(0,0,width,height/2))
    pygame.draw.rect(screen, floorColor, pygame.Rect(0,height/2,width,height))
    for r in range(70):
        dof=0
        disH=1000000000
        hx=player.getX()
        hy=player.getY()
        aTan=-1/math.tan(ra)
        if ra > math.pi:
            ry=((int(player.getY())>>6)<<6)-0.0001
            rx=(player.getY()-ry)*aTan+player.getX()
            yo=-64
            xo=-yo*aTan
        if ra < math.pi:
            ry=((int(player.getY())>>6)<<6)+64
            rx=(player.getY()-ry)*aTan+player.getX()
            yo=64
            xo=-yo*aTan
        if ra==0 or ra==math.pi:
            rx=player.getX();
            ry=player.getY();
            dof=maxDof;
        while dof < maxDof:
            mx=int(rx/64)
            my=int(ry/64)
            mp=my*mapT.getMapX()+mx
            if mp >= 0 and mp<mapT.getMapX()*mapT.getMapY() and mapT.getBlockID(mp)>0:
                mh=mapT.getBlockID(mp)
                hx=rx
                hy=ry
                disH=dist(player.getX(),player.getY(),hx,hy,ra)
                dof=maxDof
            else:
                rx+=xo
                ry+=yo
                dof+=1

        #Vertical
        dof=0
        disV=1000000000
        vx=player.getX()
        vy=player.getY()
        nTan=-math.tan(ra)
        if ra > P2 and ra < P3:
            rx=((int(player.getX())>>6)<<6)-0.0001
            ry=(player.getX()-rx)*nTan+player.getY()
            xo=-64
            yo=-xo*nTan
        if ra < P2 or ra > P3:
            rx=((int(player.getX())>>6)<<6)+64
            ry=(player.getX()-rx)*nTan+player.getY()
            xo=64
            yo=-xo*nTan
        if ra==0 or ra==math.pi:
            rx=player.getX();
            ry=player.get();
            dof=maxDof;
        while dof < maxDof:
            mx=int(rx/64)
            my=int(ry/64)
            mp=my*mapT.getMapX()+mx
            if mp >= 0 and mp<mapT.getMapX()*mapT.getMapY() and mapT.getBlockID(mp)>0:
                mv=mapT.getBlockID(mp)
                vx=rx
                vy=ry
                disV=dist(player.getX(),player.getY(),vx,vy,ra)
                dof=maxDof
            else:
                rx+=xo
                ry+=yo
                dof+=1

        color=BLACK
        if disV<disH:
            rx=vx
            ry=vy
            mp=(int(ry)>>6)*mapT.getMapX()+(int(rx)>>6)
            disT=disV
            color=BLACK
            if mv>=0 and mv<len(blocks):
                block: Block=mapT.getBlock(mp)
                color=block.getVColor()
        if disV>disH:
            rx=hx
            ry=hy
            mp=(int(ry)>>6)*mapT.getMapX()+(int(rx)>>6)
            disT=disH
            color=BLACK
            if mh>=0 and mh<len(blocks):
                block: Block=mapT.getBlock(mp)
                color=block.getHColor()
        #pygame.draw.line(screen, color, pygame.math.Vector2(player.getX()+4,player.getY()+4), pygame.math.Vector2(rx,ry),3)

        ca=player.getPlayerAngle()-ra
        if ca < 0:
            ca+=2*math.pi
        if ca > 2*math.pi:
            ca-=2*math.pi
        disT=disT*math.cos(ca)
        if disT==0:
            disT+=0.000000001
        maxLineHeight=height
        lineH=(mapT.getMapS()*maxLineHeight)/disT
        if lineH>maxLineHeight: lineH=maxLineHeight
        lineO=int((maxLineHeight/2)-lineH/2)
        lineWidth=int((width+20)/70)
        #pygame.draw.line(screen, floorColor, pygame.math.Vector2(r*lineWidth+(lineWidth),height), pygame.math.Vector2(r*lineWidth+(lineWidth),lineO+lineH), lineWidth)
        #pygame.draw.line(screen, ceilingColor, pygame.math.Vector2(r*lineWidth+(lineWidth),0), pygame.math.Vector2(r*lineWidth+(lineWidth),lineO), lineWidth)
        pygame.draw.line(screen, color, pygame.math.Vector2(r*lineWidth+8,lineO), pygame.math.Vector2(r*lineWidth+8,lineO+lineH),lineWidth)

        ra+=math.radians(1)
        if ra < 0:
            ra+=2*math.pi
        if ra > 2*math.pi:
            ra-=2*math.pi


floorColor=(0,0,0)
ceilingColor=(0,0,0)
player=None
mapT=None

def loadMap(file,blocks):
    global player, mapT, floorColor, ceilingColor
    mapT=Map(file,blocks)
    floorColor=mapT.getFloorColor()
    ceilingColor=mapT.getCeilingColor()
    if player is None:
        player=Player(150,mapT,blocks)
    else:
        player.updateMap(mapT)

if __name__=="__main__":
    pygame.init()
    pygame.font.init()
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    GREY=(132,132,132)

    P2=math.pi/2
    P3=3*math.pi/2

    width=1260
    height=720

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    screen=pygame.display.set_mode([width,height])
    pygame.display.set_caption("Game")

    done=False
    clock=pygame.time.Clock()

    blocks={"air":Block(collidable=False)}
    getBlockData()
    #mapT=Map("data/map.dat",blocks)
    loadMap("data/map.dat",blocks)
    #player=Player(150,mapT,blocks)
    locked=False

    myfont = pygame.font.SysFont('Arial', 30)

    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    locked=not locked
                    pygame.mouse.set_visible(not locked)
                    pygame.event.set_grab(locked)

        screen.fill(GREY)

        keys=pygame.key.get_pressed()

        #movePlayer(keys)
        player.movePlayer(keys,locked,clock)

        #drawMap()
        drawRays()
        #drawPlayer()
        textsurface = myfont.render("X: "+"{0:.2f}".format(player.getX())+" Y: "+"{0:.2f}".format(player.getY()), True, (0, 0, 0))
        screen.blit(textsurface,(0,0))

        pygame.display.flip()

        clock.tick(60)

    pygame.font.quit()
    pygame.quit()