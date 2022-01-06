# -*- coding: utf-8 -*-
import time
from requests.auth import HTTPDigestAuth
import ssl
import urllib3
import requests
import json
import os
import openpyxl
import env
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Cloud():
    def __init__(self,*args,**kwargs):
        print("args,kwargs",args,kwargs)
        self.PyQtGUIInfo = kwargs.get("PyQtGUIInfo","PyQtGUIInfo为空")
        self.PyQtGUIInfo = json.dumps(self.PyQtGUIInfo, indent=4, sort_keys=False, ensure_ascii=False)
    def getEnv(self):
        env=self.PyQtGUIInfo
        return env


