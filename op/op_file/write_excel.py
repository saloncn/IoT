# -*-coding:utf-8-*-
import xlwings


def write_excel(in_xlname, in_shtname, in_cell, in_value):
    app_xl = xlwings.App(visible=False)
    # print("Open excel in write_excel", flush=True)
    book_xl = app_xl.books.open(in_xlname)
    sheet_xl = book_xl.sheets(in_shtname)
    sheet_xl.range(in_cell).value = in_value
    book_xl.save()
    app_xl.quit()


def write_cells(in_xlname, in_shtname, in_cells, in_values):
    app_xl = xlwings.App(visible=False)
    # print("Open excel in write_excel", flush=True)
    book_xl = app_xl.books.open(in_xlname)
    sheet_xl = book_xl.sheets(in_shtname)
    for i in range(len(in_cells)):
        sheet_xl.range(in_cells[i]).value = in_values[i]
    book_xl.save()
    app_xl.quit()

