# -*-coding:utf-8-*-
import sys


def write_txt(in_txt_name, in_value):
    f_txt = open(in_txt_name, "a+")
    f_txt.write(in_value)   # 参数只能是string不能是list
    f_txt.write("\r\n")
    f_txt.close()
