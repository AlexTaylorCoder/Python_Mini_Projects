import turtle
from random import randint

width = 500 
height = 400
padding = 70
s = turtle.Screen()
s.setup(width,height)
bet = s.textinput(title="Bet",prompt="Choose a turtle to bet on")
colors = ["red","blue","green"]
winner = ""
turtles = []
for i,color in enumerate(colors):
    t = turtle.Turtle("turtle")
    t.pu()
    t.color(color)
    t.goto(-(width // 2) + padding, (-(height // 2) + (i * 30)) + padding)
    turtles.append(t)

racing = True
while racing:
    for i,t in enumerate(turtles):
        if t.xcor() > (width // 2) - padding:
            winner = colors[i]
            racing = False
        t.forward(randint(10,20))


print(winner)
if bet == winner:
    print("You are correct!")
else:
    print("You have lost!")