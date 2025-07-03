import multiprocessing
import os
import time
from collections import defaultdict

import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter





'''
    这个函数包含了两种检查：单列检查和整页检查
    如果column_name 传入了参数就只对某一列进行检查
    如果column_name 为none就对整页检查
'''
def check_sheet_or_column(args,column_name=None):
    file_path,sheet_name = args
    """扫描单个sheet页的空单元格并返回结果"""
    empty_cells = []

    #try:
        # 使用pandas批量读取整个sheet页数据
    df = pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        header=None,
        dtype=str,
      #  engine='openpyxl'
    )
    # 将空白字符串转换为NaN
    #df = df.replace(r'^\s*$', np.nan, regex=True)
    row = df.iloc[3].tolist()
    none_index_list = [i for i, x in enumerate(row) if pd.isna(x)]   # 得到某一列数据，然后把为空的数据对应的index提出来
    print(none_index_list)
    # 获取空值位置
    empty_positions = np.argwhere(df.isnull().values)

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



def check_table_parallel(file_path):
    """全sheet页并行静态数据检查"""
    start_time = time.time()
    empty_cells_dict = defaultdict(list)

 #   try:
    if not os.path.exists(file_path):
       # logger.error(f"文件不存在: {file_path}")
        print(f"文件不存在: {file_path}")
        return empty_cells_dict

    # 获取所有sheet名称
    xl = pd.ExcelFile(file_path, engine='openpyxl')
    sheet_names = xl.sheet_names
    xl.close()

    print(f"工作簿包含 {len(sheet_names)} 个工作表，启动并行扫描...")

    # 进程池并行处理
    max_workers = min(multiprocessing.cpu_count(), len(sheet_names))
    with multiprocessing.Pool(processes=max_workers) as pool:

        args = ((file_path,name) for name in sheet_names)
        print(args)
        result  = pool.map(check_sheet_or_column, args)
        for future in result:
            #print(future,args[1])
            empty_cells_dict[future[0]] =future[1]

   # except Exception as e:

        #logger.error(f"处理Excel时发生全局错误: {str(e)}")
        #print(f"处理Excel时发生全局错误: {str(e)}")
    return  empty_cells_dict



#todo 看看单进程查全表需要多长时间

if __name__ == '__main__':
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'

    # 日志目录
    log_dir = r'd:\Config'
    sheet_name ="HCZBShenShou"
    #sheet_name ="HCZBShenShou"
    start = time.time()


    #单页检查
    res_dic =check_sheet_or_column((file_path,sheet_name),'C')
    print(res_dic[0]+str(res_dic[1]))


    #整表处理
   # res=  check_table_parallel(file_path)
  #  print(res)


    print(time.time() - start)
