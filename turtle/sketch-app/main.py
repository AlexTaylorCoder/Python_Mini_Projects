import turtle


t = turtle.Turtle()
s = turtle.Screen()
t.speed(9)

rotate = 0



s.listen()
s.onkey(lambda: t.forward(10),"w")
s.onkey(lambda: t.backward(10),"s")
s.onkey(lambda: t.setheading(-10 + t.heading()),"a")
s.onkey(lambda: t.setheading(10 + t.heading()),"d")
s.onkey(lambda: t.clear(),"c")


s.exitonclick()