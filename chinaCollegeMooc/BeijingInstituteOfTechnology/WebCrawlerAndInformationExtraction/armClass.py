#coding:utf-8
import random
userList=['lin','zhou','li']
class warm:
    def __init__(self):
        self.useragent=random.choice(userList)
    def getpost(self):
        useragent = self.useragent
        print(useragent)

warm().getpost()