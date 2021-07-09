#! /usr/bin/env python
# -*- coding: cp1251 -*-

from Tkinter import *
import time
import thread


class Clock(Label):

    def __init__(self, master, format, **kw):
	apply(Label.__init__, (self, master, kw))
	thread.start_new_thread(self.clock_update, (format,))

    def clock_update(self, format):
	while 1:    
	    try:
		current_time = time.strftime(format)
		self.config(text = current_time)
		self.update()
		time.sleep(1)
	    except TclError:
		thread.exit()


root = Tk(className="SPclock")
root.title("SPclock")
frame = Frame(root)
frame.pack()
clock = Clock(frame, '%H:%M:%S')
clock.bind("<Button-3>", lambda e: root.destroy())
clock.pack()
root.mainloop()
