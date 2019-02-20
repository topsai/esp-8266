#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "范斯特罗夫斯基"
# Email: hurte@foxmail.com
# Date: 2019/2/15
import os
import network
import time
import json
import dht
import machine
from machine import Pin, Timer
import wifi_conn as wifi_config
from umqtt.simple import MQTTClient
import ubinascii
import neopixel
from builtins import hasattr, getattr

temperature_humidity = []
# 智能灯开关对应的GPIO管脚
LED = Pin(2, Pin.OUT, value=1)
d = dht.DHT11(machine.Pin(4))
# rgb灯带
np = neopixel.NeoPixel(machine.Pin(5), 12)
# 关灯
last_color = (255, 255, 255)
color = (0, 0, 0)
for i in range(12):
    np[i] = color
np.write()
net_state = False
# # 初始化LED
# led_pin = Pin(2, Pin.OUT, value=1)

tim = Timer(-1)
print("初始化")

# 每个MQTT的客户端应该使用一个唯一的client_id
"""
topic 命名 
command_topic :clallback方法名+_command_topic
state_topic : command_topic + 'State'
"""

CLIENT_ID = ubinascii.hexlify(machine.unique_id())
command_topic = b"home-assistant/arduino1/laserLight"
state_topic = b"home-assistant/arduino1/laserLightState"
s = "asas"
rgbstate_topic = b"home/rgbState"
rgb_command_topic = b"home/rgb"
ends = '_command_topic'

# 定义于MQTT代理服务器的连接信息
CONFIG = {
    "broker": "10.0.0.13",
    "mqtt_user": "homeassistant",
    "mqtt_password": "hachina",
    "mqtt_topic_command": b"hachina/hardware/led01/switch",
    "mqtt_topic_commands": b"hachina/hardware/led01/state",
    "s": b"asas",
    "ss": b"123",
    "dht11_state": b"home-assistant/window/contact",
}


class option:
    # DHT11
    def get_temp(self):
        d.measure()
        global data
        data = b'{"temperature": "%s", "humidity": "%s"}' % (d.temperature(), d.humidity())
        print('发布温湿度', data)
        return data

    # RGB LIGHT
    def rgb(self, msg):
        # msg = b'{"color": {"r": 255, "b": 236, "g": 182}, "state": "ON"}'
        global r, g, b, last_color, color
        msg = json.loads(msg)
        state = msg.get("state")
        rgb_color = msg.get("color")
        if state == "ON":
            print('rgb on')
            if rgb_color:
                color = (rgb_color['r'], rgb_color['g'], rgb_color['b'])
                last_color = color
            else:
                color = last_color
        else:
            print('rgb off')
            color = (0, 0, 0)
        for i in range(12):
            np[i] = color
        np.write()


def sub_cb(topic, msg):
    global c
    print((topic, msg))
    try:
        # 获取方法名
        fun = topic.decode().split('/')[-1]
        print(fun)
        # 获取方法
        if hasattr(opt, fun):
            fun = getattr(opt, fun)
        fun(msg)
        c.publish(topic + b"State", msg)
    except:
        pass


def run_client():
    global c
    # 创建MQTT的客户端对象
    c = MQTTClient(CLIENT_ID, CONFIG["broker"], user=CONFIG["mqtt_user"], password=CONFIG["mqtt_password"])
    # 设置当订阅的信息到达时的处理函数
    c.set_callback(sub_cb)
    # 连接MQTT代理服务器
    c.connect()
    # 订阅命令信息
    c.subscribe(command_topic)
    c.subscribe(s)
    c.subscribe(rgb_command_topic)
    tim.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: c.publish("office/sensor1", opt.get_temp()))
    # c.subscribe(CONFIG["dht11_state"])
    print("Connected to %s, subscribed to %s topic" % (CONFIG["broker"], CONFIG["mqtt_topic_command"]))
    try:
        while True:
            c.wait_msg()
    finally:
        c.disconnect()


if __name__ == '__main__':
    opt = option()


    def b_link(t):  # period 延时 毫秒
        # 1000 初始化；  100 配置wifi ； 500 ap配置模式； 2000 正常
        tim.init(period=t, mode=Timer.PERIODIC, callback=lambda t: toggle())


    def toggle():
        if LED.value():
            LED.value(0)
        else:
            LED.value(1)


    def init_wifi():  # 重置
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
        # 停止blink
        tim.deinit()
        # 执行代码
        while True:
            try:
                run_client()
            except:
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
