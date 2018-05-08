# -*-coding:utf-8-*-
import time
import xlwings


def read_excel(in_xlname, in_shtname, in_rowid):
    app_xl = xlwings.App(visible=False)
    # print("Open excel in read_excel", flush=True)
    book_xl = app_xl.books.open(in_xlname)
    sheet_xl = book_xl.sheets(in_shtname)
    if in_rowid == 0:    # get 0 will return number of row
        row = sheet_xl.api.UsedRange.Rows.count
    else:    # return cells of the in_rowid row
        row = sheet_xl.range('A1').expand().value[in_rowid]   # 第一行是列标题，value的index从0开始，expand会得到整个sheet所有行
    app_xl.quit()
    # print("row is : ", row, flush=True)
    return row




