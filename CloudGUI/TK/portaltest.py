# -*- coding: utf-8 -*-
import json
import os
import queue,http.client
import time
import urllib.parse
import ssl
import urllib3
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class CSP_HTTP_API():
    publicObject = queue.Queue()
    def __init__(self, **kwargs):
        self.requestAgain = 0
        self.HttpType = "CSP"
        self.HttpClient = None
        self.serverIP = kwargs.get('serverIP','3.180.2.11')
        self.serverPort = kwargs.get('serverPort',31943)
        self.HttpClient = http.client.HTTPSConnection(self.serverIP,self.serverPort)
        self.bspSession = ""
        self.Token = ""
        self.appID = "-1"
        self.appVersion = '-1'
        self.appName = '-1'
        self.SessionTokenHeader = ""
        self.csp_version = ""  # csp版本信息
        self.zkMemInfo = ""  # zk信息,固定信息，查询一次后记录，避免重复查询
        self.uriBase = "https://" + self.serverIP + ":" + str(self.serverPort)
        self.loginHeader = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                            "Accept-Encoding": "gzip, deflate, sdch, br",
                            "Accept-Language": "zh-CN,zh;q=0.8",
                            "Cache-Control": "max-age=0",
                            "Connection": "keep-alive",
                            "Cookie": "theme=lightday; bspsession=deleted; locale=zh-cn",
                            "Host": self.serverIP + ":" + str(self.serverPort),
                            "Referer": "https://" + self.serverIP + ":" + str(
                                self.serverPort) + "/unisso/website/login/loginpage?service=%2Funisess%2Fv1%2Fauth%3Fservice%3D%252Funisso%252Fwebsite%252Fhome%252Fhomepage",
                            "Upgrade-Insecure-Requests": "1",
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"}
        self.objectDict = queue.Queue()

        self.uni_conf_ver = ''  # 统一配置接口 ver 参数，由handleParams使用
    # 登陆，获取ticket：ST-593-mRXfTpZcwY5raE2XdX4vsoob-sso
    def __LogIn_and_Get_Ticket(self, username, password):
        # 函数入口打log，方便定位
        print('Calling CSP_LogIn_and_Get_Ticket, '
                          'ip: %s, port: %s, username: %s, password: %s' % (
                              self.serverIP, self.serverPort, username, password))
        username = urllib.parse.quote(username)
        password = urllib.parse.quote(password)
        # 新url，暂时注释
        # url = self.uriBase + "/unisso/validateUser.action?service=%2fauth"
        url = self.uriBase + "/unisso/validateUser.action?service=https%3A%2F%2F" + self.serverIP + "%3A31943%2Funisess%2Fv1%2Fauth%3Fservice%3Dhttps%253A%252F%252F" + self.serverIP + "%253A31943%252Fcspportalwebsite%252F%2523%252Fhome"
        params1 = "userpasswordcredentialsUsername=%s&userpasswordcredentialsPassword=%s&__checkbox_warnCheck=true&Submit=Login&userpasswordcredentialsVerifycode=" % (
            username, password)
        print('Get_Ticket-params1',params1)
        header1 = self.loginHeader.copy()
        header1["Content-Type"] = "application/x-www-form-urlencoded"
        header1["Origin"] = "https://" + self.serverIP + ":" + str(self.serverPort)
        header1["Content-Length"] = str(len(params1))
        self.HttpClient.request("POST", url, params1, header1)
        response1 = self.HttpClient.getresponse()
        response = response1.read()
        print('获取ticket的响应结果为%s' % str(response))
        headers = response1.getheader('location')
        print('获取ticket的请求头为headers : %s' % str(headers))
        self.Cookie = response1.getheader("Set-Cookie")
        print(type(headers))
        print('headers is %s' % str(headers))
        self.Ticket = str(headers).split("ticket=")[1]
        print('获取ticket')
        print(response1.read())
        return response1.read()

    # 通过ticket获取session
    def __LogIn_By_Ticket(self, ticket):
        ip = self.serverIP
        port = self.serverPort
        print('Calling CSP_LogIn_By_Ticket, '
                          'ip: %s, port: %s, ticket: %s' % (ip, port, ticket))

        # 新版本 url 以及 参数
        # url = self.uriBase + "/unisess/v1/auth?service=%2fauth&ticket=" + ticket
        # params1 = "service=2Funisso%2Fwebsite%2Fhome%2Fhomepage&ticket=" + ticket

        # 老版本登录 url 以及 参数, 供老版本调试使用。
        url = self.uriBase + "/unisess/v1/auth?service=https%3A%2F%2F" + ip + "%3A31943%2Fcspportalwebsite%2F%23%2Fhome&ticket=" + ticket
        params1 = "service=%2Fcspportalwebsite%2F%23%2Fhome&ticket=" + ticket

        self.HttpClient.request("GET", url, params1, self.loginHeader)
        response1 = self.HttpClient.getresponse()
        response1.read()
        headers = response1.getheader('set-cookie')
        print('登录调试')
        print(str(headers))
        # print(str(response1.msg.dict))
        self.bspSession = headers.split("bspsession=")[1].split(";")[0]
        print(response1.read())
        return response1.read()

    # 通过bsSession获取token
    def __LogIn_By_Bspsession_t(self, bspsession):
        ip, port = self.serverIP, self.serverPort
        print('Calling CSP_LogIn_By_Bspsession_t, '
                          'ip: %s, port: %s, bspsession: %s' % (ip, port, bspsession))
        t = str(time.time()).split(".")[0]
        url = self.uriBase + "/unisess/v1/auth/session?t=" + str(t)
        params1 = "t=" + str(t)
        header1 = self.loginHeader.copy()
        # header1["Referer"] = "https://" + ip + ":" + str(port) + "/cspportalwebsite/"
        # header1["Cookie"] = "theme=lightday; locale=zh-cn; bspsession=" + bspsession
        # 新版本要更改
        header1["Referer"] = "https://" + ip + ":" + str(port) + "/unisso/website/home/homepage"
        header1["Cookie"] = "locale=zh-cn; bspsession=" + bspsession
        print('开始获取session')
        print('Bspsession-url',url)

        self.HttpClient.request("GET", url, params1, header1)
        response1 = self.HttpClient.getresponse()
        httpsResponseBody1 = str(response1.read())
        print('httpsResponseBody1',httpsResponseBody1,type(httpsResponseBody1))
        self.Token = httpsResponseBody1.split('":"')[1].split('","')[0]
        self.UserID = httpsResponseBody1.split('"user":{"id":"')[1].split('"')[0]
        self.UserName = httpsResponseBody1.split('"user":{"id":"')[1].split('"name":"')[1].split('"')[0]
        print(self.Token, self.UserID, self.UserName)
        print(response1.read())
        return response1.read()
    def InitSTHeader(self):
        self.SessionTokenHeader = {
            "Accept": '*/*',
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "bspsession": "cspportal",
            "Connection": "close",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": "locale=zh-cn; bspsession=" + self.bspSession + "; theme=lightday",
            "Host": self.serverIP + ":" + str(self.serverPort),
            "namespace": "manage",
            "Origin": "https://" + self.serverIP + ":" + str(self.serverPort),
            "portalLanguage": "zh-cn",
            "Referer": "https://" + self.serverIP + ":" + str(self.serverPort) + "/cspportalwebsite/",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "X-Uni-Crsf-Token": self.Token,
            'clusterId': '00000000-0000-0000-0000-000000000000',
            'language': 'CH'
        }
    def CSP_Login(self,**kwargs):
        # 记录用户名和密码,方便后续更新token
        self.username = kwargs.get('username','admin')
        self.password = kwargs.get('password','Huawei@132')
        self.__LogIn_and_Get_Ticket(self.username, self.password)
        self.__LogIn_By_Ticket(self.Ticket)
        self.__LogIn_By_Bspsession_t(self.bspSession)
        self.InitSTHeader()

    def getResponse(self):
        try:
            response = self.HttpClient.getresponse()
            self.response = response
            self.requestAgain = 0
        except  Exception as e:
            # 重新登入
            print('token过期,重新登入请求')
            if self.requestAgain < 3:
                self.requestAgain += 1
                self.HttpClient.close()
                self.HttpClient = http.client.HTTPSConnection(self.serverIP, self.serverPort, None, None, None, 1000)
                self.CSP_Login(self.username, self.password)
                # 重新请求获取response
                self.request(self.method, self.url, self.body, isAgain=True)
                response = self.getResponse()
            else:
                response = None
        return response

    def handleParams(self, params):
        '''
        处理params为符合格式的字符,目前仅支持处理json格式的字符和字典类型数据
        1. 处理格式
        2. 处理objects属性
        2019/09/27
        # 先存在问题，读取出来的 type：不存在public，只有private和非private，先不做处理
        '''
        params = json.dumps(params)
        return params
    def CSP_ServiceConfig(self, params):
        print('Calling CSP_ServAndInstance, '
                         'ip: %s, port: %s, bspsession: %s,params: %s' % (
                             self.serverIP, self.serverPort, self.bspSession, params))
        # params = self.handleParams(params)
        url = self.uriBase + "/om/v1/configuration"
        print("no handleparams:%s" % params)
        self.request("POST", url, params)
        response1 = self.HttpClient.getresponse()
        response_result = response1.read()
        print("响应: %s" % response_result.decode('UTF-8','strict'))
        return response_result
    def request(self, method, url, body=None, isAgain=False, header=None):
        '''
        :param method: 请求的方式
        :param url: 请求的地址
        :param body: 请求的参数
        :param isAgain: 表示是否是再次请求 : 默认False 表示不是,True 表示是
        '''
        # 每次执行前,先将之前的请求关闭
        if hasattr(self, 'response'):
            self.response.close()
        header = self.SessionTokenHeader
        if not header:
            header = header
        # 如果不是再次请求,将用户的method,url和 body 记录到对象中
        if not isAgain:
            body = self.handleParams(body)
            self.method = method
            self.url = url
            self.body = body
            try:
                self.HttpClient.request(method, url, body, header)
            except  Exception as e:
                print('无法发送请求的原因是: %s' % e)
                print('无法发送请求，重新登陆')
                self.requestAgain += 1
                self.HttpClient.close()
                self.HttpClient = http.client.HTTPSConnection(self.serverIP, self.serverPort, None, None, None, 12)
                self.CSP_Login(self.username, self.password)
                self.HttpClient.request(self.method, self.url, self.body, header)
        else:
            self.HttpClient.request(self.method, self.url, self.body, header)
    def CSP_LoginOut(self):
        ip, port = self.serverIP, self.serverPort
        print('Calling CSP_LoginOut, '
                          'ip: %s, port: %s' % (ip, port))

        url = self.uriBase + "/unisess/v1/logout?service=%2Fcspportalwebsite%2F%23%2Fhome"
        header1 = self.loginHeader.copy()
        header1["Referer"] = "https://" + ip + ":" + str(port) + "/cspportalwebsite/"
        header1["Cookie"] = "locale=zh_cn; bspsession=%s; theme=lightday" % self.bspSession
        params = "/cspportalwebsite/#/home"
        self.HttpClient.request("GET", url, params, header1)
        self.HttpClient.close()

    def CSP_Get_APPID_By_Type(self):
        ip, port = self.serverIP, self.serverPort
        print('Calling CSP_Get_AppVersion, '
                          'ip: %s, port: %s, bspsession: %s' % (ip, port, self.bspSession))
        url = self.uriBase + "/csp/modulekeeper/v1/applications/appVersion"
        self.request('GET', url)
        response1 = self.getResponse()
        a = str(response1.read(), 'utf-8')
        print('CSP_Get_AppVersion-response1',a,type(a))
        info = json.loads(a)
        dataInfo = info.get("data", [])
        print('dataInfo',dataInfo)
        appType = "CloudIVS3000"
        for dInfo in dataInfo:
            curType = dInfo.get("app_type", "")
            if curType == appType:
                self.appID = str(dInfo.get("app_id", "-1"))
                self.appVersion = str(dInfo.get('app_version', '-1'))
                self.appName = str(dInfo.get('app_name', '-1'))
                print('appID',self.appID)
                return self.appID

    def CSP_DomainConfig(self, **kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        print('appID',appID)
        domainName=kwargs.get('domainName','Domain')
        params = {
	"payload": {
		"appid": appID,
		"cmdtype": "Config",
		"oprtype": "Set",
		"service": "IVSBMService",
		"data": {
			"modifiedData": {
				"domain": "%s"%domainName,
				"description": ""
			},
			"originalData": {
				"id": 1,
				"domain": "Domain-0001",
				"description": "null"
			}
		},
		"object": {
			"name": "com.huawei.ivs.bmu.mml.DomainConf",
			"ver": "003",
			"own": "private"
		}
	}
}
        resInfo = self.CSP_ServiceConfig(params)
        print('CSP_DomainConfig-resInfo',resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        return resInfo

    def CSP_DomainConfig(self, **kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        print('appID', appID)
        domainName = kwargs.get('domainName', 'Domain')
        params = {
            "payload": {
                "appid": appID,
                "cmdtype": "Config",
                "oprtype": "Set",
                "service": "IVSBMService",
                "data": {
                    "modifiedData": {
                        "domain": "%s" % domainName,
                        "description": ""
                    },
                    "originalData": {
                        "id": 1,
                        "domain": "Domain-0001",
                        "description": "null"
                    }
                },
                "object": {
                    "name": "com.huawei.ivs.bmu.mml.DomainConf",
                    "ver": "003",
                    "own": "private"
                }
            }
        }
        resInfo = self.CSP_ServiceConfig(params)
        print('CSP_DomainConfig-resInfo', resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        return resInfo
    def getClustersInfo(self):
        clustersInfo = {}
        appID = self.CSP_Get_APPID_By_Type()
        params = {
            "payload": {"appid": appID, "cmdtype": "Maintain", "service": "VCNSvcMgrService", "instances": ["ALL"],
                        "oprtype": "querySurveillancePlatform", "language": "en",
                        "object": {"name": "SMU_CLDINFLIST", "ver": "000", "own": "private"}, "data": {"P1": "21"}}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        print("getClustersInfo",resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg == u'Operation succeeded':
            ClusterList = jsonRes['payload']['objects'][0]['data'][0]['ClusterList'][0]
            clustersInfo['ClusterCode'] = ClusterList['ClusterCode']
        return clustersInfo

    def setClusterConfig(self, **kwargs):

        print('self.getClustersInfo()',self.getClustersInfo())
        clusterCode = str(self.getClustersInfo()['ClusterCode'])
        appID = self.CSP_Get_APPID_By_Type()
        clusterName=kwargs.get('clusterName','MCluster-0001')
        params = {
            "payload": {"appid": appID, "cmdtype": "Maintain", "service": "IVSBMService", "oprtype": "editClusterInfo",
                        "language": "en", "object": {"name": "ClusterMPUConf", "ver": "000", "own": "private"},
                        "data": {"clusterCode": str(clusterCode), "name": str(clusterName),
                                 "isLoadBalance": 0, "isFaultShift": 0, "autoCreatState": "",
                                 "isForward": 2, "sensitivityLimit": "10", "loadBalancingLimit": "10"}}}
        resInfo = self.CSP_ServiceConfig(params)
        print('CSP_DomainConfig-resInfo', resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        return resInfo

    def setVCNDCGService(self):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"cmdtype":"Config","oprtype":"Set","service":"VCNDCGService","object":{"name":"DCG_CFG","ver":"011","own":"private"},"data":{"modifiedData":{"ConfigValue":"0","ConfigSensitiveValue":""},"originalData":{"ConfigName":"ONVIF_HTTPS"}}}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg=="Operation succeeded":
            remas='更改ONVIF HTTP成功'
        else:
            remas = '更改ONVIF HTTP失败'
        print(remas)

    def setVCNSvcMgrService(self):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","service":"VCNSvcMgrService","oprtype":"setAuthType","language":"en","object":{"name":"SMU_DIGEST_AUTHEN_CONFIG","ver":"000","own":"private"},"data":{"extra_domain_docking_authen_type":2,"device_access_authen_type":2,"north_1400_authen_type":2}}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg=="Operation succeeded":
            remas='更改摘要认证算法配置成功'
        else:
            remas = '更改摘要认证算法配置失败'
        print(remas)

    def CSP_Get_LogLevel(self, params):
        print('Calling CSP_Get_LogLevel, '
                         'ip: %s, port: %s, bspsession: %s,params: %s' % (
                             self.serverIP, self.serverPort, self.bspSession, params))
        # params = self.handleParams(params)
        url = self.uriBase + "/Runlog/LogServiceRPC/autoQuery"
        print("params:%s" % params)
        self.request("POST", url, params)
        response1 = self.HttpClient.getresponse()
        response_result = response1.read()
        print("响应: %s" % response_result.decode('UTF-8','strict'))
        return response_result

    def set_LogLevel(self, **kwargs):
        """
        改对应模块的日志级别
        :param moduel: 修改模块服务名称
        :param loglevel: 修改日志级别
        :param kwargs:
        :return: 返回响应体中的state字段，为OK表示修改成功
        """
        appID = self.CSP_Get_APPID_By_Type()
        serviceNameList=['BMU-BMAgent','GaussAPI-BMAgent','GaussCDB-BMAgent','IVSBMService','MNG-BMAgent','MPU-R-BMAgent','MPU-T-BMAgent',
                         'SafeVideo-BMAgent','VCNAPI-BMAgent','VCNApiDSUService','VCNAPIService','VCNDCGService','VCNImgRecService',
                         'VCNImgTransService','VCNMediaRecService','VCNMediaTransService','VCNMpuSvcCtrlService','VCNPCGService',
                         'VCNSafeVideoService','VCNSIPService','VCNSlaveClusterMgrService','VCNSvcMgrService','VCNTVUService','ZK-BMAgent']
        for serviceName in serviceNameList:
            params={"cmd":"MODIFY_LOG_LEVEL","appId":appID,"serviceName":serviceName,"logLevel":"DEBUG","depend":"","namespace":"null","timeout":30}
            resInfo = self.CSP_Get_LogLevel(params)
            print('set_LogLevel-resInfo', resInfo.decode('utf-8'))
            resInfo = eval(resInfo.decode('utf-8'))
        if resInfo["state"]=="OK":
            remas='30minDebug成功'
        else:
            remas = '30minDebug失败'
        return remas

    def modifyConf(self, **kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        clusterName=kwargs.get('clusterName','MCluster-0001')
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","service":"IVSBMService","oprtype":"modifyConf","language":"en","object":{"name":"ConfChannel","ver":"001","own":"private"},"data":{"type":"UseAesCBCAlgorithmV3","confInfo":[{"key":"StreamEncryption","value":"0"},{"key":"VCNMultiDomain","value":"0"},{"key":"UseESDK","value":"0"}]}}}
        resInfo = self.CSP_ServiceConfig(params)
        print('modifyConf-resInfo', resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        if resInfo["returncode"] == "0":
            remas = '加密算法配置开关关闭成功'
        else:
            remas = '加密算法配置开关关闭失败'
        print(remas)
        return remas

    def get2288ServerList(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","oprtype":"get2288ServerList","service":"IVSBMService","object":{"name":"IVSStorageCfg","ver":"000","own":"private"}}}
        resInfo = self.CSP_ServiceConfig(params)
        print('modifyConf-resInfo', resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        NodeList=resInfo['payload']['objects'][0]['data'][0]['NodeList']
        print('NodeList',NodeList)
        return NodeList

    def createRaidGroup(self,**kwargs):
        NodeList=self.get2288ServerList()
        appID = self.CSP_Get_APPID_By_Type()
        for Node in NodeList:
            nodeCode=Node['NodeCode']
            vmID = Node['VmID']
            dockerName = Node['DockerName']
            params = {"payload":{"appid":appID,"cmdtype":"Maintain","oprtype":"createRaidGroup","service":"IVSBMService","object":{"name":"IVSStorageCfg","ver":"000","own":"private"},"data":{"nodeCode":nodeCode,"raidMode":2,"raidConfigMode":0,"operateMode":1,"vmID":vmID,"dockerName":dockerName}}}
            resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg == "Operation succeeded":
            remas = '创建raid组成功'
        else:
            remas = '创建raid组失败'
        print(remas)
        return remas
    def getNodeInfo(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","service":"IVSBMService","oprtype":"getNodeInfo","language":"en","object":{"name":"NodeInfoManager","ver":"000","own":"private"},"data":"null"}}
        resInfo = self.CSP_ServiceConfig(params)
        print('getNodeInfo-resInfo', resInfo.decode('utf-8'))
        resInfo = eval(resInfo.decode('utf-8'))
        getNodeInfo=resInfo['payload']['objects'][0]['data']
        print('getNodeInfo',getNodeInfo)
        return getNodeInfo

    def getserverIpList(self):
        getserverIpList=[]
        getNodeInfo=self.getNodeInfo()
        for NodeInfo in getNodeInfo:
            getserverIpList=getserverIpList+[NodeInfo['serverIp']]
        print('getserverIpList',getserverIpList)
        getserverIpList=list(set(getserverIpList))
        print('getserverIpList',getserverIpList)
        return getserverIpList

    def CSP_UploadThirdPluginZip(self):
        nHeaders = {}
        nHeaders["Cookie"] = self.SessionTokenHeader["Cookie"]
        nHeaders["X-Uni-Crsf-Token"] = self.SessionTokenHeader["X-Uni-Crsf-Token"]
        nHeaders["Content-Type"] = "multipart/form-data;boundary=zhaoxinyuanNBjiuvans"
        appID = self.CSP_Get_APPID_By_Type()
        url = self.uriBase + "/%s/sem/module/uploadModule.do?moduleType=i_dcg" % appID
        zipList=["plugin_dcg_bocong_2.1.0_x86_signature.zip",
                 "plugin_dcg_dahua_2.1.0_x86_signature.zip",
                 "plugin_dcg_hikvision_2.1.0_x86_signature.zip",
                 "plugin_dcg_ifaas_2.1.0_x86_signature.zip",
                 "plugin_dcg_infinov_2.1.0_x86_signature.zip",
                 "plugin_dcg_kedacom_2.1.0_x86_signature.zip",
                 "plugin_dcg_rtsp_2.1.0_x86_signature.zip",
                 "plugin_dcg_uniview_2.1.0_x86_signature.zip"
                 ]

        at = time.time()
        for ziu in zipList:
            # path = "\\\\7.222.113.161\\Distribute\\IVS_V900\develop\\vcn_x86_Plugin\\release\\%s" % (filePa)
            path = ".\\%s"%ziu
            with open(path, 'rb') as f:
                print("本次上传插件是" + ziu)
                m = MultipartEncoder(
                    fields={'tiFile': (path, f, 'multipart/form-data')},
                    boundary='zhaoxinyuanNBjiuvans')
                session = requests.Session()
                session.headers.update(nHeaders)
                res = session.post(url=url, data=m, verify=False)
                print("resis%s" % res)
        bt = time.time()
        print('所有插件上传耗时为%s秒' % str(int(bt - at)))
        try:
            for zi in zipList:
                os.remove(".\\%s"%zi)
        except:
            pass
        return res.text

    def CSP_thirdPlugin_install(self):
        """
        安装第三方插件
        :param appID:1000
        :param code: 插件code编码
        :rtype: object
        """
        appID = self.CSP_Get_APPID_By_Type()
        zipList = ["i_dcg_bocong_bocong_12_2.1.0",
                   "i_dcg_dhsdk_dahua_5_2.1.0",
                   "i_dcg_hiksdk_hikvision_3_2.1.0",
                   "i_dcg_ifaas_ifaas_8_2.1.0",
                   "i_dcg_infinova_infinova_11_2.1.0",
                   "i_dcg_kedasdk_keda_10_2.1.0",
                   "i_dcg_rtsp_huawei_22_2.1.0",
                   "i_dcg_unvsdk_uniview_14_2.1.0"
                   ]
        for zil in zipList:
            params = {"payload": {"appid": appID, "instances": ["ALL"], "cmdtype": "Maintain", "oprtype": "installModule",
                                  "service": "IVSBMService",
                                  "object": {"name": "ModuleConf", "ver": "000", "own": "private"},
                                  "data": {"actionParams": {"allNodes": "allNodes", "aimCode": zil}}}}
            resInfo=self.CSP_ServiceConfig(params)
            print("csp上操作结果为： %s" % resInfo.decode('utf-8'), type(resInfo))
        jsonRes = json.loads(resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg == "Operation succeeded":
            remas = '插件安装与上传成功'
        else:
            remas = '插件安装与上传失败'
        print(remas)
        return remas

    def getOuterIpPool(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","oprtype":"getOuterIpPool","service":"IVSBMService","object":{"name":"OuterIPPoolConf","ver":"001","own":"private"},"data":{}}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        ipEnd = jsonRes['payload']['objects'][0]['data'][0]['ipSegs'][0]['ipEnd']
        print("ipEnd",ipEnd)
        return ipEnd
    def getfloatGWIP(self,**kwargs):
        num=self.getOuterIpPool()
        floatGWIP='.'.join(num.split(".")[0:-1]+[str(int(num.split(".")[-1])+1)])
        print(floatGWIP)
        return floatGWIP
    def VCNMpuSvcCtrlService(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        params = {"payload":{"appid":appID,"instances":["ALL"],"cmdtype":"Maintain","oprtype":"query","service":"VCNMpuSvcCtrlService","object":{"name":"SCU_RECPOLICY","ver":"000","own":"private"}}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        print("VCNMpuSvcCtrlService",jsonRes)
        NodeCode=''
        NodeList=jsonRes['payload']['objects']
        for Node in NodeList:
            print('Node',Node)
            if 'MPUR' in str(Node):
                if Node['data'][0]['payload']['data']['NodeList']['NodeInfo']['ScuId']=='MPUR-0001':
                    NodeCode=Node['data'][0]['payload']['data']['NodeList']['NodeInfo']['NodeCode']
        print("NodeCode",NodeCode)
        return NodeCode

    def setFloatGWIP(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        floatGWIP = self.getfloatGWIP()
        nvrCode=self.VCNMpuSvcCtrlService()
        clusterCode = self.getClustersInfo()['ClusterCode']
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","service":"IVSBMService","oprtype":"setFloatGWIP","language":"en","object":{"name":"ClusterMPUMem","ver":"000","own":"private"},"data":{"clusterCode":clusterCode,"nvrCode":nvrCode,"floatGWIP":floatGWIP},"timeout":"60"}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        returnmsg = jsonRes['returnmsg']
        if returnmsg == "Operation succeeded":
            remas = '浮动网关设置成功'
        else:
            remas = '浮动网关设置失败'
        print(remas)
        return remas
    def getfloatCGCode(self,**kwargs):
        appID = self.CSP_Get_APPID_By_Type()
        clusterCode = self.getClustersInfo()['ClusterCode']
        params = {"payload":{"appid":appID,"cmdtype":"Maintain","service":"IVSBMService","oprtype":"vcnClusterMemberInfo","language":"en","object":{"name":"ClusterVcn","ver":"000","own":"private"},"data":{"clusterNode":clusterCode},"timeout":"60"}}
        resInfo = self.CSP_ServiceConfig(params)
        jsonRes = json.loads(resInfo)
        floatGw=self.getfloatGWIP()
        floatCGCode=''
        for i in jsonRes["payload"]["objects"][0]["data"]:
            if i["floatGw"]==floatGw:
                floatCGCode=i["floatCGCode"]
                break
        print("getfloatCGCode",floatCGCode)
        return floatCGCode


if __name__=="__main__":
    csp=CSP_HTTP_API(serverIP='90.41.42.11')
    res=csp.CSP_Login()
    resInfo = csp.setFloatGWIP()
    print("csp上操作结果为： %s" % resInfo,type(resInfo))
    csp.CSP_LoginOut()
