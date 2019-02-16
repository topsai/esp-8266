#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "范斯特罗夫斯基"
# Email: hurte@foxmail.com
# Date: 2019/2/15
import time
import network
import machine


def test():
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.scan()  # scan for access points
    wlan.isconnected()  # 判断是否连接
    wlan.connect('essid', 'password')  # connect to an AP
    wlan.config('mac')  # get the interface's MAC adddress
    wlan.ifconfig()  # get the interface's IP/netmask/gw/DNS addresses

    ap = network.WLAN(network.AP_IF)  # create access-point interface
    ap.active(True)  # activate the interface
    ap.config(essid='ESP-AP')  # set the ESSID of the access point


def wifi(ssid, pwd):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, pwd)  # connect to an AP
        while not wlan.isconnected():
            time.sleep(2)
        print('network config:', wlan.ifconfig())
        return True
    except:
        return False


def ap(state):
    # 开启 ap 模式
    ap = network.WLAN(network.AP_IF)
    if state:
        ap.active(True)  # activate the interface
        ap.config(essid='ESP-AP-FFFFFF', authmode=network.AUTH_WPA_WPA2_PSK, password="12345678")
    else:
        ap.active(False)


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('CU_FAN', ':abc1234567')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def web_server():
    import socket
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>智能家居</title>
    </head>
    <body>
    <label>SSID:<input id="SSID" name="SSID"></label><br/>
    <label>PWD:<input id="PWD" name="PWD"></label><br/>
    <button class="getbtn btn">GET请求</button>
    </body>
    <script type="text/javascript">
        //get请求
        document.querySelector(".getbtn").onclick = function () {
            let xmlhttp = new XMLHttpRequest();
            let ssid = document.getElementById('SSID').value;
            let pwd = document.getElementById('PWD').value;
            // get方法带参数是将参数写在url里面传过去给后端
            xmlhttp.open("GET", "/?SSID=" + ssid + "&PWD=" + pwd, true);
            xmlhttp.setRequestHeader("SSID", ssid);
            xmlhttp.setRequestHeader("PWD", pwd);
            console.log(xmlhttp);
            xmlhttp.send();
            // readyState == 4 为请求完成，status == 200为请求陈宫返回的状态
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                    let data = xmlhttp.responseText;
                    document.write(data);
                    console.log(data);
                }
            }
        };
    
    </script>
    
    </html>
    """

    ok = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>智能家居</title>
    </head>
    <body>
        <p> OK 设置完成 !</p>
        <p>正在重启...</p>
    </body>
    </html>
    """

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    while True:
        conn, addr = s.accept()
        print('client connected from', addr)
        request = conn.recv(1024)
        if request:
            print(request)
            request = request.decode()
            # request = request.decode()
            method = request.split(' ')[0]
            print('nethod----->', method)
            print('all-data======>', request.split(' '))
            data = request.split(' ')[1]
            if 'SSID' in data and 'PWD' in data:
                print("ssid in data ")
                data = data[7:]
                ssid, pwd = data.split('&PWD=')
                print('SSID:', ssid)
                print('PASSWORD:', pwd, type(pwd))
                f = open('config.py', 'w')
                f.write('SSID = "%s"\nPWD = "%s"' % (ssid, pwd))
                f.close()
                conn.sendall(ok)
                conn.close()
                # 配置wifi账号密码成功
                # 关闭 ap 模式
                network.WLAN(network.AP_IF).active(False)
                # 重启
                print('restart !!!')
                machine.reset()
        print("send html")
        conn.sendall(html)
        print("send html ok")
        conn.close()
