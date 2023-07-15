# -*- coding: utf-8 -*-
"""
Created on 20 July 09:32:34 2022

@author: Ting
"""

import pandas as pd
import xlwt
import sys, fitz  # pip install PyMuPDF
import os
import datetime
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import openpyxl
import easyocr
import datetime
from PIL import Image  # pip install pillow
from PIL import ImageEnhance
import cv2
import numpy as np

import warnings
warnings.filterwarnings("ignore")


####------截取第1页第1个表（题头）------#####       
def gettitle(lefttop_x, rightbottom_x, lefttop_all_y, page, res_title, label, mat):
    n=1 #设置一个变量
    height=13 #每一行的高度
    if label=='left': n=6 #左边需要识别六个内容
    if label=='first': height=97 #first是指那个大的shuanghuan

   #label是right的时候陷入循环
    for i in range(1, n+1):   
        if i==2 or i==5: continue 
        lefttop_y = lefttop_all_y + height*(i-1)
        rightbottom_y = lefttop_all_y + height*i 
        if label=='first': mat = fitz.Matrix(12, 12).prerotate(int(90)) #顺时针旋转90°
        res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat) #截取图片+预处理+ocr识别
        # print(res)  
    
        ###----将结果储存在res_title 
        if i==1:  #第一行，只获取第1个数据
            if label=='first': res_title[1]=res[0]
            if label=='middle': res_title[10]=res[0] 
            if label=='left': res_title[2], res_title[3], res_title[4]=res[0][:8], res[0][8:-2].replace(' ',''), res[0][-2:]              
            if label=='right': res_title[8], res_title[9] = res[0].replace(' ','') , res[1].replace(' ','')
                    
        if i==3: res_title[5]= res[0]                
        if i==4: res_title[6]=res[0] + '-' + res[1]        
        if i==6: res_title[7]=res[0] 
         
    return res_title
    
####------截取第1页第2个表，最左边的参数列（从下往上截）------#####
def getarg12(lefttop_x, rightbottom_x, rightbottom_all_y12, page, mat):
    lefttop_y = rightbottom_all_y12 - 12*7 # 12是表格中每一行的高度 
    rightbottom_y = rightbottom_all_y12    
    res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat) #截取图片+预处理+ocr识别       
    # print(res) 
    return res    

####------截取第1页第2个表，左/右表格的数据(从下往上)------#####
def gethalf12(lefttop_x, rightbottom_x, rightbottom_all_y12, res_arg, page, res_data, label, mat): #左上/右下x轴的值
    n = len(res_arg)    
    n = n if res_arg[0] == 'Var' else n-1 #当存在Ca行时，res_arg的第0个字符必为'Var'
    
    lefttop_y = rightbottom_all_y12 - 12*(n-1) 
    rightbottom_y = rightbottom_all_y12
    
    if label=='first': 
        lefttop_y = rightbottom_all_y12 - 12*n 
        rightbottom_y = rightbottom_all_y12 - 12*(n-1)
        
    res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat) #截取图片+预处理+ocr识别       
          
    res=solvemistake(res) #手动纠错
    # print(res) 
    
    ####--------将每个结果写入res_data对应位置
    if label=='first': res_data[1:2+1]=res
    
    if label=='left':  
        res_data[3: 9+1]=res[:7][::-1] #逆序 
        res_data[17: 23+1]=res[14:21][::-1]
        res_data[31: 37+1]=res[21:28][::-1]
        if n==7: res_data[45: 51+1]=res[28:35][::-1]   #有Ca行
        
    if label=='right':
        res_data[10: 16+1]=res[:7]   
        res_data[24: 30+1]=res[14:21]
        res_data[38: 44+1]=res[21:28]
        if n==7: res_data[52: 58+1]=res[28:35]
    return res_data

####------截取第1页第3个表，左/右表格的数据(从左到右，竖着截。因为横向每个空格数字挨得太近，易出错，但纵向表格有固定间隔)------#####
def gethalf13(lefttop_x, rightbottom_x, lefttop_all_y, page, res_data, label, mat): #左上/右下x轴的值
    n=4    
    if label=='first': n=1
    lefttop_y = lefttop_all_y # 12是表格中每一行的高度 
    rightbottom_y = lefttop_all_y + 12*n    
    
    res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat) #截取图片+预处理+ocr识别    
    
    res=solvemistake(res) #手动纠错d
    # print(res) 
    
    # ###-----将每个结果写入res_data对应位置
    if label=='first': res_data[61:62+1]=res
    
    if label=='left':  #没有Fβ行 
        res_data[63: 69+1]=res[:7][::-1] #逆序 
        res_data[77: 83+1]=res[14:21][::-1]
        res_data[91: 97+1]=res[-7:][::-1]          
        
    if label=='right':     
        res_data[70: 76+1]=res[:7]   
        res_data[84: 90+1]=res[14:21]
        res_data[98: 104+1]=res[-7:]  
           
    return res_data


####------截取第2页第1个表（从上往下）------#####
def gethalf21(lefttop_x, rightbottom_x, lefttop_all_y, page, res_data,label, mat): #左上/右下x轴的值
    n=4  #共4行
    lefttop_y = lefttop_all_y  
    rightbottom_y = lefttop_all_y + 12*n # 12是表格中每一行的高度
    
    res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat)
    res=solvemistake(res) #手动纠错
    # print(res) 
    
    ###将每个结果写入res_data对应位置
    if label=='left': 
        res_data[107], res_data[109], res_data[111] = res[0], res[1], res[3]  
        
    if label=='right': 
        res_data[108], res_data[110], res_data[112] = res[0], res[1], res[3]    
           
    return res_data

####------截取第2页,第2个表------#####
def gethalf22(lefttop_x, rightbottom_x, lefttop_y, rightbottom_y, page, res_data, label, mat):
    res = prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat)

    res=solvemistake(res) #手动纠错
    # print(res) 
    
    ##将每个结果写入res_data对应位置
    if label=='left': res_data[113]=res[0]   
    if label=='right': res_data[114: 115+1]=res[0: 1+1] 
          
    return res_data

####------截取图片+预处理+ocr识别---###
def prohanding(lefttop_x, lefttop_y, rightbottom_x, rightbottom_y, page, mat):    
    mp = (lefttop_x, lefttop_y)        
    mp1 = (rightbottom_x, rightbottom_y)   
    clip = fitz.Rect(mp, mp1)  # 想要截取的区域,只要左上和右下坐标即可定位    
    pix = page.get_pixmap(matrix=mat, clip=clip) #截取的图片
    
    orgpng_path = './output/pic' + '/' + 'org_images.png'
    pix.save(orgpng_path)  # 将图片写入指定的文件夹内
    
    #图像预处理
    png_path = pic_preprocess(orgpng_path)
    
    #ocr识别
    reader = easyocr.Reader(['en'], gpu=False)
    print("结束OCR")  
    res = reader.readtext(png_path, detail=0, width_ths = 0.9) 
    return res

####---图片预处理
def pic_preprocess(png_path):     
    img = cv2.imread(png_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #彩色图转成灰度图       
    dst = cv2.equalizeHist(gray) #直方图均化        
    gaussian = cv2.GaussianBlur(dst, (3, 3), 0) # 高斯滤波降噪，(3, 3)卷积核
    # cv2.imshow("gaussian", gaussian)        
    img2 = cv2.Canny(gaussian, 50, 100, apertureSize=3) #边缘检测（高斯滤波卷积维度会影响边缘检测, (9,9)滤波降噪时会将直线检测为曲线）
    # cv2.imshow("img2", img2)      
    
    # '''霍夫直线检测'''
    minLineLength = 90 #90是线的宽度,比个短的线会忽略 
    maxLineGap = 10  #两条线段之间的最大间隔，如果小于此值，这两条直线就被看成是一条直线
    # HoughLinesP函数是概率直线检测，注意区分HoughLines函数
    lines = cv2.HoughLinesP(img2, 1, np.pi/180, 100, minLineLength=minLineLength,maxLineGap=maxLineGap) #100是识别的阈值
    lines1 = lines[:, 0, :]  # 降维处理    
    for x1, y1, x2, y2 in lines1: # line 函数勾画直线
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 9) #(x1,y1),(x2,y2)坐标位置； (255,255,255)设置BGR通道颜色为白色；9是设置颜色粗浅度
    # cv2.imshow('outtest2',img) 
    houghpng_path = './output/pic' + '/' + 'hough_images.png' 
    cv2.imwrite(houghpng_path, img)      

      
    
    # '''图像腐蚀'''
    src = cv2.imread(houghpng_path, cv2.IMREAD_UNCHANGED)

    kernel = np.ones((3,3), np.uint8) ## 设置卷积核5*5     
    erosion = cv2.erode(src, kernel) ## 图像的腐蚀，默认迭代次数
    # cv2.imshow('after erosion',erosion) #腐蚀后图片
    outpng_path = './output/pic' + '/'+ 'houghlines_erosion.png'

    cv2.imwrite(outpng_path, erosion) 
    #cv2.waitKey(0) #关闭图像show窗口
    cv2.destroyAllWindows()
    return outpng_path


##----ocr识别结果手动纠错---###
def solvemistake(res):
    ##--将识别为一行的数据进行拆分--###
    copy = res.copy() #复制res列表【不能用copy=res, 该方式当修改copy时, res也会修改】
    for j in range(len(copy)):
        item=copy[j] 
        if item.count('.') > 1:  #多个框的数字识别到一个字符串中
            temp=[] #字符串中各个数字组成的列表
            idx=[-1] #字符串中小数点的id
            for i in range(len(item)):
                if item[i]=='.' : idx.append(i+1)         
            for i in range(len(idx)-1):
                each = item[idx[i]+1: idx[i+1]+1]
                temp.append(each)   

            iddel=res.index(item) #待删除的item在res中的id
            res = res[:iddel] + temp + res[iddel+1:] #不取l[iddel]  
            
    res=[i.replace(' ','')  for i in res] #去除空格
    res=[i.replace(',','.') for i in res] #逗号换成小数点
    return res    

##----将列表数据写入excel/txt---###
def data_write(d, titles, datas, tem_path, pdf_name): 
    wb = openpyxl.load_workbook(tem_path) #打开excel模板文档
    sheet = wb.active
    
    ###---题头数据---###
    sheet['A'  + str(1)].value = 'Project name:' + titles[3]
    sheet['A'  + str(2)].value = 'Part name:' + titles[7]
    sheet['A'  + str(3)].value = 'Part NO.:' + titles[2] + 'Gear' + titles[10]
    sheet['A'  + str(4)].value = 'Drawing version:' + titles[4]
    sheet['A'  + str(5)].value = 'Ser NO.:' + titles[5]
    sheet['A'  + str(6)].value = 'Partner:' + titles[1]
    sheet['A'  + str(7)].value = 'Factory:' + titles[1]
    sheet['A'  + str(8)].value = 'Line NO.:' + titles[1]
    sheet['A'  + str(9)].value = 'Measure device NO.:' + titles[6]
    #将date修改为‘年月日’的顺序
    date=titles[8].split('.')
    date=''.join(date[::-1])
    sheet['A'  + str(10)].value = 'Date:' + date
    sheet['A'  + str(11)].value = 'Time:' + titles[9] + ':00'
    sheet['A'  + str(12)].value = 'Stats counts:' + str(d) #自增，第d个文件
    
    ###---除题头外的数据---###
    datas=[float(i) for i in datas] #将str转换为float
    j=13 #减去的值
    for i in range(14, 128+1):  # 将res_data中1-54个数据写入excel(#第'i'行)       
        if i==72: sheet['B'  + str(i)].value = round(datas[5] - datas[3], 1)
        elif i==73: sheet['B'  + str(i)].value = round(datas[12] - datas[10], 1)
        elif i==118: sheet['B'  + str(i)].value = round(datas[65] - datas[63], 1)        
        elif i==119: sheet['B'  + str(i)].value = round(datas[72] - datas[70], 1)
        else: sheet['B'  + str(i)].value = datas[i-j]
        
        sheet['F'  + str(i)].value = sheet['B'  + str(i)].value
        
    #没有Ca行时，删除excel中58-71行(共14行)
    if datas[45:51]==[0,0,0,0,0,0]: sheet.delete_rows(58, amount=14)
    
    out_fold='./output'
    xlsxpath=out_fold + '/' + 'xlsx' + '/' + '%s.xlsx' % pdf_name[:-4]
    print("xlsxpath:", xlsxpath)
    wb.save(xlsxpath) #保存文件,xlsx格式
    
    print('开始写入txt文件...')
    df = pd.read_excel(xlsxpath, header=None)
    df.to_csv(out_fold + '/' + 'txt' + '/' + '%s.txt' % pdf_name[:-4], header=None, sep='\t', index=False) # 写入txt, 以制表符'\t'分隔
    print('文件写入成功!')



        
        
        