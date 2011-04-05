#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
from CarnetDeVol import Flight, CarnetDeVol, Track, Gpx
from CarnetDeVol import datetime2gpx, gpx2datetime 


class Menu(object):
    
    def cdv_create(self):
        """ This function create a new CarnetDeVol
        """
        print "TODO"
  
    def cdv_save(self):
        print("saved")
        self.CDV.save()

    def cdv_dump(self):
        """ Debug function dump xml file
        """
        print self.CDV.dump()

    def cdv_open(self, filename=None):
        """ This function open an existing CarnetDeVol
        """
        if not filename:
            print "Please give a CarnetDeVol name:",
            response = raw_input()
            self.cdv_filename = response+".cdv"
        else:
            self.cdv_filename = filename
        print "Opening "+self.cdv_filename
        try:
            self.CDV=CarnetDeVol(xmlfilename=self.cdv_filename)
        except IOError, e:
            print str(e)
    
    def cdv_print(self):
        """ print a resumé of carnetdevol
        """
        if self.CDV:
            self.CDV.printFlights()
        else:
            print("No carnetdevol loaded")

    def cdv_addflight(self):
        """ Adding new flight in cdv xml file
        """
        list_flightNumber = self.CDV.getFlightNumbers()
        print("Give a flight number (default %d)"%(list_flightNumber[-1]+1))
        response = raw_input()
        try:
            if response == "":
                flight_num = list_flightNumber[-1]+1
            else:
                flight_num = int(raw_input())
        except Exception, e:
            print("[ERROR] "+str(e))
            return
        if flight_num in list_flightNumber:
            print("[ERROR] This flight number is already used")
            return
        self.CDV.addFlights(flight_num=flight_num)

    def cdv_print_flight(self, flight_num):
        """ Print a flight
        """

    def cdv_edit_flight(self):
        """ Edit a flight
        """
        self.cdv_print()
        print("Give a flight number:"),
        response = raw_input()
        if int(response) in self.CDV.getFlightNumbers():
            flight = self.CDV.getFlight(int(response))
            exit = False
            while not exit:
                print("What do you want to do ('q' back to main menu)")
                print(" 1 - Modify date")
                print(" 2 - Modify site")
                print(" 3 - Modify duration")
                print(" 4 - Modify wing")
                print(" 5 - Modify description")
                print(" 6 - Adding a track")
                print(" 7 - Delete track")
                print ">",
                response = raw_input()
                if   response == "1":
                    print("Current date is : "+str(flight.getDate()))
                    print("Give a date in format : AAAA-MM-DDTHH:MM:SSZ" )
                    rdate = raw_input()
                    try:
                        date = gpx2datetime(rdate.strip())
                    except Exception, e:
                        print("Entry error: "+str(e))
                        continue
                    flight.setDate(date)
                elif response == "2":
                    try:
                        print("Current site is : "+str(flight.getSite()))
                    except UnicodeEncodeError:
                        pass
                    print("Give new site name :")
                    site = raw_input()
                    flight.setSite(site)
                elif response == "3":
                    print("Current duration is :"+str(flight.getDuration()))
                    print("Give new duration in seconds:")
                    duration = raw_input()
                    try:
                        flight.setDuration(duration)
                    except Exception, e:
                        print("wrong value :"+str(e))
                        continue
                elif response == "4":
                    try:
                        print("Current wing is :"+str(flight.getWing()))
                    except UnicodeEncodeError:
                        pass
                    print("Give new wing name :")
                    wing = raw_input()
                    flight.setWing(wing)
                elif response == "5":
                    try:
                        print("Current desc is :"+str(flight.getDesc()))
                    except UnicodeEncodeError:
                        pass
                    print("Give new description :")
                    desc = raw_input()
                    flight.setDesc(desc)
                    print("description modified :"+str(flight.getDesc()))
                elif response == "6":
                    if flight.getTrack() != None:
                        print("Can't add new track, delete it before")
                    else:
                        print("Please give a GPX filename")
                        filename = raw_input()
                        gpx = Gpx(filename)
                        names = gpx.getTrackNames()
                        print("Find "+str(len(names))+" tracks")
                        for index in range(len(names)):
                            print(" "+str(index)+" - "+str(names[index]))
                        print("Give track number you want to add:")
                        number = raw_input()
                        flight.addTrack(gpx.getTrack(names[int(number)]).node)

                elif response == "7":
                    flight.delTrack()
                    print("Track deleted")
                elif response == "q":
                    exit = True
                else:
                    print "[ERR] Wrong entry "+str(response)
        else:
            print("No flight with number "+str(response))

        

if __name__ == "__main__":
    print "Welcome in CarnetDeVol"
    menu = Menu()
    if len(sys.argv) == 2:
         menu.cdv_open(sys.argv[1])
    while exit != True:
        if menu.CDV:
            print "Current CarnetDeVol is \033[32;1m"+str(menu.CDV.getName()+"\033[0m")
        else:
            print "No CarnetDeVol open"
        print ""
        print "What do you want to do ('q' for quit)?"
        print " 1 - Create new CarnetDeVol."
        print " 2 - Open an existing CarnetDeVol."
        print " 3 - Print CarnetDeVol"
        if menu.CDV:
            print " 4 - Adding new fly"
            print " 5 - (DEBUG)Print all xml"
            print " 6 - Save"
            print " 7 - Edit flight"
        print ">",
        response = raw_input()
        if   response == "1":
            menu.cdv_create()
        elif response == "2":
            menu.cdv_open()
        elif response == "3":
            menu.cdv_print()
        elif response == "4":
            if menu.CDV:
                menu.cdv_addflight()
            else:
                print("open a carnetdevol before")
        elif response == "5":
            if menu.CDV:
                menu.cdv_dump() 
            else:
                print("open a carnetdevol before")
        elif response == "6":
            if menu.CDV:
                menu.cdv_save() 
            else:
                print("open a carnetdevol before")
        elif response == "7":
            if menu.CDV:
                menu.cdv_edit_flight() 
            else:
                print("open a carnetdevol before")
        elif response == "q":
            exit = True
        else:
            print "[ERR] Wrong entry "+str(response)


