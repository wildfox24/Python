from Tkinter import *
import math

tk = Tk(); tk.title(u'График функции'); f = Frame(tk); f.pack()
c = Canvas(f, bg="White", width=300, height=200)
c.pack(expand=1, fill=BOTH)
line = []
for x in range(1, 290, 2):
  line.extend([x+5, 100-int(math.sin(x/25.)*50)])
c.create_line(line)
c.create_line(0, 100, 290, 100, arrow="last")
c.create_line(5, 10, 5, 190, arrow="first")
c.create_text(90, 60, text="y=sin(x)")
c.create_text(165, 100, text="2p", font="Symbol", anchor=NW)
c.create_text(9, 100, text="0", font="Symbol", anchor=NW)
tk.mainloop()

