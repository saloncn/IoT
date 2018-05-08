# -*-coding:utf-8-*-
import traceback
import configparser
import sys
import time
import threading
from op.op_file import read_excel
from op.op_file import write_excel
from op.op_serial import op_serial

# 读取预配置
cf = configparser.ConfigParser(interpolation=None)
cf.read("pre.ini")
xlname = cf.get('IoT', 'xlname')
shtnames = cf.get('IoT', 'shtname')
logname = cf.get('log', 'logname')

# 全局变量
out_log = ""
dyn_module = ""
fun_name = ""


# 根据所调用的模块及函数去获取相关串口日志
def get_log(in_module, in_fun):
    global out_log
    out_log = op_serial.op_real_log(in_module, in_fun)


def do_case(in_fun, in_give, in_want):
    global dyn_module
    # print("give is %s type is %s" % (in_give, type(in_give)), flush=True)
    # 可以考虑换种方式，两个参数都传为空时就直接传None传入
    if in_want is None and in_give is not None:  # EXCEL中的空单元格读到Python中认为是None
        get_value = getattr(dyn_module, in_fun)(in_give)  # 动态执行函数
    elif in_give is None and in_want is not None:
        get_value = getattr(dyn_module, in_fun)(in_want)  # 动态执行函数
    elif in_give is None and in_want is None:
        get_value = getattr(dyn_module, in_fun)()  # 动态执行函数
    else:
        get_value = getattr(dyn_module, in_fun)(in_give, in_want)  # 动态执行函数
    # eval(fun_str)(in_value)
    return get_value


def main(in_xlname, in_shtname):
    global module_name
    global fun_name
    global logname
    # 将异常日志输出到指定文件
    saveout = sys.stdout
    fsock = open(logname, 'a+')
    sys.stdout = fsock
    try:
        num_row = read_excel.read_excel(in_xlname, shtname, 0)
        cols = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G'}  # 将列从数据转换成字母
        for i in range(1, num_row):
            print('>>>>>>>>Read row %d>>>>>>>>' % i, flush=True)
            fsock.flush()
            cells_row = read_excel.read_excel(in_xlname, shtname, i)  # 获取每一行数据返回 list类型
            # cells_row = str(cells_row)
            print("cells are : ", cells_row, flush=True)
            is_test = cells_row[1]
            fun_name = cells_row[2]
            input_give = cells_row[3] if len(cells_row) >= 4 else None  # 判断cells_row长度小于3时赋值None
            input_want = cells_row[4] if len(cells_row) >= 5 else None  # 判断cells_row长度小于4时赋值None
            if int(is_test) == 0:
                continue
            print('>>>>>>>>Run the %d case>>>>>>>>' % i, flush=True)
            fsock.flush()
            # 调用相关模块函数之前将日志捕获功能get_log打开，利用定时器多线程与do_case同时运行
            timer = threading.Timer(0, get_log, [module_name, fun_name])
            timer.start()
            # out_log = get_log(module_name, fun_name)
            out_value = do_case(fun_name, input_give, input_want)
            timer.cancel()
            if out_value == "" and out_log == "":
                continue
            if out_value != "":
                cell = cols.get(6) + str(i + 1)  # 有效内容从第二行开始，第一行是列名称
                write_excel.write_excel(in_xlname, shtname, cell, out_value)
            if out_log != "":
                cell = cols.get(7) + str(i + 1)
                write_excel.write_excel(in_xlname, shtname, cell, out_log)
    except Exception as e:
        print("\r\n%s >> %s" % (
            time.strftime("%F %X"), (str(module_name) + '.' + str(fun_name))))  # 当前日期时间2018-03-30 15:43:22
        traceback.print_exc(file=sys.stdout)
        fsock.flush()
    finally:
        sys.stdout = saveout
        fsock.close()


if __name__ == "__main__":
    for shtname in shtnames.split(","):
        dyn_module = __import__(shtname)
        module_name = dyn_module
        main(xlname, shtname)


