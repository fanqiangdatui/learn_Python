# -*- coding: utf-8 -*-
import time

from requests.auth import HTTPDigestAuth
import ssl
import urllib3
import requests
import json
import os
import urllib
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
env={"北京四":{"ak": "102559065820210301100052",
    "sk": "1025590658202103011000526d4ae1087cf14e008fbed45818411c87",
    "eudms":"https://api-ivm.myhuaweicloud.com",
    "userid":"85826388920210609172648"},
     "上海一":{"ak": "df53000fc713409545fe00c2fcff4b2d",
    "sk": "61ba0eb195d06579e3978b60cce1414d2929615845a4c422128288c3ab5036dc",
    "eudms":"https://121.36.193.23:443",
    "userid":"31092853220210609152250"
                      }
     }
class CLOUD():

    def GetToken(self,envType):
        data={
        "ak": env[envType]["ak"],
        "sk": env[envType]["sk"]}
        url=env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/enterprises/access-token"
        response=requests.post(url,json=data,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        access_token = responsetext['access_token']
        print(access_token)
        return access_token
    def GetHLSURL(self,envType,channels):
        access_token=CLOUD().GetToken(envType)

        url = env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/devices/channels/cloud-live/url"

        payload = json.dumps({
          "channels": channels
        })
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print(type(payload))
        response = requests.post(url, headers=headers, data=payload,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        HLSURL = responsetext["channels"][0]["live_url"]
        print(HLSURL)
        return HLSURL

    def GetHLSHTML(self,envType,channels):
        HLSURL = CLOUD().GetHLSURL(envType,channels)
        HLSHTML='''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>m3u8实况</title>
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
        path=path+"\\HLSHTML.html"
        print(path)
        if os.path.exists(path):
            os.remove(path)
        HLSHTMLfile=open(path,"w",encoding='utf-8')
        HLSHTMLfile.write(HLSHTML)
        HLSHTMLfile.close()

    def GetPlayBackHLSURL(self,envType,channels):
        access_token=CLOUD().GetToken(envType)
        device_id=channels[0]["device_id"]
        channel_id = channels[0]["channel_id"]
        playback_protocol = channels[0]["playback_protocol"]
        start_time = channels[0]["start_time"]
        end_time = channels[0]["end_time"]

        url = env[envType]["eudms"]+"/v1/"+env[envType]["userid"]+"/devices/"+device_id+"/channels/"+channel_id+"/cloud-records/playback-url?"+"start_time="+start_time+"&end_time="+end_time+"&playback_protocol="+playback_protocol
        headers = {
          'Access-Token': access_token,
          'Content-Type': 'application/json'
        }
        print("url:",url)
        response = requests.get(url, headers=headers,verify=False)
        responsetext = json.loads(response.text)
        jr = json.dumps(json.loads(response.text), indent=4, sort_keys=False, ensure_ascii=False)
        print('************json.dumps.response.text:', jr, type(jr), type(responsetext))
        PlayBackHLSURL = responsetext["playback_url"]
        print(PlayBackHLSURL)
        return PlayBackHLSURL

    def GetPlayBackHLSHTML(self,envType,channels):
        PlayBackHLSURL = CLOUD().GetPlayBackHLSURL(envType,channels)
        BackHLSHTML='''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>m3u8实况</title>
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
        path=path+"\\PlayBackHLSHTML.html"
        print(path)
        if os.path.exists(path):
            os.remove(path)
        HLSHTMLfile=open(path,"w",encoding='utf-8')
        HLSHTMLfile.write(BackHLSHTML)
        HLSHTMLfile.close()

    def GetCloudReList(self,envType,channels):
        access_token = CLOUD().GetToken(envType)
        device_id = channels[0]["device_id"]
        channel_id = channels[0]["channel_id"]
        record_type = channels[0]["record_type"]
        start_time = channels[0]["start_time"]
        end_time = channels[0]["end_time"]

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