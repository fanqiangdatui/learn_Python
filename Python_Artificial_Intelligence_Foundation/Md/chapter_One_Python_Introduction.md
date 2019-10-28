#7、海龟绘图坐标系问题
import  turtle as t  
t.showturtle()  #显示箭头  
t.showturtle()  #显示箭头  
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
![turtle_Foundation](https://github.com/fanqiangdatui/image/blob/master/Snipaste_2019-10-28_19-56-41.png)
#8、海龟绘图画出奥运五环       
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
![turtle_Olympic_Rings](https://github.com/fanqiangdatui/image/blob/master/Snipaste_2019-10-28_20-31-33.png)




