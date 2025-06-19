from Tools.ConfigChecker import ConfigChecker
from Tools.XlsxReader import XlsxReader
import pytest


class ConfigBase:


    def setup_class_base(self,talbe_name):
        self.check_table =talbe_name
        self.xlsxReader = XlsxReader(self.check_table)
        self.configChecker = ConfigChecker()


    @pytest.fixture()
    def get_head_list(self):
        return self.xlsxReader.get_head_list()


    #为空检查
    def check_null(self,column_name):
       pass#为空检查服务器已经做了
       #  column_list = self.xlsxReader.get_column_list_by_name(column_name)
       # # self.configChecker.check_null(column_list,self.check_table,column_name)  #为空检查
       #  self.configChecker.check_null(column_list,self.check_table,column_name)  #为空检查


    #重复检查
    def check_repeat(self,column_name):
        print(self.check_table)
        column_list = self.xlsxReader.get_column_list_by_name(column_name)
        self.configChecker.check_repeat(column_list,self.check_table,column_name)

    # 格式检查
    def check_regext(self,column_name,regex):
      column_list = self.xlsxReader.get_column_list_by_name(column_name)
      self.configChecker.check_regex(column_list,regex,self.check_table,column_name)  #为空检查

    #值域检查
    def check_range(self,column_name,min,max):
        column_list = self.xlsxReader.get_column_list_by_name(column_name)
        self.configChecker.check_range(column_list,min,max,self.check_table,column_name)

