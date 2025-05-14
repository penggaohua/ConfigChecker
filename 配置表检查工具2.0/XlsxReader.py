#coding=utf-8
import xlrd

xlsx_path = r"E:\Common\Config"

class XlsxReader:
    def __init__(self,xlsx_name):
        self.path = xlsx_path
        self.xlsx_name= xlsx_name
        self.ignore_lines = 3;#忽略的行数，一般配置表前3行有特殊作用不做配置，所以读取数据时忽略这3行
        self.xl = xlrd.open_workbook(self.path+"\\"+self.xlsx_name)
        #self.xl = xlrd.open_workbook(self.xlsx_name)
        self.sheet = self.xl.sheet_by_index(0)
        self.column_name_list  = self.get_head_list() #得到表的列名（表头）
        self.num_rows = self.sheet.nrows  # 获取总行数

    #得到列名也就是第一行（表头）
    def get_head_list(self):
        return self.sheet.row_values(0)


    #通过列名得到某一列的数据
    def get_column_list_by_name(self,name):
        #把名字转换成index再通过self.sheet.col_values（index）得到整列数据
        head_list = self.get_head_list()
        if name in head_list:
            index  = head_list.index(name)
            return self.sheet.col_values(index,self.ignore_lines)
        else:
            print("该配置表没有%s列"%name )

    #得到一行的数据
    def get_row_list_by_index(self,index):
        return self.sheet.row_values(index)





if __name__ == '__main__':
    xlrd = XlsxReader("ChapterConfig.xlsx")
    res = xlrd.get_column_list_by_name("id")
    print(res)
