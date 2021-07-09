# A "Python console" for Windows CE.
#
# Also works on NT/9x (with a few limitations!) - useful for debugging!
#
# Used 2 threads - one for UI (ie, the message loop) and another thread
# for executing Python code.  Uses very simple events to synchronise the 2!

# 01/11/16 12:38
# Horizontal scroll removed 
#
# 02/10/08 23:24 Telion
# font change, icon fix, input() and raw_input() are added
#
# 02/10/16 13:25 Telion
# Command history by Ctrl-B, Ctrl-N
# Clear Screen by Alt-L
# Command logging: shell.log() for detail
# Half of Multiple line re-editing bug fixed
#
# To do: Supress redraw during operation... Help for using pcceshell.
#   "!" os.system escape and Python script execution with args, redirect?
#

from win32gui import *
from win32event import *
import sys
import string
import thread, threading
import traceback
import code # std module for compilation utilities.
import new
import os
import imp

IDOK=1
IDCANCEL=2

GWL_WNDPROC=-4
FIXED_PITCH=1
ANSI_FIXED_FONT=11

IDC_WAIT = 32514
HWND_TOP=0
CS_VREDRAW=1
CS_HREDRAW=2

CW_USEDEFAULT=0x80000000

WM_CHAR=258
WM_COMMAND=273
WM_DESTROY=2
WM_QUIT=18
WM_SETFOCUS=7
WM_SETFONT=48
WM_SETREDRAW=11
WM_SIZE=5
WM_USER=1024

WHITE_BRUSH=0
SW_SHOW=5
SW_SHOWNORMAL=1

WS_SYSMENU=524288
WS_CLIPCHILDREN=33554432
WS_CHILD=1073741824
WS_VISIBLE=268435456
WS_HSCROLL=1048576
WS_VSCROLL=2097152
if sys.platform=="wince":
	WS_OVERLAPPEDWINDOW=0
else:
	WS_OVERLAPPEDWINDOW=13565952

EM_GETLINECOUNT=186
EM_GETSEL=176
EM_LINEINDEX=187
EM_LINEFROMCHAR=201
EM_LINELENGTH=193
EM_SETSEL=177
EM_REPLACESEL=194

ES_LEFT=0
ES_MULTILINE=4
ES_WANTRETURN=4096
ES_AUTOVSCROLL=64
ES_AUTOHSCROLL=128

IDR_MENU=101
IDM_EXIT=40001
IDM_ABOUT=40002
#IDD_ABOUT=40002
#IDM_ABOUT=7234
IDD_ABOUT=111

if UNICODE:
	TEXT = Unicode
else:
	TEXT = lambda x: x

if sys.platform=="wince":
	OutputDebugString = NKDbgPrintfW
else:
	from win32api import OutputDebugString
	
try:
	sys.ps1
except AttributeError:
	sys.ps1 = ">>> "
	sys.ps2 = "... "

class SimpleShell:
	editMessageMap = {}
	def __init__(self):
		self.bInteract = 0 # Am I interacting?
		self.hwnd = None
		self.hwndEdit = None
		self.outputQueue = []
		self.outputQueueLock = threading.Lock()

		# Allocate some events for thread sync
		self.currentBlockItems = None
		self.eventInteractiveInputAvailable = CreateEvent(None, 0, 0, None)
		self.eventClosed = CreateEvent(None, 0, 0, None)

		# Added by Telion for alias, history, input( ), etc..
		self.reading = '' # readline flag and data
		self.pChar = 0 # readline current line number
		self.pLine = 0 # readline current line length

		self.fixedpitch = 0
		self.charset = 128
		self.lf=LOGFONT()
		self.plf=pLOGFONT(self.lf)
		self.lf.lfFaceName="" ### specify the face name you want
		self.lf.lfHeight=14
		self.lf.lfWidth=0

		self.hist = []
		self.hidx = -1
		self.histpos = 0
		self.maxhist = 30
		self.cmdlogname = sys.prefix+r"\cmdlog.txt"

		self._paint = 1

	def __del__(self):
		print "InteractiveManager dieing"

	def write(self, text):
		text = string.replace(text, "\n", "\r\n")
		self.outputQueueLock.acquire()
		self.outputQueue.append(text)
		self.outputQueueLock.release()
		try:
			PostMessage(self.hwnd, WM_USER, 0, 0)
		except:
			pass
		
	def Run(self):
		PumpMessages()	

	#def GetEditMessageMap(self):
	#	return {WM_CHAR : self.OnEditChar}
	def GetEditMessageMap(self):
		map = {WM_CHAR : self.OnEditChar}
		#map[WM_KEYDOWN] = self.OnEditKeyDown # for command history
		#map[0x0100] = self.OnEditKey # WM_KEYDOWN
		#map[0x0101] = self.OnEditKey # WM_KEYUP
		#map[0x0104] = self.OnEditKey # WM_SYSKEYDOWN
		#map[0x0105] = self.OnEditKey # WM_SYSKEYUP
		map[0x0106] = self.OnEditKey # WM_SYSCHAR
		#map[0x0108] = self.OnEditKey # WM_LAST
		#map[0x0103] = self.OnEditKey # WM_DEADCHAR
		#map[0x0107] = self.OnEditKey # WM_SYSDEADCHAR
		map[0x0f] = self.OnParentPaint # WM_PAINT
		return map

	def OnEditKey(self,hWnd, msg, wparam, lparam):
		if wparam == 0x6c: #Alt-L
			if 1:
			#if raw_input('\nClear Screen ?(y/n) ').lower() == 'y': # This hangs, too
				self.cls()
			return
		#print repr(hex(wparam))+":"+repr(hex(lparam))
		#if MessageBox(self.hwndEdit,repr(hex(wparam))+":"+repr(hex(lparam)), "Key typed",0):
		#	return
		return CallWindowProc(self.oldEditWndProc, hWnd, msg, wparam, lparam)

	def OnParentPaint(self, hwnd, msg, wparam, lparam):
		#sys.__stdout__.write(repr(self._paint)+":"+repr(hex(wparam))+"\n")
		if self._paint:
			return CallWindowProc(self.oldEditWndProc, hwnd, msg, wparam, lparam)
		return

	def GetParentMessageMap(self):
		map={}
		map[WM_DESTROY] = self.OnParentDestroy
		map[WM_SIZE] = self.OnParentSize
		map[WM_SETFOCUS] = self.OnParentSetFocus
		map[WM_USER] = self.OnParentUser
		map[WM_COMMAND] = self.OnParentCommand
		map[0x0f] = self.OnParentPaint # WM_PAINT
		return map
	
	def Init(self):
		try:
			self.hinst = GetModuleHandle(None)
		except NameError: # Not on CE??
			self.hinst = sys.hinst # But this is :-)
			
		try:
			self.cmdlog = open(self.cmdlogname,'ab')
		except:
			self.cmdlog = None

		InitCommonControls()

		wc = WNDCLASS()
		wc.hInstance = self.hinst
		wc.style=CS_HREDRAW | CS_VREDRAW
		wc.hbrBackground = GetStockObject(WHITE_BRUSH)
		wc.lpszClassName = TEXT("PYTHON_CE")
		# This code passes a dictionary as the "wndproc", rather than a function.
		wc.lpfnWndProc = self.GetParentMessageMap() #self.MainWndProc
		self.classAtom = RegisterClass(wc)
		
		if sys.platform=="wince":
			style = WS_CLIPCHILDREN
		else:
			style = WS_OVERLAPPEDWINDOW
			
		self.hwnd = CreateWindow( self.classAtom, "Python CE", style, \
	                      0, 0, CW_USEDEFAULT, CW_USEDEFAULT, \
	                      0, 0, self.hinst, None)
		#WM_SETICON = 128
		#SendMessage(self.hwnd,128,0,LoadIcon(self.hinst,103)) # Small 16 x 16
		#SendMessage(self.hwnd,128,1,LoadIcon(self.hinst,104)) # Large 32 x 32
		self.icon() # use default icons( large and small)
    
		left, top, right, bottom = GetClientRect(self.hwnd)

#		print sys.platform, type(sys.platform)
		if sys.platform=="wince":
			self.hCmdBar = CommandBar_Create(self.hinst, self.hwnd, 1)
			CommandBar_InsertMenubar(self.hCmdBar, self.hinst, IDR_MENU, 0)
			CommandBar_AddAdornments(self.hCmdBar, 0, 0)
			top = CommandBar_Height(self.hCmdBar)

		#style = WS_CHILD|WS_VISIBLE|WS_VSCROLL|WS_HSCROLL|ES_LEFT|ES_MULTILINE|ES_WANTRETURN|ES_AUTOHSCROLL
		style = WS_CHILD|WS_VISIBLE|WS_VSCROLL|ES_LEFT|ES_MULTILINE|ES_WANTRETURN
		self.hwndEdit=CreateWindow("EDIT", None, style, \
				      left, top, (right-left), (bottom-top), \
		                      self.hwnd, 0, self.hinst, None)    
	
		self.oldEditWndProc = SetWindowLong(self.hwndEdit, GWL_WNDPROC, self.GetEditMessageMap())# self.EditWndProc)

		if sys.platform != "wince":
			SendMessage(self.hwndEdit, WM_SETFONT, GetStockObject(ANSI_FIXED_FONT), 0)

		if self.fixedpitch:
			self.setfont()

		ShowWindow(self.hwnd, SW_SHOW)
		UpdateWindow(self.hwnd)

		EnableWindow(self.hwndEdit, 1)
	
		SetFocus(self.hwndEdit)
		SetCursor(LoadCursor(0,0))

	def Term(self):
		UnregisterClass(self.classAtom, self.hinst)

	def log(self,onoff=""):
		# 1 := on,  0 := off
		if onoff == "":
			if self.cmdlog:
				print "Logging on:", self.cmdlog
			else:
				print "Logging off"
			print """	shell.log(1) for turning on
	shell.log(0) for turning off
	shell.log(-1) for deleting log file"""
			return
		
		if onoff > 0:
			try:
				self.cmdlog = open(self.cmdlogname,'ab')
				print "Command log on"
			except:
				self.cmdlog = None
				print "Failed to open Command log file"
		elif onoff < 0:
			if raw_input('Delete CCommand log: %s ? (y/n)' % self.cmdlogname,'ab').lower() == 'y':

				if self.cmdlog: self.cmdlog.close()
				try:
					os.unlink(self.cmdlogname)
					print "Command log deleted"
				except:
					print "Failed to delete Command log"
			pass
		else:
			self.cmdlog.close()
			self.cmdlog = None
			print "Command log closed. Logging off"
		return
	
	def cls(self):
		# clear the screen
		#if MessageBox(0,"Clear Screen?", "PythonCE2.2+",0|0|4|32) == 6:
		#	pass
		#  This messageBox hangs Python.
		if 0: # All these does not work for supending redraw while select and replace..
			self._paint = 0
			PostMessage(self.hwnd, WM_SETREDRAW, 0, 0)
			#SendMessage(self.hwndEdit, 194, 0, TEXT("Clearing the Screen OK?(y/n)"))
			SendMessage(self.hwndEdit, 0xb1, 0,-1) # EM_SETSEL entire text
			SendMessage(self.hwndEdit, EM_REPLACESEL, 0, TEXT(sys.ps1))
			PostMessage(self.hwndEdit, WM_SETREDRAW, 1, 0)
			PostMessage(self.hwnd, 0x0f, 0, 0) # WM_PAINT
			self._paint = 1
			UpdateWindow(self.hwnd)
			#SendMessage(self.hwndEdit, 0x0f, 0, 0)
			#SendMessage(self.hwndEdit, WM_CHAR,8 ,0) # Backspace...
			#sys.stdout.write()
		SendMessage(self.hwndEdit, 0xb1, 0,-1) # EM_SETSEL entire text
		SendMessage(self.hwndEdit, 194, 0, TEXT(sys.ps1))
		return

	def setfont(self,pitch=1):
			try:
				import calldll
				self.lf.lfPitchAndFamily= pitch
				self.lf.lfCharSet = self.charset
				hcoredll=calldll.ll('coredll')
				#if not hcoredll: raise "Error coredll not found"
				gpaCFI=calldll.gpa(hcoredll,'CreateFontIndirectW')
				#if not gpaCFI: raise "Error CreateFontIndirectW not found"
				#if not plf: raise "Error LOGFONT pointer not retrieved",plf
				#hfont=calldll.cff(gpaCFI,'l','l',(plf,))
				#if not hfont: raise "Error CreateFontIndirect()",hfont
				SendMessage(self.hwndEdit, 48, calldll.cff(gpaCFI,'l','l',(self.plf,)), -1)
			except: 
				pass

	def icon(self,icon=0,ls=0):
		if ls: bs=32
		else: bs=16
		try:
			SendMessage(self.hwnd,128,ls,LoadImage(self.hinst,icon,IMAGE_ICON,bs,bs,0)) 
			pass
		except:
			print "Loading icon failed? icon=",icon,ls,bs
			if ls: print "large icon 32 x 32"
			else:  print "small icon 16 x 16"
			print "icon(icon_id, large) # set 1 on large, for large (standard) Icon"
		else:
			if not icon:
				ls= not ls
				bs = 16 + ls*16
				SendMessage(self.hwnd,128,ls,LoadImage(self.hinst,icon,IMAGE_ICON,bs,bs,0)) 
	
	def icongreen(self, d=1): # icongreen(0) will bring back to default color
		if d: i=104
		else: i=0
		self.icon(i,0)
		self.icon(i,1)

	def flush(self): # dummy flush for some module that do sys.stdout.flush()
		return

	def readline(self):
		#print "\nInside shell.readline"
		#pr = '-->'
		#lpr = len(pr)
		#sys.stdout.write( "\n"+pr)
		self.reading = 'on'
		rc = WaitForMultipleObjects( (self.eventInteractiveInputAvailable, self.eventClosed), 0, INFINITE)
		if rc == WAIT_OBJECT_0:
			s = self.reading
		else:
			s='Debug shell.readline nothing'
		#print "Going Out shell.readline with "+s
		self.reading = ''
		#return repr(s)
		return s

	def _printhist(self):
		SendMessage(self.hwndEdit, 0xb1, -1,-1) # EM_SETSEL at the end
		if self.histpos:
				SendMessage(self.hwndEdit, 0xb1, self.histpos,-1) # EM_SETSEL select after prompt
				SendMessage(self.hwndEdit, WM_CHAR,8 ,0) # delete with Backspace...
			#sys.stdout.write(sys.ps1)
		else:
			cpos = SendMessage(self.hwndEdit, 187, -1) # EM_LINEINDEX start of the line
			#if SendMessage(self.hwndEdit, 193, cpos) > 4: # if linelength > 4:
			self.histpos = cpos + len(sys.ps1)
		sys.stdout.write(self.hist[self.hidx].replace("\n","\n... "))
		return


	def OnEditChar(self,hWnd, msg, wparam, lparam):# WindowProc for WM_CHAR call
		global pk
		#print hex(wparam), hex(lparam)
		# readline patch for getting currnt cursor pos by Telion
		if self.reading != '':# readline going on
			if self.reading == 'on':# first time after readline started
				self.reading = 'on2'	# change it to avoid coming back
#pypp 				self.pChar=SendMessage(hWnd, EM_LINEINDEX, -1) # get current line index
				self.pChar=SendMessage(hWnd, 187, -1) # get current line index
#pypp 				self.pLine=SendMessage(hWnd, EM_LINELENGTH, self.pChar)# get the length
				self.pLine=SendMessage(hWnd, 193, self.pChar)# get the length
		#if 1:
			#pk.write(str(wparam)+"\n")
		if wparam!=0x0D: # if it is not return key, pass it to original procedure
			# by inserting other code here,, you may capture and deal with other keys
			if wparam == 0xe and self.hist: #Ctrl-N
				if self.hidx < len(self.hist)-1:
					self.hidx += 1
					self._printhist()
					return
			if wparam == 0x2  and self.hist: #Ctrl-B
				#print self.hidx
				if self.hidx > 0:
					self.hidx -= 1
				self._printhist()
				return
			return CallWindowProc(self.oldEditWndProc, hWnd, msg, wparam, lparam)
		else: # if it is return key
#pypp 			cChar=SendMessage(hWnd, EM_LINEINDEX, -1)
			cChar=SendMessage(hWnd, 187, -1)
#pypp 			cLine=SendMessage(hWnd, EM_LINEFROMCHAR, cChar)
			cLine=SendMessage(hWnd, 201, cChar)
			if self.reading != '': # readline in underway
				self.reading = str(Edit_GetLine(hWnd, cLine, 512)) # get current line
				if cChar != self.pChar: # if user moved away from input line
					pass # just return enitre line as the result
				else:
					if len(self.reading) < self.pLine: # if user erased prompt
						pass # just return enitre line as the result
					else:	
						# self.reading = self.reading[self.pLine:]+'X-X'+repr(cChar)+','+repr(self.pChar)+"x"+repr(cLine)+','+repr(self.pLine)+"<<Debug info"
						self.reading = self.reading[self.pLine:] # remove prompt
				print ''
				SetEvent(self.eventInteractiveInputAvailable)
				#ShowCaret(hWnd)
				return 0
			elif not self.bInteract: # if not in interact, pass it to original proc.
				return CallWindowProc(self.oldEditWndProc, hWnd, msg, wparam, lparam)
			# End of readline patch by Telion

			
			HideCaret(hWnd);
			# Find the start of the block
#pypp 			numLines = SendMessage(hWnd, EM_GETLINECOUNT, 0, 0)
			numLines = SendMessage(hWnd, 186, 0, 0)
			# GetLine fails as the size is wrong??
			maxLineSize=512
			blockStart = -1
			while cLine >= 0:
				line = str(Edit_GetLine(hWnd, cLine, maxLineSize))
				if line[:4]==sys.ps1:
					blockStart = cLine
					break
				elif line[:4]!=sys.ps2:
					break
				cLine = cLine -1

			if blockStart>=0:
				# Find the end of the block.
				while 1:
					cLine = cLine + 1
					line = str(Edit_GetLine(hWnd, cLine, maxLineSize))
					if line is None or line[:4]!=sys.ps2:
						break
				blockEnd = cLine
				# blockStart is the first line
				# blockEnd is one past the block end.
				firstLine=str(Edit_GetLine(hWnd, blockStart, maxLineSize))[len(sys.ps1):]
				# Special case for an empty command - mimic Python better by writing another ">>>"
				if len(firstLine)==0 and blockStart+1==blockEnd:
					# Empty prompt - write a new one.
					self.write("\n"+sys.ps1)
				else:
					items = [firstLine]
					for cLine in range(blockStart+1, blockEnd):
						items.append( str(Edit_GetLine(hWnd, cLine, maxLineSize))[len(sys.ps2):] )

					# If the block is not at the end of the control, copy it there...
					if blockEnd != numLines:
						self.write("\n%s%s" % (sys.ps1, items[0]))
						for item in items[1:]:
							self.write("\n%s%s" % (sys.ps2, item))
					else:
						# Ready to execute.
						self.currentBlockItems = items
						codeText = string.join(self.currentBlockItems, '\n')

						SetEvent(self.eventInteractiveInputAvailable)
			
			else:
				# Not in a block - write a new prompt.
				self.write("\n"+sys.ps1)

			ShowCaret(hWnd)
			return 0
			# end of return key processing
		#return CallWindowProc(self.oldEditWndProc, hWnd, msg, wparam, lparam)
		# ^this is not needed any more

	def OnParentSize(self, hwnd, msg, wparam, lparam):
		left, top, right, bottom = GetClientRect(hwnd)
		try:
			top=CommandBar_Height(self.hCmdBar);
		except NameError: # Only on CE
			pass
		if self.hwndEdit is not None:
			SetWindowPos(self.hwndEdit, HWND_TOP, left, top, right-left, bottom-top, 0)
			ShowWindow(self.hwndEdit, SW_SHOWNORMAL)

	def OnParentDestroy(self, hwnd, msg, wparam, lparam):
		PostQuitMessage(hwnd)
		# And tell the thread waiting for us we are done!
		SetEvent(self.eventClosed)

	def OnParentSetFocus(self, hwnd, msg, wparam, lparam):
		if self.hwndEdit is not None:
			SetFocus(self.hwndEdit)
	
	def OnParentUser(self, hwnd, msg, wparam, lparam):
		# Out write function post this message.
		# We dequeue the output, and write the text.
		while self.outputQueue:
			self.outputQueueLock.acquire()
			text = string.join(self.outputQueue, '')
			self.outputQueue = []
			self.outputQueueLock.release()
			SendMessage(self.hwndEdit, EM_SETSEL, -2, -2)
			# Now check that we wont fill the control.
			# If so, remove the first lines until we are OK.
			selInfo = SendMessage(self.hwndEdit, EM_GETSEL, 0, 0)
			endPos = HIWORD(selInfo)
			lineLookIndex = 0
			lineLookLength = 0
			while endPos + len(text) - lineLookLength > 29000:
				lineLookIndex = lineLookIndex + 1
				lineLookLength = SendMessage(self.hwndEdit, EM_LINEINDEX, lineLookIndex, 0)
			if lineLookIndex > 0:
				# The SETREDRAW has no effect on CE.  If we really want this
				# I think we must respond to WM_PAINT, and ignore it for the duration
				# the redraw is turned off.
				SendMessage(self.hwndEdit, WM_SETREDRAW, 0, 0)
				SendMessage(self.hwndEdit, EM_SETSEL, 0, lineLookLength)
				SendMessage(self.hwndEdit, EM_REPLACESEL, 0, TEXT(""))
				# And back to the end.
				SendMessage(self.hwndEdit, EM_SETSEL, -2, -2)
				SendMessage(self.hwndEdit, WM_SETREDRAW, 1, 0)
				
			#SendMessage(self.hwndEdit, EM_REPLACESEL, 0, TEXT(text))
			try:
				SendMessage(self.hwndEdit, 194, 0, TEXT(text))
			except:
				ttmp=TEXT(text) # This fails some time....
				#ttmp=unicode(text)
				SendMessage(self.hwndEdit, 194, 0, ttmp)
				#pass

	def OnParentCommand(self, hwnd, msg, wparam, lparam):
		command = LOWORD(wparam)
		if command == IDM_EXIT:
			DestroyWindow(hwnd);
		elif command == IDM_ABOUT:
			DialogBox(self.hinst, IDD_ABOUT, hwnd, AboutBoxDlgProc)
			#self.write("\n"+sys.ps1)
			self.write("")
			#ShowCaret(self.hWnd)
		return 0

CR=u"\u000D"+u"\u000A"
AboutCredit=(" Python CE 2.2+ Porting Team:\n   Brad Clements and all\n\n Based on work by:\n   Mark Hammond, David Ascher,\n\n With financial Support from:\n   Ted Shab, Ken Manheimer,\n   Michael Hauser, Frank Glass,\n   Jeff Bauer, Val Bykovsky,\n   Mark Hammond, Laura Creighton,\n   Warren Postma\n\n\n"+sys.copyright+"\n\n\n HPC2000 build:   by Telion\n  http://pages.ccapcable.com/lac/\n\n Python's nest\n  http://www.python.org/\n").replace("\n",CR)

Aboutdone = 0
#WM_INITDIALOG = 0x01100
#f=open('AbouDialog.txt','ab')

def AboutBoxDlgProc(hwnd, msg, wparam, lparam):
	global Aboutcredit, Aboutdone
	if msg==0x87 and Aboutdone==1:
		SetDlgItemText(hwnd,1000, AboutCredit)
		Aboutdone = 2
		return 0
	if msg==WM_COMMAND:
		p=LOWORD(wparam)
		if Aboutdone < 2:
			SetDlgItemText(hwnd,1000, AboutCredit)
			Aboutdone = 2
			return 0
		elif p==IDCANCEL or  p==IDOK:
			EndDialog(hwnd, 1)
			Aboutdone = 0
		return 1

	#if msg==WM_INITDIALOG: # Somehow, I couldn't get WM_INITDIALOG. So, using WM_SETFOCUS
	if msg==7:  # WM_SETFOCUS # This works most of the time....
		if Aboutdone:
			return 0
		SetDlgItemText(hwnd,1000, AboutCredit)
		Aboutdone = 1
		return 0
	
	return 0

def Interact(shell):
	shell.bInteract = 1
	#slocals = {}
	slocals = {'shell':shell} # let you use shell related things
	slocals.update(sys.modules) # You can use all modules that has been loaded if you want
	copyright = 'Type "help", "copyright", "credits" or "license" for more information.'
	sys.stdout.write("Python %s on %s\n%s\n%s" % (sys.version, sys.platform, copyright, sys.ps1))
	
	while 1:
		rc = WaitForMultipleObjects( (shell.eventInteractiveInputAvailable, shell.eventClosed), 0, INFINITE)
		if rc == WAIT_OBJECT_0:
			codeText = string.join(shell.currentBlockItems, '\n')
			if shell.cmdlog:
				shell.cmdlog.write(codeText+"\n")
				shell.cmdlog.flush()
			shell.hist.append(codeText)
			try:
				shell.hist.pop(shell.hist[:-1].index(codeText))
			except:
				pass
			hm = len(shell.hist)-shell.maxhist
			if hm > 0:
				shell.hist = shell.hist[hm:]
			shell.hidx = len(shell.hist)
			shell.histpos = 0

			try:
				codeOb = code.compile_command(codeText)
			except SyntaxError:
				sys.stdout.write("\n")
				list = traceback.print_exc(0)
				sys.stdout.write(sys.ps1)
				continue
			except:
				traceback.print_exc()
				continue

			if codeOb is None:
				sys.stdout.write("\n%s" % sys.ps2)
				continue
			sys.stdout.write("\n")

			SetCursor(LoadCursor(0, IDC_WAIT))
			try:
				try:
					exec codeOb in slocals
				except SystemExit:
					break
				except:
					exc_type, exc_value, exc_traceback = sys.exc_info()
					l = len(traceback.extract_tb(sys.exc_traceback))
					try: 1/0
					except:
						m = len(traceback.extract_tb(sys.exc_traceback))
					traceback.print_exception(exc_type,
						exc_value, exc_traceback, l-m)
					exc_traceback = None # Prevent a cycle
			finally:
				SetCursor(LoadCursor(0, 0))
				
			sys.stdout.write(sys.ps1)
		else:
			break

def RunCode(shell):
	try:
		# copy sys.argv before we stomp on it!
		sys.appargv = sys.argv[:]
		bKeepOpen = 0
		bInteract = 1
		cmdToExecute = None
		# Process sys.argv, removing args as we process them so any scripts
		# see _their_ argv!
		del sys.argv[0]
		# Remove some params the WCE debugger sometimes adds:
		sys.argv=filter(lambda arg: arg[:4]!="/WCE", sys.argv)
		i=0
		while i < len(sys.argv):
			if not sys.argv[i] or sys.argv[i][0]!='-':
				break
			if sys.argv[i]=='-i':
				bInteract = 1
				del sys.argv[i]
				continue
			elif sys.argv[i]=='-c':
				cmdToExecute = string.join(sys.argv[i+1:], ' ')
				sys.argv = sys.argv[:i-1]
				break
			i = i + 1
		
		if not sys.argv: sys.argv=['']

		if cmdToExecute is not None:
			try:
				exec cmdToExecute
			except:
				traceback.print_exc()
				bKeepOpen = 1
		elif len(sys.argv)>0 and sys.argv[0]:
			# Shift the args back to it sees itself as sys.argv[0]
			# Execute the named script
			fname = sys.argv[0]
			ext = os.path.splitext(fname)[1]
			if ext=='.pyc':
				mode="rb"
				imp_params=("pyc", mode, imp.PY_COMPILED)
			else:
				mode="r"
				imp_params=("py", mode, imp.PY_SOURCE)

			try:
				file = open(fname, mode)
			except IOError, (code, why):
				print "python: can't open %s: %s\n" % (fname, why)
				bKeepOpen = 1
				file = None
			if file:
				try:
					try:
						imp.load_module("__main__", file, fname, imp_params)
					except:
						traceback.print_exc()
						bKeepOpen = 1
				finally:
					file.close()
		else:
			bInteract = 1
		
		if bInteract:
			try:
				Interact(shell)
			except:
				traceback.print_exc()
				bKeepOpen = 1
	
		if not bKeepOpen:
			PostThreadMessage(shellThreadId, WM_QUIT, 0, 0)
	except:
		traceback.print_exc()
	
def main():
	# We run the shell in the main thread, so that when it terminates
	# (accidently or otherwise) the application terminates.
	# A seperate thread is used to execute the Python code.
	__name__ = sys.argv[0]

	# Make "shell" global just for debugging purposes
	# ie, so interactive code can see it via __main__.shell (or "ceshell.shell" on CE)
	global shell 
	shell = SimpleShell()
	global shellThreadId
	shellThreadId = thread.get_ident()
	# Create the windows, but dont start the message loop yet.
	shell.Init()

	# Can now write to the shell - assign the standard files.
	oldOut, oldErr, oldIn = sys.stdout, sys.stderr, sys.stdin
	sys.stderr = shell
	sys.stdout = shell
	sys.stdin = shell

	# Create the new thread to execute the code.
	thread.start_new(RunCode, (shell,) )
	print "pcceshell starting..."
	# Now run the shell.
	shell.Run()
	
	shell.Term()

	sys.stdout = oldOut
	sys.stderr = oldErr
	sys.stdin = oldIn

# On Windows, run this as a script.
# On CE, this module is imported and main() executed by
# the startup C code.
if __name__=='__main__':
	main()
