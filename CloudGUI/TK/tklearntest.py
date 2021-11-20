# -*- coding: utf-8 -*-
import tkinter as tk  # 使用Tkinter前需要先导入
import urllib.parse
from tkinter import ttk
import restfultest
import sshComtest
import time
import portaltest
import cloud
# from VcnUsuGui.TK.sdc import SDC
from sdc import SDC
w = tk.Tk()  # 实例化object，建立窗口w
w.wm_attributes('-topmost',1)
w.title('wx696291')  # 给窗口起名字
wh="320x470"
w.geometry(wh+'+0+500')  # 设定窗口大小
note = ttk.Notebook()
note.place(relx=0,rely=0)

frameCloud = tk.Frame()
note.add(frameCloud,text='HLS')

frameCloud2 = tk.Frame()
note.add(frameCloud2,text='mesbox')

frameVCN = tk.Frame()
note.add(frameVCN,text='VCN')

frameSDC = tk.Frame()
note.add(frameSDC,text='SDC')

var0 = tk.StringVar()
Entry_0 = tk.Entry(frameVCN, textvariable=var0, show=None, font=('微软雅黑', 8))
Entry_0.grid(row=1, column=2, sticky=tk.E + tk.W, padx=3, pady=3)

var1 = tk.StringVar()
Entry_1 = tk.Entry(frameVCN, textvariable=var1, show=None, font=('微软雅黑', 8))
Entry_1.grid(row=2, columnspan=4,sticky=tk.E + tk.W,padx=3, pady=3)

var2 = tk.StringVar()
Entry_2 = tk.Entry(frameVCN, textvariable=var2, show=None, font=('微软雅黑', 8))
Entry_2.grid(row=0, column=1, sticky=tk.E + tk.W, padx=3, pady=3)

var0.set('90.')
var1.set('此处为结果响应')

def DevNum():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    var1.set(restfultest.rest(serverIp=serverIp).DevNum())

def device_maindevice():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    floatGWIP = csp.getfloatGWIP()
    tasCode = csp.getfloatCGCode()
    connectCode=SDC().setGbt28181(SDCIP="90.85.108.213", serverIp=floatGWIP)
    var1.set(restfultest.rest(serverIp=serverIp).device_maindevice(connectCode=connectCode,tasIP=floatGWIP,tasCode=tasCode))
    csp.CSP_LoginOut()

def recyclemaindevice():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    var1.set(restfultest.rest(serverIp=serverIp).recyclemaindevice())

def Exdevice_maindevice():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    var1.set(restfultest.rest(serverIp=serverIp).Exdevice_maindevice())

def Exrecyclemaindevice():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    var1.set(restfultest.rest(serverIp=serverIp).Exrecyclemaindevice())

def record_recordplan(**kwargs):
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    Plan=kwargs.get('Plan',1)
    var1.set(restfultest.rest(serverIp=serverIp).record_recordplan(Plan=Plan))

def recordpolicybytime(**kwargs):
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    bCompress=kwargs.get('bCompress',1)
    var1.set(restfultest.rest(serverIp=serverIp).recordpolicybytime(bCompress=bCompress))

def mpunum():
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
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

def setMCluster():
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    cuIp = sshComtest.ssh(sship=var0.get()).getcuip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    domainName='Dom_' + cuIp.replace('.', '_')
    clusterName='MClu_' + cuIp.replace('.', '_')
    resInfo = csp.CSP_DomainConfig(domainName=domainName)
    print("CSP_DomainConfig-csp上操作结果为： %s" % resInfo, type(resInfo))
    time.sleep(0.5)
    resInfo1 = csp.setClusterConfig(clusterName=clusterName)
    print("setClusterConfig-csp上操作结果为： %s" % resInfo1, type(resInfo1))
    if '操作成功' in resInfo.values() and '操作成功' in resInfo.values():
        remas='设置域名集群名成功'
    else:
        remas = '设置域名集群名失败'
    csp.CSP_LoginOut()
    var1.set(remas)

def set_LogLevel():
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    resInfo = csp.set_LogLevel()
    csp.CSP_LoginOut()
    var1.set(resInfo)

def modifyConf():
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    csp.setVCNDCGService()
    csp.setVCNSvcMgrService()
    csp.modifyConf()
    resInfo = csp.setFloatGWIP()
    csp.CSP_LoginOut()
    var1.set(resInfo)

def deviceGroup(**kwargs):
    serverIp=sshComtest.ssh(sship=var0.get()).getcuip()
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    getNodeInfo = csp.getNodeInfo()
    getserverIpList = csp.getserverIpList()
    csp.CSP_LoginOut()
    var1.set(restfultest.rest(serverIp=serverIp).deviceGroupV2(getNodeInfo=getNodeInfo,getserverIpList=getserverIpList))

def setgaussportal(**kwargs):
    var1.set(sshComtest.ssh(sship=var0.get()).setgaussportal())

def createRaidGroup(**kwargs):
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    resInfo = csp.createRaidGroup()
    csp.CSP_LoginOut()
    var1.set(resInfo)

def upInstallThird(**kwargs):
    portalip = sshComtest.ssh(sship=var0.get()).getportalip()
    at = time.time()
    sshComtest.ssh(sship=var0.get()).downThirdPluginZip()
    csp = portaltest.CSP_HTTP_API(serverIP=portalip)
    res = csp.CSP_Login()
    csp.CSP_UploadThirdPluginZip()
    resInfo=csp.CSP_thirdPlugin_install()
    bt=time.time()
    resInfo=resInfo+",耗时%s秒"%str(int(bt-at))
    csp.CSP_LoginOut()
    var1.set(resInfo)


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


B = tk.Label(frameVCN, text='主节点SSH IP:',height=1, width=1,anchor='ne')
B.grid(row=1, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

c = ttk.Button(frameVCN, text="查询相机个数", command=DevNum)
c.grid(row=8, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

d = ttk.Button(frameVCN, text="添加各协议相机", command=device_maindevice)
d.grid(row=5, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

d = ttk.Button(frameVCN, text="删除各协议相机", command=recyclemaindevice)
d.grid(row=5, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

e = ttk.Button(frameVCN, text="时间与时间戳互换", command=utc_to_time)
e.grid(row=0, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

f = ttk.Button(frameVCN, text="从表格添加相机", command=Exdevice_maindevice)
f.grid(row=4, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

g = ttk.Button(frameVCN, text="删除所有相机", command=Exrecyclemaindevice)
g.grid(row=4, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

h = ttk.Button(frameVCN, text="获取cu,mpu信息", command=mpunum)
h.grid(row=3, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

i = ttk.Button(frameVCN, text="打开所有相机计划录像", command=record_recordplan)
i.grid(row=6, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

j = ttk.Button(frameVCN, text="关闭所有相机计划录像", command=lambda:record_recordplan(Plan=0))
j.grid(row=6, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

k = ttk.Button(frameVCN, text="所有相机开压缩", command=recordpolicybytime)
k.grid(row=7, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

l = ttk.Button(frameVCN, text="所有相机关压缩", command=lambda:recordpolicybytime(bCompress=0))
l.grid(row=7, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

m = ttk.Button(frameVCN, text="设置域名集群名", command=setMCluster)
m.grid(row=9, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

n = ttk.Button(frameVCN, text="迁移相机到mpu设备组", command=deviceGroup)
n.grid(row=8, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

p = ttk.Button(frameVCN, text="重置CU,portal账户", command=setgaussportal)
p.grid(row=3, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

q = ttk.Button(frameVCN, text="30minDebug", command=set_LogLevel)
q.grid(row=10, column=1,sticky=tk.E + tk.W, padx=3, pady=3)

r = ttk.Button(frameVCN, text="portal各种开关", command=modifyConf)
r.grid(row=9, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

s = ttk.Button(frameVCN, text="重建raid组", command=createRaidGroup)
s.grid(row=10, column=2,sticky=tk.E + tk.W, padx=3, pady=3)

t = ttk.Button(frameVCN, text="传和装DCG插件", command=upInstallThird)
t.grid(row=11, column=1,sticky=tk.E + tk.W, padx=3, pady=3)


vars0 = tk.StringVar()
Entry_s0 = tk.Entry(frameSDC, textvariable=vars0, show=None, font=('微软雅黑', 8))
Entry_s0.grid(row=0, column=1, sticky=tk.E + tk.W, padx=3, pady=3)

sa = tk.Label(frameSDC, text='sdc web 原IP:',height=1,width=18,anchor='ne')
sa.grid(row=0, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vars1 = tk.StringVar()
Entry_s1 = tk.Entry(frameSDC, textvariable=vars1, show=None, font=('微软雅黑', 8))
Entry_s1.grid(row=1, column=1, sticky=tk.E + tk.W, padx=3, pady=3)

sb = tk.Label(frameSDC, text='sdc web 目的IP:',height=1,width=18,anchor='ne')
sb.grid(row=1, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vars2 = tk.StringVar()
Entry_s2 = tk.Entry(frameSDC, textvariable=vars2, show=None, font=('微软雅黑', 8))
Entry_s2.grid(row=2, column=1, sticky=tk.E + tk.W, padx=3, pady=3)

sc = tk.Label(frameSDC, text='sdc web 目的网关:',height=1,width=18,anchor='ne')
sc.grid(row=2, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vars3 = tk.StringVar()
Entry_s3 = tk.Entry(frameSDC, textvariable=vars3, show=None, font=('微软雅黑', 8))
Entry_s3.grid(row=3, columnspan=4,sticky=tk.E + tk.W,padx=3, pady=3)


vars3.set('此处为sdc结果响应')
def tksetsdcip():
    SDCIP = vars0.get()
    toSDCIP = vars1.get()
    gateWayAddress = vars2.get()
    print(SDCIP,toSDCIP,gateWayAddress)
    res=SDC().setSDCIP(SDCIP=SDCIP, toSDCIP=toSDCIP, gateWayAddress=gateWayAddress)
    vars3.set(res)
sd = ttk.Button(frameSDC, text="修改ip", command=tksetsdcip)
sd.grid(row=4, columnspan=4,sticky=tk.E + tk.W, padx=3, pady=3)



varca = tk.StringVar()
Entry_ca = tk.Entry(frameCloud, textvariable=varca)
Entry_ca.grid(row=11, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
varca.set("message")
ca = tk.Label(frameCloud, text='执行结果:',height=1,width=18,anchor='ne')
ca.grid(row=11, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

varcd = tk.StringVar()
Entry_cd = ttk.Combobox(frameCloud, width=14,textvariable=varcd,font=('微软雅黑', 8))
Entry_cd['values']=("PRIMARY_STREAM","SECONDARY_STREAM_1")
Entry_cd.grid(row=9, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_cd.current("0")
cd = tk.Label(frameCloud, text='stream_type:',height=1,width=18,anchor='ne')
cd.grid(row=9, column=0,sticky=tk.E + tk.W, padx=3, pady=3)


vardc = tk.StringVar()
Entry_dc = ttk.Combobox(frameCloud, width=12,textvariable=vardc)
Entry_dc['values']=("北京四","上海一","乌兰","性能")
Entry_dc.grid(row=16, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_dc.current("1")
dc = tk.Label(frameCloud, text='环境选择:',height=1,width=18,anchor='ne')
dc.grid(row=16, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

varde = tk.StringVar()
Entry_de = ttk.Combobox(frameCloud, width=12,textvariable=varde)
Entry_de['values']=("HLS","HLS_HTTPS","HLS_DEV","HLS_DEV_HTTPS","HOLO","RTSP","RTSP,static","RTSP_DEV","RTSP_DEV,static")
Entry_de.grid(row=15, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_de.current("0")
de = tk.Label(frameCloud, text='protocol:',height=1,width=18,anchor='ne')
de.grid(row=15, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardf = tk.StringVar()
Entry_df = ttk.Combobox(frameCloud, width=12,textvariable=vardf,font=('微软雅黑', 8))
Entry_df['values']=("34020001001310000001",
                    "34020001001310000002",
                    "34020001001310000003",
                    "34020001001310000004",
                    "0","1","2","3",)
Entry_df.grid(row=14, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_df.current("4")
df = tk.Label(frameCloud, text='channel_id:',height=1,width=18,anchor='ne')
df.grid(row=14, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardg = tk.StringVar()
Entry_dg = ttk.Combobox(frameCloud, width=24,textvariable=vardg, show=None, font=('微软雅黑', 8))
Entry_dg['values']=("200国标大华SDC拾音球机SD,20012345671321234567",
                    "202国标海康SDC拾音球机SD,20212345671321234567",
                    "205好望华为SDC动检,21024125409SM3000825",
                    "213好望华为SDC拾音喇叭SD,2102412969WLM8005595",
                    "213国标华为SDC拾音喇叭SD,21312345671321234567",
                    "214国标海康SDC拾音喇叭,21412345671321234567",
                    "215国标海康NVR2T,21512345671181234567",
                    "216国标大华NVR8T,21612345671181234567",
                    "217好望华为NVR3T,2198061243WLL3000239",
                    "218好望华为IVS1800_4T,2198061240BBL9000019",
                    "221家里好望华为SDC真实SD,21024125399SM6002957",
                    "221家里国标华为SDC真实SD,22112345671321234567",
                    "222家里好望华为SDC灌SD,21024125399SM6003512",
                    )
Entry_dg.grid(row=13, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_dg.current("2")
dg = tk.Label(frameCloud, text='device_id:',height=1,width=18,anchor='ne')
dg.grid(row=13, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardh = tk.StringVar()
Entry_dh = tk.Entry(frameCloud, textvariable=vardh, show=None, font=('微软雅黑', 8))
Entry_dh.grid(row=18, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
vardh.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()-5*86400))))
dh = tk.Label(frameCloud, text='start_time:',height=1,width=18,anchor='ne')
dh.grid(row=18, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardi = tk.StringVar()
Entry_di = tk.Entry(frameCloud, textvariable=vardi, show=None, font=('微软雅黑', 8))
Entry_di.grid(row=19, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
vardi.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()+5*86400))))
di = tk.Label(frameCloud, text='end_time:',height=1,width=18,anchor='ne')
di.grid(row=19, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardj = tk.StringVar()
Entry_dj = ttk.Combobox(frameCloud, width=12,textvariable=vardj)
Entry_dj['values']=("ALL_RECORD","NORMAL_RECORD","MOTION_RECORD")
Entry_dj.grid(row=22, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_dj.current("0")
dj = tk.Label(frameCloud, text='record_type:',height=1,width=18,anchor='ne')
dj.grid(row=22, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

vardk = tk.StringVar()
Entry_dk = ttk.Combobox(frameCloud, width=12,textvariable=vardk,font=('微软雅黑', 8))
Entry_dk['values']=("13709641419,Qaz12580,MD5","13709641419,Qaz12580,SHA256")
Entry_dk.grid(row=24, column=1,sticky=tk.E + tk.W,padx=3, pady=3)
Entry_dk.current("0")


def getdevice_id():
    device_id = Entry_dg.get()
    if "," in device_id:
        device_id=device_id.split(",")[-1]
    print("getdevice_id,device_id:",device_id)
    return device_id
def GetHLS():
    device_id=getdevice_id()
    channel_id=Entry_df.get()
    live_protocol=Entry_de.get()
    stream_type=Entry_cd.get()
    channels=[
        {
            "device_id": device_id,
            "channel_id": channel_id,
            "live_protocol": live_protocol,
            "stream_type": stream_type
        }
    ]
    res = cloud.CLOUD().GetHLSURL(Entry_dc.get(),channels)
    cloud.CLOUD().GetHLSHTML(Entry_dc.get(),channels)
    varca.set(res)


cb = ttk.Button(frameCloud, text="获取实况URL", command=lambda:[GetHLS()])
cb.grid(row=21, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

def GetPlayBackHLS():
    device_id=getdevice_id()
    channel_id=Entry_df.get()
    playback_protocol=Entry_de.get()
    start_time=Entry_dh.get()
    end_time=Entry_di.get()
    infos = vardk.get()
    record_type = vardj.get()
    channels=[
        {
            "device_id": device_id,
            "channel_id": channel_id,
            "playback_protocol": playback_protocol,
            "start_time":urllib.parse.quote(start_time),
            "end_time":urllib.parse.quote(end_time),
            "record_type":record_type
        }
    ]
    res = cloud.CLOUD().GetPlayBackHLSURL(Entry_dc.get(),channels,infos)
    cloud.CLOUD().GetPlayBackHLSHTML(Entry_dc.get(),channels,infos)
    varca.set(res)
ce = ttk.Button(frameCloud, text="获取录像URL", command=GetPlayBackHLS)
ce.grid(row=21, column=1,sticky=tk.E + tk.W, padx=3, pady=3)


Textea = tk.Text(frameCloud2,width=51,height=28,font=('微软雅黑', 8))
Textea.pack()
def GetCloudReList():
    Textea.delete("1.0",tk.END)
    device_id = getdevice_id()
    channel_id = Entry_df.get()
    record_type = Entry_dj.get()
    live_protocol = Entry_de.get()
    start_time = Entry_dh.get()
    end_time = Entry_di.get()
    channels = [
        {
            "device_id": device_id,
            "channel_id": channel_id,
            "record_type": record_type,
            "live_protocol": live_protocol,
            "start_time": urllib.parse.quote(start_time),
            "end_time": urllib.parse.quote(end_time)
        }
    ]
    res = cloud.CLOUD().GetCloudReList(Entry_dc.get(), channels)
    Textea.insert("1.0", res)

cf = ttk.Button(frameCloud, text="获取录像列表", command=GetCloudReList)
cf.grid(row=23, columnspan=4,sticky=tk.E + tk.W, padx=3, pady=3)

def setrtspinfo():
    infos = vardk.get()
    res = cloud.CLOUD().rtspinfo(Entry_dc.get(), infos)
    varca.set(res)
cg = ttk.Button(frameCloud, text="设置rtsp鉴权信息", command=setrtspinfo)
cg.grid(row=24, column=0,sticky=tk.E + tk.W, padx=3, pady=3)

def getstream_ability():
    device_id=getdevice_id()
    channel_id=Entry_df.get()
    channels=[
        {
            "device_id": device_id,
            "channel_id": channel_id
        }
    ]
    res = cloud.CLOUD().getstream_ability(Entry_dc.get(),channels)
    Textea.delete("1.0", tk.END)
    Textea.insert("1.0", res)
ch = ttk.Button(frameCloud, text="码流能力集", command=getstream_ability)
ch.grid(row=25, column=0,sticky=tk.E + tk.W, padx=3, pady=3)
w.mainloop()