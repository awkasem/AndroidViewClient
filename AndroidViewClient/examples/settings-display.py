#! /usr/bin/env monkeyrunner
'''
Copyright (C) 2012  Diego Torres Milano
Created on Aug 15, 2012

@author: diego
'''


import re
import sys
import os

# This must be imported before MonkeyRunner and MonkeyDevice,
# otherwise the import fails.
# PyDev sets PYTHONPATH, use it
try:
    for p in os.environ['PYTHONPATH'].split(':'):
       if not p in sys.path:
          sys.path.append(p)
except:
    pass
    
try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass
from com.dtmilano.android.viewclient import ViewClient, View

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice


START_ACTIVITY = True
FLAG_ACTIVITY_NEW_TASK = 0x10000000

package='com.android.settings'
activity='.Settings'
componentName=package + "/" + activity

device, serialno = ViewClient.connectToDeviceOrExit()

if START_ACTIVITY:
    device.startActivity(component=componentName, flags=FLAG_ACTIVITY_NEW_TASK)
    MonkeyRunner.sleep(3)

vc = ViewClient(device=device, serialno=serialno)
vc.dump()
# this may help you find the attributes for specific Views
#vc.traverse(vc.getRoot())
text = 'Display'
view = vc.findViewWithText(text)
if view:
	print view.__smallStr__()
	print view.getCoords()
	print view['layout:mLeft'], ',', view['layout:mTop']
else:
	print "Not found"
