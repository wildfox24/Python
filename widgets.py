#! /usr/bin/env python
# -*- coding: cp1251 -*-

from Tkinter import *

root = Tk()
root.title(u"Примеры визуальных компонентов")

menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.destroy)

edit_menu = Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo")
edit_menu.add_separator()
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste", state=DISABLED)

frame = Frame(root)
frame.grid()

btn = Button(frame, text="Button")
btn.grid(row=0, column=1)

lbl = Label(frame, text="Label")
lbl.grid(row=0, column=0)

txt = Text(frame, width=30, height=6)
txt.grid(row=1, column=0)
txt.insert(AtInsert(), "Text. "*20)

cbtn = Checkbutton(frame, text="Checkbutton")
cbtn.grid(row=2, column=0)

lst = Listbox(frame, height=4, bg="white")
lst.grid(row=1, column=1)
lst.insert('end', "Item 1")
lst.insert('end', "Item 2")

radioframe = Frame(frame, relief=RAISED, borderwidth=2)
radioframe.grid(row=2, column=1, rowspan=3)

wave = StringVar()
wave.set("1")

radioframe.r1 = Radiobutton(radioframe, text="LW",
                            variable=wave, anchor=W, value="1")
radioframe.r1.pack(fill=X)
radioframe.r2 = Radiobutton(radioframe, text="MW",
                            variable=wave, anchor=W, value="2")
radioframe.r2.pack(fill=X)
radioframe.r3 = Radiobutton(radioframe, text="FM",
                            variable=wave, anchor=W, value="3")
radioframe.r3.pack(fill=X)

pic = Canvas(frame, relief=SUNKEN, bg='white', width=200,height=60)
pic.grid(row=4, column=0)

pic.create_rectangle(2, 2, "30", "30", fill="black")
pic.create_oval(10, 10, 50, 50, fill="white")
    
lbl2 = Label(frame, text="(Canvas)", bg="white")
pic.create_window(60, 30, window=lbl2)

root.mainloop()
