安全群里有个题目需要用到盲水印工具，学习下相关知识  
#1、环境准备  
相关代码在这里  
```https://github.com/chishaxie/BlindWaterMark#blindwatermark```  
首先下载该工程的zip，因为貌似无法用git克隆到本地  
解压后打开该工程  
![OpenBlindwatermark](https://github.com/fanqiangdatui/image/blob/master/Snipaste_2019-10-30_01-00-20.png)  
#2、安装相关库  
环境需要在python2.7.x上使用，需要安装的库有opencv-python、matplotlib(1.5.0)  
#3、解出盲水印  
进入对应的工程路径运行脚本  
```python bwm.py decode hui.png hui_with_wm.png wm_from_hui.png```  
![GetBlindwatermark](https://github.com/fanqiangdatui/image/blob/master/Snipaste_2019-10-30_01-07-50.png)
