#!/usr/bin/env python
# -*- coding: cp1251 -*-

import sys
import math
from Tkinter import *
s=u"График функции"
tk = Tk()
tk.title(s)
f=Frame(tk)
f.pack()
c = Canvas(f, bg="White", width=200, height=290)
c.pack(expand=1, fill=BOTH)
line = []
line1 = []
for x in range(1, 490, 2):
  line.extend([x+5, 150-int(math.sin(x/25.)*50)])
  line1.extend([x+5, 150-int(math.cos(x/25.)*50)])
c.create_line(line, smooth="1")
c.create_line(line1)
c.create_line(0, 150, 490, 150, arrow="last")
c.create_line(5, 10, 5, 290, arrow="first")
c.create_text(90, 60, text=s+": y=sin(x)", font=("Verdana","8","bold","underline"))
c.create_text(165, 80, text="2p", font=("Arial","10"), anchor=NW)
c.create_text(9, 80, text="0", font=("Arial","10"), anchor=NW)
tk.mainloop()

