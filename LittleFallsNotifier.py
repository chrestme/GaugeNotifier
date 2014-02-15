#!/usr/bin/python
#-*- encoding: utf-8 -*-

import pycurl
import xml.etree.ElementTree as ET
import StringIO
import os

#Get XML data from USGS site
c = pycurl.Curl()
c.setopt(pycurl.URL, "http://waterservices.usgs.gov/nwis/iv/?format=waterml,1.1&sites=01646500&period=PT2H&parameterCd=00060,00065,00010")
b = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, b.write)
c.perform()

#Read XML data into tree structure
root = ET.fromstring(b.getvalue())

#Set Gauge Title Info
title_content = root[1][0][0].text

#Set Temp Data and convert to degrees F
degF = 9.0/5.0*float(root[1][2][0].text)+32.0

#Set Stage data and calculate change in last hour
stageFirst = root[3][2][0].text
stageLast = root[3][2][3].text
stageDelta = float(stageLast) - float(stageFirst)
stageUnit = root[3][1][4][0].text
sign = ''
if (stageDelta > 0.00):
    #up arrow
    sign = u"\u25b2"
elif (stageDelta < 0.00):
    #down arrow
    sign = u"\u25bc"
stageChangeInfo = sign + str(abs(stageDelta)) + " ft/h"


#Set Flow data
flow = root[2][2][0].text
flowUnit = root[2][1][4][0].text
if (flowUnit == "ft3/s"):
    flowUnit = "ft³/s"

message_content = stageFirst+' '+stageUnit+'\t'+flow+' '+flowUnit+'\t'+str(degF)+"\xc2\xb0 F\t" + stageChangeInfo.encode('utf-8')
clickthru_url = "http://waterdata.usgs.gov/usa/nwis/uv?01646500"
#print title_content
#print message_content

os.system("terminal-notifier -message \"%s\" -title \"%s\" -open \"%s\"" % (message_content, title_content, clickthru_url))
