import pandas as pd




#所有检查类的父类，如果没有实现就会打印“暂不支持”
class ConfigCheckerBase:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.sheet_name = None
        self.column_letter=None


    def init_checker(self,sheet_name,column_letter=None):
        self.sheet_name= sheet_name
        self.column_letter=column_letter
        self.df = pd.read_excel(self.file_path,sheet_name=sheet_name,header=None,dtype=str,)



    def check_column(self,sheet_name,column_name):
        return "暂不支持"

    def check_sheet(self,sheet_name):
        return "暂不支持"

    def check_table(self):
        return "暂不支持"



ccb = ConfigCheckerBase("c:")


