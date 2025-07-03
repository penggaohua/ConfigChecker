import multiprocessing
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from openpyxl.utils import column_index_from_string, get_column_letter

from PyCharmMiscProject.ConfigCheckerBase import ConfigCheckerBase


class ConfigCheckerRange():
    def __init__(self,file_path):
        self.file_path = file_path
    #单列数值范围检查
    def check_range(self,sheet_name, column_letter,min_value=0.0,max_value=0.0):
        print("单列方位检查")
        if(min_value>=max_value):return
        resultDic = defaultdict(list)
        try:
            # 读取 Excel 文件
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet_name,
                header=None,
                dtype=str,
            )

            # 将列字母转换为列索引 (0-based)
            column_num = column_index_from_string(column_letter) - 1

            # 检查列索引是否有效
            if column_num >= df.shape[1]:
                raise ValueError(f"列字母 {column_letter} 超出范围，表格只有 {df.shape[1]} 列")

            # 提取指定列的数据
            column_data = df.iloc[4:, column_num]
            # 转换为数值类型（处理非数值数据）
            numeric_data = pd.to_numeric(column_data, errors='coerce')
            #排除为 none的值
            valid_mask = ~numeric_data.isna()
            valid_data = numeric_data[valid_mask]
            in_range = (valid_data >= min_value) & (valid_data <= max_value)

            # 获取不在区间内的值及其索引
            outliers = valid_data[~in_range].index
            res  = [i+1  for  i  in  outliers]

            resultDic[column_letter].extend(res)
            return resultDic

        except Exception as e:
            print(f"发生错误: {e}")
            return


#多列数值范围检测




if __name__ == '__main__':
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'

    start = time.time()
    ccr  = ConfigCheckerRange(file_path)
    res  =  ccr.check_range("WKshenshou","A",10.0,100)

    print(res)
    #res =  check_uniqueness_column("WKshenshou","A",file_path)

   # res  = check_uniqueness_sheet("WKshenshou",file_path)
    #res_table = check_uniqueness_table(file_path)

    #    print(f"<UNK>: {res_table}")
    #   print(time.time() - start)