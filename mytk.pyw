#!/usr/bin/env python
# -*- coding: cp1251 -*-

import sys
#sys.path+['\\CF Card\\Python24\\python24.zip\\lib-tk']
from Tkinter import *
import tkMessageBox
from ScrolledText import *
from tkFileDialog import *

def btnExit(event):
    fname=askopenfilename()
    tkMessageBox.showinfo(u'Выбор файла', u'Выбран файл:'+fname)
    tkMessageBox.showwarning(u'Выход', u'Хотите выйти?')
    resp=tkMessageBox.askyesno(u'Выход', u'Хотите выйти?')
    if 1==resp:
        root.quit()

def convUtf(event=None):
    global sText
    st=sText.get()
    #sText=event.char
    s=event.char
    st+=s.decode('utf8') 
    btn.config(text=st)

root=Tk()
sx, sy=root.wm_maxsize()
root.wm_geometry('%dx%d+0+%d' %(sx-6, sy-55, 3))
root.title(u'Главное окно')
fr=Frame(root)
fr.pack(expand=YES, fill=BOTH)
btnText='Это метка без привязки!'.decode('cp1251')
Label(fr, text=btnText, font=('',10,'bold')).pack(side=TOP, expand=NO, fill=X)
entry=Entry(fr)
sText=StringVar()
entry.config(textvariable=sText)
entry.bind('<KeyPress>', convUtf)
entry.pack(side=TOP, expand=NO, fill=X)
entry.insert(0, btnText)
btn=Button(fr, text=u'Выход')
btn.bind("<ButtonRelease>", btnExit)
btn.pack(side=TOP, expand=NO)
sct=ScrolledText(fr, bg="white", width=100, height=100)
sct.pack(side=TOP, expand=YES, fill=BOTH)
root.mainloop()

