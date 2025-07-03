from collections import defaultdict

import pandas as pd
from openpyxl.utils import column_index_from_string


class ConfigCheckerMaxLength:
    def __init__(self,file_path):
        self.file_path = file_path


    def check_max_length(self,sheet, column_letter,max_len):
            resultDic = defaultdict(list)
       # try:
            # 读取 Excel 文件
            df = pd.read_excel(
                self.file_path,
                sheet_name=sheet,
                header=None,
                dtype=str,
            )

            # 将列字母转换为列索引 (0-based)
            column_num = column_index_from_string(column_letter) - 1

            # 检查列索引是否有效
            if column_num >= df.shape[1]:
                raise ValueError(f"列字母 {column_letter} 超出范围，表格只有 {df.shape[1]} 列")

            # 提取指定列的数据
            column_data = df.iloc[:, column_num]

            lengths = column_data.astype(str).str.len()
            #print(lengths)
            # 检查是否超过最大长度
            exceeds = lengths > max_len
            resultDic[column_letter].append([idx + 1 for idx in exceeds[exceeds].index])
            return resultDic

           # exceeds  =[len(str(item))>max_len for item in column_data]
        #    exceeds_indices=[i for i,x in enumerate(exceeds) if x ]
          #  print(exceeds)

       ##    print(f"发生错误: {e}")
         #   return

if __name__ == '__main__':
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'
  #  file_path = r'd:\Config\PlayerSkills.xlsx'
    sheet_name = "WKshenshou"
   # str= '对周围敌人造成[82dc69]339.3[-]%攻击的伤害并造成灼烧，3秒内每秒造成红莲圣子[82dc69]8.5[-]%攻击的伤害'
    checker = ConfigCheckerMaxLength(file_path)
    res  = checker.check_max_length(sheet_name,"C",3)
    print(str(res))