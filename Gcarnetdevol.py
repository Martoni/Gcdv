#!/usr/bin/python

# First run tutorial.glade through gtk-builder-convert with this command:
# gtk-builder-convert tutorial.glade tutorial.xml
# Then save this file as tutorial.py and make it executable using this command:
# chmod a+x tutorial.py
# And execute it:
# ./tutorial.py

__VERSION__ = "0.1-git"
__AUTHORS__ = ["Fabien Marteau <fabien.marteau@martoni.fr>"]
__WEB__     = "www.martoni.fr" 
__LICENSE__ = """ 
'THE BEER-WARE LICENSE' (Revision 42):
<fabien.marteau@martoni.fr> wrote this file. As long as you retain this notice you
can do whatever you want with this stuff. If we meet some day, and you think
this stuff is worth it, you can buy me a beer in return. 
"""

import sys, datetime, os
from CarnetDeVol import Flight, CarnetDeVol, Track, Gpx
from CarnetDeVol import datetime2gpx, gpx2datetime 

import pygtk
import gtk

CDV = None

def second2time(time_in_secondes):
    """ Convert time in secondes in HH:MM:SS
    """
    hours = time_in_secondes/(60*60)
    minutes = (time_in_secondes/60) - (hours*60)
    seconds = time_in_secondes - (hours*60*60+minutes*60)
    return "%02d:%02d:%02d"%(hours, minutes, seconds)

def time2second(time_str):
    """ Convert time in HH:MM:SS in seconds
    """
    if len(time_str) != 8:
        raise Exception("Wrong lenght of duration string")
    time_tab = time_str.split(":")
    return int(time_tab[0])*60*60+int(time_tab[1])*60+int(time_tab[2])

def string2datetime(datetime_str):
    if len(datetime_str) != 17:
        raise Exception("Wrong lenght of duration string")
    vdate = datetime_str.split('-')[0]
    vdate = vdate.split('/')
    vtime = datetime_str.split('-')[1]
    vtime = vtime.split(':')
    return datetime.datetime(
           day=   int(vdate[0]),
           month= int(vdate[1]),
           year = int(vdate[2]) + 2000,
           hour=  int(vtime[0]),
           minute=int(vtime[1]),
           second=int(vtime[2]))

class ListFly(object):

    def appendFly(self, fly):
        if fly.getTrack() == None:
            track = "Non"
        else:
            track = "Oui"
        self.treestore.append(['%04d'%fly.getNumber(), fly.getSite(),
                                gpx2datetime(
                                    fly.getDate()).strftime(
                                        "%d/%m/%y-%H:%M:%S"),
                                second2time(fly.getDuration()),
                                str(fly.getWing()), track,
                                str(fly.getDesc())])
    def suppressFly(self, fly):
        for entry in self.treestore:
            fly_num = fly.getNumber()
            if int(entry[0]) == fly_num:
                print "try to suppress fly number "+str(fly_num)
                print str(entry[0])
                self.treestore.remove(self.treestore.get_iter(self.getRowNum(fly)))
        self.cdv.delFlight(fly)

    def getFly(self, row_number):
        return self.cdv.getFlight(int(self.treestore[row_number][0]))

    def getRowNum(self, fly):
        row_num = 0
        for entry in self.treestore:
            if int(entry[0]) == fly.getNumber():
                    return row_num
            row_num = row_num + 1

    def selected(self):
        model,iterat = self.treeview.get_selection().get_selected()
        return self.getFly(model.get_path(iterat))

    def numEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setNumber(new_text)
        self.treestore[path][0] = new_text
    def siteEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setSite(new_text)
        self.treestore[path][1] = new_text
    def dateEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setDate(string2datetime(new_text))
        self.treestore[path][2] = new_text
    def durEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setDuration(time2second(new_text))
        self.treestore[path][3] = new_text
    def wingEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setWing(new_text)
        self.treestore[path][4] = new_text
    def desEdited(self, cellrenderertext, path, new_text):
        self.getFly(path).setDesc(new_text)
        self.treestore[path][6] = new_text

    def __init__(self, cdv, builder):
        self.treeview = builder.get_object("treeview")
        self.treestore = gtk.ListStore(str, str, str, str, str, str, str)
        self.cdv = cdv
                
        self.treeview.set_model(self.treestore)

        self.numCol  = gtk.TreeViewColumn("Num")
        self.siteCol = gtk.TreeViewColumn("Site")
        self.dateCol = gtk.TreeViewColumn("Date")
        self.durCol  = gtk.TreeViewColumn("Temps de vol")
        self.wingCol = gtk.TreeViewColumn("Voile")
        self.trackCol= gtk.TreeViewColumn("Trace")
        self.desCol  = gtk.TreeViewColumn("Description")

        self.treeview.append_column(self.numCol)
        self.treeview.append_column(self.siteCol)
        self.treeview.append_column(self.dateCol)
        self.treeview.append_column(self.durCol)
        self.treeview.append_column(self.wingCol)
        self.treeview.append_column(self.trackCol)
        self.treeview.append_column(self.desCol)

        self.cell = gtk.CellRendererText()

        self.cellNum = gtk.CellRendererText()
        self.cellNum.connect("edited", self.numEdited)
        self.cellNum.set_property("editable", True)
        self.cellNum.set_property("editable-set", True)
        self.numCol.pack_start(self.cellNum, True)
        self.numCol.add_attribute(self.cellNum, 'text', 0)
        self.numCol.set_sort_column_id(0)

        self.cellSite = gtk.CellRendererText()
        self.cellSite.connect("edited", self.siteEdited)
        self.cellSite.set_property("editable", True)
        self.siteCol.pack_start(self.cellSite, True)
        self.siteCol.add_attribute(self.cellSite, 'text', 1)
        self.siteCol.set_sort_column_id(1)

        self.cellDate = gtk.CellRendererText()
        self.cellDate.connect("edited", self.dateEdited)
        self.cellDate.set_property("editable", True)
        self.dateCol.pack_start(self.cellDate, True)
        self.dateCol.add_attribute(self.cellDate, 'text', 2)
        self.dateCol.set_sort_column_id(2)

        self.cellDur = gtk.CellRendererText()
        self.cellDur.connect("edited", self.durEdited)
        self.cellDur.set_property("editable", True)
        self.durCol.pack_start(self.cellDur, True)
        self.durCol.add_attribute(self.cellDur, 'text', 3)
        self.durCol.set_sort_column_id(3)

        self.cellWing = gtk.CellRendererText()
        self.cellWing.connect("edited", self.wingEdited)
        self.cellWing.set_property("editable", True)
        self.wingCol.pack_start(self.cellWing, True)
        self.wingCol.add_attribute(self.cellWing, 'text', 4)
        self.wingCol.set_sort_column_id(4)

        self.trackCol.pack_start(self.cell, True)
        self.trackCol.add_attribute(self.cell, 'text', 5)
        self.trackCol.set_sort_column_id(5)

        self.cellDes = gtk.CellRendererText()
        self.cellDes.connect("edited", self.desEdited)
        self.cellDes.set_property("editable", True)
        self.desCol.pack_start(self.cellDes, True)
        self.desCol.add_attribute(self.cellDes, 'text', 6)
        self.desCol.set_sort_column_id(6)

        self.treeview.set_reorderable(True)

class Gcdv(object):
    # windows signals
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()
    # menu items signals
    def on_open_cdv_menu_activate(self, widget, data=None):
        """ Open menu
        """
        dialog = gtk.FileChooserDialog( "Open..",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*.cdv")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.cdv = CarnetDeVol(xmlfilename=dialog.get_filename()) 
            self.fillListFlies()
        elif response == gtk.RESPONSE_CANCEL:
            pass
        dialog.destroy()

    def on_imagemenuitem3_activate(self, widget, data=None):
        """ Save menu
        """
        self.cdv.save()

    def on_save_as_menu_activate(self, widget, data=None):
        """ Save as menu
        """
        dialog = gtk.FileChooserDialog( "Save as ...",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*.cdv")
        dialog.add_filter(filter)
        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.cdv.setXmlFilename(filename)
            self.cdv.setName(filename.split(".")[0].split("/")[-1])
            self.cdv.save()
            self.window.set_title("CarnetDeVol - "+str(self.cdv.getName()))
        elif response == gtk.RESPONSE_CANCEL:
            pass
        dialog.destroy()


    def on_quit_menu_item_activate(self, widget, data=None):
        """ Quit menu
        """
        gtk.main_quit()

    # edit menu
    def on_add_fly_activate(self, widget, data=None):
        """ Add menu
        """
        new_num = self.cdv.getMaxFlightNum()+1
        self.cdv.addFlight(new_num)
        self.listFlies.appendFly(self.cdv.getFlight(new_num))
    def on_del_fly_activate(self, widget, data=None):
        """ Delete menu
        """
        try:
            fly_activated = self.listFlies.selected()
            self.listFlies.suppressFly(fly_activated)
        except:
            pass
    # track menu
    def on_add_track_activate(self, widget, data=None):
        """ add track menu
        """


    # about menu
    def on_about_menu_activate(self, widget, data=None):
        """ About menu
        """
        about = gtk.AboutDialog()
        about.set_name("GCarnetDeVol")
        about.set_version(__VERSION__)
        about.set_website(__WEB__)
        about.set_license(__LICENSE__)
        about.set_authors(__AUTHORS__)
        about.run()
        about.destroy()

    # right clic
    def on_treeview_button_release_event(self, widget, data=None):
        if data.button == 3:
            print "fly selected "+str(self.listFlies.selected().getNumber())

    # list signals
    def on_treeview_row_activated(self, widget, data, col):
        """ data = (row_number,) """
        print "data : "+str(data)+" col : "+str(col)
        fly = self.listFlies.getFly(data[0])

    # init windows
    def __init__(self, cdv=None):
        self.cdv = cdv
        self.builder = gtk.Builder()
        self.builder.add_from_file("gui_cdv.xml")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("window")
        if cdv.getName()==None:
            self.window.set_title("CarnetDeVol - New*")
        else:
            self.window.set_title("CarnetDeVol - "+str(cdv.getName()))
        self.fillListFlies()

        self.statusbar = self.builder.get_object("statusbar1")
        self.statusbar.contextid = self.statusbar.get_context_id("time status")
        self.statusbar.push(self.statusbar.contextid,
             "Duree totale de vol : "+second2time(CDV.getTotalDuration())+\
             "  -  Temps moyen d'un vol: "+\
              second2time(CDV.getTotalDuration()/CDV.getNumberOfFlights())+\
             "  -  Nombre total de vol : "+str(CDV.getNumberOfFlights()))
                           

    def fillListFlies(self): 
        self.listFlies = ListFly(self.cdv, self.builder)
        if self.cdv != None:
            for fly in self.cdv.getFlights():
                self.listFlies.appendFly(fly)

if __name__ == "__main__":
    try:
        os.popen("gtk-builder-convert gui_cdv.glade gui_cdv.xml")
    except:
        pass
    if len(sys.argv) == 2:
        CDV = CarnetDeVol(xmlfilename=sys.argv[1])
    else:
        CDV = CarnetDeVol()

    print("Duree totale de vol : "+second2time(CDV.getTotalDuration()))
    print("Temps moyen d'un vol: "+\
            second2time(CDV.getTotalDuration()/CDV.getNumberOfFlights()))
    print("Nombre total de vol : "+str(CDV.getNumberOfFlights()))
    app = Gcdv(CDV)
    app.window.show()
    gtk.main()

