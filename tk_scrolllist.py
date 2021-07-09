#!/usr/bin/python
# -*- coding: cp1251 -*-
from Tkinter import *

class Scrollist(Frame):
 def __init__(self, parent=None, **config):
   Frame.__init__(self, parent,config)
   self.pack(fill=BOTH, expand=YES)
   self.lst=Listbox(self, selectmode=SINGLE)
   self.make_windgets()
 def make_windgets(self):
   self.lst.pack(expand=YES, fill=BOTH)
   scr=Scrollbar(self.lst,command=self.lst.yview)
   scr.pack(side=RIGHT, fill=Y)
   self.lst.config(yscrollcommand=scr.set)
 def add_items(self,item,dir=END):
   self.lst.insert(dir, unicode(str(item),'cp1251'))
 def get_items(self):
   pass
   # ...
 def del_items(self):
   pass
   # ...

if __name__=='__main__':
 root = Tk()
 Form = Frame(root)
 Form.pack(fill=BOTH, expand=YES)
 MegaWidget=Scrollist(Form)
 for i in xrange(1000):
  MegaWidget.add_items('Item #'+str(i))
 MegaWidget.mainloop()
