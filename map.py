from block import Block

class Map:
    def __init__(self, file, blocks):
        self._loadMap(file, blocks)
        self.mapS=64
    def _loadMap(self, file, blocks):
        with open(file, "r") as f:
            self.blocks=blocks
            size=f.readline().strip()
            self.mapX=int(size.split(",")[0])
            self.mapY=int(size.split(",")[1])
            playerPos=f.readline().strip()
            self.px=float(playerPos.split(",")[0])
            self.py=float(playerPos.split(",")[1])
            ceilingColorString=f.readline().strip().split(",")
            floorColorString=f.readline().strip().split(",")
            self.floorColor=tuple(float(i)*255 for i in floorColorString)
            self.ceilingColor=tuple(float(i)*255 for i in ceilingColorString)
            self.map=[]
            for y in range(self.mapY):
                yString=f.readline().strip()
                yBlocks=yString.split(",")
                if yBlocks[len(yBlocks)-1]=='':
                    yBlocks=yBlocks[:len(yBlocks)-1]
                if len(yBlocks)<self.mapX:
                    for x in range(self.mapX-len(yBlocks)):
                        yBlocks.append("1")
                for block in yBlocks[:self.mapX]:
                    if not block.isnumeric():
                        block="1"
                    self.map.append(list(blocks.values())[int(block)].createNew())
    def getPlayerPos(self)->tuple:
        return (self.px, self.py)
    def getPlayerX(self)->float:
        return self.getPlayerPos()[0]
    def getPlayerY(self)->float:
        return self.getPlayerPos()[1]
    def getSize(self)->tuple:
        return (self.mapX, self.mapY)
    def getMapX(self)->int:
        return self.getSize()[0]
    def getMapY(self)->int:
        return self.getSize()[1]
    def getFloorColor(self)->tuple:
        return self.floorColor
    def getCeilingColor(self)->tuple:
        return self.ceilingColor
    def getBlock(self, mp)->Block:
        return self.map[mp]
    def getBlockAtPosition(self, x, y)->Block:
        return self.getBlock(y*self.mapX+x)
    def getBlockID(self, mp)->int:
        return self.getBlock(mp).getID()
    def getMapS(self)->int:
        return self.mapS
    def updateMap(self, *args):
        if len(args)==2:
            self.map[args[0]]=args[1]
        elif len(args)==3:
            self.map[args[1]*self.mapX+args[0]]=args[2]
    def getMap(self)->list:
        return self.map
    def isValidPosition(self, mp):
        return (mp >=0 and mp < self.mapX*self.mapY)
    def isValidBlock(self, mp):
        return (self.getBlockID(mp)>=0 and self.getBlockID(mp)<len(self.blocks))

if __name__=="__main__":
    raise Exception("You buffoon, use raycast.py")