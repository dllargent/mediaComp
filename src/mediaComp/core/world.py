
def makeWorld(width=None, height=None):
    if(width and height):
        w = World(width, height)
    else:
        w = World()
    return w


def getTurtleList(world):
    if not isinstance(world, World):
        print("getTurtleList(world): Input is not a world")
        raise ValueError
    return world.getTurtleList()