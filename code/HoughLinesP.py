# -*- coding: utf-8 -*-
"""
Created on 20 July 15:06:28 2022

@author: Ting
"""

import cv2
import numpy as np

imagePath = '../output/pic/org_images.png'
img = cv2.imread(imagePath)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

dst = cv2.equalizeHist(gray) #直方图均化

gaussian = cv2.GaussianBlur(dst, (3, 3), 0) # 高斯滤波降噪（(3, 3)卷积）
# cv2.imshow("gaussian", gaussian)

img2 = cv2.Canny(gaussian, 50, 100, apertureSize=3) #边缘检测（高斯滤波卷积维度会影响边缘检测, (9,9)滤波降噪时会将直线检测为曲线）
cv2.imshow("img2", img2)


minLineLength = 90 #线的宽度,比个短的线会忽略
maxLineGap = 10  #两条线段之间的最大间隔，如果小于此值，这两条直线就被看成是一条直线
# HoughLinesP函数是概率直线检测，注意区分HoughLines函数
lines = cv2.HoughLinesP(img2, 1, np.pi/180, 100, minLineLength=minLineLength,maxLineGap=maxLineGap)
lines1 = lines[:, 0, :]  # 降维处理
# line 函数勾画直线
# (x1,y1),(x2,y2)坐标位置
# (0,255,0)设置BGR通道颜色
# 2 是设置颜色粗浅度
for x1, y1, x2, y2 in lines1:
    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 9)

cv2.imshow('outtest2',img) 
cv2.imwrite('../output/houghlines_test2.png',img) 
houghpng_path = '../output/houghlines_test2.png'

# '''图像腐蚀'''
src = cv2.imread(houghpng_path, cv2.IMREAD_UNCHANGED)
kernel = np.ones((3,3), np.uint8) ## 设置卷积核3*3     
erosion = cv2.erode(src, kernel) ## 图像的腐蚀，默认迭代次数
cv2.imshow('after erosion',erosion) #腐蚀后图片
outpng_path = '../output' + '/'+ 'houghlines_erosion.png'
cv2.imwrite(outpng_path, erosion) 

cv2.waitKey(0) #关闭图像show窗口
cv2.destroyAllWindows()


'''将所有方框线去除后，一起识别效果不好：因为默认横向识别，而横向每个数字较挤'''
import easyocr
png_path='../output/houghlines_test2.png'
reader = easyocr.Reader(['en'], gpu=False)  
res = reader.readtext(png_path, detail=0, width_ths = 0.5) 
print(res)




