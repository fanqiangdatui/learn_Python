import json


class sdk():
    def sdkaddtxt(self,**kwargs):
        nvrCode=kwargs.get('nvrCode','0')
        tasCode = kwargs.get('tasCode', '0')
        tasIP = kwargs.get('tasIP', '0')
        connectCode = kwargs.get('connectCode', '0')
        deviceOperInfos={
                    "deviceOperInfo": [
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "Huawei@132",
                                "deviceUser": "admin",
                                "protocolType": "DHSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 37777,
                                    "name": "1_大华SD_42",
                                    "domainCode": "",
                                    "code": "00000000000000010000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.56.160.42",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "Huawei@132",
                                "deviceUser": "admin",
                                "protocolType": "ONVIF",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 80,
                                    "name": "2_ONVIF_SD_21",
                                    "domainCode": "",
                                    "code": "00000000000000020000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.85.158.21",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "HuaWei123",
                                "deviceUser": "admin",
                                "protocolType": "HWSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 6060,
                                    "name": "3_华为路_233",
                                    "domainCode": "",
                                    "code": "00000000000000030000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.85.108.233",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "HuaWei123",
                                "deviceUser": "admin",
                                "protocolType": "UNVSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 80,
                                    "name": "4_宇视_18",
                                    "domainCode": "",
                                    "code": "00000000000000040000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.56.160.18",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "HuaWei123",
                                "deviceUser": "admin",
                                "protocolType": "HIKSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 8000,
                                    "name": "5_海康SD_50",
                                    "domainCode": "",
                                    "code": "00000000000000050000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "51.32.28.50",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "HuaWei123",
                                "deviceUser": "admin",
                                "protocolType": "IFAAS",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 8000,
                                    "name": "6_云天励飞_141",
                                    "domainCode": "",
                                    "code": "00000000000000060000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.85.158.141",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "root",
                                "deviceUser": "root",
                                "protocolType": "AXISSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 80,
                                    "name": "7_安迅士_139",
                                    "domainCode": "",
                                    "code": "00000000000000070000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "90.85.158.139",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "maxDirectConnectNum": 3,
                                "devicePassword": "HuaWei123",
                                "deviceUser": "admin",
                                "protocolType": "HIKSDK",
                                "enableSchedule": 1,
                                "enableAlarm": 0,
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 8000,
                                    "name": "8_海康4K_68",
                                    "domainCode": "",
                                    "code": "00000000000000080000",
                                    "type": 1,
                                    "ipInfo": {
                                        "ip": "51.32.28.68",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        },
                        {
                            "deviceConfig": {
                                "devicePassword": "HuaWei123",
                                "tasCode": tasCode,
                                "deviceUser": "admin",
                                "protocolType": "T28181",
                                "loginType": 0,
                                "enableSchedule": 1,
                                "tasIP": {
                                    "ip": tasIP,
                                    "ipType": 0
                                },
                                "enableAlarm": 0,
                                "deviceRegPassword": "HuaWei123",
                                "nvrCode": nvrCode,
                                "deviceBasicInfo": {
                                    "port": 5080,
                                    "code": "00000000000000090000",
                                    "name": "9_T28181_213",
                                    "connectCode": connectCode,
                                    "type": 1,
                                    "parentCode": "",
                                    "ipInfo": {
                                        "ip": "",
                                        "ipType": 0
                                    }
                                }
                            },
                            "sequence": 1
                        }
                    ]
                }
        print("deviceOperInfos协议相机",json.dumps(deviceOperInfos))
        return deviceOperInfos
    def sdkdeltxt(self):
        deviceCodeList={
            "deviceCode": [
                "00000000000000010000",
                "00000000000000020000",
                "00000000000000030000",
                "00000000000000040000",
                "00000000000000050000",
                "00000000000000060000",
                "00000000000000070000",
                "00000000000000080000",
                "00000000000000090000"
            ]
        }
        return deviceCodeList