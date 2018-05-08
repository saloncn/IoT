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
desired_caps['appPackage'] = 'com.opple.eu'
desired_caps['appActivity'] = '.aty.WelcomeActivity'
# desired_caps['androidDeviceReadyTimeout'] = '30'
# desired_caps['appWaitActivity'] = '.MainActivity'

credentials = Credentials(
    username='',  # Or myusername@example.com for O365
    password=''
)

account = Account(
    primary_smtp_address='',
    access_type=DELEGATE,
    autodiscover=True,
    credentials=credentials
)


def send_mail():
    # 调用op_android.connect获取appium webdriver对象
    obj_app = op_android.connect(desired_caps)
    # 通过app发送验证码邮件
    xlname = "op_smart_lighting.xlsx"
    shtname = "send_mail"
    random_code = ""
    num_row = read_excel.read_excel(xlname, shtname, 0)
    for i in range(1, num_row):
        cells_row = read_excel.read_excel(xlname, shtname, i)  # 获取每一行数据返回 list类型
        print("cell ", cells_row)
        elem_type = cells_row[0]
        find_type = cells_row[1]
        elem_value = cells_row[2]
        input_value = cells_row[3] if len(cells_row) >= 4 else None
        op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
    png_name = "png/" + time.strftime("%d-%H-%M-%S") + ".png"
    time.sleep(0.5)
    obj_app.get_screenshot_as_file(png_name)
    print(png_name, flush=True)
    op_android.obj_quit(obj_app)

    # APP上点击获取验证码后，开始计时
    start_time = time.time()
    # time.sleep(10)
    # 获取邮件并判断主题与时间是否正确
    is_received = 0
    for i in range(1, 25):
        item = account.inbox.all().order_by('-datetime_received')[0]  # 按照接收时间新老排序后取第一封邮件
        mail_subject = item.subject
        mail_receive_utc = item.datetime_received.strftime("%F %X")
        now_utc = datetime.utcnow().strftime("%F %X")
        # 转换为时间戳比较相差10秒内
        ts_receive = time.mktime(time.strptime(mail_receive_utc, "%Y-%m-%d %H:%M:%S"))
        ts_now = time.mktime(time.strptime(now_utc, "%Y-%m-%d %H:%M:%S"))
        if ts_now - ts_receive <= 10:
            if mail_subject == "OPPLE Account Registration Confirmation.":
                is_received = 1  # 1代表收取成功，0代表收取失败
                random_code = re.search(r'[0-9]{6}', item.body).group()  # 获取正文中的6位验证码
                break
        time.sleep(5)  # 一次sleep 10秒共120秒即2分钟如果未收到邮件则返回失败
    end_time = time.time()
    cost_time = round((end_time - start_time), 2)  # round四舍五入保留两位小数
    rtn_str = "邮件收取成功，用时 " + str(cost_time) + " 秒,验证码：" + random_code if is_received else "120秒内未收取到邮件"
    return rtn_str


def update(obj_app):
    # 调用op_android.connect获取appium webdriver对象
    # obj_app = op_android.connect(app_name, activity_name)
    # 通过app发送验证码邮件
    xlname = "op_smart_lighting.xlsx"
    shtname = "update"
    start_time = 0
    end_time = 0
    update_rst = ""
    rst_appium_do = 1
    num_row = read_excel.read_excel(xlname, shtname, 0)
    for i in range(1, num_row):
        cells_row = read_excel.read_excel(xlname, shtname, i)  # 获取每一行数据返回 list类型
        print("cell ", cells_row)
        elem_type = cells_row[0]
        find_type = cells_row[1]
        elem_value = cells_row[2]
        input_value = cells_row[3] if len(cells_row) >= 4 else None
        if elem_value.find("item_separate_upgrade_btn") != -1:
            op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
            # start_time = time.time()
        #   固件升级指固件从手机通过蓝牙传输到灯上，如果传输从1%成功到100%，即视为成功
        elif elem_value.find("传输固件") != -1 and elem_value.find("传输固件100%") == -1:
            obj_app.implicitly_wait(1)
            for i in range(1, 300):
                # 有个问题查找元素不是每次都1秒超时有时会好几秒甚至10秒
                rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
                if rst_appium_do != 0 and rst_appium_do != "1":
                    print("getText type is : %s" % type(rst_appium_do), flush=True)
                    print("getText is : %s" % rst_appium_do, flush=True)
                    percent = re.search(r'[0-9]{1,3}', rst_appium_do).group()  # 获取正文中的6位验证码
                    print("percent is %s" % percent, flush=True)
                    if int(percent) >= 1:
                        start_time = time.time()
                        print("start time is : %s" % start_time, flush=True)
                        break
                    else:
                        continue
            if rst_appium_do == 0:
                print("出现其他异常", flush=True)
                update_rst = "出现其他异常"
                break
#  elif elem_value.find("固件更新失败") != -1:
        elif elem_value.find("传输固件100%") != -1:
            obj_app.implicitly_wait(400)
            rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
            if int(rst_appium_do) == 1:
                print("升级成功", flush=True)
                update_rst = "固件升级成功"
            else:
                print("升级失败", flush=True)
                update_rst = "固件升级失败"
            # print("start fail searching", flush=True)
            # obj_app.implicitly_wait(50)
            # rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
            # if rst_appium_do == 1:
            #     print("固件更新失败", flush=True)
            #     update_rst = "固件更新失败"
            # elif rst_appium_do == 0:
            #     print("start ok searching", flush=True)
            #     obj_app.implicitly_wait(800)
            #     rst_appium_do = op_android.appium_do(obj_app, "button", "textContains", "固件升级成功", None)
            #     obj_app.implicitly_wait(30)
            #     if rst_appium_do == 1:
            #         print("升级成功", flush=True)
            #         update_rst = "固件升级成功"
            #     elif rst_appium_do == 0:
            #         print("升级出现其他情况", flush=True)
            #         update_rst = "升级出现其他情况"
            end_time = time.time()
        else:
            op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)

    # 固件更新失败
    png_name = "d:/" + time.strftime("%d-%H-%M-%S") + ".png"
    time.sleep(0.5)
    obj_app.get_screenshot_as_file(png_name)
    print(png_name, flush=True)

    # APP上点击逐个升级后开始计时

    # time.sleep(10)
    # 获取邮件并判断主题与时间是否正确
    cost_time = round((end_time - start_time), 2)  # round四舍五入保留两位小数
    # cost_time = int(end_time) - int(start_time)  # round四舍五入保留两位小数
    # op_android.obj_quit(obj_app)
    # op_serial.op_serial_write()
    # rtn_str = "邮件收取成功，用时 " + str(cost_time) + " 秒,验证码：" + random_code if is_received else "120秒内未收取到邮件"
    rtn_str = update_rst + ",用时 " + str(cost_time) + " 秒"
    print("result : %s" % rtn_str, flush=True)
    return rtn_str

# 注销账户
# 安装者/管理员
# 邮箱
# 验证码
# 获取验证码
# 登录
#
# 验证码与邮箱不匹配，请再试一次(302)
# 好的
