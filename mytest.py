#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "范斯特罗夫斯基"
# Email: hurte@foxmail.com
# Date: 2019/2/19

import paho.mqtt.client as mqtt
import time

HOST = "10.0.0.14"
PORT = 1883

lcommand_topic = "home-assistant/arduino1/laserLight"
lstate_topic = "home-assistant/arduino1/laserLightState"
scommand_topic = "asas"
sstate_topic = "123"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.publish(lstate_topic)
    client.subscribe(lcommand_topic)
    client.publish(sstate_topic)
    client.subscribe(scommand_topic)


def on_message(client, userdata, msg):
    print(msg.topic + " " + ":" + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.loop_forever()

#
# def client_loop():
#     client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#     client = mqtt.Client(client_id)  # ClientId不能重复，所以使用当前时间
#     client.username_pw_set("admin", "123456")  # 必须设置，否则会返回「Connected with result code 4」
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect(HOST, PORT, 60)
#
#
#
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code " + str(rc))
#     client.subscribe("test")
#
#
# def on_message(client, userdata, msg):
#     print(msg.topic + " " + msg.payload.decode("utf-8"))
#
#
# if __name__ == '__main__':
#     client_loop()
