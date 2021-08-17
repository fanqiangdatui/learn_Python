# -*- coding: utf-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import ttk
import restfultest
import time
w = tk.Tk()  # 实例化object，建立窗口w
w.wm_attributes('-topmost',1)
w.title('适用VCN所有形态')  # 给窗口起名字
w.geometry('280x400+0+100')  # 设定窗口大小
var0 = tk.StringVar()
Entry_0 = tk.Entry(w, textvariable=var0, show=None, font=('微软雅黑', 8))
Entry_0.grid(row=1, column=2, sticky=tk.E + tk.W, padx=3, pady=3)

var1 = tk.StringVar()
Entry_1 = tk.Entry(w, textvariable=var1, show=None, font=('微软雅黑', 8))
Entry_1.grid(row=2, columnspan=4,sticky=tk.E + tk.W,padx=3, pady=3)

var2 = tk.StringVar()
Entry_2 = tk.Entry(w, textvariable=var2, show=None, font=('微软雅黑', 8))
Entry_2.grid(row=0, column=1, sticky=tk.E + tk.W, padx=3, pady=3)

var0.set('90.')
var1.set('此处为结果响应')
def getVar0Mas():
    Var0MasDict={}
    serverIp = var0.get()
    Var0MasDict["serverIp"]=serverIp
    return Var0MasDict

def DevNum():
    serverIp=getVar0Mas().get("serverIp")
    var1.set(restfultest.rest(serverIp=serverIp).DevNum())

def device_maindevice():
    serverIp=var0.get()
    var1.set(restfultest.rest(serverIp=serverIp).device_maindevice())

def recyclemaindevice():
    serverIp=var0.get()
    var1.set(restfultest.rest(serverIp=serverIp).recyclemaindevice())

def Exdevice_maindevice():
    serverIp=var0.get()
    var1.set(restfultest.rest(serverIp=serverIp).Exdevice_maindevice())

def Exrecyclemaindevice():
    serverIp=var0.get()
    var1.set(restfultest.rest(serverIp=serverIp).Exrecyclemaindevice())

def record_recordplan(**kwargs):
    serverIp=var0.get()
    Plan=kwargs.get('Plan',1)
    var1.set(restfultest.rest(serverIp=serverIp).record_recordplan(Plan=Plan))

def recordpolicybytime(**kwargs):
    serverIp=var0.get()
    bCompress=kwargs.get('bCompress',1)
    var1.set(restfultest.rest(serverIp=serverIp).recordpolicybytime(bCompress=bCompress))

def mpunum():
    serverIp=var0.get()
    nvr=restfultest.rest(serverIp=serverIp).nvrCodeDict
    rn=tn=0
    print()
    for m in nvr:
        if 'MPUR' in m:
            rn=rn+1
        else :
            tn=tn+1
    nvrstr='cu ip是%s,上面有'%serverIp+str(rn)+'个R,'+str(tn)+'个T;'+str(nvr)
    var1.set(nvrstr)


def utc_to_time():
    utc_to_time = var2.get()
    if ':' in str(utc_to_time):
        utc_to_time=int(time.mktime(time.strptime(utc_to_time, "%Y-%m-%d %H:%M:%S")))
        print(utc_to_time)
        var2.set(utc_to_time)
    else:
        utc_to_time=int(utc_to_time)
        utc_to_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utc_to_time))
        print(utc_to_time)
        var2.set(utc_to_time)


B = tk.Label(w, text='VCNAPI外部IP(CU IP):',height=1, width=1,anchor='ne')
B.grid(row=1, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

c = ttk.Button(w, text="查询相机个数", command=DevNum)
c.grid(row=3, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

d = ttk.Button(w, text="添加所有协议相机", command=device_maindevice)
d.grid(row=5, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

d = ttk.Button(w, text="删除所有协议相机", command=recyclemaindevice)
d.grid(row=5, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

e = ttk.Button(w, text="时间与时间戳互换", command=utc_to_time)
e.grid(row=0, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

f = ttk.Button(w, text="从表格添加相机", command=Exdevice_maindevice)
f.grid(row=4, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

g = ttk.Button(w, text="删除所有相机", command=Exrecyclemaindevice)
g.grid(row=4, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

h = ttk.Button(w, text="获取cu,mpu信息", command=mpunum)
h.grid(row=3, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

i = ttk.Button(w, text="打开所有相机计划录像", command=record_recordplan)
i.grid(row=6, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

j = ttk.Button(w, text="关闭所有相机计划录像", command=lambda:record_recordplan(Plan=0))
j.grid(row=6, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

k = ttk.Button(w, text="所有相机开压缩", command=recordpolicybytime)
k.grid(row=7, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

l = ttk.Button(w, text="所有相机关压缩", command=lambda:recordpolicybytime(bCompress=0))
l.grid(row=7, column=2,sticky=tk.E + tk.W, padx=3, pady=3)


w.mainloop()