# -*-coding:utf-8-*-
import winspeech
import time


# def open_excel(p_xlname):
#     try:
#         xldata = xlrd.open_workbook(p_xlname)
#         return xldata
#     except Exception:
#         print("\r\n %s >> %s : " % (time.strftime("%F %X"), sys._getframe().f_code.co_name))
#         traceback.print_exc(file=sys.stdout)


# def get_sheet_byname(p_xlname, p_shtname):
#     xlbook = open_excel(p_xlname)
#     xlsht = xlbook.sheet_by_name(p_shtname)
#     return xlsht

# def run():
#     try:
#         # init from pre.ini
#         cf = configparser.ConfigParser(interpolation=None)
#         cf.read("pre.ini")
#
#         xlname = cf.get("excel", "xlname")
#         shtname = cf.get("excel", "shtname")
#         logname = cf.get("log", "logname")
#
#         saveout = sys.stdout
#         fsock = open(logname, 'a+')
#         sys.stdout = fsock
#
#         xlsht = get_sheet_byname(xlname, shtname)
#         rowNums = xlsht.nrows
#         # ls_tmpxls = []
#         for i in range(rowNums - 1):
#             row = i + 1
#             t_value = xlsht.cell_value(row, 1)
#             t_elemType = xlsht.cell_value(row, 2)
#             t_findType = xlsht.cell_value(row, 3)
#             t_findStr = xlsht.cell_value(row, 4)
#             # time.sleep(2)
#             if t_findType == 'class':
#                 by_class_name(t_elemType, t_value, t_findStr)
#             elif t_findType == 'css':
#                 by_css(t_elemType, t_value, t_findStr)
#             elif t_findType == 'xpath':
#                 by_xpath(t_elemType, t_value, t_findStr)
#             elif t_findType == 'id':
#                 by_id(t_elemType, t_value, t_findStr)
#             elif t_findType == 'name':
#                 by_name(t_elemType, t_value, t_findStr)
#             elif t_findType == 'sleep':
#                 time.sleep(int(t_value))
#             elif t_findType == 'refresh':
#                 br.refresh()
#
#     except e_run:
#         print("\r\n%s >> " % time.strftime("%F %X"))  # 当前日期时间2018-03-30 15:43:22
#         traceback.print_exc(file=sys.stdout)
#     finally:
#         sys.stdout = saveout
#         fsock.close()


# appName = 'com.iflyrec.tjapp'
# activityName = 'bl.welcome.view.WelcomeActivity'
#
#
# def cfgCaps(in_app, in_activity):
#     desired_caps = {}
#     desired_caps['deviceName'] = '4PS4WGDQCAH69LGI'
#     desired_caps['platformName'] = 'Android'
#     desired_caps['newCommandTimeout'] = '240'
#     desired_caps['version'] = '5.1'
#     desired_caps['noReset'] = 'True'
#     desired_caps['unicodeKeyboard'] = 'True'  # 输入时使用appium,不使用系统安装的其他输入法
#     desired_caps['resetKeyboard'] = 'True'
#     desired_caps['appPackage'] = in_app
#     desired_caps['appActivity'] = in_activity
#     return desired_caps
#
#
# def defWebDriver(in_caps):
#     ad = webdriver.Remote('http://127.0.0.1:4723/wd/hub', in_caps)
#     ad.implicitly_wait(10)
#     ad.find_element_by_android_uiautomator('new UiSelector().text("开始录音")').click()
#     ad.find_element_by_android_uiautomator('new UiSelector().resourceId("com.iflyrec.tjapp:id/starRecord")').click()
#     time.sleep(5)
#     ad.find_element_by_android_uiautomator('new UiSelector().resourceId("com.iflyrec.tjapp:id/starRecord")').click()
#     print(ad.find_element_by_android_uiautomator('new UiSelector().resourceId("com.iflyrec.tjapp:id/contentTxt")').text)
#     ad.quit()

phrase = ''


def callback(in_phrase, listener):
    global phrase
    winspeech.say("再见")
    phrase = in_phrase
    print("%s TTS : %s" % (time.strftime("%F %X"), phrase), flush=True)
    listener.stop_listening()


#  实现语音指令发出，及语音反馈获取
def op_speech(in_give, in_want):
    for_value = [str(in_want).strip()]
    listener = winspeech.listen_for(for_value, callback)
    winspeech.say(str(in_give))
    time.sleep(5)
    listener.stop_listening()
    global phrase
    return phrase


def special_callback(in_phrase, listener):
    global phrase
    phrase = in_phrase
    print("%s TTS : %s" % (time.strftime("%F %X"), phrase), flush=True)
    winspeech.say("I get %s" % phrase)
    listener.stop_listening()


# 没有语音指令发出，只监听兴趣语音反馈
def op_longlisten(in_want):
    for_value = [str(in_want).strip()]
    listener = winspeech.listen_for(for_value, special_callback)
    # listener = winspeech.listen_for_anything(any_callback)
    while listener.is_listening():
        print('%s : Listening ... ' % time.strftime("%F %X"), flush=True)
        time.sleep(5)
    global phrase
    return phrase



