# -*-coding:utf-8-*-
import tailer
import time
from datetime import datetime
import threading
import serial
from op.op_file import write_txt

rtn_str = ""
com_name = "COM11"
baud = 115200
byte_size = 8
stop_bits = 1
sl = serial.Serial()

def op_serial_open():
    global  sl
    sl.port = com_name
    sl.baudrate = baud
    sl.bytesize = byte_size
    sl.stopbits = stop_bits
    sl.open()

def op_serial_write(in_str):
    global sl
    times = 1
    a = bytes(in_str, encoding='utf-8')
    while times <= 10800:
        print("now is ", times)
        times += 1
        sl.write(a)
        time.sleep(0.3)


def op_serial_listen():
    global sl
    while True:
        line = sl.readline()
        str_line = line.decode()
        if str_line:

            now_time = datetime.now().strftime("%F %X.%f >>> ")
            str_line = now_time + str_line
            write_txt.write_txt("serial.log", str_line)


def op_serial_close():
    global sl
    sl.close()



def op_log_speech(in_logname):
    global rtn_str
    for log_str in tailer.follow(open(in_logname), delay=0.5):
        if log_str.find("SendCmdToVoiceModule") >= 0:   # 默认HandleVoiceCmd都能正确接到，只判断是否有反馈发送出来
            send_str = log_str[log_str.find("SendCmdToVoiceModule"):log_str.find(",")]
            time_str = time.strftime("%F %X ")
            rtn_str = str(time_str) + str(send_str)
            # print("123", rtn_str)


def op_real_log(in_module, in_function):
    log_name = "d:\\speech.txt"
    timer = None
    if in_module == "op_speech":
        if in_function == "op_speech":
            timer = threading.Timer(1, op_log_speech, [log_name])  # 第三个参数是第二个参数所指函数的传参，以list类型给出
        elif in_function == "op_longlisten":
            timer = threading.Timer(1, op_log_speech, [log_name])
    elif in_module == "op_other":
        return 0
    if timer is not None:
        timer.start()
        time.sleep(5)
        timer.cancel()
        # print("789")
    global rtn_str
    # print("456", rtn_str)
    return rtn_str
