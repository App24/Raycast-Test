from data.blocks.api import changeMap
from block import Block

def onCollide(**kwargs):
    changeMap(kwargs["mp"], kwargs["map"], Block(kwargs["block"].getID(),kwargs["block"].getHColor(),kwargs["block"].getVColor(),kwargs["block"].isCollidable()))