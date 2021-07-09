#!/usr/bin/env python
#
import gtk
 
def button_clicked(button):
    print 'Hello World!'
 
window = gtk.Window()
window.set_title('Hello World!')
window.connect('destroy', lambda w: gtk.main_quit())
 
button = gtk.Button('Press Me')
button.connect('clicked', button_clicked)
button.show()
 
window.add (button)
window.present()
 
gtk.main()

