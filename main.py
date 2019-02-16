#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "范斯特罗夫斯基"
# Email: hurte@foxmail.com
# Date: 2019/2/15
import os
import network
import time
import machine
from machine import Pin, Timer
import wifi_conn as wifi_config

net_state = False
# 初始化LED
led_pin = Pin(2, Pin.OUT, value=1)

tim = Timer(-1)
print("初始化")


# period 延时 毫秒
def b_link(t):
    # 1000 初始化；  100 配置wifi ； 500 ap配置模式； 2000 正常
    tim.init(period=t, mode=Timer.PERIODIC, callback=lambda t: toggle())


def toggle():
    if led_pin.value():
        led_pin.value(0)
    else:
        led_pin.value(1)


# 重置
def init_wifi():
    try:
        os.remove('config.py')
    except:
        pass
    machine.reset()


b_link(1000)
print('init - blink - 1000')
# 判断是否存在wifi账号密码配置文件
file_list = os.listdir()
print(file_list)
if 'config.py' in file_list:
    import config

    if config.SSID and config.PWD:
        print('have config ,action conn wifi.....')
        b_link(100)
        net_state = wifi_config.wifi(config.SSID, config.PWD)

# 网络配置成功
if net_state:
    print('every thin is ok !')
    b_link(2000)
    pass
# 网络配置未完成
else:
    print('config state.')
    b_link(500)
    try:
        os.remove('config.py')
    except:
        pass
    # 进入 ap 模式
    wifi_config.ap(True)
    # 配置 wifi
    wifi_config.web_server()
