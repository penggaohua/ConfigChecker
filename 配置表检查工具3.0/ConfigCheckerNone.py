import multiprocessing
import os
import time
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter,column_index_from_string

from PyCharmMiscProject.ConfigCheckerBase import ConfigCheckerBase


class ConfigCheckerNone(ConfigCheckerBase):

    def __init__(self, file_path=None):

        super().__init__(file_path)

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value



    def  check_column(self,sheet_name,column_name):
        print("check column")
        return self.check_sheet_or_column(sheet_name,column_name)


    def check_sheet(self,sheet_name):
        print("check sheet")
        return self.check_sheet_or_column(sheet_name)
    '''
        这个函数包含了两种检查：单列检查和整页检查
        如果column_name 传入了参数就只对某一列进行检查
        如果column_name 为none就对整页检查
    '''
    def check_sheet_or_column(self,sheet_name,column_name=None):
        df = pd.read_excel(self.file_path,sheet_name=sheet_name,header=None,dtype=str,)
        empty_positions = np.argwhere(df.isnull().values)
        empty_cells=[]
        row = df.iloc[3].tolist()

        none_index_list = [i for i, x in enumerate(row) if pd.isna(x)]   # 得到表头一列数据，然后把表头为空的对应的index提出来
        print(none_index_list)
        # 获取空值位置

        # 转换位置为Excel坐标
        for row_idx, col_idx in empty_positions:
            col_letter = get_column_letter(col_idx + 1)
            if column_name is not None: #如果column不为空，只对参数列进行检查
                if col_letter != column_name:
                    continue
            #表头行之上不用检查
            if row_idx<4:continue
            #判断整个一行是不是空的，如果是，不计入结果
            if df.iloc[row_idx].count() == 0:
             #    print(f"{row_idx+1}整行都是空的")
                 continue
            #如果表头是空，整个一列不计入结果
            if col_idx in none_index_list:continue
            row_num = row_idx + 1
            cell_ref = f"{col_letter}{row_num}"
            empty_cells.append(cell_ref)

       # except Exception as e:
            #logger.error(f"处理工作表 '{sheet_name}' 时出错: {str(e)}")
        #    print(f"处理工作表 '{sheet_name}' 时出错: {str(e)}")

        return  sheet_name,empty_cells



    def check_table(self):
        """全sheet页并s行静态数据检查"""
        start_time = time.time()
        empty_cells_dict = defaultdict(list)

     #   try:
        if not os.path.exists(self._file_path):
           # logger.error(f"文件不存在: {file_path}")
            print(f"文件不存在: {self._file_path}")
            return empty_cells_dict

        # 获取所有sheet名称
        xl = pd.ExcelFile(self._file_path, engine='openpyxl')
        sheet_names = xl.sheet_names
        xl.close()

        print(f"工作簿包含 {len(sheet_names)} 个工作表，启动并行扫描...")

        # 进程池并行处理
        max_workers = min(multiprocessing.cpu_count(), len(sheet_names))
        with multiprocessing.Pool(processes=max_workers) as pool:

            result  = pool.map(self.check_sheet_or_column, [name for name in sheet_names])
            for future in result:
                #print(future,args[1])
                empty_cells_dict[future[0]] =future[1]

       # except Exception as e:

            #logger.error(f"处理Excel时发生全局错误: {str(e)}")
            #print(f"处理Excel时发生全局错误: {str(e)}")
        return  empty_cells_dict

    def check_cell_uniqueness(self):
        df = pd.read_excel(self.file_path,sheet_name=sheet_name,header=None,dtype=str,)
        row = df.iloc[3].tolist()





#todo 看看单进程查全表需要多长时间

if __name__ == '__main__':
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'

    # 日志目录
    log_dir = r'd:\Config'
    sheet_name ="HCZBShenShou"
    #sheet_name ="HCZBShenShou"
    start = time.time()
    cc  =  ConfigCheckerQuickClass(file_path)

    #单页检查
    res_dic =cc.check_sheet_or_column(sheet_name,'C')
    print(res_dic[0]+str(res_dic[1]))


    #整表处理
    res= cc.check_table_parallel()
    print(res)


    print(time.time() - start)
