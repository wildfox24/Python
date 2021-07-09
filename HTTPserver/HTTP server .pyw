#
# -*- coding: cp1251 -*-
# Python 2.4.3
# Простой HTTP CGI сервер

# Стандартные модули:

import sys, os, thread
import BaseHTTPServer, CGIHTTPServer
import httplib, csv
from Tkinter import *


# Наши модули:

from MyDialogs import *


# Глобальные объекты:

root = Tk()

f_Run = False # Флаг: запущен ли сервер

def fun_LoadIniFile():
	global voc_Ini
	
	try:
		s_IniFileName = os.path.basename(sys.argv[0]).split('.')[0]+' ini.txt'
		voc_Ini = {}
		for j in csv.reader(file(s_IniFileName, 'rb'), dialect='excel-tab'):
			voc_Ini[j[0]] = j[1]
		
		test = voc_Ini['DefPath'], voc_Ini['DefPort']
	except:
		voc_Ini['DefPath'] = '.'
		voc_Ini['DefPort'] = '80'
		
		writer = csv.writer(file(s_IniFileName, "wb"), dialect='excel-tab')
		for j in voc_Ini.items():
			writer.writerow(j)

voc_Ini = {} # Настройки из ini файла
fun_LoadIniFile()

var_Path = StringVar() # Домашний каталог сайта
var_Path.set(voc_Ini['DefPath'])
os.chdir(var_Path.get())

var_Port = IntVar()
var_Port.set(int(voc_Ini['DefPort']))


# Классы:

class cls_SysOutput:
	def write(self, s):
		try:
			wg_SysOutput['state'] = NORMAL
			wg_SysOutput.insert(END, s)
			wg_SysOutput.yview(END)
			wg_SysOutput['state'] = DISABLED
		except:
			pass
	
	def writeline(self, line):
		self.write(line)


# Функции:

def fun_SetPath():
	ret = fun_FolderDlg(var_Path.get())
	
	if ret:
		var_Path.set(ret)
		os.chdir(var_Path.get())


def fun_Run():
	print u'Сервер работает'
	
	server_class=BaseHTTPServer.HTTPServer
	handler_class=CGIHTTPServer.CGIHTTPRequestHandler
	server_address = ('', var_Port.get())
	httpd = server_class(server_address, handler_class)
	
	while f_Run:
		httpd.handle_request()
	
	print u'Сервер остановлен'


def fun_IndState():
	if f_Run:
		wg_ButtonStart['bg'] = 'green'
	else:
		wg_ButtonStart['bg'] = 'yellow'


def fun_StartServer():
	global f_Run

	if f_Run:
		print u'Уже запущен'
		return

	f_Run = True
	thread.start_new(fun_Run, ())
	fun_IndState()


def fun_StopServer():
	global f_Run
	
	f_Run = False

	try:
		conn = httplib.HTTPConnection("127.0.0.1", var_Port.get())
		conn.request("GET", "/index.html")
		conn.getresponse()
	except:
		pass

	try:
		fun_IndState()
	except:
		pass


def fun_StartStop():
	if not f_Run:
		fun_StartServer()
	else:
		fun_StopServer()


# Программа:

o_SysOutput = cls_SysOutput()
sys.stdout, sys.stderr = o_SysOutput, o_SysOutput

root.title(u'HTTP сервер')

wg_Frame0 = Frame(root)
wg_ButtonStart = Button(wg_Frame0, text=u'старт/стоп', command=fun_StartStop, width=11)
wg_ButtonStart.pack(side=LEFT)
Entry(wg_Frame0, textvariable=var_Port, width=5).pack(side=LEFT)
wg_Frame0.pack(side=TOP, fill=X)

wg_Frame1 = Frame(root)
Label(wg_Frame1, textvariable=var_Path, anchor=E, width=10).pack(side=LEFT, expand=YES, fill=X)
Button(wg_Frame1, text='...', command=fun_SetPath).pack(side=RIGHT)
wg_Frame1.pack(side=TOP, fill=X)

wg_ScrollY = Scrollbar(root, orient=VERTICAL)

wg_SysOutput = Text(root, width=35, height=9, yscrollcommand=wg_ScrollY.set, wrap=WORD)
wg_ScrollY.pack(side=RIGHT, fill=Y)
wg_SysOutput.pack(side=TOP, expand=YES, fill=BOTH)
wg_ScrollY['command'] = wg_SysOutput.yview
wg_SysOutput['state'] = DISABLED

print u'HTTP сервер'
print u'Порт:', var_Port.get()
fun_IndState()
fun_StartServer()

root.mainloop()
fun_StopServer()
