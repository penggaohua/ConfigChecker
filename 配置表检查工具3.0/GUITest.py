import queue
import threading
import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

from ConfigChecker import ConfigChecker
from multiprocessing import Process,Queue

class GUITest:
    def __init__(self,root, configChecker):
        self.root = root
        self.configChecker = configChecker
        self.root.title("test")
        self.root.geometry("1200x700")
        self.q =Queue()

        self.frame1 = Frame(self.root)
        self.frame1.pack(fill=tk.BOTH, expand=True)
        Button(self.frame1,text="testbutton",command=self.start_process,bg='yellow').pack(side=tk.LEFT)
        self.text_output  = scrolledtext.ScrolledText(self.frame1,width=150,height=40 )
        self.text_output.pack(fill=tk.BOTH, expand=True)




    def check_one_single(self):
     #   print(self.configChecker.check_none_column("Star"))
        res=  self.configChecker.check_none_sheet("HCZBShenShou")
        self.text_output.insert(END,res)
        #self.text_output.see(END)


    def show_in_text(self,res):
        print(" 在面板中打印")
        self.text_output.insert(END, res)
        self.text_output.see(END)

    def check_one_sheet_process(self,q):
        self.configChecker.check_none_sheet("HCZBShenShou",q)


    def show_in_text_process(self,q):
        while True:
            res = q.get
            self.text_output.insert(END,res)
            self.text_output.see(END)

    def mul_process_test(self):
        p1 =threading.Thread(target=self.show_in_text,args=(self.q,))
  #      p2 =Process(target=self.check_one_sheet_process,args=(self.q,))
        p1.start()
   #     p2.start()
        p1.join()
    #    p2.join()

    #   thread = threading.Thread(target=check_one_sheet_process,args=(lambda result: root.after(0, self.show_in_text, result),))



    def worker_task(self,q):
        self.configChecker.check_none_sheet("HCZBShenShou",q)

    def update_gui(self,queue):
        """检查队列中是否有结果并更新GUI"""
        if not queue.empty():
            result = queue.get()
            self.text_output.insert(END, result)
            self.text_output.see(END)
        else:
            root.after(100,self.update_gui, queue)  # 继续检查


    def start_process(self):
        """启动新进程执行计算任务"""
        try:

            # 创建队列用于进程间通信
            q= Queue()

            # 创建并启动进程
            process = Process(
                target=self.worker_task,
                args=(self,q)
            )
            process.daemon = True  # 主程序退出时自动终止
            process.start()

            # 定期检查队列
            self.root.after(100, self.update_gui, q)

        except ValueError:

            print("gui error")





if __name__ == "__main__":
    root = tk.Tk()
    path=  "D:\\Config"
    xlsx_name  = "竞技场神兽配置表.xlsx"
    xlsx_sheet = "HCZBShenShou"
    configChecker = ConfigChecker(path,xlsx_name,xlsx_sheet)
    app = GUITest(root,configChecker)
    app.show_in_text("heeee")
    root.mainloop()
