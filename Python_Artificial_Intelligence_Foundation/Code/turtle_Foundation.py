import  turtle as t
t.showturtle()  #显示箭头
t.width(10) #画笔宽度
t.write('狗杂真好吃')    #写字符串
t.forward(300)  #前进300像素
t.color('red')  #画笔颜色改为red
t.left(90)  #箭头左转90度
t.forward(300)
t.goto(0,50)    #去坐标(0,50)
t.penup()   #抬笔，路径不可见
t.goto(0,300)
t.pendown() #落笔，路径可见
t.circle(100)
t.color('green')