#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
from jinja2 import Environment, FileSystemLoader
from boto.ses.connection import SESConnection
import piconfig

ses = SESConnection(piconfig.AWSID, piconfig.AWSKEY)
env = Environment(loader=FileSystemLoader('./templates/'))

def gettestinfo():
    ''' 取得測試用資料 '''
    u = {
        'user': u'toomore',
        'nickname': u'Toomore Chiang',
        'mail': u'toomore0929@gmail.com',
    }
    return u

def send(info):
    ''' 發送電子報
        :info: dict 包含 [mail, user, nickname]
    '''
    ses.send_email(
        source = 'PI.ISUPHOTO.org Paper <paper@isuphoto.org>',
        subject = u'影像紀錄區電子報 #20121210',
        to_addresses = '{mail}'.format(**info),
        format = 'html',
        return_path = 'suggest@isuphoto.org',
        reply_addresses = 'suggest@isuphoto.org',
        body = template.render(**info),
    )

def output(u):
    ''' 匯出電子報檔案 htm '''
    with open('/run/shm/ppaper.htm','w') as f:
        f.write(template.render(u).encode('utf-8'))

def sendall(sendlist):
    ''' 大量傳送 '''
    for i in sendlist:
        try:
            send(i)
            print i.get('user'),i.get('nickname'),i.get('mail')
        except:
            print u'Error: ',i.get('user'),i.get('nickname'),i.get('mail')

if __name__ == '__main__':
    '''
    python ./t.py output|send|sendall template_files
    '''
    template = env.get_template(sys.argv[2])
    if sys.argv[1] == 'output':
        print u'{0:-^30}'.format(u'匯出電子報')
        output(gettestinfo())
    elif sys.argv[1] == 'send':
        print u'{0:-^30}'.format(u'寄送電子報')
        send(gettestinfo())
    elif sys.argv[1] == 'sendall':
        print u'{0:-^30}'.format(u'大量傳送電子報')
        sendall([gettestinfo(),])
    else:
        print 'output, send, sendall'
    print sys.argv
