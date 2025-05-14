#coding=utf-8
import os
import time



django_path ="E:\\DjangoProject\\QaAuto\\templates\\"

#pytest命令
now = time.strftime("%Y%m%d_%H%M%S",time.localtime(time.time()))
print(now)
html_name = django_path+ "configcheck_"+now+".html"
cmd_pytest = "python3 -m pytest --html={0} --self-contained-html".format(html_name)

#cd到指定目录命令
root_path= os.path.dirname(os.getcwd())
cmd_goto_project="cd/d %s"%root_path


#发送结果


#两条命令结合
cmd = '''  %s  &  %s &'''%(cmd_goto_project,cmd_pytest)

if __name__ == '__main__':
    os.system(cmd)
