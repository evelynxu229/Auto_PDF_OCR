# -*- coding: utf-8 -*-
"""
Created on 20 July 11:16:25 2022

@author: Ting
"""


"""使用watchdog实时监测 data文件夹下的新增文件"""
from watchdog.observers import Observer
from watchdog.events import *
import time
import os
from shmain import main
import sys
import traceback
import warnings
warnings.filterwarnings("ignore")


class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)
        
    def on_created(self, event): # 创建文件或文件夹
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))
        
        ###----对新增pdf文件进行ocr识别------###
        try: #执行可能产生异常的代码块
            new_pdfs=[] #新增pdf的列表
            new_pdfs.append(event.src_path[:])
            #这个是变换的文件的路径，截取后面的pdf的名称，所以需要按照文件来变
            
            print('对新增pdf文件进行识别')
            pdfdir_path = r"./data"  # pdf文件夹路径，如果要是用于生产，应该换成生产的pdf存放路径

            n=len(os.listdir(pdfdir_path)) #当前文件夹下的文件个数
            d=n-len(new_pdfs)+1 #处理第d个文件（从1开始编号），就是从新增的那个文件开始
            main(pdfdir_path, new_pdfs, d) #调用ocr识别函数
        except:  
            # 记录控制台Traceback信息
            errorFile = open('./log/shuanghuanMatchlog_traceback.log', 'a', encoding='utf-8')
            traceback.print_exc(file=errorFile)
            errorFile.close()
 
if __name__ == "__main__":
    
    observer = Observer()
    event_handler = FileEventHandler()
    monitor_path = "./data" # 监听目录

    observer.schedule(event_handler, monitor_path, recursive=True)  
    
    observer.start()
    try:
        while True: #循环监听
           
            time.sleep(0.01) # 监控频率（0.01s/1次）
    except KeyboardInterrupt: #手动KeyboardInterrupt关闭进程       
        observer.stop() #关闭进程
        
    observer.join()
    

    