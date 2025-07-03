import multiprocessing
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from openpyxl.utils import column_index_from_string, get_column_letter

from PyCharmMiscProject.ConfigCheckerBase import ConfigCheckerBase


class ConfigCheckerUniqueness(ConfigCheckerBase):
    def __init__(self, file_path,):
        super().__init__(file_path)
    #单列唯一性检测


    #方案1：wkshenshou B 耗时 0.08554744720458984
    def check_column( self,sheet_name, column_letter):
      #  try:
            # 读取 Excel 文件
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                #usecols=column_letter,
                dtype=str
            )
            # 将列字母转换为列索引 (0-based)
            column_num = column_index_from_string(column_letter) - 1

            # 检查列索引是否有效
            if column_num >= df.shape[1]:
                raise ValueError(f"列字母 {column_letter} 超出范围，表格只有 {df.shape[1]} 列")

            # 提取指定列的数据
            column_data = df.iloc[:, column_num]
            duplicates = {}


            #方案1  0.08554744720458984
            # 找出重复的值及其出现的所有位置（行号+1转换为1-based）
            for value, group in column_data.groupby(column_data):
                # 将 pandas 索引（0-based）转换为 Excel 行号（1-based）
                if(len(group) <= 1): continue
                indices = [idx + 1 for idx in group.index.tolist()]
                duplicates[value] = indices


            value_counts = column_data.value_counts()

            # 筛选出现次数 > 1 的值
            duplicates = value_counts[value_counts > 1].to_dict()

            # 获取每个重复值的行号（转换为1-based）
            duplicate_indices = {}
            for value in duplicates.keys():
                indices = column_data[column_data == value].index.tolist()
                duplicate_indices[value] = [i + 1 for i in indices]  # Excel行号从1开始

            return column_letter,duplicates

      #  except Exception as e:
         #   print(f"发生错误: {e}")
           # return {}








    #单页唯一型检测
    def check_sheet(self,sheet_name):
        print("检查单页各列的唯一性---->")
        df = pd.read_excel(
            self.file_path,
            sheet_name=sheet_name,
            header=None,
            dtype=str,
        )
        all_columns = [get_column_letter(i) for i in range(1, df.shape[1] + 1)]
        result=[]
        #方案1：单进程耗时0.8505
        for  column in all_columns:
            # 表头为空的列不检测
            column_idx = column_index_from_string(column) - 1
            cell_value = df.iloc[3, column_idx]
            if pd.isna(cell_value) :continue        # 表头为空的列不检测
            res= self.check_column(sheet_name,column)
            result.append(res)
            #print(f"{sheet_name}{column} 列检测结果")
        return sheet_name,result


    #整表唯一性检测
    def check_table(self):
        empty_cells_dict  = defaultdict(list)
        xl = pd.ExcelFile(self.file_path, engine='openpyxl')
        sheet_names = xl.sheet_names

        max_workers = min(multiprocessing.cpu_count(), len(sheet_names))
        with multiprocessing.Pool(processes=max_workers) as pool:
            args =(sheet_name for sheet_name in sheet_names)
            result = pool.map(self.check_sheet, args)

            for sheet_name, sheet_results in result:
                if sheet_results:
                    empty_cells_dict[sheet_name] = sheet_results

        return empty_cells_dict




if __name__ == '__main__':
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'

    start = time.time()
    cc = ConfigCheckerUniqueness(file_path)

   # res =  cc.check_column("WKshenshou","B")
    res  = cc.check_sheet("WKshenshou")

    print(res)

    #cc = ConfigCheckerUniqueness(file_path)

    #res_table= cc.check_table()

    #print(f"<UNK>: {res_table}")
    print(time.time() - start)