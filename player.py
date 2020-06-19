import math, pygame
from block import Block
from map import Map

class Player:
    def __init__(self, speed:float, mapP:Map, blocks:list):
        self.px=mapP.getPlayerX()
        self.py=mapP.getPlayerY()
        self.speed=speed
        self.pa=0
        self.pdx=math.sin(self.pa)*speed
        self.pdy=math.cos(self.pa)*speed
        self.pdsidex=math.cos(-self.pa)*speed
        self.pdsidey=math.sin(-self.pa)*speed
        #self.mapX=mapP.getMapX()
        #self.mapY=mapP.getMapY()
        self.map=mapP
        self.blocks=blocks
    def getPos(self)->tuple:
        return (self.py, self.px)
    def getX(self)->float:
        return self.getPos()[0]
    def getY(self)->float:
        return self.getPos()[1]
    def getPlayerAngle(self)->float:
        return self.pa
    def movePlayer(self, keys:tuple, locked:bool,clock):
        deltaMousePos=pygame.mouse.get_rel()
        if locked:
            self.pa+=deltaMousePos[0]*0.2*(clock.get_time()/1000)
            if self.pa<0:
                self.pa+=2*math.pi
            if self.pa>2*math.pi:
                self.pa-=2*math.pi
            self.pdx=math.sin(self.pa)*self.speed*(clock.get_time()/1000)
            self.pdy=math.cos(self.pa)*self.speed*(clock.get_time()/1000)
            self.pdsidex=math.cos(-self.pa)*self.speed*(clock.get_time()/1000)
            self.pdsidey=math.sin(-self.pa)*self.speed*(clock.get_time()/1000)


        if keys[pygame.K_d]:
            nextX=int(self.px+self.pdsidex)>>6
            nextY=int(self.py+self.pdsidey)>>6
            prevX=int(self.px-self.pdsidex)>>6
            prevY=int(self.py-self.pdsidey)>>6
            if not self.collide(nextX, nextY, prevX, prevY):
                self.px+=self.pdsidex
                self.py+=self.pdsidey
        if keys[pygame.K_a]:
            nextX=int(self.px-self.pdsidex)>>6
            nextY=int(self.py-self.pdsidey)>>6
            prevX=int(self.px+self.pdsidex)>>6
            prevY=int(self.py+self.pdsidey)>>6
            if not self.collide(nextX, nextY, prevX, prevY):
                self.px-=self.pdsidex
                self.py-=self.pdsidey

        if keys[pygame.K_w]:
            nextX=int(self.px+self.pdx)>>6
            nextY=int(self.py+self.pdy)>>6
            prevX=int(self.px-self.pdx)>>6
            prevY=int(self.py-self.pdy)>>6
            if not self.collide(nextX, nextY, prevX, prevY):
                self.px+=self.pdx
                self.py+=self.pdy
        if keys[pygame.K_s]:
            nextX=int(self.px-self.pdx)>>6
            nextY=int(self.py-self.pdy)>>6
            prevX=int(self.px+self.pdx)>>6
            prevY=int(self.py+self.pdy)>>6
            if not self.collide(nextX, nextY, prevX, prevY):
                self.px-=self.pdx
                self.py-=self.pdy

    def collide(self, nextY, nextX, prevY, prevX)->bool:
        nextMp=nextY*self.map.getMapX()+nextX
        prevMp=prevY*self.map.getMapX()+prevX
        x=int(self.px)>>6
        y=int(self.py)>>6
        mp=x*self.map.getMapX()+y
        if self.map.isValidPosition(nextMp):
            block=Block()
            if self.map.isValidBlock(nextMp):
                block=self.map.getBlock(nextMp)
                block.onCollision({"mp":nextMp,"map":self.map, "block":block, "blocks":self.blocks})
            if self.map.getBlockID(nextMp)==0 or not block.isCollidable():
                return False
        return True
if __name__=="__main__":
    raise Exception("You buffoon, use raycast.py")