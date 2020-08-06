#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk, ImageGrab,ImageEnhance
import threading
from urllib import request
import ssl
from bs4 import BeautifulSoup
import tkinter.font as tkFont
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
import time
# 摄像机设置
# 0是代表摄像头编号，只有一个的话默认为0
capture = cv.VideoCapture(0)

def closecamera():
    capture.release()
def button1():
    global headimage#大头照
    global halfimage#半身照
    name, idnum = getnameandID()
    if idnum=="IDCardNo'].value='":
        idnum = simpledialog.askstring('手动输入身份证', '无法读取，请输入', initialvalue="请输入身份证号码")
    ref, frame = capture.read()
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    face_cascade = cv.CascadeClassifier('./config.xml')
    faces = face_cascade.detectMultiScale(cvimage, 1.15,3) #人脸检测
    try:
        x=faces[0][0]
        y=faces[0][1]
        w=faces[0][2]
        h=faces[0][3]
        # 抓取1寸照
        headimage = frame[y - int(h / 2): y + h + int(h * 0.6), x - int(w / 3): x + w + int(w / 3)]
        headimage = cv.resize(headimage, (206, 289), interpolation=cv.INTER_CUBIC)
        cv.imencode('.jpg', headimage)[1].tofile(lb1["text"] + '/' + idnum + '.jpg')  # 支持中文路径

        #打开图片调亮度
        headimg=Image.open(lb1["text"] + '/' + idnum + '.jpg')
        # 获取亮度调整期
        image_bright = ImageEnhance.Brightness(headimg)
        # 亮度增强, 参数大于1增强
        headimg = image_bright.enhance(brparam)

        # 获取色彩调整期
        image_color = ImageEnhance.Color(headimg)
        # 色彩, 参数大于1增强
        headimg = image_color.enhance(clparam)

        # 对比度调解
        headimg = headimg.point(lambda i: i * lmparam)
        #保存图片
        headimg.save(lb1["text"] + '/' + idnum + '.jpg',quality=95, subsampling=0)




        # 抓取半身照
        halfimage = frame[y - int(h * 0.8): y + h + int(h *3), x - int(w * 1.6): x + w + int(w * 1.6)]
        halfimage = cv.resize(halfimage, (413, 500), interpolation=cv.INTER_CUBIC)
        cv.imencode('.jpg', halfimage)[1].tofile(lb2["text"]+ '/' + idnum + '.jpg')  # 支持中文路径

        # 打开图片调亮度
        halfimg = Image.open(lb2["text"] + '/' + idnum + '.jpg')
        # 获取亮度调整期
        image_bright = ImageEnhance.Brightness(halfimg)
        # 亮度增强, 参数大于1增强
        halfimg = image_bright.enhance(brparam)

        # 获取色彩调整期
        image_color = ImageEnhance.Color(halfimg)
        # 色彩, 参数大于1增强
        halfimg = image_color.enhance(clparam)

        # 对比度调解
        halfimg = halfimg.point(lambda i: i * lmparam)
        # 保存图片
        halfimg.save(lb2["text"] + '/' + idnum + '.jpg', quality=95, subsampling=0)



    except:
        pass
    #显示身份证号码和姓名
    ft =tkFont.Font(family='楷体', size=10, weight=tkFont.BOLD)
    lb=Label(top, text=name+":"+idnum, font=ft, width=30, height=2,fg="red")
    lb.place(x=170, y=490)
    #预览1寸照片
    global img
    global tkImage1
    img = Image.open(lb1["text"]+'/'+idnum+".jpg")  # 打开图片
    tkImage1 = ImageTk.PhotoImage(image=img)
    canvas1.create_image(0, 0, anchor=NW, image=tkImage1)

    # 预览半身照片
    global img2
    global tkImage11
    img2 = Image.open(lb2["text"]+'/'+idnum+".jpg")  # 打开图片
    tkImage11 = ImageTk.PhotoImage(image=img2)
    canvas2.create_image(0, 0, anchor=NW, image=tkImage11)
    top.update()
#获取姓名和身份证号码
'''
def getnameandID():
    # 利用非认证上下文环境替换认证的上下文环境
    ssl._create_default_https_context = ssl._create_unverified_context
    # 需要这样设置一下
    url = "https://127.0.0.1:20008/doreadcard"
    rsp = request.urlopen(url)
    html = rsp.read().decode()
    soup = BeautifulSoup(html, 'html.parser')
    name=soup.script.string.split(";")[5][-4:-1]
    id=soup.script.string.split(";")[14][-19:-1]
    return name,id

'''
def getnameandID():
    return "name","412326189089892121"

#选择保存路径1寸照
def selectPath():
    global path
    path=StringVar()
    path_ = askdirectory()
    path.set(path_)
    if path.get():
        lb1["text"]=path.get()
        fr1= open('pathfile1', 'w', encoding='utf-8')
        fr1.write(path.get())
        fr1.close()

#选择保存路径半身照
def selectPath1():
    global path1
    path1=StringVar()
    path_ = askdirectory()
    path1.set(path_)
    if path1.get():
        lb2["text"] = path1.get()
        fr2 = open('pathfile2', 'w', encoding='utf-8')
        fr2.write(path1.get())
        fr2.close()

#亮度响应函数
brparam = 1
def scale_bright(scale_var):
    global brparam
    brparam=float(scale_var)+1

#色彩调解
clparam=1
def scale_color(scale_var):
    global clparam
    clparam=float(scale_var)+1

#对比调解
lmparam=1
def scale_lambda(scale_var):
    global lmparam
    lmparam=float(scale_var)+1


# 界面相关
window_width = 1345
window_height =700
image_width = int(window_width * 0.6)
image_height = int(window_height * 0.6)
#图片放置位置
imagepos_x = 20
imagepos_y = int(window_height * 0.01)
#按钮放置位置
butpos_x = 20
butpos_y = 480

#创建界面
top = Tk()
top.wm_title("Face*recognition")
top.geometry(str(window_width) + 'x' + str(window_height))
#top.iconbitmap('./ico.ico')
#画布区域
canvas = Canvas(top, bg='white', width=625, height=480)  # 绘制画布
#canvas = Canvas(top, bg='white')  # 绘制画布
canvas1 = Canvas(top, bg='white', width=206, height=289)  # 绘制画布
canvas2 = Canvas(top, bg='white', width=413, height=500)  # 绘制画布

#拍照按钮
ft = tkFont.Font(family='楷体', size=11, weight=tkFont.BOLD) #字体设置
b = Button(top, text='保存照片', font=ft, width=14, height=2, command=button1)
b1=Button(top, text='设置1寸照路径', font=ft, width=14, height=2, command=selectPath)
b2=Button(top, text='设置半身照路径', font=ft, width=14, height=2, command=selectPath1)

# 控件位置设置
canvas.place(x=imagepos_x, y=imagepos_y)#动态预览画面
canvas1.place(x=260+400, y=imagepos_y)  # 1寸照预览
canvas2.place(x=500+400, y=imagepos_y)  # 半身照预览
b.place(x=butpos_x, y=butpos_y+15)
b1.place(x=butpos_x,y=butpos_y+80)
b2.place(x=butpos_x,y=butpos_y+160)
#大头照保存地址
ft = tkFont.Font(family='楷体', size=10, weight=tkFont.BOLD)
lb1=Label(top, width=60,font=ft, height=2,bg='white',anchor=NW)
lb1.place(x=180, y=565)
f = open('pathfile1', 'r', encoding='utf-8')
rpath1=f.read()
lb1['text']=rpath1
f.close()

#半身照保存地址
lb2=Label(top,width=60,font=ft, height=2, bg='white',anchor=NW)
lb2.place(x=180, y=640)
f = open('pathfile2', 'r', encoding='utf-8')
rpath2=f.read()
lb2['text']=rpath2
f.close()

#照片预览标签
ft = tkFont.Font(family='楷体', size=10, weight=tkFont.BOLD)
Label(top,width=10,font=ft, height=2, anchor=NW,text="1寸照预览").place(x=706, y=300)
Label(top,width=12,font=ft, height=2, anchor=NW,text="半身照照预览").place(x=1050, y=510)

#调解亮度
br=Scale(top,label='亮度调解',from_=-1,to=1,orient=HORIZONTAL,length = 200,showvalue=0,tickinterval=1,resolution=0.01
,command=scale_bright)
br.place(x=670,y=330)
#调解色彩
br=Scale(top,label='色彩调解',from_=-1,to=1,orient=HORIZONTAL,length = 200,showvalue=0,tickinterval=1,resolution=0.01
,command=scale_color)
br.place(x=670,y=400)
#调解对比度
br=Scale(top,label='对比度调解',from_=-1,to=1,orient=HORIZONTAL,length = 200,showvalue=0,tickinterval=1,resolution=0.01
,command=scale_lambda)
br.place(x=670,y=470)

def tkImage():
    camera = cv.VideoCapture(0)
    face_cascade = cv.CascadeClassifier('./config.xml')
    global gcvimage
    global gpilImage

    while True:
        ref, frame = camera.read()
        image1 = frame
        cvimage2 = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        faces = face_cascade.detectMultiScale(cvimage2, 1.15, 3)#画人脸方框
        if len(faces)>0:
            for (x, y, w, h) in faces:
                #1寸照方框
                cv.rectangle(frame, (x-int(w/3), y -int(h/2)), (x + w + int(w/3), y + h + int(h*0.6)), (255, 0, 0), 2)
                # 标注文本
                font = cv.FONT_HERSHEY_SIMPLEX
                text = '1'
                cv.putText(frame, text, (x-int(w/3), y -int(h/2)), font, 1, (255, 0, 0), 2)
                #半身照框框
                cv.rectangle(frame, (x - int(w * 1.6), y - int(h*0.8)), (x + w + int(w * 1.6), y + h + int(h *3)),
                             (0, 0, 225), 2)
                #标注文本
                font = cv.FONT_HERSHEY_SIMPLEX
                text = '2'
                cv.putText(frame, text, (x - int(w * 1.6), y - int(h*0.8)), font, 2, (0, 0, 255), 2)
                #把脸投向窗口
                #image1 = frame[y-int(h/2): y + h+int(h*0.6), x-int(w/3): x +w + int(w/3)]
                #image1 = frame
                #if len(image1) != 0:

        gcvimage = cv.cvtColor(image1, cv.COLOR_BGR2RGBA)
        gpilImage = Image.fromarray(gcvimage)

        # 获取亮度调整期
        image_bright = ImageEnhance.Brightness(gpilImage)
        # 亮度增强, 参数大于1增强
        gpilImage = image_bright.enhance(brparam)

        # 获取色彩调整期
        image_color = ImageEnhance.Color(gpilImage)
        # 色彩增强, 参数大于1增强
        gpilImage = image_color.enhance(clparam)

        #对比度调解
        gpilImage = gpilImage.point(lambda i: i * lmparam)

        tkImage = ImageTk.PhotoImage(image=gpilImage)
        canvas.create_image(0, 0, anchor='nw', image=tkImage)
        #top.update()
        cv.waitKey(200)
        #cv.imshow('camera', frame)
        #if cv.waitKey(int(1000 / 12)) & 0xff == ord("q"):
        #    break
'''
                try:
                    image1 = cv.resize(image1, (206, 289))  # 保存为1寸照片
                    cvimage3 = cv.cvtColor(image1, cv.COLOR_BGR2RGBA)

                    top.update()
                    pilImage3 = Image.fromarray(cvimage3)
                    pilImage3.resize((289, 206), Image.ANTIALIAS)
                    tkImage = ImageTk.PhotoImage(image=pilImage3)
                    canvas.create_image(0, 0, anchor='nw', image=tkImage)
                    cv.waitKey(150)
                except:
                    print("error")
        image1 = frame
        #显示cv窗口
        cv.imshow('camera', frame)
        if cv.waitKey(int(1000/12)) & 0xff == ord("q"):
            break
'''
if __name__ == "__main__":
    t=threading.Thread(target=tkImage)
    t.start()
    top.mainloop()
    closecamera()
