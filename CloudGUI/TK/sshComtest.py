#  -*- coding:gbk -*-
import paramiko,time
class ssh():
    def __init__(self,**kwargs):
        client = paramiko.SSHClient()
        self.sship = kwargs.get('sship', '90.')
        firname = 'cspexpert'
        firpwd = 'mt2017@cspos@RD'
        rorpwd = 'cnp200@cspos@RD'
        print('self.sship',self.sship)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.sship, 22, username=firname, password=firpwd)
        channel = client.invoke_shell()
        self.channel=channel
        self.channel.send("su\n") # \n 执行命令 没有\n不执行
        buff=''
        while True:
            print(1)
            buff = self.channel.recv(65535).decode('utf-8')
            print('su-buff:', buff)
            if buff.endswith('Password: '):
                self.channel.send(rorpwd+'\n')
                time.sleep(0.1)
                self.channel.send('TMOUT=0' + '\n')
                break
        self.client=client
        print('id-self.client',id(self.client),'id -elf.channel',id(self.channel))

    def getportalip(self):
        buff=''
        cmd=r"""docker exec -ti $(docker ps |grep cspommgr |awk -F' ' '{print $1}') netstat -anp|grep 31943 |grep LISTEN|grep -v 127.0.0.1|awk '{print $4}'"""
        self.channel.send(cmd + '\n')
        while True:
            time.sleep(0.1)
            buff = buff+self.channel.recv(65535).decode('utf-8')
            print('ip-buff:', buff)
            if buff.endswith('# '):
                break
        buffsplit=buff.split('\r\n')
        print('31943buffsplit',buffsplit)
        self.portalip=buffsplit[-2].split(':')[0]
        print('self.portalip',self.portalip)
        print('id-self.client', id(self.client), 'id -elf.channel', id(self.channel))
        return self.portalip

    def getcuip(self):
        buff=''
        # cmd=r"""docker exec -ti $(docker ps |grep vcn |awk -F' ' '{print $1}') netstat -anp|grep 18531 |grep LISTEN|grep -v 127.0.0.1|awk '{print $4}'|head -1"""
        cmd=r"""docker exec -it `docker ps|grep gaussapi|awk '{print $1}'|head -1` su -c "psql -d smu -c \"select IP from TBL_DOMAIN_INFO;\"|sed -n '3,3'p" - postgres"""
        self.channel.send(cmd + '\n')
        while True:

            time.sleep(0.1)
            buff = buff+self.channel.recv(65535).decode('utf-8')
            print('ip-buff:', buff)
            if buff.endswith('# '):
                break
        buffsplit=buff.split('\r\n')
        print('18531buffsplit',buffsplit)
        self.cuip=buffsplit[-2].split(':')[0].strip(' ')
        print('self.cuip:'+self.cuip+':')
        print('id-self.client', id(self.client), 'id -elf.channel', id(self.channel))
        return self.cuip

    def setMCluster(self,**kwargs):
        MCluster='MCluster'+self.getcuip().replace('.','_')
        cmd = r"""docker exec -it `docker ps|grep gaussapi|awk '{print $1}'` su -c "gsql -d smu -c \"update tbl_cluster_info set CLUSTER_NAME='%s',CLUSTER_IS_LOADBALANCE=0,CLUSTER_IS_FAULT_SHIFT=0;\"|sed -n '1,$'p" - postgres""" % (MCluster)
        buff=''
        self.channel.send(cmd + '\n')
        while True:
            time.sleep(0.1)
            buff = buff+self.channel.recv(65535).decode('utf-8')
            print('ip-buff:', buff)
            if buff.endswith('# '):
                break
        buffsplit=buff.split('\r\n')
        print('gaussapi-buffsplit',buffsplit)
        return '更改集群名成功'

    def setgaussportal(self):
        cmd=r"""docker exec -u root -ti `docker ps | grep "cspgaussdb" | awk '{print$1}'` su - dbuser -c "gsql -d USERDB -U USERDBUSER -p 22080 -W Cspdbg@2017 -c \"update USERPASSWORD set PASSWORD='00000002EC6B2AF75D054BA275A8DD25E2085BA8F08DB055B47697AFDB4FBCA91CA2C711285F6D3179BC1CA36CC0E347A2414C5D',ISINITIALPASSWORD='0';update ACCOUNTPROFILE set NOTLOCKLOGINFAILUSER=1,LOCKINGDURATION=1,NOTSTOPNOLOGINUSER=1,DELETELOCKEDUSERPERIOD=0,DELETESTOPPEDUSERPERIOD=0,TIMEOUTVALUE=4320,FORCETIMEOUTVALUE=7200;\"";docker exec -it `docker ps|grep gaussapi|awk '{print $1}'` su -c "psql -d smu -c \"update tbl_user_info set status='1',first_login='1',max_sess_cnt=1000,login_password='063f7a59a6167ab47ce327796af065c1bf8d84729581d1d62c91aad288ada15a',register_date='3025080290530',PWD_MODIFY_DATE='3025080290530',salt='"enEg2BA0sVIL8rZh"' where login_name='admin';\"" - postgres"""
        buff = ''
        self.channel.send(cmd + '\n')
        while True:
            time.sleep(0.1)
            buff = buff+self.channel.recv(65535).decode('utf-8')
            print('ip-buff:', buff)
            if buff.endswith('# '):
                break
        buffsplit=buff.split('\r\n')
        print('gaussapi-buffsplit',buffsplit)
        return '重置CU,portal账户成功'

    def downThirdPluginZip(self):
        t = paramiko.Transport(('90.71.102.2',22))
        t.connect(username='root',password='huawei@123')
        sftp = paramiko.SFTPClient.from_transport(t)
        zipList=["plugin_dcg_bocong_2.1.0_x86_signature.zip",
                 "plugin_dcg_dahua_2.1.0_x86_signature.zip",
                 "plugin_dcg_hikvision_2.1.0_x86_signature.zip",
                 "plugin_dcg_ifaas_2.1.0_x86_signature.zip",
                 "plugin_dcg_infinov_2.1.0_x86_signature.zip",
                 "plugin_dcg_kedacom_2.1.0_x86_signature.zip",
                 "plugin_dcg_rtsp_2.1.0_x86_signature.zip",
                 "plugin_dcg_uniview_2.1.0_x86_signature.zip"
                 ]
        att = time.time()
        for zi in zipList:
            print("本次下载插件是"+zi)
            sftp.get("/IVS/V900/develop/vcn_x86_Plugin/%s"%zi, ".\\%s"%zi)
        btt=time.time()
        print('下载所有插件到本地耗时为%s秒'%str(int(btt-att)))
        t.close()
if __name__=="__main__":
    ssh().downThirdPluginZip()