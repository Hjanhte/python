import requests
from lxml import etree
import urllib.parse
import os

class BaiduImgSpider:
    def __init__(self):

        # self.yeshu=3
        self.baseurl = "http://pic.netbian.com"
        self.headers = {
            "User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"}

    def getPageUrl(self, url, con):
        # print(url)
        res = requests.get(url, headers=self.headers)
        res.encoding = "utf-8"
        html = res.text
        parseHtml = etree.HTML(html)
        tList = parseHtml.xpath('//div[@class="slist"]/ul/li/a/@href')
        self.getImgUrl(tList, con)
    # 进入图片详情页面

    def getImgUrl(self, tList, con):
        la = len(tList)*self.yeshu
        se = (con-1)/self.yeshu
        for index, t in enumerate(tList):
            tLink = self.baseurl + t
            res = requests.get(tLink, headers=self.headers)
            res.encoding = "utf-8"
            html = res.text
            parseHtml = etree.HTML(html)
            picture = parseHtml.xpath(
                '//div//div[@class="photo-pic"]/a/img/@src')[0]
            # 计算进度
            baifen = str(round((se+(index+1)/la)*100, 2))
            self.writeImage(picture, baifen)

    # 保存图片
    def writeImage(self, picture, baifen):
        path="彼岸图网"
        self.mkdir(path)
        res = requests.get(self.baseurl+picture, headers=self.headers)
        res.encoding = "utf-8"
        html = res.content
        filename = picture[23:]
        with open(path+"/"+filename, "wb") as f:
            f.write(html)
        s1 = "[%-100s]" % ("#"*int(float(baifen)))
        s2 = " %s%%" % baifen
        print(s1+s2, end="\r", flush=True)

    def workOn(self):
        print("+"+"-"*34+"+")
        print("|最新 风景 美女 影视 动物 美食 背景|")
        print("|1    2    3    4    5    6    7   |")
        print("+"+"-"*34+"+")

        dic = {"1": "/new", "2": "fengjing", "3": "meinv", "4": "youxi", "5": "dongman", "6": "yingshi",
               "7": "mingxing", "8": "qiche", "9": "dongwu", "a": "renwu", "b": "meishi", "c": "zongjiao", "d": "beijing"}
        name = input("选择类型:")
        con = 1
        self.yeshu = int(input("输入页数"))
        while con <= self.yeshu:
            if name == "1":
                url = self.baseurl+dic[name]+"/index_%d.html" % con
            else:
                url = self.baseurl+"/4k"+dic[name]+"/index_%d.html" % con
            if con == 1:
                url = url[:-13]
            self.getPageUrl(url, con)
            con += 1

    
    def mkdir(self,path):
        
        path=str(path).strip()
        path=path.rstrip("\\")
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path) 

    



if __name__ == "__main__":
    spider = BaiduImgSpider()
    spider.workOn()
    s1 = "[%s]" % ("#"*100)
    s2 = " 100% 成功!"
    print(s1+s2)
