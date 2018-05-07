# #!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/7 16:29
# @Author  : Victor (weigang) QIU
# @web     : http://www.weigang.com
# @Email   : qiu@weigang.com
# @File    : SignatureCreator.py
# @Software: PyCharm

from tkinter import *
from tkinter import messagebox
import requests
# regular express
import re
# image toolkit
from PIL import Image,ImageTk



def download_pic():
    startUrl = "http://www.uustv.com/"
    #  get name from the "entry box" when press button
    name = entry.get()
    # getrid of space strip去掉前后空格
    name = name.strip()
    if name =="":
        # if user didnt enter any characters
        messagebox.showinfo('please','enter your name')
    else:
        #  dict type,post some parameters "form data" 字典类型,网站上面签名传递的4个参数 用f12看到的  form data
        dict_paras = {
            #var name = get from user input
            'word':name ,
            'sizes':'60',
            'fonts':'jfcs.ttf',
            'frontcolor':'#000000'
        }
        result = requests.post(startUrl,data=dict_paras)
        result.encoding = 'utf-8'
        # now we get the whole html content, but we should extract the name.gif only
        html = result.text
        # print(result)
        # print(html)

        # whole html    <html xmlns="http://www.w3.org/1999/xhtml">
        # < div class ="tu" > ﻿ < img src="tmp/152567288753517.gif" / > < / div >
        #  whole html here    </html>
        # we use regular express here. (.*?) means match all
        # (.* ?)  be aware we should use ()
        reg = '<div class="tu">﻿<img src="(.*?)"/></div>'
        # reg means pattern, in str html
        imagePath = re.findall(reg,html)
        # print(imagePath)
        # something like imagePath == ['tmp/152567379449133.gif']
        imageUrl = startUrl + imagePath[0]
        # print(imageUrl)
        # something like imageUrl ==http://www.uustv.com/tmp/152567398539092.gif

        # get image content
        response = requests.get(imageUrl).content
        # mode==write binary save name.gif in the same dirctory
        with open('{}.gif'.format(name),'wb') as f:
            f.write(response)
        bm = ImageTk.PhotoImage(file='{}.gif'.format(name))
        label2 = Label(root,image = bm)
        label2.bm = bm
        label2.grid(row = 2,columnspan = 2)



# create main window
root = Tk()
root.title("Signature Creator 签名生成器 v0.1 www.weigang.com")
# should use small x
root.geometry("600x300")
# position
root.geometry("+500+300")
# root.geometry("600x300+500+300")
label = Label(root,text="enter your name",font=('verdana',15),fg='green')
label.grid()
entry = Entry(root,font=('雅黑',20),fg='green')
# layout  pack or place
entry.grid(row = 0,column = 1)
# after user press button ,then call download_pic function
button = Button(root,text="Generate",font=('verdana',15),command = download_pic)
# e=east
button.grid(row = 1,column = 1,sticky=E)



# 显示窗口 消息循环
root.mainloop()