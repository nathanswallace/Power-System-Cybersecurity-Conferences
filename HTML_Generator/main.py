# -*- coding: utf-8 -*-

#==============================================================================
# HTML Generator Main
# Author: @NathanSWallace
# This file examines all CSV files and updates the HTML tables accordingly
#==============================================================================
import os
import csv

def main():
    EventsUpdate()

def getpath(filename):
    path = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(path, filename))
    return filepath

#Function to copy and modify event template file, event.html, and save off the new one.
#def SetupEventPage(EventID):

def EventsUpdate():
    insertTable = ''
    with open(getpath("CSV_Files/events.csv"), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #If EventFolder isnt created need to create both CSV and HTML directories.
            #1st CSV directory, to store CSV of papers, talks etc for each
            if not os.path.exists(getpath("CSV_Files/"+row["EventID"])):
                os.makedirs(getpath("CSV_Files/"+row["EventID"]))
            #2nd Events directory, to store HTML code for each EventID.
            if not os.path.exists(getpath("../events/"+row["EventID"])):
                os.makedirs(getpath("../events/"+row["EventID"]))
            #Adds the row to the html table temp insert variable
            link = row['Link']
            ####### TO DO - Come back and adjust target. Open extenal link in new tab. Open internal link in same window.
            #Check to see if the app will contain an internal link to the event page or redirect to the main event's website.
            if row['InternalLink'] == 'Yes':
                link = getpath("../events/"+row["EventID"]+'/')
                #SetupEventPage(row['EventID'])
            insertTable += '<tr class="item"><td><a href="%s" target="_blank">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (link,row['Name'],row['Started'],row['Type'],row['Category'],row['Published'],row['Recorded'])

    #Copies insertTable into the proper place in the index.html file identified by [tag_events]
    with open(getpath("HTML_Templates/index.html"), 'r') as indexTemp:
        with open("index.html", "w") as fout:
            for line in indexTemp:
                fout.write(line.replace('[tag_events]', insertTable))


if __name__ == "__main__":
    main()
