#!/usr/bin/python
# -*- coding: utf-8 -*- 
# example base.py

import pygtk
pygtk.require('2.0')
import gtk

import sys
from CarnetDeVol import Flight, CarnetDeVol, Track, Gpx
from CarnetDeVol import datetime2gpx, gpx2datetime 

class GCarnetDeVol:

    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    # Another callback
    def destroy(self, widget, data=None):
        gtk.main_quit()


    def get_main_menu(self, window):
        accel_group = gtk.AccelGroup()

        # This function initializes the item factory.
        # Param 1: The type of menu - can be MenuBar, Menu,
        #          or OptionMenu.
        # Param 2: The path of the menu.
        # Param 3: A reference to an AccelGroup. The item factory sets up
        #          the accelerator table while generating menus.
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)

        # This method generates the menu items. Pass to the item factory
        #  the list of menu items
        item_factory.create_items(self.menu_items)

        # Attach the new accelerator group to the window.
        window.add_accel_group(accel_group)

        # need to keep a reference to item_factory to prevent its destruction
        self.item_factory = item_factory
        # Finally, return the actual menu bar created by the item factory.
        return item_factory.get_widget("<main>")


    def __init__(self, CDV=None):
        self.CDV = CDV

        #define menu
        self.menu_items = (
        ( "/_File",         None,         None, 0, "<Branch>" ),
        ( "/File/_New",     "<control>N", self.hello, 0, None ),
        ( "/File/_Open",    "<control>O", self.hello, 0, None ),
        ( "/File/_Save",    "<control>S", self.hello, 0, None ),
        ( "/File/Save _As", None,         None, 0, None ),
        ( "/File/sep1",     None,         None, 0, "<Separator>" ),
        ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
        ( "/_Options",      None,         None, 0, "<Branch>" ),
        ( "/Options/Test",  None,         None, 0, None ),
        ( "/_Help",         None,         None, 0, "<LastBranch>" ),
        ( "/_Help/About",   None,         None, 0, None ),
        )
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        # Sets the border width of the window.
        self.window.set_border_width(2)

        # We create a box to pack widgets into.  This is described in detail
        # in the "packing" section. The box is not really visible, it
        # is just used as a tool to arrange widgets.
        self.box1 = gtk.VBox(False, 0)
        self.window.add(self.box1)
        self.window.set_size_request(300, 200)

        # Creates a new button with the label "Hello World".
        self.button = gtk.Button("Hello World")
        self.menubar = self.get_main_menu(self.window)

        # When the button receives the "clicked" signal, it will call the
        # function hello() passing it None as its argument.  The hello()
        # function is defined above.
        self.button.connect("clicked", self.hello, None)

        # This will cause the window to be destroyed by calling
        # gtk_widget_destroy(window) when "clicked".  Again, the destroy
        # signal could come from here, or the window manager.
        self.button.connect_object("clicked", gtk.Widget.destroy, self.window)

        # This packs the button into the window (a GTK container).
        self.box1.pack_start(self.menubar, False, True, 0)
        self.box1.pack_start(self.button, True, True, 0)

        # The final step is to display this newly created widget.
        self.box1.show()
        self.button.show()
        self.menubar.show()

        # and the window
        self.window.show()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    if len(sys.argv) == 2:
        CDV = CarnetDeVol(xmlfilename=sys.argv[1])
        GCDV = GCarnetDeVol(CDV)
    else:
        GCDV = GCarnetDeVol()
    GCDV.main()

