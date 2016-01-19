#! /usr/bin/env python
# -*- coding: utf-8 -*-

IRC_BLUE = '\003' + '02'
IRC_BOLD = '\002'
IRC_RESET = '\x0f'

import urllib2
from datetime import *

from time import gmtime, strftime
from xml.dom import minidom


def parser_all_day(url, d):
    doc = urllib2.urlopen(url)
    parsed = minidom.parse(doc)

    date2 = date.today() + timedelta(d)
    weekday = date2.isoweekday() - 1
    if weekday != 0:
        date2 = date2 - timedelta(weekday)
        Date = date2.strftime("%d/%m/%Y")
    else:
        Date = date2.strftime("%d/%m/%Y")

    T = []
    for element in parsed.getElementsByTagName('event'):
        if (element.getAttribute('date') == Date and int(element.childNodes[1].firstChild.nodeValue) == weekday):
            T1 = []
            #HEURE
            for j in element.getElementsByTagName('prettytimes'):
                T1 = T1 + [IRC_BLUE + j.firstChild.nodeValue.encode('utf-8') + IRC_RESET]
            #MODULE
            for j in element.getElementsByTagName('module'):
                T1 = T1 + [IRC_BOLD + j.childNodes[1].firstChild.nodeValue.encode('utf-8') + IRC_BOLD]
            #GROUPS

            for j in element.getElementsByTagName('group'):
                bool = False
                bool2 = False
                U = []
                for k in range(1,len(j.childNodes),2):
                    U = U + [str(j.childNodes[k].firstChild.nodeValue).encode('utf-8')]

                for l in range(len(U)):
                    if 'G' in U[l]:
                        for l2 in range(len(U[l])-1):
                            if (U[l][l2] == "G" and not bool):
                                U = str(U[l][l2]) + str(U[l][l2+1])
                                T1 = T1 + [U]
                                bool = True
                                continue
                    elif 'option' in U[l]:
                        bool2 = False
                        bool = False
                        for l2 in range(len(U[l])-1):

                            if (str(U[l][l2]).isdigit() and bool):
                                U2 = U2 + str(U[l][l2])
                                T1 = T1 + ["-"] + U2 + ["-"]
                                bool2 = True

                            elif (U[l][l2] == "o" and not bool):
                                U2 = "G"
                                bool = True
                                break

                            if bool2:
                                break
                                
                    if bool:
                        break

                if not bool:
                    T1 = T1 + ["-"] + U + ["-"]
            
            #STAFF
            for j in element.getElementsByTagName('staff'):
                T1 = T1 + [j.childNodes[1].firstChild.nodeValue.encode('utf-8')]
            #ROOM
            for j in element.getElementsByTagName('room'):
                T1 = T1 + [j.childNodes[1].firstChild.nodeValue.encode('utf-8')]
            #NOTES
            for j in element.getElementsByTagName('notes'):
                if (j.firstChild.nodeValue != None):
                    T1 = T1 + [j.firstChild.nodeValue.encode('utf-8')]

            T = T + [T1]
    return T

def parser_delayed(url):
    doc = urllib2.urlopen(url)
    parsed = minidom.parse(doc)

    date2 = date.today()
    weekday = date2.isoweekday() - 1 
    if weekday != 0:
        date2 = date2 - timedelta(weekday)
        Date = date2.strftime("%d/%m/%Y")
    else:
        Date = date2.strftime("%d/%m/%Y")

    T = []
    for element in parsed.getElementsByTagName('event'):
        #DATE
        if (element.getAttribute('date') == Date and int(element.childNodes[1].firstChild.nodeValue) == weekday):
            for j in element.getElementsByTagName('starttime'):
                tmp = j.childNodes[0].nodeValue
                tmp2 = datetime.strptime(tmp,"%H:%M").time()
                today = datetime.today()

                if ((today.hour == tmp2.hour and today.minute < tmp2.minute) or (today.hour < tmp2.hour)):
                        T1 = []
                        #HEURE
                        for j in element.getElementsByTagName('prettytimes'):
                            T1 = T1 + [IRC_BLUE + j.firstChild.nodeValue.encode('utf-8') + IRC_RESET]
                        #MODULE
                        for j in element.getElementsByTagName('module'):
                            T1 = T1 + [IRC_BOLD + j.childNodes[1].firstChild.nodeValue.encode('utf-8') + IRC_BOLD]
                        #GROUPS
                        
                        for j in element.getElementsByTagName('group'):
                            bool = False
                            bool2 = False
                            U = []
                            for k in range(1,len(j.childNodes),2):
                                U = U + [str(j.childNodes[k].firstChild.nodeValue).encode('utf-8')]

                            for l in range(len(U)):
                                if 'G' in U[l]:
                                    for l2 in range(len(U[l])-1):
                                        if (U[l][l2] == "G" and not bool):
                                            U = str(U[l][l2]) + str(U[l][l2+1])
                                            T1 = T1 + [U]
                                            bool = True
                                            continue
                                elif 'option' in U[l]:
                                    bool2 = False
                                    bool = False
                                    for l2 in range(len(U[l])-1):

                                        if (str(U[l][l2]).isdigit() and bool):
                                            U2 = U2 + str(U[l][l2])
                                            bool2 = True

                                        elif (U[l][l2] == "o" and not bool):
                                            U2 = "G"
                                            bool = True
                                            break

                                        if bool2:
                                            break
                                
                                if bool:
                                    break

                            if not bool:
                                T1 = T1 + U

                        #STAFF
                        for j in element.getElementsByTagName('staff'):
                            T1 = T1 + [j.childNodes[1].firstChild.nodeValue.encode('utf-8')]
                        #ROOM
                        for j in element.getElementsByTagName('room'):
                            T1 = T1 + [j.childNodes[1].firstChild.nodeValue.encode('utf-8')]
                        #NOTES
                        for j in element.getElementsByTagName('notes'):
                            T1 = T1 + [j.firstChild.nodeValue.encode('utf-8')]

                        T = T + [T1]
    return T

