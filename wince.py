import sys
import os

sample = "sample.txt"

if os.name == 'ce':
    global sample
    import sys
    sys.path.insert(0, "\\Program Files\\Python\\lib\\python23.zip\\lib-tk")
    sample = "\\My Documents\\Personal\\sample.txt"

from Tkinter import *

class AllTkinterWidgets:
    def __init__(self, master):
        frame = Frame(master, width=240, height=320, bd=1)
        frame.pack()

	self.mbar = Frame(frame, relief = 'raised', bd=2)
	self.mbar.pack(fill = X)

	# Create File menu
	self.filebutton = Menubutton(self.mbar, text = 'File')
	self.filebutton.pack(side = LEFT)

	self.filemenu = Menu(self.filebutton, tearoff=0)
	self.filebutton['menu'] = self.filemenu

	# Populate File menu
	self.filemenu.add('command', label = 'Exit', command = self.quit)

	# Create  edit menu
	self.editbutton = Menubutton(self.mbar, text = 'Edit')
	self.editbutton.pack(side = LEFT)

	self.editmenu = Menu(self.editbutton, tearoff=0)
	self.editbutton['menu'] = self.editmenu

	# Populate edit menu
	self.editmenu.add('command', label = 'edit', command = self.stub)

	# Create  view menu
	self.viewbutton = Menubutton(self.mbar, text = 'View')
	self.viewbutton.pack(side = LEFT)

	self.viewmenu = Menu(self.viewbutton, tearoff=0)
	self.viewbutton['menu'] = self.viewmenu

	# Populate view menu
	self.viewmenu.add('command', label = 'view', command = self.stub)

	# Create  help menu
	self.helpbutton = Menubutton(self.mbar, text = 'Help')
	self.helpbutton.pack(side = RIGHT)

	self.helpmenu = Menu(self.helpbutton, tearoff=0)
	self.helpbutton['menu'] = self.helpmenu

	# Populate help menu
	self.helpmenu.add('command', label = 'help', command = self.stub)

        iframe1 = Frame(frame, bd=2, relief=SUNKEN)
        Button(iframe1, text='Click').pack(side=LEFT, padx=5)
        Checkbutton(iframe1, text='Check').pack(side=LEFT, padx=5)

        v=IntVar()
        Radiobutton(iframe1, text='dio', variable=v,
                    value=2).pack(side=RIGHT, anchor=W)
        Radiobutton(iframe1, text='Ra', variable=v,
                    value=1).pack(side=RIGHT, anchor=W)
        iframe1.pack(expand=1, fill=X, pady=10, padx=5)

        iframe2 = Frame(frame, bd=2, relief=RIDGE)
        Label(iframe2, text='Label:').pack(side=LEFT, padx=5)
        t = StringVar()
        Entry(iframe2, textvariable=t, font=("arial", 8, "normal"),
bg='white').pack(side=RIGHT, padx=0)
        t.set('Entry')
        iframe2.pack(expand=1, fill=X, pady=5, padx=5)

        iframe3 = Frame(frame, bd=2, relief=SUNKEN)
        text=Text(iframe3, height=5, width =30, font=("arial", 8, "normal"))
        fd = open(sample)
        lines = fd.read()
        fd.close()
        text.insert(END, lines)
        text.pack(side=LEFT, fill=X, padx=5)
        sb = Scrollbar(iframe3, orient=VERTICAL, command=text.yview)
        sb.pack(side=RIGHT, fill=Y)
        text.configure(yscrollcommand=sb.set)
        iframe3.pack(expand=1, fill=X, pady=10, padx=5)

        iframen = Frame(frame, bd=2, relief=FLAT)
        Message(iframen, text='This is a Message widget', width=240,
                relief=SUNKEN).pack(fill=X, padx=5)
        iframen.pack(expand=1, fill=X, pady=5, padx=5)

    def quit(self):
        root.destroy()

    def stub(self):
        pass
    
root = Tk()
root.option_add('*font', ('arial', 8, 'bold'))
all = AllTkinterWidgets(root)
root.title('Tkinter Widgets')
root.mainloop()