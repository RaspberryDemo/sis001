#!/usr/bin/python
#coding=utf-8

import socket
import socks
import requests
import re
import codecs
import os
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

base_url = 'http://sis001.us/forum/forum-229-%d.html'
keywords = ['Naturals', 'Blacked', 'X-Art', 'Wow', 'Babes', 'Anjelica', 'BLACKED', '18OnlyGirls',
            'SexArt', 'Colette']

socks.set_default_proxy(socks.SOCKS5, "192.168.0.100", 1088)
socket.socket = socks.socksocket
#print(requests.get('http://ifconfig.me/ip').text)

wanted = []
for i in range(1, 30):
    r = requests.get(base_url % i)

    r.encoding = 'gbk'
    html = r.text
    
    soup = BeautifulSoup(html, 'html5lib')
    
    for link in soup.find_all(href=re.compile('^thread')):
        if not link.string:
            continue
        for word in keywords:
            if word in link.string:
                print link.string
                wanted.append({'link': link.get('href'), 'text': link.string})

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(THIS_DIR))
template = env.get_template('template/sis.template')

content = template.render(wanted=wanted)

fp = codecs.open('/home/pi/pywork/boots/templates/sis.html', 'w', 'utf-8')
fp.write(content)
fp.close()
