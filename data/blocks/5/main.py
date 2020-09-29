from data.blocks.api import changeMap

def onCollide(**kwargs):
    changeMap("data/map1.dat", kwargs["player"],300,300,kwargs["blocks"])