查看版本包：带auto关键字的表示为离线
cat /usr/app/bin/version
查看算法包：带auto关键字的表示为离线
cat /usr/alg_model/version_facedt_dl
离线版本位置
\\10.186.123.81\Distribute\SDC_OneTrack\master\

使用ffmpeg软件将mp4格式的视频文件，转换为灌流使用的h265或h264格式。
命令如下：
ffmpeg -i test.mp4 -vcodec copy -f h264 test.h264 //将test.mp4转换为test.h264格式
ffmpeg -i test.mp4 -vcodec copy -f hevc test.h265   //将test.mp4转换为test.h265格式
ffmpeg -ss 0:1:30 -t 0:0:20 -i test.mp4 -vcodec copy -acodec copy test1.mp4   //截取视频，-ss为开始时间，-t为持续时间
上面是最常用的几条命令，受原mp4编码格式影响，通常上述两个命令只有一个能成功。如采用选择h265编码格式获取的视频，转换为h264格式时会失败。

通过在nfsroot目录下敲mount -t nfs -o nolock 3.200.0.57：/d/nfsroot /nfsroot命令
可以完成设备的nfsroot目录和本地nfsroot目录同步，在pc的nfsroot下创建文件或拷贝文件就可以在设备的nfsroot目录下同步
2.但是当设备重启后，所有挂载就断开了，所以我们需要让设备启动的时候就挂载上，需要在startapp.sh或者mount.sh中加入挂载命令。startapp.sh或者mount.sh修改其一即可，用vi指令打开startapp.sh，拉到最后，输入，IP就是自己的小网IP
使用ssh登录IPC的后台，默认用户名和密码：admin  ChangeMe123  在切换到root账号  su - root  密码HuaWei123

修改mount.sh文件
mount.sh所在目录为/usr/app/bin/mount.sh
命令为：
mount -t nfs -o nolock ipadress:/d/nfsroot /nfsroot
cp /nfsroot/VideoTestCfg /usr/setting/VideoTestCfg
touch /tmp/AnalyseVideoControlCfg
其中ipadress为你的本地ip地址，后面跟着本地nfsroot路径。(上面安装nfs工具后设置的路径）

vi /usr/app/bin/mount.sh
mount -t nfs -o nolock 192.168.5.171:/home/nfsroot /nfsroot
cp /nfsroot/VideoTestCfg /usr/setting/VideoTestCfg
touch /tmp/AnalyseVideoControlCfg



FILE_PATH=/nfsroot/stream_files, //灌流文件所在目录
FILE_NAME=test11.h265,//灌流文件的文件名
ENCODE_TYPE=H265, //编码方式
FRAME_RATE=25,   //帧率
WIDTH=4096,     //灌流文件 实际像素WIDTH
HEIGHT=2160,    //灌流文件 实际像素HEIGHT
CIRCLE_SEND=1,  //1代表循环灌流，0为不循环


900版本可以不重启，在/usr/app/bin目录下修改mount.sh权限，执行脚本，然后重新拉流即可播放视频，指令如下：
umount -l /nfsroot      // 取消挂载
cd /usr/app/bin
chmod 777 /usr/app/bin/mount.sh
./mount.sh
touch /tmp/AutoRestart  // 重新拉流
cat /proc/umap/venc |grep -C 4 'VENC STREAM STATE' // 查看帧率

chmod 777 /usr/app/bin/mount.sh && /usr/app/bin/mount.sh && touch /tmp/AutoRestart