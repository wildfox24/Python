#! /usr/bin/env python
# -*- coding: cp1251 -*-
from Tkinter import *

window=Tk()
window.title(u'Простое графическое окно')
label=Label(window, text=u'Простая текстовая метка')
label.config(fg='red', font=('Verdana', 14, 'bold'))
label.pack()
button=Button(window, text=u'Закрыть', font=('Verdana', 12, 'bold'), command=window.quit)
button.pack(expand=YES, fill=X)
window.mainloop()
