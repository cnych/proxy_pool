# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import time
import re
import requests

try:
    from importlib import reload  # py3 实际不会实用，只是为了不显示语法错误
except:
    import sys  # py2

    reload(sys)
    sys.setdefaultencoding('utf-8')

sys.path.append('../')

from Util.utilFunction import robustCrawl, getHtmlTree
from Util.WebRequest import WebRequest

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """

    def __init__(self):
        pass

    @staticmethod
    def freeProxyFirst(page=10):
        """
        抓取无忧代理 http://www.data5u.com/
        :param page: 页数
        :return:
        """
        url_list = ['http://www.data5u.com/',
                    'http://www.data5u.com/free/',
                    'http://www.data5u.com/free/gngn/index.shtml',
                    'http://www.data5u.com/free/gnpt/index.shtml']
        for url in url_list:
            html_tree = getHtmlTree(url)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    yield ':'.join(ul.xpath('.//li/text()')[0:2])
                except Exception as e:
                    pass

    @staticmethod
    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
                proxy_number)
        request = WebRequest()
        # html = request.get(url).content
        # content为未解码，text为解码后的字符串
        html = request.get(url).text
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    @staticmethod
    def freeProxyThird(days=1):
        """
        抓取ip181 http://www.ip181.com/
        :param days:
        :return:
        """
        url = 'http://www.ip181.com/'
        html_tree = getHtmlTree(url)
        try:
            tr_list = html_tree.xpath('//tr')[1:]
            for tr in tr_list:
                yield ':'.join(tr.xpath('./td/text()')[0:2])
        except Exception as e:
            pass

    @staticmethod
    def freeProxyFourth():
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """
        url_list = ['http://www.xicidaili.com/nn',  # 高匿
                    'http://www.xicidaili.com/nt',  # 透明
                    ]
        for each_url in url_list:
            tree = getHtmlTree(each_url)
            proxy_list = tree.xpath('.//table[@id="ip_list"]//tr')
            for proxy in proxy_list:
                try:
                    yield ':'.join(proxy.xpath('./td/text()')[0:2])
                except Exception as e:
                    pass

    @staticmethod
    def freeProxyFifth():
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        """
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
            # 需要过滤掉<p style="display:none;">的内容
            xpath_str = """.//*[not(contains(@style, 'display: none'))
                                and not(contains(@style, 'display:none'))
                                and not(contains(@class, 'port'))
                                ]/text()
                        """
            for each_proxy in proxy_list:
                try:
                    # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                    ip_addr = ''.join(each_proxy.xpath(xpath_str))
                    port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                    yield '{}:{}'.format(ip_addr, port)
                except Exception as e:
                    pass

    @staticmethod
    def freeProxySixth():
        """
        抓取讯代理免费proxy http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10
        :return:
        """
        url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10'
        request = WebRequest()
        try:
            res = request.get(url).json()
            for row in res['RESULT']['rows']:
                yield '{}:{}'.format(row['ip'], row['port'])
        except Exception as e:
            pass

    @staticmethod
    def freeProxy7():
        """快代理"""
        url = 'http://www.kuaidaili.com/free/inha/{page}/'
        for page in range(1, 100):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)

            for idx in range(1, 15):
                try:
                    ip = tree.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[1]'.format(idx))[0].text
                    port = tree.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[2]'.format(idx))[0].text
                    yield '{}:{}'.format(ip, port)
                except Exception as e:
                    pass

    @staticmethod
    def freeProxy8():
        """快代理"""
        url = 'http://www.kuaidaili.com/free/intr/{page}/'
        for page in range(1, 100):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)

            for idx in range(1, 15):
                try:
                    ip = tree.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[1]'.format(idx))[0].text
                    port = tree.xpath('//*[@id="list"]/table/tbody/tr[{}]/td[2]'.format(idx))[0].text
                    yield '{}:{}'.format(ip, port)
                except Exception as e:
                    pass

    # @staticmethod
    # def freeProxy9():
    #     url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=991105941669949&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=2&an_tr=1&an_an=1&an_ha=1&sep=1'
    #     req = requests.get(url)
    #     result = req.text
    #     result = req.text.split('\n')
    #     for res in result:
    #         yield res
    #     time.sleep(5)

    @staticmethod
    def freeProxy9():  # 需要用代理访问
        url = 'http://www.cnproxy.com/proxyedu{page}.html'
        for page in range(1, 2):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)

            for idx in range(2, 101):
                try:
                    addr = tree.xpath('//*[@id="proxylisttb"]/table[3]/tbody/tr[{}]/td[1]/text()[1]'.format(idx))
                    print addr
                    yield addr
                except Exception as e:
                    pass

    # @staticmethod
    # def freeProxy10():
    #     try:
    #         for idx in range(1, 2000):
    #             url = 'http://www.httpdaili.com/api.asp?ddbh=93353817459342547&noinfo=true&old=1&sl=100'
    #             req = requests.get(url)
    #             for ip in req.text.split('\n'):
    #                 if ip != '':
    #                     yield ip
    #             time.sleep(0.5)
    #     except Exception as e:
    #         print e

    # @staticmethod
    # def freeProxy11():
    #     url = 'http://dev.kuaidaili.com/api/getproxy/?orderid=931107806741688&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=1&method=1&an_an=1&an_ha=1&format=json&sep=1'
    #     req = requests.get(url)
    #     result = req.json()
    #     for res in result['data']['proxy_list']:
    #         yield res
    #     time.sleep(2)

if __name__ == '__main__':
    gg = GetFreeProxy()
    # for e in gg.freeProxyFirst():
    #     print(e)
    #
    # for e in gg.freeProxySecond():
    #     print(e)
    #
    # for e in gg.freeProxyThird():
        # print(e)

    # for e in gg.freeProxyFourth():
    #     print(e)

    # for e in gg.freeProxyFifth():
    #     print(e)

    # for e in gg.freeProxySixth():
    #     print(e)
    for e in gg.freeProxy8():
        print(e)
