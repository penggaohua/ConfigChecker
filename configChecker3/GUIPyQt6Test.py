import shutil
import sys
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel, \
    QLineEdit, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal

from ConfigCheckerQuick import *

from PyCharmMiscProject.ConfigCheckerQuickClass import ConfigCheckerQuickClass


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

    #    self.label_table_name= QLabel("表名：")
    #    self.input_table_name = QLineEdit()
       # self.input_table_name.setGeometry(10,10,10,10)
        self.label_sheet_name= QLabel("页名：")
        self.input_sheet_name = QLineEdit()
        self.input_sheet_name.setText("HCZBShenShou")

        self.label_column_name= QLabel("列字母：")
        self.input_column_name = QLineEdit()
        self.input_column_name.setPlaceholderText("请输入列字母，必须是大写，不要有空格")
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
        bottom_layout.addWidget(self.button_check_single_column)
        bottom_layout.addWidget(self.button_check_sheet)
        bottom_layout.addWidget(self.button_check_table)
        bottom_layout.addWidget(self.button_output_result)

        layout.addLayout(bottom_layout)


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

    #--------检查方法-------------------------------------------

    def check_single_column(self):
        print("单列检测")
        path=self.input.text()
        sheet_name=self.input_sheet_name.text()
        column_name=self.input_column_name.text()
        #todo 更细致的输入检查 ：为空 ，不存在列字母，参数有误
        if(column_name == ""):
            self.show_text("error ------->   列字母未输入")
            return

        self.configchecker.file_path=path
        res  =  self.configchecker.check_sheet_or_column(sheet_name,column_name)
        out_put = res[0] + str(res[1])
        with open("temp.log", 'w', encoding='utf-8') as f:
            f.write(str(out_put))
        self.show_text(out_put)


    def check_sheet(self):
        print("单页检测")
        path = self.input.text()
        sheet_name = self.input_sheet_name.text()

        self.configchecker.file_path = path
        res = self.configchecker.check_sheet_or_column(sheet_name)
        out_put = res[0] + str(res[1])
        with open("temp.log", 'w', encoding='utf-8') as f:
            f.write(str(out_put))
        self.show_text(out_put)



    def check_table(self):
        path = self.input.text()
        self.configchecker.file_path = path
        res =self.configchecker.check_table_parallel()
        with open("temp.log", 'w', encoding='utf-8') as f:
            f.write(str(res))
        print("写入完毕")
        self.show_text_from_file()





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
    configCheckerQuickClass= ConfigCheckerQuickClass(file_path)

    app = QApplication(sys.argv)
  #  window = MainWindow(check_table_parallel)
    window = MainWindow(configCheckerQuickClass)
    window.show()
    print(time.time() - start)
    sys.exit(app.exec())
