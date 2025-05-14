import pytest
import re
from collections import Counter
from xlutils.copy import copy
import xlrd
import xlwt
import time

class ConfigCheckerXlsx:
    def __init__(self,check_table):
        #一般配置表前3行是表头，不参与检查
        self.ignore_row = 3
        self.check_table =  check_table
        self.oldwb = xlrd.open_workbook(check_table)
        self.newWb = copy(self.oldwb)
        self.newWbs = self.newWb.get_sheet(0)


    # 索引检查
    def check_reference(self, list_checK,column_name, com_table_name,com_column_name,com_column_list,row,column):
        # list_check 被检查的列
        # com_talbe_name 需要索引到的表名
        # com_column_name 需要索引到的列名
        print("check reference")
        res_list= list()
        for index, sub in enumerate(list_checK):
            if sub not in com_column_list:
                res_list.append(index+self.ignore_row+1)
        if(len(res_list)==0):
            self.newWbs.write(row, column, "pass")
        else:
            self.newWbs.write(row,column,'{0}列    第{1}行  无法索引到  {2}表的{3}列'.format(column_name,res_list,com_table_name,com_column_name))

    # 为空检查
    def check_null(self, list_check,column_name,row,column):
        print("check null")
        res_list= list()
        self.newWbs.write(row, column,"pass")
        for index, sub in enumerate(list_check):
            if(len(str(sub).strip()) == 0):
                res_list.append(index+self.ignore_row+1)
        if (len(res_list) == 0):
            self.newWbs.write(row, column, "pass")
        else:
            self.newWbs.write(row,column,' {0}列  第{1}行  为空 '.format(column_name,res_list))

    # 重复检查
    def check_repeat(self, list_check,column_name,row,column):
        print("check repeat")

        if(list_check==None):
            self.newWbs.write(row,column, "{0}为空".format(list_check))
        else:
            if (len(set(list_check)) == len(list_check)):#set() 的长度和原来的相等说明没有重复项
                self.newWbs.write(row,column, "pass")
                return

        counter_list_check = Counter(list_check)
        repeat_item = [key for key,value in counter_list_check.items() if value>1] #得到重复元素的列表
        res_str= str()
        for item in repeat_item:
            item_repeat_row = [i+self.ignore_row+1 for i,sub in enumerate(list_check) if sub == item]
            res_str+='   {0}列   {1}   在{2}行重复\n  '.format(column_name,item,item_repeat_row)
        self.newWbs.write(row,column ,res_str)


    # 格式检查
    # 检查指定列是否符合给定的正则表达式
    def check_regex(self,list_check,regex ,column_name,row,column):
        print("check regex")
        self.newWbs.write(row, column, 'pass')
        res_list= list()
        for index, sub in enumerate(list_check):
            #sub= str(sub)
            pattern = re.compile(regex)
            if pattern.fullmatch(sub)==None:
                res_list.append(index+self.ignore_row+1)

        if (len(res_list) == 0):
            self.newWbs.write(row, column, "pass")
        else:
            self.newWbs.write(row, column, ' {0}列  第{1}行  格式有误'.format(column_name, res_list))

    # 值域检查
    def check_range(self,list_check,min,max,column_name,row,column):
        #被检查的内容必须是数值
        #todo 考虑字符也可以装换成数字
        res_list = list()

        for  index,sub  in enumerate(list_check):
            if len(str(sub).strip()) != 0:
                num = float(sub)
            if(num<min or num>max or len(str(sub).strip()) == 0):
                res_list.append(index+self.ignore_row+1)
        if(len(res_list)==0):
            self.newWbs.write(row,column,'pass')
        else:
            self.newWbs.write(row,column,' {0}列  第{1}行  超出预期范围[{2} ,{3}]'.format(column_name,res_list,min,max))


    def save_xls(self):
        time_str= time.time()
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime(time.time()))
        self.newWb.save("result/result"+now+".xls")

