# -*- coding: utf-8 -*-
"""
Created on 20 July 14:54:17 2022

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
import warnings
warnings.filterwarnings("ignore")

from shPdfOcr import *


def pyMuPDF_fitz(d, zoom_x, zoom_y, pdf_name, pdfPath, tem_path):

    pdfDoc = fitz.open(pdfPath) # 按页读取pdf
    
    page1 = pdfDoc[0] #第1页
    page2 = pdfDoc[1] #第2页
    rect = page1.rect  # 第pg页的页面大小,rect= Rect(0.0, 0.0, 595.2000122070312, 841.6799926757812)    

    rotate = int(0) # 图片旋转角度
    mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate) # 放大图片(x y轴同时放大)+旋转图片
    
    ###初始化储存空间
    res_title=['0' for i in range(11)] #题头共10个待识别字符串
    res_data=[0 for i in range(116)] #除题头外共有115个数字，len(res_data)=115,便于从1开始计数
    
    #"""第1页,第1个表（题头）"""
    lefttop_all_y11=71 #第1个表 左上y轴点的值
    mat11 = fitz.Matrix(12, 12).prerotate(rotate)  #数字和英文混合识别，增加放大倍数
    res_title = gettitle(0, 51, 147, page1, res_title, 'first', mat11) #读取题头标记的1.1处数据
    res_title = gettitle(57+320, 145+280, lefttop_all_y11, page1, res_title, 'middle', mat11) #读取题头标记的2.0处数据(放在res[10]中)
    res_title = gettitle(120, 270, lefttop_all_y11, page1, res_title, 'left', mat11)
    res_title = gettitle(475, 575, lefttop_all_y11-13, page1, res_title, 'right', mat11)
    print(res_title)
    
    #"""第1页，第2个表（从下往上截）"""
    lefttop_all_y12=rect.br[1]/2 - 12*1 #第二个表，左上y轴点的值
    rightbottom_all_y12=rect.br[1]/2 + 12*6 #右下y轴（最多有7行，最少6行）
    
    #1.------第1页,第2个表,最左边的参数列------#####    
    res_arg12 = getarg12(57, 80, rightbottom_all_y12, page1, mat)
    print(res_arg12)
   
    #2.------截取第1页第2个表，左/右表格的数据------#####
    mat12 = fitz.Matrix(5, 6).prerotate(rotate) #纵向放大倍数更大，消除一些短框线无法去除问题
    res_data=gethalf12(107, 558, rightbottom_all_y12, res_arg12, page1, res_data, 'first', mat12)    
    res_data=gethalf12(107, 298, rightbottom_all_y12, res_arg12, page1, res_data, 'left',  mat12) #第一页第二个表左边图（右-左读取，逆序）
    res_data=gethalf12(368, 558, rightbottom_all_y12, res_arg12, page1, res_data, 'right', mat12) #第一页第二个表左边图（左-右）    
    # print(res_data)
    
    """第1页,第3个表"""
    lefttop_all_y13=780
    res_data=gethalf13(107, 558, lefttop_all_y13-12, page1, res_data, 'first',  mat)    
    res_data=gethalf13(107, 298, lefttop_all_y13, page1, res_data, 'left',  mat)    
    res_data=gethalf13(368, 558, lefttop_all_y13, page1, res_data, 'right', mat)    
    # print(res_data)
    
    """第2页,第1个表（Act.value 两列）"""
    lefttop_all_y21=610
    res_data=gethalf21(237, 313, lefttop_all_y21, page2, res_data, 'left', mat)
    res_data=gethalf21(388, 464, lefttop_all_y21, page2, res_data, 'right', mat)
    # print(res_data)
    
    """第2页,第2个表"""
    res_data=gethalf22(237, 313, 802, 802+12, page2, res_data, 'left', mat)
    res_data=gethalf22(411+20, 453+85, 802+12, 802+24, page2, res_data, 'right', mat)
    print(res_data)
    
    data_write(d, res_title, res_data, tem_path, pdf_name) #将数据写入excel/txt


def main(pdfdir_path, paths, d):
    zoom_x, zoom_y = 5, 5 #x,y轴放大倍数
    for i in range(len(paths)):
        pdf_name=paths[i]
        print('处理第{0}个文件: {1}'.format(d, pdf_name)) # 显示处理到第几个文件,及其name
    

        #pdfPath = pdfdir_path + "/" + pdf_name #pdf文件的完整地址
        pdfPath=pdf_name
        tem_path = r"../template/shuanghuanTemplate.xlsx" #模板文档路径

        print(pdfPath)
        pyMuPDF_fitz(d, zoom_x, zoom_y, pdf_name, pdfPath, tem_path)


if __name__ =='__main__':
    pdfdir_path = r"../data"  # ----------->需要修改为pdf文件夹路径
    paths = os.listdir(pdfdir_path) # 获取pdfdir_path路径中所有pdf文件名，返回list
    d = 0  # 运行时显示处理到第几个文件了
    
    zoom_x, zoom_y = 5, 5  #x,y轴放大倍数
    for i in range(len(paths)):
        pdf_name=paths[i]
        print('处理第{0}个文件: {1}'.format(d, pdf_name)) # 显示处理到第几个文件,及其name
        pdfPath = pdfdir_path + "/" + pdf_name #pdf文件的完整地址  

        tem_path = r"../template/shuanghuanTemplate.xlsx" #模板文档路径

        pyMuPDF_fitz(d, zoom_x, zoom_y, pdf_name, pdfPath, tem_path)