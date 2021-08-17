# -*- coding: utf-8 -*-
from requests.auth import HTTPDigestAuth
import ssl
import urllib3
import requests
import json
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class NVR():
	def getGbt28181(self,**kwargs):
		SDCIP=kwargs.get("SDCIP","")
		url = 'https://%s:443/API/Web/Login'%SDCIP
		print('url',url)
		response = requests.post(url, auth=HTTPDigestAuth('admin', 'Huawei@IVM123'),verify=False)
		headers = response.headers
		res=json.loads(response.text)
		print(res,type(res))

		print("headers",headers,type(headers))
		session=headers["Set-Cookie"][8:-23]
		csrftoken=headers['X-csrftoken']
		print(session,csrftoken)
		headers = {'Cookie':'session=%s'%session,'X-csrftoken':'%s'%csrftoken
				   }

		url = 'https://%s:443/API/NetworkConfig/T28181/Get'%SDCIP
		print('url', url, headers)
		print('headers', headers)
		response = requests.post(url, headers=headers,verify=False)
		res=json.loads(response.text)
		print(res,type(res))
		return res
	def setGbt28181(self,**kwargs):
		SDCIP = kwargs.get("SDCIP", "")
		serverIp=kwargs.get("serverIp", "")
		prename=''.join(SDCIP.split('.')[-2:]).zfill(6)
		print(prename)
		loginName=prename+'00001320000001'
		json={
	'enable': 1,
	'mediaType': 6,
	'audioInTransType': 0,
	'encryptionType': 0,
	'isDeleteRepeatStream': 1,
	'h265Enable': 1,
	'loginName': loginName,
	'serverIp': serverIp,
	'serverPort': 5080,
	'portRange': 1,
	'serverMinPort': 0,
	'serverMaxPort': 10000,
	'deviceID': loginName,
	'localPort': 5800,
	'productName': prename+'00002000000001',
	'loginDomain': prename+'0000',
	'password': 'HuaWei123',
	'interfaceIndex': 0,
	'expiration': 3600,
	'heartBeatInterval': 60,
	'heartBeatCount': 3,
	'streamId': 0,
	'channelId': prename+'00001310000001',
	'multiChannelNum': 0,
	'alarmInId': [{
		'index': 0,
		'channelId': prename+'00001340000001'
	},
	{
		'index': 1,
		'channelId': ''
	},
	{
		'index': 2,
		'channelId': ''
	},
	{
		'index': 3,
		'channelId': ''
	}],
	'audioOutId': [{
		'index': 0,
		'channelId': ''
	}],
	'gb35114_INFO': {
		'gb35114Enable': 0,
		'gb35114EffectiveTime': 600,
		'gb35114SignCheckEnable': 0
	},
	'softwareVersion': {
		'verSoftware': 'SDC9.0.RC1.SPC1.B002',
		'verUboot': 'U-Boot2016.11',
		'verKernel': 'Linux4.19.41',
		'verHardware': 'B'
	},
	'protocolVersion': 0,
	'backupServer': {
		'backupServerID': '',
		'backupServerIP': '',
		'backupServerPort': 5060,
		'backupServerDomain': ''
	},
	'shLandMarkEnable': 0
}

		url = 'https://%s/SDCAPI/V1.0/Gbt28181/PlatformParam?ServerType=3'%SDCIP
		print(json)
		response = requests.put(url, json=json,auth=HTTPDigestAuth('ApiAdmin', 'HuaWei123'),verify=False)
		res=response.text
		print(res,type(res))
		return loginName
	def getSDCIP(self,**kwargs):
		SDCIP=kwargs.get("SDCIP","")
		url = 'http://%s/SDCAPI/V1.0/NetworkIaas/NetPortPara?ulMeshIndex = 0'%SDCIP
		response = requests.get(url, auth=HTTPDigestAuth('ApiAdmin', 'HuaWei123'))
		res=json.loads(response.text)
		print(res,type(res))
		return res
	def setSDCIP(self,**kwargs):
		try:
			SDCIP = kwargs.get("SDCIP", "")
			toSDCIP=kwargs.get("toSDCIP","")
			gateWayAddress=kwargs.get("gateWayAddress","")
			json=self.getSDCIP(SDCIP=SDCIP)
			url = 'https://%s/SDCAPI/V1.0/NetworkIaas/NetPortPara?ulMeshIndex=0'%SDCIP
			print(json)
			sjson=json.copy()
			sjson["IPAddress"]=toSDCIP
			sjson["gateWayAddress"] = gateWayAddress
			# sjson["gateWayAddress"]='.'.join(toSDCIP.split('.')[:-1]+["1"])
			print("sjson",sjson)
			response = requests.put(url, json=sjson,auth=HTTPDigestAuth('ApiAdmin', 'HuaWei123'),verify=False,timeout=2)
			res=response.text
			print(res,type(res))
			StatusString=res[-40:-5]
		except:
			StatusString="超时"
		return StatusString

if __name__=='__main__':
	# res=SDC().setSDCIP(SDCIP="51.32.66.216", toSDCIP="51.32.66.211", gateWayAddress="51.32.64.1")
	# res = SDC().getGbt28181(SDCIP="10.58.74.54")
	res = NVR().getGbt28181(SDCIP="10.58.74.47")
	print(res)