# -*-coding:utf-8-*-
import sys

# read all txt contents to a list variable
def read_txt(in_txt_name):
    f_txt = open(in_txt_name, "r")
    rtn_rst = f_txt.readlines()
    f_txt.close()
    return rtn_rst

