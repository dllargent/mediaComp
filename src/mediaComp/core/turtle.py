from ..models.Picture import Picture
from turtle import Turtle

def turn(turtle, degrees=90) -> None:
    if not isinstance(turtle, Turtle):
        print("turn(turtle[, degrees]): Input is not a turtle")
        raise ValueError
    else:
        turtle.turn(degrees)


def turnRight(turtle) -> None:
    if not isinstance(turtle, Turtle):
        print("turnRight(turtle): Input is not a turtle")
        raise ValueError
    else:
        turtle.turnRight()


def turnToFace(turtle, x, y=None) -> None:
    if y == None:
        if not (isinstance(turtle, Turtle) and isinstance(x, Turtle)):
            print("turnToFace(turtle, turtle): First input is not a turtle")
            raise ValueError
        else:
            turtle.turnToFace(x)
    else:
        if not isinstance(turtle, Turtle):
            print("turnToFace(turtle, x, y): Input is not a turtle")
            raise ValueError
        else:
            turtle.turnToFace(x, y)


def turnLeft(turtle) -> None:
    if not isinstance(turtle, Turtle):
        print("turnLeft(turtle): Input is not a turtle")
        raise ValueError
    else:
        turtle.turnLeft()


def forward(turtle, pixels=100) -> None:
    if not isinstance(turtle, Turtle):
        print("forward(turtle[, pixels]): Input is not a turtle")
        raise ValueError
    else:
        turtle.forward(pixels)


def backward(turtle, pixels=100) -> None:
    if not isinstance(turtle, Turtle):
        print("backward(turtle[, pixels]): Input is not a turtle")
        raise ValueError
    if (None == pixels):
        turtle.backward()
    else:
        turtle.backward(pixels)


def moveTo(turtle, x, y) -> None:
    if not isinstance(turtle, Turtle):
        print("moveTo(turtle, x, y): Input is not a turtle")
        raise ValueError
    turtle.moveTo(x, y)


def makeTurtle(world) -> Turtle:
    if not (isinstance(world, World) or isinstance(world, Picture)):
        print("makeTurtle(world): Input is not a world or picture")
        raise ValueError
    turtle = Turtle(world)
    return turtle


def penUp(turtle) -> None:
    if not isinstance(turtle, Turtle):
        print("penUp(turtle): Input is not a turtle")
        raise ValueError
    turtle.penUp()


def penDown(turtle) -> None:
    if not isinstance(turtle, Turtle):
        print("penDown(turtle): Input is not a turtle")
        raise ValueError
    turtle.penDown()


def drop(turtle, picture) -> None:
    if not isinstance(turtle, Turtle):
        print("drop(turtle, picture): First input is not a turtle")
        raise ValueError
    if not isinstance(picture, Picture):
        print("drop(turtle, picture): Second input is not a picture")
        raise ValueError
    turtle.drop(picture)

def getXPos(turtle) -> int:
    if not isinstance(turtle, Turtle):
        print("getXPos(turtle): Input is not a turtle")
        raise ValueError
    return turtle.getXPos()


def getYPos(turtle) -> int:
    if not isinstance(turtle, Turtle):
        print("getYPos(turtle): Input is not a turtle")
        raise ValueError
    return turtle.getYPos()


def getHeading(turtle) -> int:
    if not isinstance(turtle, Turtle):
        print("getHeading(turtle): Input is not a turtle")
        raise ValueError
    return turtle.getHeading()