# coding: cp1251

import sys, os
from Tkinter import *

def fun_FolderDlg(path, mode='folder', *argv):
	font='Helvetica 10 bold'
	win = Toplevel()
	def quit():
		var_path.set(False)
		win.quit()
	
	def ok():
		win.quit()
	
	def UpdateDir():
		wg_list.delete(0,END)
		d=os.listdir(var_path.get())
		d.sort()
		if var_path.get() <>'\\': d.insert(0, '..')
		
		for j in d:
			if os.path.isdir(os.path.join(var_path.get(),j)) or j=='..':
				wg_list.insert(END, unicode(j))
		
		if mode=='folder': return
		for j in d:
			if os.path.isfile(os.path.join(var_path.get(),j)):
				if (var_ext.get()<>'*.*' and j.split('.')[-1].lower()==var_ext.get().split('.')[-1]) or var_ext.get()=='*.*':
					try:
						wg_list.insert(END, unicode(j))
					except: pass
		

	def fun_DirCh(event):
		if os.path.isdir(os.path.join(var_path.get(), wg_list.get(wg_list.curselection()))) or wg_list.get(wg_list.curselection())=='..':
			var_path.set(os.path.abspath(os.path.join(var_path.get(), wg_list.get(wg_list.curselection()))))
			UpdateDir()
			if mode <> 'folder': var_file.set('')
		else:
			if mode <> 'folder': var_file.set(wg_list.get(wg_list.curselection()))
		

	def fun_top():
		if var_path.get() <> '\\':
			var_path.set(os.path.abspath(os.path.join(var_path.get(), '..')))
			UpdateDir()

	wg_Frame0=Frame(win)
	if mode<>'folder':
		def fun_ext(a,b,c):
			UpdateDir()
		wg_Frame1=Frame(win)
		var_ext=StringVar()
		var_file=StringVar()
		wg_ext=OptionMenu(wg_Frame1, var_ext, *argv)
		wg_ext.pack(side=RIGHT)
		wg_ext['width']=6
		if mode=='save': Entry(wg_Frame1, width=18, textvariable=var_file, font=font).pack(side=LEFT, fill=X, expand=YES)
		else: Label(wg_Frame1, textvariable=var_file, width=5, anchor=W, font=font, relief=SUNKEN, bg='white').pack(side=LEFT, fill=X, expand=YES)
		var_ext.set('*.*')
		var_ext.trace('w', fun_ext)
		wg_Frame1.pack(fill=X)
	Label(wg_Frame0, width=5).pack(side=RIGHT)
	w=7
	Button(wg_Frame0, text=u'Вверх', width=w, command=fun_top).pack(side=LEFT)
	#Button(wg_Frame0, text=u'Зайти', width=w).pack(side=LEFT)
	Button(wg_Frame0, text=u'Отмена', width=w, command=quit).pack(side=RIGHT)
	Button(wg_Frame0, text=u'Выбор', width=w, command=ok).pack(side=RIGHT)
	wg_Frame0.pack(side=BOTTOM, fill=X)
	var_path=StringVar()
	Label(win, textvariable=var_path, width=5, relief=SUNKEN, bg='white', font=font, anchor=E).pack(fill=X)
	var_path.set(path)
	if mode=='open': win.title(u'Открыть файл')
	elif mode=='save': win.title(u'Сохранить файл')
	else: win.title(u'Выбор каталога')
	win.protocol('WM_DELETE_WINDOW', quit)
	wg_scr=Scrollbar(win, orient=VERTICAL)
	wg_scr.pack(side=RIGHT, fill=Y)
	wg_list=Listbox(win, width=15, height=5, yscrollcommand=wg_scr.set, font=font)
	wg_list.pack(side=LEFT, fill=BOTH, expand=YES)
	wg_list.bind('<ButtonRelease>', fun_DirCh)
	wg_scr['command']=wg_list.yview
	UpdateDir()
	if sys.platform == 'Pocket PC':
		win.state('zoomed')
	
	win.focus_set()
	win.grab_set()
	win.mainloop()
	win.destroy()

	if var_path.get() == 'False': return False
	
	if mode=='folder': return var_path.get()
	else:
		#if os.path.isfile(os.path.join(var_path.get(), var_file.get())):
		
		return var_path.get(), var_file.get(), os.path.join(var_path.get(), var_file.get())


