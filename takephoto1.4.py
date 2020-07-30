#!/usr/bin/python
# -*- coding: UTF-8 -*-
from tkinter import *
import cv2 as cv
from PIL import Image, ImageTk
import threading
from urllib import request
import ssl
from bs4 import BeautifulSoup
import tkinter.font as tkFont
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
# 摄像机设置
# 0是代表摄像头编号，只有一个的话默认为0
capture = cv.VideoCapture(0)

def getframe():
    ref, frame = capture.read()

def closecamera():
    capture.release()

def button1():
    global image1
    global image5
    name, idnum = getnameandID()
    if idnum=="IDCardNo'].value='":
        idnum = simpledialog.askstring('手动输入身份证', '无法读取，请输入', initialvalue="请输入身份证号码")
    ref, frame = capture.read()
    cvimage = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    face_cascade = cv.CascadeClassifier('./config.xml')
    faces = face_cascade.detectMultiScale(cvimage, 1.3, 5) #人脸检测
    try:
        x=faces[0][0]
        y=faces[0][1]
        w=faces[0][2]
        h=faces[0][3]
        # 抓取1寸照
        image1 = frame[y - int(h / 2): y + h + int(h * 0.6), x - int(w / 3): x + w + int(w / 3)]
        image1 = cv.resize(image1, (206, 289), interpolation=cv.INTER_CUBIC)
        cv.imencode('.jpg', image1)[1].tofile(path.get() + '/' + idnum + '.jpg')  # 支持中文路径

        # 抓取半身照
        image5 = frame[y - int(h * 0.8): y + h + int(h *3), x - int(w * 1.6): x + w + int(w * 1.6)]
        image5 = cv.resize(image5, (413, 500), interpolation=cv.INTER_CUBIC)
        cv.imencode('.jpg', image5)[1].tofile(path1.get() + '/' + idnum + '.jpg')  # 支持中文路径
    except:
        print('error')


    #显示身份证号码和姓名
    ft =tkFont.Font(family='Fixdsys', size=14, weight=tkFont.BOLD)
    lb=Label(top, text=name+"\n"+idnum, font=ft, width=20, height=3)
    lb.place(x=20, y=350)

    #预览1寸照片
    global img
    global tkImage1
    img = Image.open(path.get()+'/'+idnum+".jpg")  # 打开图片
    tkImage1 = ImageTk.PhotoImage(image=img)
    canvas1.create_image(0, 0, anchor='nw', image=tkImage1)


    # 预览半身照片
    global img2
    global tkImage11
    img2 = Image.open(path1.get()+'/'+idnum+".jpg")  # 打开图片
    tkImage11 = ImageTk.PhotoImage(image=img2)
    canvas2.create_image(0, 0, anchor='nw', image=tkImage11)
    top.update()
#获取姓名和身份证号码
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

#选择保存路径1寸照
def selectPath():
    global path
    path=StringVar()
    path_ = askdirectory()
    path.set(path_)
    ft1 = tkFont.Font(family='Fixdsys', size=10, weight=tkFont.BOLD)
    lb1 = Label(top, text=path.get(), font=ft1, width=80, height=2)
    lb1.place(x=200, y=560)


#选择保存路径半身照
def selectPath1():
    global path1
    path1=StringVar()
    path_ = askdirectory()
    path1.set(path_)
    ft2 = tkFont.Font(family='Fixdsys', size=10, weight=tkFont.BOLD)
    lb2= Label(top, text=path1.get(), font=ft2, width=80, height=2)
    lb2.place(x=200, y=620)

# 界面相关
window_width = 930
window_height =700
image_width = int(window_width * 0.6)
image_height = int(window_height * 0.6)
#图片放置位置
imagepos_x = 20
imagepos_y = int(window_height * 0.01)
#按钮放置位置
butpos_x = 20
butpos_y = 450

#创建界面
top = Tk()
top.wm_title("Face recognition")
top.geometry(str(window_width) + 'x' + str(window_height))
#top.iconbitmap('./ico.ico')
#画布区域
canvas = Canvas(top, bg='white', width=206, height=289)  # 绘制画布
canvas1 = Canvas(top, bg='white', width=206, height=289)  # 绘制画布
canvas2 = Canvas(top, bg='white', width=413, height=500)  # 绘制画布
#拍照按钮
ft = tkFont.Font(family='Fixdsys', size=12, weight=tkFont.BOLD)
b = Button(top, text='保存照片', font=ft, width=14, height=2, command=button1)
b1=Button(top, text='设置1寸照路径', font=ft, width=14, height=2, command=selectPath)
b2=Button(top, text='设置半身照路径', font=ft, width=14, height=2, command=selectPath1)



# 控件位置设置
canvas.place(x=imagepos_x, y=imagepos_y)#动态预览画面
canvas1.place(x=260, y=imagepos_y)  # 1寸照预览
canvas2.place(x=500, y=imagepos_y)  # 半身照预览
b.place(x=butpos_x, y=butpos_y)
b1.place(x=butpos_x,y=butpos_y+80)
b2.place(x=butpos_x,y=butpos_y+160)

def tkImage():
    camera = cv.VideoCapture(0)
    face_cascade = cv.CascadeClassifier('./config.xml')
    global cvimage3
    global pilImage3
    while True:
        ref, frame = camera.read()
        cvimage2 = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
        faces = face_cascade.detectMultiScale(cvimage2, 1.3, 5)#画人脸方框
        if len(faces)>0:
            for (x, y, w, h) in faces:
                #1寸照方框
                cv.rectangle(frame, (x-int(w/3), y -int(h/2)), (x + w + int(w/3), y + h + int(h*0.6)), (255, 0, 0), 2)
                #半身照框框
                cv.rectangle(frame, (x - int(w * 1.6), y - int(h*0.8)), (x + w + int(w * 1.6), y + h + int(h *3)),
                             (0, 0, 225), 2)
                #把脸投向窗口
                image1 = frame[y-int(h/2): y + h+int(h*0.6), x-int(w/3): x +w + int(w/3)]
                if len(image1) != 0:
                    try:
                        image1 = cv.resize(image1, (206, 289))  # 保存为1寸照片
                        cvimage3 = cv.cvtColor(image1, cv.COLOR_BGR2RGBA)

                        top.update()
                        pilImage3 = Image.fromarray(cvimage3)
                        pilImage3.resize((289, 206), Image.ANTIALIAS)
                        tkImage = ImageTk.PhotoImage(image=pilImage3)
                        canvas.create_image(0, 0, anchor='nw', image=tkImage)
                        k = cv.waitKey(150)
                    except:
                        print("error")

        #显示cv窗口
        cv.imshow('camera', frame)
        if cv.waitKey(int(1000/12)) & 0xff == ord("q"):
            break

if __name__ == "__main__":
    t=threading.Thread(target=tkImage)
    t.start()
    top.mainloop()
    closecamera()
