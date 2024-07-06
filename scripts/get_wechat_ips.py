# !/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@文件        :get_wechat_ips.py
@时间        :2024/05/23 09:51:33
@作者        :tx
@版本        :1.0
@说明        :获取微信服务器IP地址
"""


import os
from wechatpy import WeChatClient


def get_wechat_ips():
    client = WeChatClient(
        os.environ["APPID"], os.environ["APPSECRET"]
    )  # appid, appsecret
    ips = client.misc.get_wechat_ips()

    with open("./rule-providers/wechat.txt","r+") as f:
        data = f.read()
        for ip in ips:
            if ip not in data:
                f.write("  - IP-CIDR,{}/32\n".format(ip))


def main():
    get_wechat_ips()


if __name__ == "__main__":
    main()
