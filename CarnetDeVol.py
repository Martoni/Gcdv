#!/usr/bin/python
# -*- coding: utf-8 -*- 

import xml.etree.ElementTree as ET
import datetime
import math

XML_HEADER = '<?xml version="1.0" encoding="utf-8"?>'

def XMLBeautifier(xml_data):
    """
    This function make XML output looks better and more readable.
    Fabrice Mousset <fabrice.mousset@laposte.net>

    Can be done with "indent" function in ElementTree
    """
    xml_text = ""
    xml_ident = 0
    for xml_line in xml_data.split('<'):
        xml_line = xml_line.strip()
        if(len(xml_line) > 0):
            if xml_line.endswith("/>"):
                xml_text += ' '*xml_ident + "<" + xml_line + "\n"
            else:
                if(xml_line.startswith('/')):
                    xml_ident -= 4
                    xml_text += ' '*xml_ident + "<" + xml_line + "\n"
                else:
                    xml_text += ' '*xml_ident + "<" + xml_line + "\n"
                    xml_ident += 4
    return xml_text

def rad(value):
    """ convert rad in deg """
    RADIANS_PER_DEGREE = (math.pi)/180
    return  value*RADIANS_PER_DEGREE

def datetime2gpx(datetime):
  """ return datetime in gpx format:
  2011-03-04T12:30:08Z
  """
  return ("%04d-%02d-%02dT%02d:%02d:%02dZ"%\
          (datetime.year,
           datetime.month,
           datetime.day,
           datetime.hour,
           datetime.minute,
           datetime.second))

def gpx2datetime(datestring):
    vdate = datestring.split('T')[0]
    vdate = vdate.split('-')
    vtime = datestring.split('T')[1][:-1]
    vtime = vtime.split(':')
    return datetime.datetime(
           year = int(vdate[0]),
           month= int(vdate[1]),
           day=   int(vdate[2]),
           hour=  int(vtime[0]),
           minute=int(vtime[1]),
           second=int(vtime[2]))
 
class CdvError(Exception):
    """ Manage exception
    TODO
    """
    pass

class CarnetDeVol:
    """ Manage CarnetDeVol object
    """
    def __init__(self, xmlfilename=None):
        if xmlfilename == None:
            print "TODO: create a new CarnetDeVol"
        else:
            self.xmlfilename = xmlfilename
            self.xml = ET.parse(xmlfilename)
            self.cdv_root = self.xml.getroot()
            if self.cdv_root.tag != "cdv":
                raise Exception("This xml file is not a CarnetDeVol file: "+\
                                str(self.cdv_root.tag))
    def dump(self):
        return ET.dump(self.cdv_root)

    def save(self):
        savefile = open(self.xmlfilename, "w")
        savefile.write(XML_HEADER + '\n' +\
                XMLBeautifier(ET.tostring(self.cdv_root,"utf-8")))
        savefile.close()

    def getName(self):
        """ Return name of the carnet de vol
        """
        return self.cdv_root.get("name")

    def setName(self, name):
        """ Set the name of carnetdevol
        """
        print("TODO")

    def getFlightNumbers(self):
        """ Return the list of flights number
        """
        return sorted([fly.getNumber() for fly in self.getFlights()])
    def getMaxFlightNum(self):
        try:
            return self.getFlightNumbers()[-1]
        except IndexError:
            return 0

    def getFlights(self):
        """ Return a list of flights under the CarnetDeVol
        """
        return [Flight(node) for node in self.cdv_root.getchildren()]

    def getFlight(self, flight_num):
        """ Return the flight given by number
        """
        for flight in self.getFlights():
            if flight.getNumber() == flight_num:
                return flight
        return None

    def delFlight(self, fly):
        """ Suppress a flight from list
        """
        self.cdv_root.remove(fly.node)

    def addFlight(self, flight_num):
        """ Adding new flight under carnetdevol
        """
        new_flight = Flight(number=flight_num)
        new_flight.setDate(datetime.datetime.now())
        self.cdv_root.append(new_flight.node)

    def printFlights(self):
        """ Print an array of each flight
        """
        NUM_SIZE=3
        DATE_SIZE=20
        SITE_SIZE=24
        DESC_SIZE=50
        TRACK_SIZE=5
        print("")
        print("-"*(NUM_SIZE+DATE_SIZE+SITE_SIZE+DESC_SIZE+TRACK_SIZE+5))
        print( "%-*s|"%(NUM_SIZE,"Num")+\
               "%-*s|"%(DATE_SIZE,"Date")+\
               "%-*s|"%(SITE_SIZE,"Site")+\
               "%-*s|"%(DESC_SIZE,"Description")+\
               "%-*s|"%(TRACK_SIZE,"Track"))
        print("-"*(NUM_SIZE+DATE_SIZE+SITE_SIZE+DESC_SIZE+TRACK_SIZE+5))
        for fly in self.getFlights():
            if fly.getTrack():
                track="Yes"
            else:
                track="No"
            print("%-*s|"%(NUM_SIZE,"%03s"%fly.getNumber())+\
                  "%-*s|"%(DATE_SIZE,fly.getDate()[:DATE_SIZE])+\
                  "%-*s|"%(SITE_SIZE,fly.getSite()[:SITE_SIZE])+\
                  "%-*s|"%(DESC_SIZE,fly.getDesc().replace('\n',' ')[:DESC_SIZE])+\
                  "%-*s|"%(TRACK_SIZE,track[:TRACK_SIZE]))
        print("-"*(NUM_SIZE+DATE_SIZE+SITE_SIZE+DESC_SIZE+TRACK_SIZE+5))
        print("")

class Flight:
    """ Manage flights
    """
    def __init__(self, node=None, number=None):
        self.track = None
        if node==None:
            if not number:
                raise Exception("No flight number")
            self.node = ET.Element("flight",attrib={"number":str(number)})
        elif node.tag == "flight":
            self.node = node
        else:
            raise Exception("Can't create flight, wrong node")

    def getNumber(self):
        return int(self.node.get("number"))
    def setNumber(self, number):
        self.node.set("number", str(int(number)))
    def getDate(self):
        date_node = self.node.find("date")
        if date_node == None or date_node.text == None:
            return ""
        else:
            return date_node.text.strip("\n\t ")

    def getSite(self):
        site_node = self.node.find("site")
        if site_node == None or site_node.text == None:
            return ""
        else:
            return site_node.text.strip("\n\t ")
    def getDuration(self):
        duration_node = self.node.find("duration")
        if duration_node == None or duration_node.text == None:
            return 0
        else:
            return int(duration_node.text.strip("\n\t "))
    def getDesc(self):
        desc_node = self.node.find("description")
        if desc_node == None or desc_node.text == None:
            return ""
        else:
            return desc_node.text.strip("\n\t ")
    def getWing(self):
        wing_node = self.node.find("wing")
        if wing_node == None or wing_node.text == None:
            return ""
        else:
            return wing_node.text.strip("\n\t ")

    def getTrack(self):
        if self.track != None:
            return self.track
        track = self.node.find("trkseg")
        if track == None:
            return None
        self.track = Track(self.node.find("trkseg"))
        return self.track

    def delTrack(self):
        track = self.node.find("trkseg")
        self.node.remove(track)
        self.track = None

    def addTrack(self, node):
        if self.track != None:
            raise Exception("Can't add track, there already is a track in this flight")
        self.track = Track(node)
        self.node.append(node)

    def setDate(self, date):
        date_element = self.node.find("date")
        if date_element == None:
            date_element = ET.Element("date")
            date_element.text = datetime2gpx(date)
            self.node.append(date_element)
        else:
            date_element.text = datetime2gpx(date)

    def setSite(self, site):
        site_element = self.node.find("site")
        if site_element == None:
            site_element = ET.Element("site")
            site_element.text = str(site) 
            self.node.append(site_element)
        else:
            site_element.text = site

    def setDuration(self, duration):
        duration_element = self.node.find("duration")
        if duration_element == None:
            duration_element = ET.Element("duration")
            duration_element.text = str(duration) 
            self.node.append(duration_element)
        else:
            duration_element.text = str(duration)

    def setWing(self, wing):
        wing_element = self.node.find("wing")
        if wing_element == None:
            wing_element = ET.Element("wing")
            wing_element.text = str(wing) 
            self.node.append(wing_element)
        else:
            wing_element.text = wing

    def setDesc(self, desc):
        desc_element = self.node.find("description")
        if desc_element == None:
            desc_element = ET.Element("description")
            desc_element.text = str(desc) 
            self.node.append(desc_element)
        else:
            desc_element.text = str(desc)

class Gpx(object):
    """ Manage GPX files
    """
    def __init__(self, filename):
        self.xmlfilename = filename
        self.xml = ET.parse(self.xmlfilename)
        self.root = self.xml.getroot()
        self.track_dict = {}
        if self.root.tag != "gpx":
            raise Exception("This xml file is not a gpx file: "+\
                    str(self.root.tag))
        for track in self.root.getchildren():
            self.track_dict[track.find("name").text] = Track(node = track.find("trkseg"))
       
    def getTrackNames(self):
        return self.track_dict.keys()

    def getTrack(self, name):
        return self.track_dict[name]

class Track(object):
    """ Manage Track in GPX format
    """
    def __init__(self, node=None):
        if node==None:
            print "TODO"
        else:
            self.node = node
    def getPoints(self):
        """ Return list of points
        """
        return [Point(node) for node in self.node.getchildren()]

    def getDateTimes(self):
        """ Return sorted list of Datetime
        """
        return sorted([point.getDateTime for point in self.getPoints])

    def getFirstPoint(self):
        return self.getDateTimes()[0]
    def getLastPoint(self):
        return self.getDateTimes()[-1]
    def getFlightDuration(self):
        return self.getLastPoint().getDateTime()-\
                    self.getFirstPoint().getDateTime()

class Point:
    """ Manage point
    """
    def __init__(self, node=None):
        if node == None:
            print "TODO"
            return None
        else:
            self.node = node
    def distanceH(self, point):
        """ Calculate horizontal distance 
        between point and self : point - self
        """
        return point.getElevation()-self.getElevation()

    def distanceV(self, point):
        """ Calculate vertical distance
        between point and self : point - self
        """
        R=6378137

        if (self.getLatitude() == point.getLatitude) and\
            (self.getLongitude() == point.getLongitude()):
            return 0
        # R x arcos [ sin(lat1) x sin(lat2) + cos(lat1) x cos(lat2) x cos(lon2-lon1) ]
        return R * math.acos(
                math.sin(rad(point1["Latitude"]))*math.sin(rad(point2["Latitude"])) +\
                math.cos(rad(point1["Latitude"]))*math.cos(rad(point2["Latitude"]))*\
                math.cos(rad(point2["Longitude"])-rad(point1["Longitude"]))
            )

    def getDateTime(self):
        return gpx2datetime(self.node.find("time").text)
    def getLatitude(self):
        return float(self.node.get("lat"))
    def getLongitude(self):
        return float(self.node.get("lon"))
    def getElevation(self):
        return float(self.node.find("ele").text)

     
