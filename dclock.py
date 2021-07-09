#! /usr/bin/env python
# -*- coding: cp1251 -*-

from Tkinter import *
import time

root = Tk(); lf = LabelFrame(root,text=u" Электронные часы "); lf.pack()
root.title(u"Электронные часы")
time_var = StringVar()
time_label = Label(lf, textvariable=time_var, font="Courier 50", bg="Black", fg="#00B000")
time_label.pack()
date = Label(lf, text=time.strftime("%A %d-%m-%Y", time.localtime()), font="Verdana 12", bg="Black", fg="#00B000")
date.pack(expand=1, fill=X)
def tick():
  """Обновление табло электронных часов"""
  t = time.localtime(time.time())
  if t[5] % 2:  # эффект мигающего двоеточия
    fmt = "%H:%M"
  else:
    fmt = "%H %M"
  time_var.set(time.strftime(fmt, t))
  time_label.after(500, tick)  # следующий tick через 0.5 с

time_label.after(500, tick)
root.mainloop()
