# -*- coding: utf-8 -*-
import time
from requests.auth import HTTPDigestAuth
import ssl
import urllib3
import requests
import json
import os
import openpyxl
import urllib
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
env={"北京四":{"ak": "fe46ddffe424132f5e35bd46d8080538",
            "sk": "51316904693aaf653908e5fe09e04e012ebeccc61e423793cc20006558892b94",
            "eudms":"https://api-ivm.myhuaweicloud.com",
            "userid":"85826388920210609172648",
            "apig": "https://api-ivm.myhuaweicloud.com",
            "dmajavaip":"https://api-ivm.myhuaweicloud.com",
            "enterprise_id": "5669365720200916104630",
            "umsip":"https://application.holisens.huawei.com"
            },
     "上海一":{"ak": "df53000fc713409545fe00c2fcff4b2d",
            "sk": "61ba0eb195d06579e3978b60cce1414d2929615845a4c422128288c3ab5036dc",
            "eudms":"https://121.36.193.23:443",
            "userid":"31092853220210609152250",
            # "apig": "https://api-ivm.myhuaweicloud.com"},
            "apig": "https://124.70.158.153:7200",
            "dmajavaip":"https://api-ivm-sh.myhuaweicloud.com",
            "enterprise_id": "116636688920200902142452",
            "umsip":"https://124.70.158.153:443"
            },
     "乌兰":{"ak": "bc72cb4391957521bc9b05252ef6ed0b",
            "sk": "58836ff3a264b5470bf0c1643b71a3d1c9b4319ae3033c72b12aa0fe80c6363a",
            "eudms":"http://100.94.174.66:18090",
            "userid":"64797698520210602101823",
            "apig": '',
            "dmajavaip":"",
           "enterprise_id": "125865530520210114171228",
           "umsip":"https://100.93.28.26:8081"
           },
     "性能": {"ak": "8e6421bdd50ebc5b71a2fa7836c0f8f6",
            "sk": "5506c15ed8aec38926c912ffb5884c0f59ff3a96ca877f21cf792b47ec059c49",
            "eudms": "http://100.85.254.13:18090",
            "userid": "142806919520211102153255",
            "apig": "",
            "dmajavaip": "",
            "enterprise_id": "5669365720200916104630",
            "umsip": ""
            },
     "G42": {"ak": "7447f18719d0ae7087d927d7366c6b2a",
            "sk": "8126a9f130727e76a9cea1f605fd43e9c88d4dcb9ccfb7046be0f4a4cbfbf5c2",
            "eudms": "https://121.37.196.216:443",
            "userid": "29778234920211223064904",
            "apig": "https://api-ivm-gz-g42.myhuaweicloud.com",
            "dmajavaip": "",
            "enterprise_id": "5802624820210826173521",
            "umsip": ""
            },
     "广州特性": {"ak": "420801b0b3fc1a4427181748436296c0",
             "sk": "207235accdb5ee8e40dc575ea44960a7a2d1ec6a1e8957abfb94cc0a4b97805c",
             "eudms": "http://124.71.212.163:18090",
             "userid": "129052444320211025100945",
             "apig": "https://api-ivm-gz-feature.myhuaweicloud.com",
             "dmajavaip": "",
             "enterprise_id": "5802624820210826173521",
             "umsip": ""
             }
     }
class CLOUD():

    def GetToken(self,envType,channels):
        data={
        "ak": env[envType]["ak"],
        "sk": env[envType]["sk"]}
        user_id = CLOUD().GetUserId(envType,channels)
        env[envType]["userid"] = user_id
        url=env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/enterprises/access-token"
        response=requests.post(url,json=data,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        access_token = responsetext['access_token']
        print(access_token)
        return access_token

    def GetUserId(self,envType,channels):
        data = {
            "account": channels[0]['account'],
            "password": channels[0]['password'],
            "app_lan": "zh-CN",
            "app_version": "1.0.0.1.20190101",
            "app_type": 2
        }
        url = env[envType]["umsip"] + "/v2/eums/login"
        response = requests.post(url, json=data, verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************GetUserId-json.dumps.response.text:', jr, type(jr), type(responsetext))
        user_id = responsetext['data']["user_id"]
        print('userid:',user_id)
        return user_id

    def GetHLSURL(self,envType,channels):
        access_token=CLOUD().GetToken(envType,channels)

        url = env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/devices/channels/cloud-live/url"
        isstatic=0
        print("url:",url)
        if "static" in channels[0]['live_protocol']:
            isstatic=1
            channels[0]['live_protocol'] = channels[0]['live_protocol'].split(",")[0]
        if "DEV" in channels[0]['live_protocol']:
            channels[0]['live_protocol'] = channels[0]['live_protocol'].split("_")[0]
        payload = json.dumps({
          "channels": channels
        })
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print("payload",payload,type(payload))
        response = requests.post(url, headers=headers, data=payload,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        if responsetext["channels"][0]["result"]["msg"]== "Success":
            HLSURL = responsetext["channels"][0]["live_url"]
            if isstatic==1:
                HLSURL="rtsp://"+channels[0]['account']+":"+channels[0]['password']+"@"+HLSURL[7:]
        else:
            HLSURL = responsetext["channels"][0]["result"]["msg"]

        print("HLSURL",HLSURL)
        return HLSURL

    def GetHLSHTML(self,envType,channels):
        HLSURL = CLOUD().GetHLSURL(envType,channels)
        HLSHTML='''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>live</title>
    <link href="https://cdn.bootcss.com/video.js/7.6.5/alt/video-js-cdn.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/video.js/6.6.2/video.js"></script>
    <script src="https://cdn.bootcss.com/videojs-contrib-hls/5.15.0/videojs-contrib-hls.min.js"></script>
</head>
<body>
    <video id="myVideo" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" width="1080" height="708" data-setup='{}'>  
        <!-- <source id="source" src="http://d2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.m3u8"  type="application/x-mpegURL">   -->
        <source id="source" src="%s"  type="application/x-mpegURL">
    </video>
</body>
<script>    
    // videojs 简单使用  
    var myVideo = videojs('myVideo',{
        bigPlayButton : true, 
        textTrackDisplay : false, 
        posterImage: false,
        errorDisplay : false,
    })
</script>
</html>'''%HLSURL
        print(HLSHTML)
        path=os.getcwd()
        path=path+"\\live.html"
        print(path)
        if os.path.exists(path):
            os.remove(path)
        HLSHTMLfile=open(path,"w",encoding='utf-8')
        HLSHTMLfile.write(HLSHTML)
        HLSHTMLfile.close()

    def GetPlayBackHLSURL(self,envType,channels,infos):
        access_token=CLOUD().GetToken(envType,channels)
        device_id=channels[0]["device_id"]
        channel_id = channels[0]["channel_id"]
        playback_protocol = channels[0]["playback_protocol"]
        record_type=channels[0]["record_type"]
        start_time = channels[0]["start_time"]
        end_time = channels[0]["end_time"]
        print("GetPlayBackHLSURL,channels",channels)
        rt="&record_type="+record_type
        if "DEV" in playback_protocol:
            if record_type=="ALL_RECORD":
                rt=""
            url = env[envType]["eudms"] + "/v1/" + env[envType][
                "userid"] + "/devices/" + device_id + "/channels/" + channel_id + "/device-records/web-playback-url?" + "start_time=" + start_time + "&end_time=" + end_time+"&protocol="+playback_protocol.split(",")[0]+rt
        else:
            url = env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/devices/"+device_id+"/channels/"+channel_id+"/cloud-records/playback-url?"+"start_time="+start_time+"&end_time="+end_time+"&playback_protocol="+playback_protocol.split(",")[0]+rt
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print("GetPlayBackHLSURL,url:",url)
        response = requests.get(url, headers=headers,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        PlayBackHLSURL = responsetext.get("playback_url",responsetext)
        if "static" in playback_protocol and "playback_url" in responsetext:
            PlayBackHLSURL = "rtsp://"+channels[0]['account']+":"+channels[0]['password']+"@" + PlayBackHLSURL[7:]
        print(PlayBackHLSURL)
        return PlayBackHLSURL

    def GetPlayBackHLSHTML(self,envType,channels,infos):
        PlayBackHLSURL = CLOUD().GetPlayBackHLSURL(envType,channels,infos)
        BackHLSHTML='''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>record</title>
    <link href="https://cdn.bootcss.com/video.js/7.6.5/alt/video-js-cdn.min.css" rel="stylesheet">
    <script src="https://cdn.bootcss.com/video.js/6.6.2/video.js"></script>
    <script src="https://cdn.bootcss.com/videojs-contrib-hls/5.15.0/videojs-contrib-hls.min.js"></script>
</head>
<body>
    <video id="myVideo" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" width="1080" height="708" data-setup='{}'>  
        <!-- <source id="source" src="http://d2zihajmogu5jn.cloudfront.net/bipbop-advanced/bipbop_16x9_variant.m3u8"  type="application/x-mpegURL">   -->
        <source id="source" src="%s"  type="application/x-mpegURL">
    </video>
</body>
<script>    
    // videojs 简单使用  
    var myVideo = videojs('myVideo',{
        bigPlayButton : true, 
        textTrackDisplay : false, 
        posterImage: false,
        errorDisplay : false,
    })
</script>
</html>'''%PlayBackHLSURL
        print("PlayBackHLSURL:",PlayBackHLSURL)
        path=os.getcwd()
        path=path+"\\record.html"
        print(path)
        if os.path.exists(path):
            os.remove(path)
        HLSHTMLfile=open(path,"w",encoding='utf-8')
        HLSHTMLfile.write(BackHLSHTML)
        HLSHTMLfile.close()

    def GetCloudReList(self,envType,channels):
        access_token = CLOUD().GetToken(envType,channels)
        device_id = channels[0]["device_id"]
        channel_id = channels[0]["channel_id"]
        record_type = channels[0]["record_type"]
        live_protocol=channels[0]["live_protocol"]
        start_time = channels[0]["start_time"]
        end_time = channels[0]["end_time"]
        print("GetCloudReList,channels",channels)
        if "DEV" in live_protocol:
            url = env[envType]["eudms"] + "/v1/" + env[envType][
            "userid"] + "/devices/" + device_id + "/channels/" + channel_id + "/device-records?" + "start_time=" + start_time + "&end_time=" + end_time +"&limit=" + "1000"
        else:
            url = env[envType]["eudms"] + "/v1/" + env[envType][
            "userid"] + "/devices/" + device_id + "/channels/" + channel_id + "/cloud-records?" + "start_time=" + start_time + "&end_time=" + end_time + "&record_type=" + record_type

        headers = {
            'Access-Token': access_token,
            'Content-Type': 'application/json'
        }
        print("url:", url)
        response = requests.get(url, headers=headers, verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        GetCloudReList = jr
        print(GetCloudReList)
        return GetCloudReList

    def rtspinfo(self,envType,infos,channels):
        access_token=CLOUD().GetToken(envType,channels)
        url = env[envType]["apig"]+"/v1/"+env[envType]["userid"]+"/media/connection-info"

        payload = json.dumps({
            "media_name": infos.split(",")[0],
            "media_password": infos.split(",")[1],
            "auth_type": infos.split(",")[2]
        })
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print("payload",payload,type(payload))
        respon = requests.post(url, headers=headers, data=payload,verify=False)
        response = requests.get(url, headers=headers, data=payload, verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        return responsetext

    def getstream_ability(self,envType,channels):
        access_token=CLOUD().GetToken(envType,channels)
        device_id=channels[0]["device_id"]
        channel_id = channels[0]["channel_id"]
        url = env[envType]["dmajavaip"] + "/v1/" + env[envType][
            "userid"] + "/devices/" + device_id + "/channels/" + channel_id + "/stream-ability"

        headers = {
          'Content-Type': 'application/json',
            'client-type':'ISV',
            'Authorization': 'Bearer ' + access_token
        }
        print("getstream_ability-headers:",headers)
        print("getstream_ability-uri:", url)
        response = requests.get(url, headers=headers, verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************stream_ability-json.dumps.response.text:', jr, type(jr), type(responsetext))
        return jr

    def getCloudDevlist(self):
        '''
        从xlsx生成
        :return:
        '''
        wb = openpyxl.load_workbook('.\\cloud.xlsx')
        for sdk in wb.sheetnames:
            sheet = wb[sdk]
            devlist = []
            for row in sheet.rows:
                rlist = []
                for r in row:
                    print(r.value)
                    rlist = rlist + [r.value]
                print(rlist,'------')
                devlist.append({
    "device_id" : rlist[0],
    "channel_id" : rlist[1],
    "all_day" : "true"})
            devlist=devlist[1:]
            devlist = {
  "plans" : devlist
}
            print(devlist)
            return devlist

    def setRecordPlan(self,envType,channels):
        access_token=CLOUD().GetToken(envType,channels)
        url = env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/devices/channels/record-plan"
        payload = json.dumps(CLOUD().getCloudDevlist())
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print("payload",payload,type(payload))
        print("url",url)
        response = requests.put(url, headers=headers, data=payload,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        return jr


if __name__=='__main__':
    CLOUD().getCloudlistlist()
