import shutil
import sys


from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, \
    QLineEdit, QHBoxLayout, QComboBox
from PyQt6.QtCore import QThread, pyqtSignal

from PyCharmMiscProject.ConfigCheckerQuick import *
from PyCharmMiscProject.ConfigCheckerRange import ConfigCheckerRange
from PyCharmMiscProject.ConfigCheckerMaxLength import ConfigCheckerMaxLength

from PyCharmMiscProject.ConfigCheckerNone import ConfigCheckerNone
from PyCharmMiscProject.ConfigCheckerReference import check_reference_split
from PyCharmMiscProject.ConfigCheckerUniqueness import ConfigCheckerUniqueness


class TextLoader(QThread):
    """后台线程加载文本数据"""
    text_chunk_ready = pyqtSignal(str)
    loading_finished = pyqtSignal()

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.chunk_size = 1024 * 1024  # 1MB 每块

    def run(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                while True:
                    chunk = f.read(self.chunk_size)
                    if not chunk:
                        break
                    self.text_chunk_ready.emit(chunk)
            self.loading_finished.emit()
        except Exception as e:
            print(f"加载文件错误: {e}")

class MainWindow(QMainWindow):
    def __init__(self,ConfigChecker):
        self.configchecker =ConfigChecker
        super().__init__()
        self.setWindowTitle("配置表检查v6.5")
        self.resize(1200, 600)
        #配置表路径输入
        self.label = QLabel("配置表路径:")
        self.input = QLineEdit()
        self.input.setPlaceholderText(r"请输入配置表路径:")
        self.input.setText(r"d:\Config\竞技场神兽配置表.xlsx")

        #self.label_table_name= QLabel("表名：")
        # self.input_table_name = QLineEdit()
        # self.input_table_name.setGeometry(10,10,10,10)
        self.label_sheet_name= QLabel("页名：")
        self.input_sheet_name = QLineEdit()
        self.input_sheet_name.setText("WKshenshou")

        self.label_column_name= QLabel("列字母：")
        self.input_column_name = QLineEdit()
        self.input_column_name.setText("A")
        self.input_column_name.setPlaceholderText("请输入列字母，必须是大写，不要有空格")
        #创建下拉框
        self.combobox = QComboBox()
        self.combobox.addItems(["为空", "唯一性"])


        #创建按钮
        self.button_check_single_column = QPushButton("单列检查", self)
      #  self.button_check_single_column.clicked.connect(lambda :self.check_single_column(fun))
      #  self.button_check_single_column.clicked.connect(lambda :self.check_single_column(self.configchecker.check_sheet_or_column))
        self.button_check_single_column.clicked.connect(self.check_single_column)
        self.button_check_sheet = QPushButton("单页检查", self)
        self.button_check_sheet.clicked.connect(self.check_sheet)
        self.button_check_table = QPushButton("全表检查", self)
        self.button_check_table.clicked.connect(self.check_table)
        self.button_output_result = QPushButton("导出结果", self)
        self.button_output_result.clicked.connect(self.output_check_result)

        # 创建文本编辑器
        self.text_edit = QPlainTextEdit()
        self.text_edit.setReadOnly(True)  # 设置为只读


        #范围检查
        self.label_min_value = QLabel("最小值（包含）")
        self.input_min_value = QLineEdit()
        self.input_min_value.setText('0')
        self.input_min_value.setPlaceholderText("输入最小值")
    #self.input_min_value.setFixedWidth(80)
        self.label_max_value= QLabel("最大值（包含）")
        self.input_max_value = QLineEdit()
        self.input_max_value.setText('100')
        self.input_max_value.setPlaceholderText("输入最大值")
        #self.input_max_value.setFixedWidth(80)
      #  self.input_max_value.setFixedWidth(60)

        self.button_check_range = QPushButton("范围检查", self)
        self.button_check_range.setFixedWidth(300)
        self.button_check_range.clicked.connect(self.check_range_column)

        #长度检查
        self.label_max_length = QLabel("单元格内容最大长度（包含）")
        self.input_max_length = QLineEdit()
        self.input_max_length.setFixedWidth(600)
        self.button_max_length = QPushButton("最大长度检查", self)
        self.button_max_length.clicked.connect(self.check_max_length)


        # 创建布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input)
    #    layout.addWidget(self.label_table_name)
      #  layout.addWidget(self.input_table_name  )
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.label_sheet_name)
        top_layout.addWidget(self.input_sheet_name)

        top_layout.addWidget(self.label_column_name)
        top_layout.addWidget(self.input_column_name)
        layout.addLayout(top_layout)
        layout.addWidget(self.text_edit)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.combobox)

        bottom_layout.addWidget(self.button_check_single_column)
        bottom_layout.addWidget(self.button_check_sheet)
        bottom_layout.addWidget(self.button_check_table)
        bottom_layout.addWidget(self.button_output_result)

        #范围检查布局
        bottom_layout_range = QHBoxLayout()
        bottom_layout_range.addWidget(self.label_min_value)
        bottom_layout_range.addWidget(self.input_min_value)
        bottom_layout_range.addWidget(self.label_max_value)
        bottom_layout_range.addWidget(self.input_max_value)
        bottom_layout_range.addWidget(self.button_check_range)

        #长度检查布局
        bottom_layout_length=QHBoxLayout()
        bottom_layout_length.addWidget(self.label_max_length)
        bottom_layout_length.addWidget(self.input_max_length)
        bottom_layout_length.addWidget(self.button_max_length)

        #索引检查布局
        self.input_reference_target_path = QLineEdit()
        self.input_reference_target_path.setPlaceholderText("目标表格路径")
        self.input_reference_target_sheet = QLineEdit()
        self.input_reference_target_sheet.setPlaceholderText("目标表格页名")
        self.input_reference_target_sheet.setFixedWidth(100)

        self.input_reference_target_column = QLineEdit()
        self.input_reference_target_column.setPlaceholderText("目标表格列字母")
        self.input_reference_target_column.setFixedWidth(100)
        self.button_reference_check = QPushButton("索引检查", self)
        self.button_reference_check.clicked.connect(self.check_reference )

        self.button_reference_check.setFixedWidth(300)

        bottom_layout_refer = QHBoxLayout()
        bottom_layout_refer.addWidget(self.input_reference_target_path)
        bottom_layout_refer.addWidget(self.input_reference_target_sheet)
        bottom_layout_refer.addWidget(self.input_reference_target_column)
        bottom_layout_refer.addWidget(self.button_reference_check)




        layout.addLayout(bottom_layout)
        layout.addLayout(bottom_layout_range)
        layout.addLayout(bottom_layout_length)
        layout.addLayout(bottom_layout_refer)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    #通过读取文件显示到GUI
    def  show_text_from_file(self):
    # 启动加载线程
        self.loader = TextLoader("temp.log")
        self.loader.text_chunk_ready.connect(self.append_text)
        self.loader.loading_finished.connect(self.on_loading_finished)
        self.loader.start()

    #直接显示到GUI
    def show_text(self,res):
        self.text_edit.setPlainText(res )



    def append_text(self, chunk):
        """追加文本块到编辑器"""
        self.text_edit.appendPlainText(chunk)

    def on_loading_finished(self):
        """加载完成后的处理"""
        print("文本加载完成")


    #把检测结果导出到配置表目录下 CheckResult
    #报告命名规则  表名_时间戳.log
    def output_check_result(self):
        path=self.input.text()
        dir_path = os.path.dirname(path)+r"\\CheckResult\\"
        name_without_ext = os.path.splitext(os.path.basename(path))[0]

        timestamp = time.time()  #
        local_time = time.localtime(timestamp)
        formatted_time = time.strftime("%Y%m%d_%H%M%S", local_time)
        output_path = dir_path +name_without_ext+"_"+formatted_time+".log"
        print(output_path)
        shutil.copy("temp.log", output_path)


    def get_check_type(self):
        check_type = self.combobox.currentText()
        print(check_type)
        index = self.combobox.currentIndex()
        type_list = [ConfigCheckerNone,ConfigCheckerUniqueness]
        return type_list[index]


    #--------检查方法-------------------------------------------

    def check_single_column(self):
        #根据选项来执行具体的检查

        print("单列检测")
        func = self.get_check_type()


        path=self.input.text()
        sheet_name=self.input_sheet_name.text()
        column_name=self.input_column_name.text()
        #todo 更细致的输入检查 ：为空 ，不存在列字母，参数有误
        if(column_name == ""):
            self.show_text("error ------->   列字母未输入")
            return

        self.configchecker = func(path)
        res  =  self.configchecker.check_column(sheet_name,column_name)
        out_put =str(res)
        with open("temp.log", 'w', encoding='utf-8') as f:
            f.write(str(out_put))
        self.show_text(out_put)


    def check_sheet(self):
        print("单页检测")
        func = self.get_check_type()

        path = self.input.text()
        sheet_name = self.input_sheet_name.text()
        self.configchecker  = func(path)
        res = self.configchecker.check_sheet(sheet_name)
        out_put =str(res)
        with open("temp.log", 'w', encoding='utf-8') as f:
            f.write(str(out_put))
        self.show_text(out_put)



    def check_table(self):
        path = self.input.text()
        func = self.get_check_type()
        self.configchecker  = func(path)
        res =self.configchecker.check_table()
        with open("temp.log", 'w', encoding='utf-8') as f:

            f.write(str(res))
        print("写入完毕")
        self.show_text_from_file()

    def check_range_column(self):
        try:
            print("check range column")
            min = self.input_min_value.text()
            min_value =float(min)
            max = self.input_max_value.text()
            max_value =float(max)
            sheet_name = self.input_sheet_name.text()
            column_letter = self.input_column_name.text()
            path = self.input.text()
            checker = ConfigCheckerRange(path)
            res = checker.check_range(sheet_name,column_letter,min_value,max_value)
            print(res)

            with open("temp.log", 'w', encoding='utf-8') as f:
                f.write("范围检查:\n")
                f.write(str(res))
            self.show_text(str(res))
        except Exception as e  :
            print(e)



    def check_max_length(self):
        try:
            print("check_max_length")
            sheet_name = self.input_sheet_name.text()
            column_letter = self.input_column_name.text()
            path = self.input.text()
            max_length = self.input_max_length.text()
            print(max_length)
            checker = ConfigCheckerMaxLength(path)
            res = checker.check_max_length(sheet_name,column_letter,float(max_length))
            with open("temp.log", 'w', encoding='utf-8') as f:
                f.write("最大长度检查:\n")
                f.write(str(res))
            self.show_text(str(res))
        except Exception as e :
            print(e)

    def check_reference(self):
        try:
            print("check reference")
            #源表格
            source_path = self.input.text()
            source_sheet_name = self.input_sheet_name.text()
            source_column_name = self.input_column_name.text()
            #目标表格
            target_path = self.input_reference_target_path.text()
            target_sheet_name = self.input_reference_target_sheet.text()
            target_column_name = self.input_reference_target_column.text()

            res = check_reference_split(source_path,source_sheet_name,source_column_name,target_path,target_sheet_name,target_column_name)

            with open("temp.log", 'w', encoding='utf-8') as f:
                    f.write("索引检查:\n")
                    f.write(str(res))
            self.show_text(str(res))
        except Exception as e :
            print(e)


if __name__ == "__main__":
    start = time.time()
    #全表检查
    file_path = r'd:\Config\竞技场神兽配置表.xlsx'

    # 日志目录
    sheet_name = "HCZBShenShou"

    # 单页检查
    # res_dic =scan_sheet_for_empty_cells((file_path,sheet_name))
    #  print(res_dic[0]+str(res_dic[1]))

    # 整表处理
    # res = parallel_static_data_check(file_path)
    # print(res)
    # with open("result2.log", 'w', encoding='utf-8') as f:
    #     f.write(str(res))
    configChecker= ConfigCheckerNone(file_path)

    app = QApplication(sys.argv)
  #  window = MainWindow(check_table_parallel)
    window = MainWindow(configChecker)
    window.show()
    print(time.time() - start)
    sys.exit(app.exec())
