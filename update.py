# coding: utf-8

"""查看网页是否更新
"""

import requests
import time
from html.parser import HTMLParser

import mail


URL = 'http://1000658.tx2010.cn/article_list.do?cid=2'
LATEST = 'Mon May 09 00:00:00 CST 2016'


class myHtmlParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        # 通过创建两个开关:data和get_data来控制是否将当前tag的data保存到titles列表
        # div_lvl避免<div>嵌套和多次出现，导致endtag误判
        self.data = False
        self.getdata = False
        self.div_lvl = 0
        self.titles = []

    def handle_starttag(self, tag, attrs):
        """当标签里的属性为所需属性时，提取属性值
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname in each[0]:
                    return each[1]
            return None"""

        if tag == 'div':
            self.div_lvl += 1
            for k, v in attrs:
                if k == 'class' and v == 'textlist':
                    self.data = True

        if tag == 'em' and self.data == True:
            self.getdata = True

        if tag == 'a' and self.data == True:
            self.getdata = True

    def handle_endtag(self, tag):
        if tag == 'div':
            self.div_lvl -= 1
            if self.div_lvl == 0:
                self.data = False

        if tag == 'em' and self.getdata == True:
            self.getdata = False

        if tag == 'a' and self.getdata == True:
            self.getdata = False

    def handle_data(self, data):
        if self.getdata == True:
            # print("==={}".format(data))
            self.titles.append(data)


# 判断是否更新,更新的话，获取标题
def get_title(text):
    if not text:
        return None
    updates = myHtmlParser()
    updates.feed(text)
    updates.close()
    # print(updates.titles)
    latest = time.mktime(time.strptime(LATEST.replace('CST', ''),
                                       "%a %b %d %H:%M:%S %Y"))
    i = 0
    update_titles = []
    while i < len(updates.titles):
        timestamp = time.mktime(time.strptime(updates.titles[i].replace('CST', ''),
                                              "%a %b %d %H:%M:%S %Y"))
        if timestamp <= latest:
            return update_titles
        update_titles.append(updates.titles[i+1])
        i += 2
    return update_titles
    """该脚本最开始用正则表达式来处理HTML
    updates = re.findall(r'<em>(.+?)</em>.+?<a.+?">(.+?)</a>', text, re.S)
    # print(updates[0][0])
    if updates[0][0] != "Mon May 09 00:00:00 CST 2016":
        return updates[0][1]
    else:
        return None"""

if __name__ == '__main__':
    r = requests.get(URL)
    # print(type(r.status_code))
    if r.status_code == 200:
        titles = '\n'.join(get_title(r.text))
        action = mail.Mail()
        if titles:
            res = action.send_mail('网页更新：\n{}'.format(titles))
        else:
            res = action.send_mail('没更新')
        print(res)
    else:
        print('链接失败：{}'.format(r.status_code))
