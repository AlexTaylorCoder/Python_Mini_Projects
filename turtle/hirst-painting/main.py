import colorgram
import turtle
import tkinter as TK

r = 50
colors = colorgram.extract('hirst.jpg',25)
rgb_colors = []
for color in colors:
    r = color.rgb.r
    g = color.rgb.g
    b = color.rgb.b
    rgb_colors.append((r,b,g))
print(rgb_colors)

def draw():
    t = turtle.Turtle()
    turtle.colormode(255)
    for i,points in enumerate(rgb_colors):
        t.pu()
        t.speed(0)
        if i % 5 == 0:
            print("ran")
            t.backward(250)
            t.right(90)
            t.forward(50)
            t.left(90)
        t.color(points)
        t.forward(50)
        t.pd()
        t.circle(10)


draw()


        