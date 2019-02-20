#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "范斯特罗夫斯基"
# Email: hurte@foxmail.com
# Date: 2019/2/19

from umqtt.simple import MQTTClient
from machine import Pin
import ubinascii
import machine

# 智能灯开关对应的GPIO管脚
LED = Pin(2, Pin.OUT, value=1)

# 每个MQTT的客户端应该使用一个唯一的client_id
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

# 定义于MQTT代理服务器的连接信息
CONFIG = {
    "broker": "10.0.0.14",
    "mqtt_user": "homeassistant",
    "mqtt_password": "hachina",
    "mqtt_topic_command": b"hachina/hardware/led01/switch",
    "mqtt_topic_state": b"hachina/hardware/led01/state",
}


def sub_cb(topic, msg):
    global c
    print((topic, msg))
    if msg == b"ON":
        LED.value(0)
        if "mqtt_topic_state" in CONFIG:
            c.publish(CONFIG["mqtt_topic_state"], b"ON")
    elif msg == b"OFF":
        LED.value(1)
        if "mqtt_topic_state" in CONFIG:
            c.publish(CONFIG["mqtt_topic_state"], b"OFF")


def main():
    global c
    # 创建MQTT的客户端对象
    c = MQTTClient(CLIENT_ID, CONFIG["broker"], user=CONFIG["mqtt_user"], password=CONFIG["mqtt_password"])

    # 设置当订阅的信息到达时的处理函数
    c.set_callback(sub_cb)

    # 连接MQTT代理服务器
    c.connect()

    # 订阅命令信息
    c.subscribe(CONFIG["mqtt_topic_command"])
    print("Connected to %s, subscribed to %s topic" % (CONFIG["broker"], CONFIG["mqtt_topic_command"]))

    try:
        while True:
            c.wait_msg()
    finally:
        c.disconnect()


if __name__ == '__main__':
    main()
