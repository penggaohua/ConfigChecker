import pandas as pd
from openpyxl.utils import column_index_from_string





def check_reference_split(source_file, source_sheet, source_column,
                               target_file, target_sheet, target_column,
                               separator=';'):
    """
    检查源表中的数据（可能包含分隔符分割的多个值）是否存在于目标表中
    参数:
    - separator: 用于分割源表单元格值的分隔符，默认为分号
    """
    try:
        # 读取源表和目标表数据
        source_df = pd.read_excel(source_file, sheet_name=source_sheet, header=None,dtype='str') #dtyp='str'可以禁用自动转换
        target_df = pd.read_excel(target_file, sheet_name=target_sheet, header=None,dtype='str')

        # 转换列字母为索引
        if isinstance(source_column, str):
            source_col_idx = column_index_from_string(source_column) - 1
        else:
            source_col_idx = source_column

        if isinstance(target_column, str):
            target_col_idx = column_index_from_string(target_column) - 1
        else:
            target_col_idx = target_column

        # 提取需要比较的列数据（从第5行开始）
        source_data = source_df.iloc[4:, source_col_idx].dropna().astype(str)
        target_data = target_df.iloc[4:, target_col_idx].dropna().astype(str)

        # 将目标数据转换为集合，加速查找
        target_set = set(target_data)

        # 记录不存在的值及其所在行
        #not_found = []
        not_found_details = []

        # 遍历源数据，拆分每个单元格并检查存在性
        for idx, cell_value in source_data.items():
            # 拆分单元格值
            values = [v.strip() for v in cell_value.split(separator) if v.strip()]
            # 检查每个拆分后的值是否存在
            missing_values = [v for v in values if v not in target_set]
            #print("missing_values", )
           # print(missing_values)
            if missing_values:
               # not_found.extend(missing_values)
                not_found_details.append({
                    'row': idx + 1,  # Excel行号
                    'cell_value': cell_value,
                    'missing_values': missing_values
                })

        return  not_found_details

    except Exception as e:
        print(f"发生错误: {e}")
        return {}



if __name__ == '__main__':
    file_path_source = r'd:\Config\竞技场神兽配置表.xlsx'
    file_path_target = r'd:\Config\PlayerSkills.xlsx'

    #res=  check_data_existence_split(file_path_source,"WKshenshou","D",file_path_target,"Skills","A" )
    res=  check_reference_split(file_path_source,"WKshenshou","A",file_path_target,"Sheet1","C" )
    print(res)