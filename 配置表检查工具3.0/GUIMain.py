#coding=utf-8
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk,scrolledtext
from ConfigChecker import ConfigChecker
import  configparser

import threading
from multiprocessing import Process, JoinableQueue



class  GUIMain:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("配置表检查工具v6.1")
        self.root.geometry("1000x600+10+10")
        self.is_select = True
    def set_frame(self):
        return Frame(self.root)

    def set_button(self,frame,btn_name,btn_command,bg="white"):
        return Button(frame,text=btn_name,bg=bg,command=btn_command)

    def set_Entry(self,frame,width,input_str=""):
        str_var = StringVar()
        str_var.set(input_str)
        return Entry(frame, width=width, textvariable=str_var)


    def set_lable(self,frame,label_name):
         return  Label(frame, text=label_name)

    def set_check_button(self,frame,button_text,value):
        return Checkbutton (frame,text=button_text,onvalue=True,offvalue=False,variable=value)


    def set_scroll_text(self,frame,width,height):
         return scrolledtext.ScrolledText(frame, width=width, height=height, font=("宋体", 10))

    def test(self,text_output):
        res = "test \n"
        print("this is a method for test ")
        text_output.insert(END, res)
        text_output.see(END)

    def show_in_text(self,res,text_output):
        print(" 在面板中打印")
        text_output.insert(END, res)
        text_output.see(END)



    def clean_text(self,text_output):
        text_output.delete('1.0', 'end')

    def get_entry_content(self,entry):
        return entry.get()

    def main(self):
        self.root.mainloop()

    def select_all(self,atr_dic):
        self.is_select = True ^ self.is_select
        for value in atr_dic.values():
            value.set(self.is_select )

    def show_in_text_process(self,q ):
        while True:
            res=  q.get()
            self.show_in_text(res,text_output)
            print("res:"+res)



if __name__=='__main__':
    #q = Queue()
    q=JoinableQueue()

    GUIMain = GUIMain()

    #从config.ini读取默认配置表地址
    cf = configparser.ConfigParser()
    cf.read("config.ini",encoding='utf-8')
    config_table_default_path = cf.get("config_path", "config_path")
    config_table_name=cf.get("config_path","table_name")
    config_sheet_name=cf.get("config_path","sheet_name")
    configChecker=None
    def init_configChecker():
        global configChecker
        configChecker = ConfigChecker(
            GUIMain.get_entry_content(entry_config_path),
            GUIMain.get_entry_content(entry_table_name),
            GUIMain.get_entry_content(entry_sheet_name)
        )
    def fun_check_none_single():
       print("fun_check_none_single")
       init_configChecker()
       res= configChecker.check_none_column(GUIMain.get_entry_content(entry_field_name))
       GUIMain.show_in_text(res,text_output)

    def fun_check_none_sheet():
        init_configChecker()
        # configChecker.check_none_sheet(GUIMain.get_entry_content(entry_sheet_name),GUIMain,text_output,q)
        # while True:
        #     out_res=  q.get()
        #     print( "消费："+out_res)
        #     GUIMain.show_in_text(out_res, text_output)


        # configchecker.check_none_sheet() 作为一个生产者不断把每列检测结果写入queue，guimain.show_in_text()作为消费者不断把queue的结果在前端面板打印出来

        sheet_name= GUIMain.get_entry_content(entry_sheet_name)

        with Process(target=configChecker.check_none_sheet, args=(sheet_name,q,))  as p1:
            with Process(target=GUIMain.show_in_text_process, args=(q,text_output,)) as p2:

                p1.start()
                p2.start()
                p1.join()
                p2.join()


    def fun_check_none_table():
        init_configChecker()
        configChecker.check_none_table(GUIMain,text_output)
       # GUIMain.show_in_text(res, text_output)


    frame1 = GUIMain.set_frame()
    frame2 = GUIMain.set_frame()
    frame3 = GUIMain.set_frame()
    frame4 = GUIMain.set_frame()
    frame5 = GUIMain.set_frame()


    # frame1
    label_config_path = GUIMain.set_lable(frame1, "配置表目录:")
    entry_config_path = GUIMain.set_Entry(frame1,60,config_table_default_path)
    button_check_none = GUIMain.set_button(frame1, "为空检查",fun_check_none_single ,bg="skyblue")
    button_check_none_sheet = GUIMain.set_button(frame1, "指定页为空检查",fun_check_none_sheet ,bg="skyblue")
    button_check_none_table = GUIMain.set_button(frame1, "整表为空检查",fun_check_none_table ,bg="skyblue")


    button_clear_log = GUIMain.set_button(frame1, "清空日志", lambda: GUIMain.clean_text(text_output))
    label_config_path.pack(padx=15, side=LEFT)
    entry_config_path.pack(padx=15, side=LEFT)
    button_check_none.pack(padx=15, side=LEFT)
    button_check_none_sheet.pack(padx=15, side=LEFT)
    button_check_none_table.pack(padx=15, side=LEFT)
    button_clear_log.pack(padx=15, side=LEFT)
    frame1.grid(row=1, column=0, pady=5, sticky=W)

    # frame2
    # 表名 、页名、 字段名
    label_table_name = GUIMain.set_lable(frame2, "表名:")
    entry_table_name = GUIMain.set_Entry(frame2, 30,config_table_name)
    label_table_name.pack(padx=15, side=LEFT)
    entry_table_name.pack(padx=15, side=LEFT)

    label_sheet_name = GUIMain.set_lable(frame2, "页名:")
    entry_sheet_name = GUIMain.set_Entry(frame2, 30,config_sheet_name)
    label_sheet_name.pack(padx=15, side=LEFT)
    entry_sheet_name.pack(padx=15, side=LEFT)

    label_field_name = GUIMain.set_lable(frame2, "字段名:")
    entry_field_name = GUIMain.set_Entry(frame2, 30)
    label_field_name.pack(padx=15, side=LEFT)
    entry_field_name.pack(padx=15, side=LEFT)




    frame2.grid(row=2, column=0, pady=10, sticky=W)



    # list_check_def = [GUIMain.set_check_button(frame3, key, value).pack(padx=5, side=LEFT) for key, value in
#                      def_atr_dic.items()]
 #   btn_select_all_def = GUIMain.set_button(frame3, "全选/取消", lambda: GUIMain.select_all(def_atr_dic))
  #  btn_select_all_def.pack(padx=15, side=LEFT)

    # frame4
 #   entry_regex = GUIMain.set_Entry(frame4, 65, "请输入要搜索的内容，支持正则表达式")
    # btn_reg_search = GUIMain.set_button(frame4, "正则搜索", lambda: GUIMain.show_in_text(
    #     logAnalyer.pattern_search(entry_regex.get()), text_output))
    # btn_search = GUIMain.set_button(frame4, "搜索日志", lambda: GUIMain.show_in_text(
    #     logAnalyer.search_atk_def(atk_atr_dic, def_atr_dic, entry_atk.get(), entry_def.get(),
    #                               check_button_value_atk.get(), check_button_value_def.get()), text_output),
    #                                      bg="skyblue")
 #   btn_truncate_res = GUIMain.set_button(frame4, "清空搜索", lambda: GUIMain.clean_text(text_output))

  #  # entry_regex.pack(padx=15, side=LEFT)
  # #  btn_reg_search.pack(padx=15, side=LEFT)
  #  # btn_search.pack(padx=15, side=LEFT)
  #   btn_truncate_res.pack(padx=15, side=LEFT)
  #   frame4.grid(row=3, column=0, pady=5, sticky=W)
  #
  #   # frame5
    text_output = GUIMain.set_scroll_text(frame5, 130, 40)
    #label_compare = GUIMain.set_lable(frame5, "对比池:")
  #  text_output_compare = GUIMain.set_scroll_text(frame5, 260, 20)
    text_output.grid(row=0, column=0, sticky=W, pady=10, padx=10)
  #  label_compare.grid(row=1, column=0, sticky=W, padx=10)
 #   text_output_compare.grid(row=2, column=0, sticky=N)
    frame5.grid(row=4, column=0, pady=5, sticky=N)

    # button2.pack(padx=15,side=LEFT)
    # button3.pack(padx=15,side=LEFT)

    GUIMain.main()

