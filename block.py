class Block:
    def __init__(self, id:int=0, vcolor=(0,0,0,0), hcolor=(0,0,0,0), collidable:bool=True):
        self.vcolor=vcolor
        self.hcolor=hcolor
        self.id=id
        self.collidable=collidable
        self.onCollideFunc=()
        self.onLeaveFunc=()
    def createNew(self):
        block=Block(self.id,self.vcolor,self.hcolor,self.collidable)
        block.setOnCollision(self.onCollideFunc)
        block.setOnLeave(self.onLeaveFunc)
        return block
    def getVColor(self):
        return self.vcolor
    def getHColor(self):
        return self.hcolor
    def isCollidable(self)->bool:
        return self.collidable
    def getID(self)->int:
        return self.id
    def setOnCollision(self, func):
        self.onCollideFunc=func
        return self
    def getOnCollision(self):
        return self.onCollideFunc
    def setOnLeave(self, func):
        self.onLeaveFunc=func
        return self
    def onCollision(self, kwargs):
        if self.onCollideFunc!=():
            self.onCollideFunc(**kwargs)
    def onLeave(self, kwargs):
        if self.onLeaveFunc!=():
            self.onLeaveFunc(**kwargs)