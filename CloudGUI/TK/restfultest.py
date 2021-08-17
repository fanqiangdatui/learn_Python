# -*- coding: utf-8 -*-
import time
import openpyxl
import requests,json
import urllib3
import math
import sdktxt
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class rest():
    def __init__(self,**kwargs):
        self.restses = requests.session()
        self.serverIp=kwargs.get('serverIp','')
        self.serverPort=kwargs.get('serverPort','18531')
        self.uriBase='https://'+self.serverIp+':'+self.serverPort+'/'
        self.userName=kwargs.get('userName','admin')
        self.password = kwargs.get('password', 'super123')
        self.data = {
            "userName": self.userName,
            "password": self.password
        }
        self.header={'Content-Type': 'application/json'}
        print (self.serverIp,self.serverPort,self.uriBase,self.userName,self.password,self.data,self.header,self.restses)

        url = self.uriBase+'loginInfo/login/v1.0'
        data=json.dumps(self.data)

        response = self.restses.post(url, data=data, headers=self.header,timeout=5,verify=False)
        print ('loginInfo/login/v1.0--response.text:',json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False),'\r\n')
        print ("loginInfo/login/v1.0--response.headers:",response.headers,'\r\n')
        print ('loginInfo/login/v1.0--session:',self.restses,'\r\n')

        url = self.uriBase+'device/domainRoute/v1.1?'
        response = self.restses.get(url,verify=False)
        responsetext = json.loads(response.text)
        self.domainCode=responsetext['domainRouteInfos']['domainRouteList']['domainRoute'][0]['domainCode']
        self.restses = self.restses
        print ('--response.text:',json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False),response.text,type(response.text))

        url = self.uriBase+'playback/nvrlist/0/{domainCode}/1/10'.format(domainCode=self.domainCode)
        payload = {}
        response = self.restses.get(url, data=payload,verify=False)
        responsetext = json.loads(response.text)
        a = responsetext['nvrInfos']['deviceBriefInfoList']['deviceBriefInfo']
        nvrCodeDict={}
        for i in a:
            if 'MPU' in i["deviceBasicInfo"]['name']:
                nvrCodeDict[i["deviceBasicInfo"]['name']]=i["deviceBasicInfo"]['code']
        self.nvrCodeDict=nvrCodeDict
        print('nvrCodeDict',self.nvrCodeDict)
        self.nvrCode = self.nvrCodeDict['MPUR-0001']
        print ('--response.text:',json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False))

    def device_deviceconfig(self):
        url = self.uriBase+'device/deviceconfig/4/01560155564199490101/'+self.domainCode
        response = self.restses.get(url,verify=False)
        jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print ('************json.dumps.response.text:',jr)
        return response.status_code

    def recyclemaindevice(self):
        url = self.uriBase+'device/maindevice/recyclemaindevice/v1.0'
        deviceCodeList=sdktxt.sdk().sdkdeltxt()
        d={
    "domainCode": self.domainCode,
    "deviceNum": len(deviceCodeList['deviceCode']),
    "deviceCodeList": deviceCodeList
}
        for key, value in d.items():
            if value is None:
                del d[key]
        print('************data',d,type(d))
        response = self.restses.delete(url,json=d,verify=False)
        jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print ('************json.dumps.response.text:',jr)
        return '删除各协议相机成功'

    def device_maindevice(self,**kwargs):
        url = self.uriBase+'device/maindevice/v1.0'
        tasCode = kwargs.get('tasCode')
        tasIP =kwargs.get('tasIP')
        connectCode =kwargs.get('connectCode')
        deviceOperInfos=sdktxt.sdk().sdkaddtxt(nvrCode=self.nvrCode,connectCode=connectCode,tasIP=tasIP,tasCode=tasCode)
        d={
	"domainCode": self.domainCode,
	"deviceNum": len(deviceOperInfos['deviceOperInfo']),
	"deviceOperInfos": deviceOperInfos
}
        for key, value in d.items():
            if value is None:
                del d[key]
        print('************data',d,type(d))
        response = self.restses.post(url,json=d,verify=False)
        jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print ('************json.dumps.response.text:',jr)
        return '添加各协议相机成功'

    def getSDKlistlist(self):
        '''
        从xlsx生成
        :return:
        '''
        wb = openpyxl.load_workbook('.\\ipctest.xlsx')
        SDKlistlist = []
        ipc6code = '0000'
        portDict={'HWSDK':6060,'onvif':80,'DHSDK':37777,'HIKSDK':8000}
        for sdk in wb.sheetnames:
            sheet = wb[sdk]
            rlistlist = []
            for row in sheet.rows:
                rlist = []
                for r in row:
                    print(r.value)
                    rlist = rlist + [r.value]
                print(rlist)
                rlistlist = rlistlist + [rlist]
            rlistlist[0]
            MPURi = rlistlist[0].index('*集群或NVR编码')
            if '*IP' in rlistlist[0]:
                ipi = rlistlist[0].index('*IP')
            else:
                ipi = ''
            if '*端口' in rlistlist[0]:
                porti = rlistlist[0].index('*端口')
            else:
                porti = ''
            if '*用户名' in rlistlist[0]:
                deviceUseri = rlistlist[0].index('*用户名')
            else:
                deviceUseri = ''
            if '*密码' in rlistlist[0]:
                devicePasswordi = rlistlist[0].index('*密码')
            else:
                devicePasswordi = ''

            rlistlist = rlistlist[1:]

            print('-----------rlistlist', rlistlist)
            minrlistlist=[]
            for rrlist in rlistlist:
                ipp = str(rrlist[ipi])
                if ':' in ipp:
                    print('有批量设备，ip是',ipp)
                    num=int(ipp.split(':')[-1])
                    ipseg='.'.join(ipp.split(':')[0].split('.')[0:-1])
                    ipstarnum=int(ipp.split(':')[0].split('.')[-1])
                    for ipstr in range(ipstarnum,ipstarnum+num):
                        ipstrlist = rrlist.copy()
                        ipstrlist[ipi]=ipseg+'.'+str(ipstr)
                        minrlistlist = minrlistlist + [ipstrlist]
                        print('minrlistlist',minrlistlist)
                        print('ipstrlist',ipstr,ipstrlist)
                else:
                    print('进了else')
                    minrlistlist = minrlistlist + [rrlist]
            print('minrlistlist',minrlistlist)
            rlistlist=minrlistlist
            print('-----------rlistlist', rlistlist)

            SDKlist = []
            for rlist in rlistlist:
                ip = str(rlist[ipi])
                MPUR = rlist[MPURi]
                port = rlist[porti]
                deviceUser = rlist[deviceUseri]
                devicePassword = rlist[devicePasswordi]
                if deviceUser is None:
                    deviceUser='admin'
                if port is None and sdk in portDict.keys():
                    port = portDict[sdk]
                if devicePassword is None:
                    devicePassword = 'HuaWei123'
                ipc12code = ''.join(list(map(lambda x: x.zfill(3), ip.split('.'))))
                ipc20code = ipc6code + ipc12code + '0000'
                SDK = {
                    "deviceConfig": {
                        "maxDirectConnectNum": 3,
                        "devicePassword": devicePassword,
                        "deviceUser": deviceUser,
                        "protocolType": sdk,
                        "enableSchedule": 1,
                        "enableAlarm": 0,
                        "nvrCode": self.nvrCodeDict[MPUR],
                        "deviceBasicInfo": {
                            "port": port,
                            "name": ip,
                            "domainCode": '',
                            "code": ipc20code,
                            "type": 1,
                            "ipInfo": {
                                "ip": ip,
                                "ipType": 0
                            }
                        }
                    },
                    "sequence": 1
                }
                SDKlist = SDKlist + [SDK]
                print('------SDK',SDK)
            SDKlistlist = SDKlistlist + SDKlist
            print('-----------SDKlist', SDKlist)
        print('-----------SDKlistlist', SDKlistlist)
        return SDKlistlist

    def Exdevice_maindevice(self):
        try:
            ct = time.time()
            url = self.uriBase + 'device/maindevice/v1.0'
            SDKlistlist=self.getSDKlistlist()
            print('SDKlistlist',SDKlistlist)
            ma = 50
            mathsdk = math.ceil(len(SDKlistlist) / ma)
            SDKlistlistlist = []
            print(mathsdk)
            if mathsdk > 1:
                for sdki in range(mathsdk):
                    malist = SDKlistlist[sdki * ma:(sdki + 1) * ma]
                    SDKlistlistlist = SDKlistlistlist + [malist]
                    print(malist)
            else:
                SDKlistlistlist = [SDKlistlist]
            print('SDKlistlistlist', SDKlistlistlist)
            print(len(SDKlistlistlist[0]))

            for sdkll in SDKlistlistlist:
                deviceOperInfos={
                    "deviceOperInfo": sdkll
                }
                d={
            "domainCode": self.domainCode,
            "deviceNum": len(sdkll),
            "deviceOperInfos": deviceOperInfos
        }
                print('************data',d,type(d))
                at=time.time()
                print(at)
                time.sleep(5)
                try:
                    self.restses.post(url,json=d,timeout=90,verify=False)
                except:
                    pass
                bt=time.time()
                print(bt)
                print('rest耗时%s秒'%str(int(bt-at)))
            dt=time.time()
            dtt=str(int(dt-ct))
            print('添加设备耗时%s秒'%dtt)
            return '表格加相机成功,耗时%s秒'%dtt
        finally:
            self.restses.close()

    def masterDeviceList(self):
        codeListlist=[]
        for NVRCode in self.nvrCodeDict:
            url = self.uriBase+'device/masterDeviceList/v1.1?fromIndex=1&toIndex=1000&NVRCode={NVRCode}&domainCode='.format(NVRCode=self.nvrCodeDict[NVRCode])+self.domainCode
            response = self.restses.get(url,verify=False)
            responsetext = json.loads(response.text)
            jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print ('************json.dumps.response.text:',jr,type(jr),type(responsetext))
            deviceBriefInfo = responsetext['deviceBriefInfos']['deviceBriefInfo']
            print(deviceBriefInfo)
            codeList = []
            for code in deviceBriefInfo:
                print('code', code)
                codeList = codeList + [code['deviceBasicInfo']['code']]
            print('-------------codeList',codeList)
            codeListlist=codeListlist+codeList

        print('-------------codeListlist',codeListlist)
        return codeListlist

    def Exrecyclemaindevice(self):
        url = self.uriBase+'device/maindevice/recyclemaindevice/v1.0'
        deviceCodeList={
        "deviceCode": self.masterDeviceList()
    }
        d={
    "domainCode": self.domainCode,
    "deviceNum": len(deviceCodeList['deviceCode']),
    "deviceCodeList": deviceCodeList
}
        try:
            print('************data',d,type(d))
            response = self.restses.delete(url,json=d,timeout=120,verify=False)
            jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print ('************json.dumps.response.text:',jr)
            return '删除所有相机成功'
        except:
            return '超时'

    def DevNum(self):
        DevNum=len(self.masterDeviceList())
        return '相机个数为%s'%DevNum

    def device_deviceList(self):
        url = self.uriBase+'device/deviceList/v1.0?deviceType=2&fromIndex=1&toIndex=20000'
        response = self.restses.get(url,verify=False)
        responsetext = json.loads(response.text)
        jr=json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print ('************json.dumps.response.text:',jr,type(jr),type(responsetext))
        cameraBriefInfo = responsetext['cameraBriefInfos']['cameraBriefInfoList']['cameraBriefInfo']
        print(cameraBriefInfo)
        videoCodeList = []
        for camera in cameraBriefInfo:
            print('camera', camera)
            videoCodeList = videoCodeList + [camera['code']]
        print('-------------videoCodeList',videoCodeList)
        return videoCodeList

    def record_recordplan(self,**kwargs):
        url = self.uriBase + 'record/recordplan/v1.0'
        videoCodeList = {
            "cameraCode": self.device_deviceList()
        }
        Plan =kwargs.get('Plan',1)
        d = {
  "cameraNum": len(self.device_deviceList()),
  "cameraCodeList":videoCodeList,
    "recordPlan": {
        "recordMethod": 0,
        "enableRecordPlan": Plan,
        "recordPlanType": 2,
        "planInfoNum": 0
    }
}
        try:
            print('************data', d, type(d))
            response = self.restses.put(url, json=d, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            if Plan==1:
                return '开启所有计划录像成功'
            else:
                return '关闭所有计划录像成功'
        except:
            return '超时'

    def recordpolicybytime(self, **kwargs):
        url = self.uriBase + 'record/recordpolicybytime/v1.0'
        bCompress=kwargs.get('bCompress',1)
        cameraCodeList=self.device_deviceList()
        print('cameraCodeList',cameraCodeList)
        for cameraCode in cameraCodeList:
            d = {
        "cameraCode":cameraCode,
        "recordPolicy": {
            "recordMode": 0,
            "time": 9999,
            "planStreamType": 1,
            "alarmStreamType": 1,
            "alarmRecordTTL": 9999,
            "manualRecordTTL": 9999,
            "preRecord": 2,
            "preRecordTime": 30,
            "associatedAudio": 1,
            "bCompress": bCompress
        }
    }
            try:
                print('************data', d, type(d))
                response = self.restses.post(url, json=d, timeout=4, verify=False)
                jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
                print('************json.dumps.response.text:', jr)
            except:
                pass
        if response.status_code==200:
            if bCompress==1:
                return '所有相机开压缩成功'
            else:
                return '所有相机关压缩成功'

    def deviceGroup(self):
        urldeviceGroupInfotest = self.uriBase + 'device/deviceGroupInfo/v1.0'
        datadeviceGroupInfotest = {"name": str(time.time()).split('.')[0], "parentID": "0"}
        print('************datadeviceGroupInfotest,data', datadeviceGroupInfotest, type(datadeviceGroupInfotest))
        response = self.restses.post(urldeviceGroupInfotest, json=datadeviceGroupInfotest, timeout=120, verify=False)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr)
        deviceGroupID=int(json.loads(response.text)['deviceGroupID'])
        for gi in range(1,deviceGroupID+1):
            urldeviceGroupInfotest = self.uriBase + 'device/deviceGroupInfo/v1.0'
            datadeviceGroupInfotest = {"groupId":str(gi),"domainCode":self.domainCode}
            print('************datadeviceGroupInfotest,data', datadeviceGroupInfotest, type(datadeviceGroupInfotest))
            response = self.restses.delete(urldeviceGroupInfotest, json=datadeviceGroupInfotest, timeout=120,
                                         verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)

        mpcodict={}
        for k,v in self.nvrCodeDict.items():
            url = self.uriBase + 'device/masterDeviceList/v1.1?fromIndex=1&toIndex=1000&NVRCode={NVRCode}&domainCode='.format(
                NVRCode=v) + self.domainCode
            response = self.restses.get(url, verify=False)
            responsetext = json.loads(response.text)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************masterDeviceList.json.dumps.response.text:', jr, type(jr), type(responsetext))
            deviceBriefInfo = responsetext['deviceBriefInfos']['deviceBriefInfo']
            print(deviceBriefInfo)
            codeList = []
            for code in deviceBriefInfo:
                print('code', code)
                codeList = codeList + [code['deviceBasicInfo']['code']]
            print('-------------codeList', codeList)
            mpcodict[k]=codeList
        print('-------------mpcodict', mpcodict)
        ic=deviceGroupID+1
        for ke,va in mpcodict.items():
            urldeviceGroupInfo = self.uriBase + 'device/deviceGroupInfo/v1.0'
            datadeviceGroupInfo={"name":ke,"parentID":"0"}
            print('************datadeviceGroupInfo,data', datadeviceGroupInfo, type(datadeviceGroupInfo))
            response = self.restses.post(urldeviceGroupInfo, json=datadeviceGroupInfo, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            devList=[]
            for c0000 in va:
                devList=devList+[{"devCode": (c0000[:-4]+'0101'), "fromGroupID": 0}]
            print('devList',devList)
            urldeviceToGroup = self.uriBase + 'device/deviceToGroup/v1.0'
            datadeviceToGroup={ "domainCode": self.domainCode, "targetGroupID": ic,"devList":devList }
            print('************deviceToGroupo,data', datadeviceGroupInfo, type(datadeviceGroupInfo))
            response = self.restses.put(urldeviceToGroup, json=datadeviceToGroup, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            ic=ic+1
        return '迁移相机到设备组成功'

    def deviceGroupV2(self,**kwargs):
        getNodeInfo=kwargs.get('getNodeInfo','')
        getserverIpList = kwargs.get('getserverIpList', '')
        urldeviceGroupInfotest = self.uriBase + 'device/deviceGroupInfo/v1.0'
        datadeviceGroupInfotest = {"name": str(time.time()).split('.')[0], "parentID": "0"}
        print('************datadeviceGroupInfotest,data', datadeviceGroupInfotest, type(datadeviceGroupInfotest))
        response = self.restses.post(urldeviceGroupInfotest, json=datadeviceGroupInfotest, timeout=120, verify=False)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr)
        deviceGroupID=int(json.loads(response.text)['deviceGroupID'])
        #新添加的一个组ID

        for gi in range(1,deviceGroupID+1):
            urldeviceGroupInfotest = self.uriBase + 'device/deviceGroupInfo/v1.0'
            datadeviceGroupInfotest = {"groupId":str(gi),"domainCode":self.domainCode}
            print('************datadeviceGroupInfotest,data', datadeviceGroupInfotest, type(datadeviceGroupInfotest))
            response = self.restses.delete(urldeviceGroupInfotest, json=datadeviceGroupInfotest, timeout=120,
                                         verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)

        mpcodict={}
        fuGroupIDListDict={}
        for serverIp in getserverIpList:
            groudip=serverIp.split('.')[2]
            urlserverIp = self.uriBase + 'device/deviceGroupInfo/v1.0'
            dataserverIp={"name":groudip,"parentID":"0"}
            #MPU设备组名称
            print('************dataserverIp,data', dataserverIp, type(dataserverIp))
            response = self.restses.post(urlserverIp, json=dataserverIp, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            fuGroupIDList = int(json.loads(response.text)['deviceGroupID'])
            fuGroupIDListDict[serverIp]=fuGroupIDList
        print('fuGroupIDListDict',fuGroupIDListDict)

        for k,v in self.nvrCodeDict.items():
            url = self.uriBase + 'device/masterDeviceList/v1.1?fromIndex=1&toIndex=1000&NVRCode={NVRCode}&domainCode='.format(
                NVRCode=v) + self.domainCode
            response = self.restses.get(url, verify=False)
            responsetext = json.loads(response.text)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************masterDeviceList.json.dumps.response.text:', jr, type(jr), type(responsetext))
            deviceBriefInfo = responsetext['deviceBriefInfos']['deviceBriefInfo']
            print(deviceBriefInfo)
            codeList = []
            for code in deviceBriefInfo:
                print('code', code)
                codeList = codeList + [code['deviceBasicInfo']['code']]
            print('-------------codeList', codeList)
            mpcodict[k]=codeList
        print('-------------mpcodict', mpcodict)

        ic=deviceGroupID+1+len(getserverIpList)
        for ke,va in mpcodict.items():
            urldeviceGroupInfo = self.uriBase + 'device/deviceGroupInfo/v1.0'
            for NodeInfo in getNodeInfo:
                if ke==NodeInfo['nodeName']:
                    kename=ke+'_'+NodeInfo['nodeCode'][0:3]+'_'+NodeInfo['containerId'][0:3]
                    parentID=fuGroupIDListDict['%s'%NodeInfo['serverIp']]

            datadeviceGroupInfo={"name":kename,"parentID":parentID}
            #MPU设备组名称
            print('************datadeviceGroupInfo,data', datadeviceGroupInfo, type(datadeviceGroupInfo))
            response = self.restses.post(urldeviceGroupInfo, json=datadeviceGroupInfo, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            devList=[]
            for c0000 in va:
                devList=devList+[{"devCode": (c0000[:-4]+'0101'), "fromGroupID": 0}]
            print('devList',devList)
            urldeviceToGroup = self.uriBase + 'device/deviceToGroup/v1.0'
            datadeviceToGroup={ "domainCode": self.domainCode, "targetGroupID": ic,"devList":devList }
            print('************deviceToGroupo,data', datadeviceGroupInfo, type(datadeviceGroupInfo))
            response = self.restses.put(urldeviceToGroup, json=datadeviceToGroup, timeout=120, verify=False)
            jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
            print('************json.dumps.response.text:', jr)
            ic=ic+1
        return '迁移相机到设备组成功'
if __name__=='__main__':
    print(sdktxt.sdk().sdktxt(nvrCode=1))