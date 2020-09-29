from game import loadMap

def changeMap(file, player, x, y,blocks):
    loadMap(file,blocks)
    player.setX(x)
    player.setY(y)