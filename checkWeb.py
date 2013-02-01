#!/usr/bin/env python
import sys
from subprocess import Popen, PIPE
import urllib
import argparse



def sendRTX(message):
    sendStr = "http://im.ec3s.net:8012/SendNotify.cgi?receiver=1980&msg=" + message + "&title=crmURLCheckERR"
    Popen(["curl", sendStr], stdout=PIPE, stderr=PIPE).communicate()[0]


parser = argparse.ArgumentParser()
parser.add_argument("url_list", help="Name of the file contains the list of urls to check")
parser.add_argument("-s", "--sendRTX", help="Send error message through RTX", action="store_true")
args = parser.parse_args()

listFile = '%s/%s' % (sys.path[0], args.url_list)
lines = open(listFile).readlines()
for l in lines:
    if l.strip() == '':
        continue
    try:
        url, shouldCode = tuple(l.strip().split(' '))
        code = urllib.urlopen(url).getcode()
        if int(shouldCode) != int(code):
            sys.stdout.write('E')
            if args.sendRTX:
                sendRTX(url)
        else:
            sys.stdout.write('.')
    except Exception, e:
        print 'E' + str(e)
        if args.sendRTX:
            sendRTX(url + str())

