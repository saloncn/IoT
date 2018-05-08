# -*-coding:utf-8-*-
from datetime import datetime
from exchangelib import DELEGATE, Account, Credentials
import re
import time
from op.op_android import op_android
from op.op_file import read_excel
from op.op_file import write_excel
from op.op_serial import op_serial


# global variable
desired_caps = {}
desired_caps['deviceName'] = '0123456789ABCDEF'  # meizu MX6
# desired_caps['udid'] = '0815f8259c5e2302'   #  meizu MX6
desired_caps['platformName'] = 'Android'
desired_caps['newCommandTimeout'] = '240'
desired_caps['version'] = '5.1'
desired_caps['noReset'] = 'True'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
desired_caps['appPackage'] = 'no.nordicsemi.android.mcp'
desired_caps['appActivity'] = '.DeviceListActivity'
# desired_caps['androidDeviceReadyTimeout'] = '30'
desired_caps['appWaitActivity'] = '.MainActivity'

obj_app = op_android.connect(desired_caps)
time.sleep(10)
obj_app.quit()
