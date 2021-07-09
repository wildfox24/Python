
#IdleCE
import sys, os, time
OS = os.name.lower() #Should be 'ce' on WinCE

vanilla = globals().copy()
if OS == 'ce':
    for p in sys.path:
        if p[-12:].lower() == "python23.zip":
            sys.path.append(p + "\\lib-tk")
            break
from Tkinter import *
import tkMessageBox
import tkFileDialog
from Editor import Editor# as SyntaxHighlightingText


class Document:
    """Callable class for document information."""
    
    def __init__(self, controller, name, filename, editor):
        """Keep a referance to the calling application, and the editor window."""
        self.controller = controller
        self.name = name
        self.filename = filename
        self.editor = editor
        
    
    def __call__(self):
        """Hides the current editor and dispays our editor."""
        self.controller.editor.forget()
        self.controller.editor = self.editor
        self.controller.editor.pack()
        self.controller.curDoc = self
        self.controller.filename = self.filename
        self.controller.root.title('IdleCE - %s' %self.name)
                
    
    def __del__(self):
        """Make note when self is destroyed."""
        del(self.editor)
        print "Document %s has been destroyed!"
        
class Idle:
    """The base class for the mini idle."""
    
    def __init__(self,root):
        """This is where the interface is created.
        
        This stuff is mostly straight forward except the wframe and how the work spaces are implemented.
        The wframe is a container for the current work space.  When the user clicks on the editor/clipboard
        button the wframe is told to forget about what it's doing and instead pack the desired set of widgets.
        """
        
        root.title('IdleCE')
        self.maxDocs = 5
        self.docs = []
        self.curDoc = None
        self.lastDir = '\\' # Should be stored between sessions
        
        self.top = None
        self.root = root
        root.grid_rowconfigure(1, weight=2)
        root.grid_columnconfigure(0, weight=2)
        
        frame = Frame(root) # root frame
        frame.grid(row=0,column=0,sticky=E+W)
    
        self.wframe = Frame(root) # work frame
        self.wframe.grid(row=1,column=0,sticky=NSEW)
    
        # # Editor widget
        # self.edit = Editor(wframe)
        # self.edit.pack(fill=BOTH, expand=1)
        # self.edit.clipper = self.addClip
        # self.editor = self.edit.editor
    
        # Clipper widget group
        self.clip = Frame(self.wframe, bd=2, relief=SUNKEN)
        # Not packed
        
        scrollbar = Scrollbar(self.clip)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.clipper = Listbox(self.clip, bd=0, yscrollcommand=scrollbar.set)
        self.clipper.pack(fill=BOTH, expand=1)
        self.clipper.bind('<Double-Button-1>', self.changeClip)
        
        scrollbar.config(command=self.clipper.yview)
        
        # Menus
        btn = Menubutton(frame,text="File",padx=1,pady=1)
        btn.pack(side=LEFT)
        submenu = Menu(btn,tearoff=False)
        btn["menu"] = submenu
        submenu.add_command(label="New",command=self.new)
        submenu.add_command(label="Open",command=self.open)
        submenu.add_command(label="Save",command=self.save)
        submenu.add_command(label="Save as",command=self.saveas)
        submenu.add_separator()
        submenu.add_command(label="Close",command=self.close)
        submenu.add_command(label="Exit",command=self.exit)
        
        btn = Menubutton(frame,text="Edit",padx=1,pady=1)
        btn.pack(side=LEFT)
        submenu = Menu(btn,tearoff=False)
        btn["menu"] = submenu
        submenu.add_command(label="Undo",command=self.edit_undo)
        submenu.add_command(label="Redo",command=self.edit_redo)
        submenu.add_separator()
        submenu.add_command(label="Finder",command=self.finder)
        submenu.add_command(label="Goto",command=self.goto)
        submenu.add_separator()
        submenu.add_command(label="Cut",command=self.cut)
        submenu.add_command(label="Copy",command=self.copy)
        submenu.add_command(label="Paste",command=self.paste)
        submenu.add_separator()
        submenu.add_command(label="Indent",command=self.indent_region)
        submenu.add_command(label="Dedent",command=self.dedent_region)
        submenu.add_command(label="Comment",command=self.comment_region)
        submenu.add_command(label="UnComment",command=self.uncomment_region)
            
        btn = Button(frame,text="Run",padx=1,pady=1, relief=FLAT,command=self.run)
        btn.pack(side=LEFT)
    
        self.editbtn = Button(frame,text="Editor",padx=1,pady=1, relief=FLAT, state=DISABLED, command=self.showEditor)
        self.editbtn.pack(side=LEFT)
        
        self.clipbtn = Button(frame,text="Clipper",padx=1,pady=1, relief=FLAT,command=self.showClipper)
        self.clipbtn.pack(side=LEFT)
        
        # Window menu, menu is reassociated when documents are closed
        btn = Menubutton(frame,text="Window",padx=1,pady=1)
        btn.pack(side=LEFT)
        self.MDImenu = Menu(btn,tearoff=False)
        btn["menu"] = self.MDImenu
        self.MDImenu.add_command(label="Close all",command=self.closeAll)
        self.MDImenu.add_separator()
        self.new()
        
        btn = Menubutton(frame,text="Help",padx=1,pady=1)
        btn.pack(side=LEFT)
        submenu = Menu(btn,tearoff=False)
        btn["menu"] = submenu
        submenu.add_command(label="About",command=self.about_dialog)
       
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.editor.focus()
            
    def showEditor(self):
        self.editbtn.config(state=DISABLED)
        self.clipbtn.config(state=NORMAL)
        self.clip.forget()
        self.editor.pack()
    
    
    def showClipper(self):
        self.clipbtn.config(state=DISABLED)
        self.editbtn.config(state=NORMAL)
        self.editor.forget()
        self.clip.pack(fill=BOTH, expand=1)
    
    def addClip(self, item):
        """Called by the editor to add items to the clipper list."""
        items = self.clipper.get(0,END)
        if item not in items:
            self.clipper.insert(0, item)
            if self.clipper.size() > 20:
                self.clipper.delete(0)
    
    def changeClip(self, evt=None):
        """Gets the selected text from the clipper and puts it on the clipboard."""
        index = self.clipper.curselection()
        text = self.clipper.get(index)
        self.editor.clipboard_clear()
        self.editor.clipboard_append(text)
        return 'break'
    
    def finder(self):
        """Displays a text find dialog."""
        try:
            self.finder.show()
        except:
            self.finder = Finder(self)
    
    def run(self):
        """Executes the code in the current document.
        
        """
        answer = 'spam'
        if self.editor.changed():
            answer = tkMessageBox._show("Save File","Save the current file?",icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNOCANCEL)
        if answer == 'yes':
            self.save()
        elif answer == 'cancel':
            return
        code = self.editor.get()
        self.root.withdraw()
        try:
            exec code in vanilla
        except:
            print "There has been an error during execution"
            time.sleep(5)
            self.root.deiconify() #!!! on PPC you can close the console and idleCE remains running so
            raise                 #!!! so we need to deiconify on error or you will have an invisable program...
        time.sleep(5)
        self.root.deiconify()
    
    def about_dialog(self):
        """Sillyness"""
        top = Toplevel()
        top.title("about")
        top.resizable(0,0)
        top.focus_set()
    
        about = """
    
        IdleCE v2.0b
    
    A miniaturized imitation of
    the python ide: idle.
    
    This software is distibuted
    under the Gnu-GPL. Please Visit
    http://www.gnu.org/licenses/gpl.txt
    to see the license.
        """
        info = Label(top,text=about)
        info.pack(side=TOP,padx=6)
    
        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack(side=BOTTOM,fill=X)
    
    
    def open(self):
        """Spawn a new editor, and load the contents of the file (if len(docs) < maxDocs)."""
        if len(self.docs) < self.maxDocs:
            self.filename = tkFileDialog.askopenfilename(filetypes=[("Python files",".py"),("All files","*")], initialdir=self.lastDir)
            if self.filename:
                self.lastDir = os.path.dirname(self.filename)
            else:
                return
            if OS == 'ce': # Just passing filename fails...
                self.filename = self.filename.replace('/','\\')
            try:
                file = open(self.filename)
                self.newDoc(os.path.basename(self.filename))
                text = file.readlines()
                file.close()
                self.editor.put(text)
                self.editor.changed(reset=True)
            except IOError, info:
                tkMessageBox.showerror('Exception!',info)
        else:
            tkMessageBox.showerror('Too many files!', 'You have reached the open file limit.')
            
    
    
    
    def saveas(self):
        """Save the current document with a new name."""
        # Called if no filename is set or Saveas is picked
        self.filename = tkFileDialog.asksaveasfilename(initialdir=self.lastDir)
        if self.filename:
            self.lastDir = os.path.dirname(self.filename)
        else:
            return
        if OS == 'ce':
            self.filename = self.filename.replace('/','\\')
        try:
            file = open(self.filename,'w')
            text = self.editor.get()
            file.write(text)
            file.flush()
            file.close()
            self.curDoc.name = os.path.basename(self.filename)
            self.curDoc.filename = self.filename
            self.regenDocs()
            self.root.title('IdleCE - ' + self.curDoc.name)
            self.editor.changed(reset=True)
            # Fill out the current docs data...
        except Exception, info:
            tkMessageBox.showerror('Exception!',info)
    
    
    def save(self):
        """Save the current document or do save as if filename is unknown."""
        try:
            file = open(self.filename,'w')
            text = self.editor.get()
            file.write(text)
            file.flush()
            file.close()
            self.editor.changed(reset=True)
        except:
            self.saveas() # If no file has been accessed
    
    
    def new(self):
        """Spawn a new editor if len(docs) < maxDocs."""
        if len(self.docs) < self.maxDocs:
            self.filename = ''
            self.newDoc()
        else:
            tkMessageBox.showerror('Too many files!', 'You have reached the open file limit.')
    
    def close(self):
        """Closes the current document."""
        if self.editor.changed():
            answer = tkMessageBox._show("Save File","Save the current file?",icon=tkMessageBox.QUESTION,type=tkMessageBox.YESNOCANCEL)
            if answer == 'yes':
                self.save()
            elif answer == 'cancel':
                return
        doc = self.curDoc
        self.docs.remove(self.curDoc)   # Remove the doc from the doc list
        self.editor.forget()            # Remove the editor widget from the app
        self.editor.destroy()
        self.editor = None              # Remove our reference to the editor obj
        del(self.curDoc)                # Delete the document object
        print 'Document still has %s referances...' %(sys.getrefcount(doc)-2)
        if self.docs:
            self.curDoc = self.docs[0]
            self.editor = self.curDoc.editor
            self.editor.pack()
            self.filename = self.curDoc.filename
            self.root.title('IdleCE - ' + self.curDoc.name)
        else:   # If there aren't any docs open make a new one
            self.newDoc()
        self.regenDocs() # Rebuild the docs menu
            
    def closeAll(self):
        """Call close for every open document."""
        while len(self.docs) > 1:
            self.close()
        self.close() # Closes the last doc, a new empty is made but we don't care
    
    
    def exit(self):
        """Close all open files and kill the application."""
        self.closeAll()       
        # End the program firmly.
        root.destroy()
        root.quit()
    
    
    def newDoc(self, name=''):
        """Create a new document object and set it as the current doc."""
        if not name:
            name = 'Blank Doc'
            
        # Forget the old editor
        try:
            self.editor.forget()
        except: # I should find the exception type for this (could hide bugs)
            # No editor open (init)
            pass
        
        # Editor widget
        self.editor = Editor(self.wframe)
        self.editor.pack(fill=BOTH, expand=1)
        self.editor.clipper = self.addClip
        self.editor.focus()
        self.editor.changed(reset=True)
            
        self.curDoc = Document(self, name, self.filename, self.editor)
        # Add to doc list and windows menu
        self.docs.append(self.curDoc)
        self.MDImenu.add_command(label=name,command=self.curDoc)
        self.root.title('IdleCE - ' + name)
    
    
    
    def regenDocs(self):
        """Clear and re-fill the window menu from self.docs."""
        self.MDImenu.delete(2, END) # First two entries stay
        for doc in self.docs:
            self.MDImenu.add_command(label=doc.name, command=doc) # Is command keeping a referance to my doc?
    
    # The following are functions bound to menus, which referance editor functions
    
    def edit_undo(self):
        self.editor.edit_undo
    
    
    def edit_redo(self):
        self.editor.edit_redo()
    
    
    def goto(self):
        self.editor.goto()
    
    
    def cut(self):
        self.editor.cut()    
    def copy(self):
        self.editor.copy()
        
    
    def paste(self):
        self.editor.paste()
        
    
    def indent_region(self):
        self.editor.indent_region()
        
    
    def dedent_region(self):
        self.editor.dedent_region()
        
    
    def comment_region(self):
        self.editor.comment_region()
        
    
    def uncomment_region(self):
        self.editor.uncomment_region()
    


class Finder:
    """UI and methods for finding and replacing text.
    
    This class mainly makes use of the search capabilities already built into
    the Tkinter Text widget.
    """
    
    def __init__(self, root):
        self.root = root
        
        self.top = Toplevel()
        top = self.top
        self.top.title("Finder")
        self.top.resizable(0,0)
        self.top.transient(self.root.root)
        self.top.focus_set()
        self.top.protocol("WM_DELETE_WINDOW", self.hide) #doesn't seem to work
        
        l = Label(top, text='Find:')
        l.grid(row=0, column=0, sticky=W)
        
        self.find = Entry(top)
        self.find.grid(row=0, column=1, columnspan=3)
        
        l = Label(top, text='Replace:')
        l.grid(row=1, column=0)
        
        self.replace = Entry(top)
        self.replace.grid(row=1, column=1, columnspan=3)
    
        btn = Button(top, text='Find', command=self.findit)
        btn.grid(row=0, column=4, sticky=NSEW)
        
        btn = Button(top, text='Replace', command=self.replaceit)
        btn.grid(row=1, column=4, sticky=NSEW)
        
        btn = Button(top, text='Replace all', command=self.replaceAll)
        btn.grid(row=2, column=4, sticky=NSEW)
        
        self.find.bind('<Return>', self.findit)
        
        # Variables for the check boxes
        self.up = IntVar()
        self.re = IntVar()
        self.match = IntVar()
        self.match.set(1)
        
        # The up check box
        f = Frame(top)
        f.grid(row=2, column=0, sticky=NSEW)
        
        l = Label(f, text='Up')
        l.pack(side=LEFT)
        
        btn = Checkbutton(f, variable=self.up)
        btn.pack(side=LEFT)
        
        # The re check box
        f = Frame(top)
        f.grid(row=2, column=1, sticky=NSEW)
        
        l = Label(f, text='Re')
        l.pack(side=LEFT)
        
        btn = Checkbutton(f, variable=self.re)
        btn.pack(side=LEFT)
        
        # The match check box
        f = Frame(top)
        f.grid(row=2, column=2, sticky=NSEW)
        
        l = Label(f, text='No case')
        l.pack(side=LEFT)
        
        btn = Checkbutton(f, variable=self.match)
        btn.pack(side=LEFT)
        
        # This makes sure the finder is visable
        top.update()
        geo = top.geometry()
        shape = geo[:geo.index("+")]
        top.geometry(shape + "+20+100")
        top.resizable(0,0)
    
    def findit(self, evt=None):
        text = self.find.get()
        self.find.select_range(0, END)
        if text:
            self.root.editor.find(text, self.up.get(), self.re.get(), self.match.get())
            self.root.editor.focus()
    
    def replaceit(self):
        text = self.replace.get()
        self.root.editor.replace(text)    
    def replaceAll(self):
        done = False
        ftext = self.find.get()
        rtext = self.replace.get()
        if ftext and rtext:
            while not done:
                done = self.root.editor.find(ftext, up.get())
                if not done:self.root.editor.replace(rtext)    
    def hide(self):
        self.top.withdraw()
    
    def show(self):
        self.top.deiconify()

if __name__ == '__main__':
    root = Tk()
    if OS=='ce':
        sizex, sizey = root.wm_maxsize()
        root.wm_geometry("%dx%d+0+%d"%(sizex-6,sizey*37/64+1,sizey/90))
        # Deep magic by Sebastian, fixes text selection issues.
        b1motion = root.bind_class('Text','<B1-Motion>')
        root.bind_class('Text','<B1-Motion>','if {![info exists ::tk::Priv(ignoreB1Motion)]} {%s}'%b1motion)
        root.bind_class('Text','<B1-Leave>','set ::tk::Priv(ignoreB1Motion) 1')
        root.bind_class('Text','<B1-Enter>','array unset ::tk::Priv ignoreB1Motion')
    app = Idle(root)
    root.mainloop()
