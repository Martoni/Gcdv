#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
# Script permettant d'analyser les vols en parapente.
# Version 0.1
#TODO:
# - Mieux gérer le xml (pour éviter le bug du \n avant la balise <trk>
# - Multi-plot

import sys
import getopt
from xml.dom.minidom import parse
import matplotlib.pyplot as plt
import math

fig = plt.figure()

def usage():
    print "utilisation: analysevol [option] FICHIER.gpx"

def horaireToSecondes(horaire):
    horaire = horaire.split('T')[-1][:-1].split(':')
    return 60*60*int(horaire[0]) + 60*int(horaire[1]) + int(horaire[2])

def moyList(tabular):
    sum = 0
    for i in tabular:
        sum += i
    return (sum/len(tabular))

def plotTabular(tabular, moyenne=0):
    if moyenne != 0:
        mini_tab = []
        for k in range(moyenne):
            mini_tab.append(tabular[1])
        tabular2 = []
        for j in tabular:
            mini_tab = mini_tab[1:]
            mini_tab.append(j)
            tabular2.append(moyList(mini_tab))
        plt.plot(range(len(tabular)), tabular, range(len(tabular2)), tabular2)
    else:
        plt.plot(range(len(tabular)), tabular)

def tauxDeChute(coordonees):
    tdc = []
    old_point = coordonees.pop()
    for point in coordonees: 
        tdc.append((point['Altitude'] - old_point['Altitude'])/(horaireToSecondes(point['Temps'])-horaireToSecondes(old_point['Temps'])))
        old_point = point
    return tdc

def finesse(coordonees):
    MAX_FINESSE = 11
    fin_tab = []
    old_point = coordonees.pop()
    for point in coordonees:
        finesse = math.fabs(distance2D(point, old_point)/(old_point["Altitude"] - point["Altitude"]))
        if finesse > MAX_FINESSE:
            finesse = MAX_FINESSE
        fin_tab.append(finesse)
        old_point = point
    return fin_tab

def rad(value):
    """ converti des degrées en radian """
    RADIANS_PER_DEGREE = (math.pi)/180
    ret =  value*RADIANS_PER_DEGREE
    return ret

def egaux(point1, point2):
    if point1["Longitude"] != point2["Longitude"]:
        return 0
    if point1["Latitude"] != point2["Latitude"]:
        return 0
    return 1

def distance2D(point1, point2):
    """ calcule la distance à plat entre deux points:
        point = {"Longitude":valeur, "Latitude":valeur}
    """
    R = 6378137

    if egaux(point1, point2):
        return 0
    # R x arcos [ sin(lat1) x sin(lat2) + cos(lat1) x cos(lat2) x cos(lon2-lon1) ]
    return R * math.acos(
                math.sin(rad(point1["Latitude"]))*math.sin(rad(point2["Latitude"])) +\
                math.cos(rad(point1["Latitude"]))*math.cos(rad(point2["Latitude"]))*\
                math.cos(rad(point2["Longitude"])-rad(point1["Longitude"]))
            )

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--helps"):
            usage()
            sys.exit()
    source = "".join(args)

    if source == "":
        usage()
        sys.exit(2)
    elif (source.split(".")[-1] != "gpx"):
        print "Must be a gpx file, not a "+source.split(".")[-1]+" file."

    F_GPX = open(source, 'r');
    track = parse(source).documentElement._get_firstChild().getElementsByTagName("trkseg").pop()
    Latitude=[]
    Longitude=[]
    Altitude=[]
    point_tab=[]
    for point in track._get_childNodes():
        if point.nodeName == 'trkpt':
            point_tab.append({'Latitude':float(point.getAttribute('lat')),
                             'Longitude':float(point.getAttribute('lon')),
                             'Altitude':float(point.getElementsByTagName('ele').pop().firstChild.data),
                             'Temps':point.getElementsByTagName('time').pop().firstChild.data})
    old_point = point_tab[0]
    distance_parcouru = 0
    for point in point_tab:
        print "Lon:"+str(point['Longitude'])+\
                            " Lat:"+str(point['Latitude'])+\
                            " Alt:"+str(point['Altitude'])+\
                            " temps:"+str(point['Temps'])+\
                            " dist:"+str(distance2D(point, old_point))+\
                            " chute:"+str(old_point["Altitude"]-point["Altitude"])
        distance_parcouru += distance2D(point, old_point)
        old_point = point

    print "Distance horizontale parcourue : "+str(distance_parcouru)

#    plotTabular(tauxDeChute(point_tab), 10)
    plotTabular(finesse(point_tab), 10)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
