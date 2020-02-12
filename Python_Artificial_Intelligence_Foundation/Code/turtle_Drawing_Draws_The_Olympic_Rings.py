import turtle as t
color=['blue','black','red','yellow','green']
t.width(10)
for i in range(3):
    t.color(color[i])
    t.penup()
    t.goto(120 * i, 0)
    t.pendown()
    t.circle(50)
for i in range(3,5):
    t.color(color[i])
    t.penup()
    t.goto(60+120*(i-3),-50)
    t.pendown()
    t.circle(50)
    
    t.showturtle()

