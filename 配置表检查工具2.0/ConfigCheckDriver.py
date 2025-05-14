from Tools.XlsxReader import  XlsxReader
from Tools.ConfigBase import  ConfigBase
from Tools.ConfigCheckerXlsx import  ConfigCheckerXlsx
import pytest

config_path= "E:\Common\Config\\"

configChecker =ConfigCheckerXlsx("E:\Common\Config\checklist.xlsx")
xlsxReader_checklist = XlsxReader("checklist.xlsx")

for  index  in  range(1,xlsxReader_checklist.num_rows):
    check_row  =  xlsxReader_checklist.get_row_list_by_index(index)

    table_name =check_row[0]
    xlsxReader_table = XlsxReader(table_name)

    column_name_list =list()
    if check_row[1] == "ALL":
        column_name_list = xlsxReader_table.get_head_list()
    else:
        column_name_list =check_row[1].split(";")

    # action  关键字驱动
    action  = check_row[2]
    for index_column_name_list,column_name in  enumerate(column_name_list):
        list_check = xlsxReader_table.get_column_list_by_name(column_name)
        if action == "check_repeat":
            configChecker.check_repeat(list_check, column_name, index, 4+index_column_name_list)
        elif action == "check_null":
            configChecker.check_null(list_check,column_name,index,4+index_column_name_list)
        elif action == "check_range":
            range_list = check_row[3].split(";")
            configChecker.check_range(list_check,float(range_list[0]),float(range_list[1]),column_name,index,4+index_column_name_list)
        elif action == "check_regex":
            regex = check_row[3]
            configChecker.check_regex(list_check,regex,column_name,index,4+index_column_name_list)
        elif action == "check_reference":
            com_table_info = check_row[3].split(";")
            com_table_name = com_table_info[0]
            com_column_name = com_table_info[1]
            com_column_list =XlsxReader(com_table_name).get_column_list_by_name(com_column_name)
            configChecker.check_reference(list_check,column_name,com_table_name,com_column_name,com_column_list,index,4+index_column_name_list)



        configChecker.save_xls()
