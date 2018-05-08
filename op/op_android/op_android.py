# -*-coding:utf-8-*-
import time
import subprocess
from appium import webdriver


appium_log = "appium.log"
f = open(appium_log, 'w')

def preWifiCfg():
    desired_caps = {}
    desired_caps['deviceName'] = '4PS4WGDQCAH69LGI'
    desired_caps['platformName'] = 'Android'
    desired_caps['newCommandTimeout'] = '240'
    desired_caps['version'] = '5.1'
    desired_caps['noReset'] = 'True'
    desired_caps['appPackage'] = 'com.android.settings'
    desired_caps['appActivity'] = 'com.oppo.settings.SettingsActivity'
    ad = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    ad.find_element_by_name('WLAN').click()
    ad.find_element_by_name('MERCURY_EF36').click()
    try:
        ad.find_element_by_id('com.coloros.wirelesssettings:id/password').send_keys('12345678')
        time.sleep(1)
        ad.find_element_by_name('连接').click()
    except Exception as e:
        pass

    time.sleep(5)
    ad.quit()


def start_appium():
    global f
    if f.closed:
        f = open(appium_log, 'w')
    cmd_str = '"C:\\Program Files (x86)\\Appium\\node.exe" "C:\\Program Files (x86)\\Appium\\node_modules\\appium\\lib\\server\\main.js"  --address 127.0.0.1 --port 4723 --session-override --platform-name Android --platform-version 23 --automation-name Appium --log-no-color'
    # subprocess.Popen(cmd_str, shell=True)
    subprocess.Popen(cmd_str, shell=True, stdout=f.fileno())
    time.sleep(5)


def stop_appium():
    global f
    cmd_str = 'taskkill /im node.exe /f'
    subprocess.Popen(cmd_str, shell=True)
    f.close()
    # child = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE)



def restart_appium():
    stop_appium()
    time.sleep(3)
    start_appium()


def connect(in_caps):
    desired_caps = in_caps
    restart_appium()
    appium_conn = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    appium_conn.implicitly_wait(10)
    return appium_conn


def appium_do(in_obj, in_elem_type, in_find_type, in_elem_value, in_input_value):
        obj_app = in_obj
        rst_str = "1"
        try:
            if in_elem_type == "input":
                if in_find_type == "text":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().text("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "textContains":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "textMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textMatches("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "textStartsWith":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textStartsWith("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "resourceId":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().resourceId("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "resourceIdMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().resourceIdMatches("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "className":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().className("' + in_elem_value + '")').send_keys(in_input_value)
                elif in_find_type == "classNameMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().classNameMatches("' + in_elem_value + '")').send_keys(in_input_value)
            elif in_elem_type == "button":
                if in_find_type == "text":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().text("' + in_elem_value + '")').click()
                elif in_find_type == "textContains":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("' + in_elem_value + '")').click()
                elif in_find_type == "textMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textMatches("' + in_elem_value + '")').click()
                elif in_find_type == "textStartsWith":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textStartsWith("' + in_elem_value + '")').click()
                elif in_find_type == "resourceId":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().resourceId("' + in_elem_value + '")').click()
                elif in_find_type == "resourceIdMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().resourceIdMatches("' + in_elem_value + '")').click()
                elif in_find_type == "className":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().className("' + in_elem_value + '")').click()
                elif in_find_type == "classNameMatches":
                    obj_app.find_element_by_android_uiautomator('new UiSelector().classNameMatches("' + in_elem_value + '")').click()
            elif in_elem_type == "getText":
                rst_str = obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("' + in_elem_value + '")').text
        except Exception as e:
                print("\r\n%s >>" % (time.strftime("%F %X")), flush=True)  # 当前日期时间2018-03-30 15:43:22
                print(e, flush=True)
                return 0
        else:
            print("typeeeeee is %s" % type(rst_str), flush=True)
            return rst_str


def obj_quit(in_obj):
    obj_app = in_obj
    obj_app.quit()
    stop_appium()

