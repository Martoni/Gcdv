#!/usr/bin/python

# First run tutorial.glade through gtk-builder-convert with this command:
# gtk-builder-convert tutorial.glade tutorial.xml
# Then save this file as tutorial.py and make it executable using this command:
# chmod a+x tutorial.py
# And execute it:
# ./tutorial.py

import sys
from CarnetDeVol import Flight, CarnetDeVol, Track, Gpx
from CarnetDeVol import datetime2gpx, gpx2datetime 

import pygtk
pygtk.require("2.0")
import gtk

CDV = None
class TutorialApp(object):      
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    def on_new_menu_item_activate(self, widget, data=None):
        print("new menu item activate")

    def __init__(self, cdv=None):
        self.cdv = cdv
        builder = gtk.Builder()
        builder.add_from_file("gui_cdv.xml")
        builder.connect_signals(self)
        self.window = builder.get_object("window")

        self.treeview = builder.get_object("treeview")
        self.treestore = gtk.ListStore(str, str)
        if self.cdv != None:
            for fly in self.cdv.getFlights(): 
                self.treestore.append(['%d'%fly.getNumber(), 'plop'])
                
        self.treeview.set_model(self.treestore)

        self.numCol = gtk.TreeViewColumn("Num")
        self.desCol = gtk.TreeViewColumn("Description")
        self.treeview.append_column(self.numCol)
        self.treeview.append_column(self.desCol)
        self.cell = gtk.CellRendererText()
        self.numCol.pack_start(self.cell, True)
        self.numCol.add_attribute(self.cell, 'text', 0)
        self.numCol.set_sort_column_id(1)
        self.desCol.pack_start(self.cell, True)
        self.desCol.add_attribute(self.cell, 'text', 0)
        self.desCol.set_sort_column_id(0)

        self.treeview.set_reorderable(True)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        CDV = CarnetDeVol(xmlfilename=sys.argv[1])
    else:
        CDV = None
    app = TutorialApp(CDV)
    app.window.show()
    gtk.main()

