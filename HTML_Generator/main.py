# -*- coding: utf-8 -*-

#==============================================================================
# HTML Generator Main
# Author: @NathanSWallace
#==============================================================================
import os
import csv

def main():
    EventsUpdate()

def getpath(filename):
    path = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(path, filename))
    return filepath

def EventsUpdate():
    insertTable = ''
    with open(getpath("CSV_Files/events.csv"), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            insertTable += '<tr class="item"><td><a href="%s" target="_blank">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (row['Link'],row['Name'],row['Started'],row['Type'],row['Category'],row['Published'],row['Recorded'])
    with open(getpath("HTML_Templates/index.html"), 'r') as indexTemp:
        with open("index.html", "w") as fout:
            for line in indexTemp:
                fout.write(line.replace('[tag_events]', insertTable))


if __name__ == "__main__":
    main()
