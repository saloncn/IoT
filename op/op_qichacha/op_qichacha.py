# -*-coding:utf-8-*-
import time
# import os
import sys
from op.op_android import op_android
from op.op_file import read_excel
from op.op_file import write_excel
from op.op_file import read_txt
from op.op_file import write_txt

desired_caps = {}
desired_caps['deviceName'] = '0123456789ABCDEF'  # meizu MX6
# desired_caps['udid'] = '0815f8259c5e2302'   #  meizu MX6
desired_caps['platformName'] = 'Android'
desired_caps['newCommandTimeout'] = '240'
desired_caps['version'] = '5.1'
desired_caps['noReset'] = 'True'
desired_caps['unicodeKeyboard'] = 'True'
desired_caps['resetKeyboard'] = 'True'
desired_caps['appPackage'] = 'com.android.icredit'
desired_caps['appActivity'] = 'com.android.icredit.ui.SplashActivity'
# desired_caps['androidDeviceReadyTimeout'] = '30'
# desired_caps['appWaitActivity'] = '.MainActivity'

cur_dir = sys.path[0] + "\\"


def get_info():
    global obj_app
    # 调用op_android.connect获取appium webdriver对象
    # 通过app发送验证码邮件
    # xlname = cur_dir + "op_qichacha.xlsx"
    # shtname = "get_info"
    txtname = cur_dir + "op_qichacha.txt"
    start_time = time.time()
    now_time = 0
    # update_rst = ""
    # rst_appium_do = 1
    # num_row = read_excel.read_excel(xlname, shtname, 0)
    mobile_list = read_txt.read_txt(txtname)
    # for i in range(1, num_row):
    for mobile in mobile_list:
        mobile = mobile.strip("\n")
        now_time = time.time()
        if now_time - start_time > 3600:   #  每隔3600秒重启一次APPIUM,因为NODE对APPIUM做了内存限制64位1.9G，32位1G，运行时间长会导致内存溢出
            start_time = time.time()
            obj_app.quit()
            op_android.restart_appium()
            obj_app = op_android.connect(desired_caps)
        print("Now test: ", mobile)
        # print("Now test : %d" % i)
        # cells_row = read_excel.read_excel(xlname, shtname, i)  # 获取每一行数据返回 list类型
        # print("cell ", cells_row)
        # phone_num = str(int(cells_row[0]))
        try:
            obj_app.implicitly_wait(20)
            obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("品牌名等")').click()
            time.sleep(1)
            obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("地址等关键词")').send_keys(mobile)
            # obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("地址等关键词")').send_keys(phone_num)
        except Exception as e:
            png_name = "png/" + time.strftime("%d-%H-%M-%S") + ".png"
            time.sleep(0.5)
            obj_app.get_screenshot_as_file(png_name)
            print(png_name, flush=True)
            continue
        try:
            obj_app.implicitly_wait(1)
            obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("法定代表人")')
        except Exception as e:
            try:
                obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("经营者")')
            except Exception as e:
                try:
                    obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("执行事务合伙人")')
                except Exception as e:
                    try:
                        obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("负责人")')
                    except Exception as e:
                        rst_str = "no"
                        print("Not find %s" % e, flush=True)
                    else:
                        rst_str = obj_app.find_elements_by_xpath('//*[@text="负责人"]/../*')[1].text
                else:
                    rst_str = obj_app.find_elements_by_xpath('//*[@text="执行事务合伙人"]/../*')[1].text
            else:
                rst_str = obj_app.find_elements_by_xpath('//*[@text="经营者"]/../*')[1].text
        # obj_app.find_element_by_android_uiautomator('new UiSelector().textContains("法定代表人")')
        else:
            rst_str = obj_app.find_elements_by_xpath('//*[@text="法定代表人"]/../*')[1].text
            # rst_str = obj_app.find_elements_by_xpath('//*[@text="经营者"]/../*')[1].text
            # print("number is %s and name is %s" % (phone_num, rst_str))
        print("number is %s and name is %s" % (mobile, rst_str))
        # out_cell = "B" + str(i+1)
        # write_excel.write_excel(xlname, shtname, out_cell, rst_str)

        write_txt.write_txt(txtname, mobile+","+rst_str)
        obj_app.find_element_by_android_uiautomator('new UiSelector().className("android.widget.ImageButton")').click()


try:
    obj_app = op_android.connect(desired_caps)
    get_info()
except Exception as e:
    print("\r\n%s >> %s" % (time.strftime("%F %X"), e ))
finally:
    obj_app.quit()
#         if elem_value.find("item_separate_upgrade_btn") != -1:
#             op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
#             # start_time = time.time()
#         #   固件升级指固件从手机通过蓝牙传输到灯上，如果传输从1%成功到100%，即视为成功
#         elif elem_value.find("传输固件") != -1 and elem_value.find("传输固件100%") == -1:
#             obj_app.implicitly_wait(1)
#             for i in range(1, 300):
#                 # 有个问题查找元素不是每次都1秒超时有时会好几秒甚至10秒
#                 rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
#                 if rst_appium_do != 0 and rst_appium_do != "1":
#                     print("getText type is : %s" % type(rst_appium_do), flush=True)
#                     print("getText is : %s" % rst_appium_do, flush=True)
#                     percent = re.search(r'[0-9]{1,3}', rst_appium_do).group()  # 获取正文中的6位验证码
#                     print("percent is %s" % percent, flush=True)
#                     if int(percent) >= 1:
#                         start_time = time.time()
#                         print("start time is : %s" % start_time, flush=True)
#                         break
#                     else:
#                         continue
#             if rst_appium_do == 0:
#                 print("出现其他异常", flush=True)
#                 update_rst = "出现其他异常"
#                 break
# #  elif elem_value.find("固件更新失败") != -1:
#         elif elem_value.find("传输固件100%") != -1:
#             obj_app.implicitly_wait(400)
#             rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
#             if int(rst_appium_do) == 1:
#                 print("升级成功", flush=True)
#                 update_rst = "固件升级成功"
#             else:
#                 print("升级失败", flush=True)
#                 update_rst = "固件升级失败"
#             # print("start fail searching", flush=True)
#             # obj_app.implicitly_wait(50)
#             # rst_appium_do = op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
#             # if rst_appium_do == 1:
#             #     print("固件更新失败", flush=True)
#             #     update_rst = "固件更新失败"
#             # elif rst_appium_do == 0:
#             #     print("start ok searching", flush=True)
#             #     obj_app.implicitly_wait(800)
#             #     rst_appium_do = op_android.appium_do(obj_app, "button", "textContains", "固件升级成功", None)
#             #     obj_app.implicitly_wait(30)
#             #     if rst_appium_do == 1:
#             #         print("升级成功", flush=True)
#             #         update_rst = "固件升级成功"
#             #     elif rst_appium_do == 0:
#             #         print("升级出现其他情况", flush=True)
#             #         update_rst = "升级出现其他情况"
#             end_time = time.time()
#         else:
#             op_android.appium_do(obj_app, elem_type, find_type, elem_value, input_value)
#
#     # 固件更新失败
#     png_name = "d:/" + time.strftime("%d-%H-%M-%S") + ".png"
#     time.sleep(0.5)
#     obj_app.get_screenshot_as_file(png_name)
#     print(png_name, flush=True)
#
#     # APP上点击逐个升级后开始计时
#
#     # time.sleep(10)
#     # 获取邮件并判断主题与时间是否正确
#     cost_time = round((end_time - start_time), 2)  # round四舍五入保留两位小数
#     # cost_time = int(end_time) - int(start_time)  # round四舍五入保留两位小数
#     # op_android.obj_quit(obj_app)
#     # op_serial.op_serial_write()
#     # rtn_str = "邮件收取成功，用时 " + str(cost_time) + " 秒,验证码：" + random_code if is_received else "120秒内未收取到邮件"
#     rtn_str = update_rst + ",用时 " + str(cost_time) + " 秒"
#     print("result : %s" % rtn_str, flush=True)
#     return rtn_str

