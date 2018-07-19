# -*- coding: utf-8 -*-

#==============================================================================
# HTML Generator Main
# Author: @NathanSWallace
# This file examines all CSV files and updates the HTML tables accordingly
#==============================================================================
import os
import csv

#Global dictionary to hold abbreivatons
abbrevs = {"type": {'A':'Annual', 'B':'Held Every Two Years', 'M': 'Held Multiple Times a Year'},
            "category":{'E&S':'Engineering & Scientific', 'T':'Tutorials','V':'Vendor Exhibition', 'S':'Standards Creation', 'G':'General ICS'}}

def main():
    EventsUpdate()

def getpath(filename):
    path = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(path, filename))
    return filepath

#Function to copy and modify event template file, event.html, and save off the new one.
def SetupEventPage(row):
    insertTable = ''
    TotalPapers = 0
    with open(getpath("HTML_Templates/event.html"), 'r') as eventTemp:
        with open("events/"+row["EventID"]+'/'+'event.html', "w") as fout:
            #Iterate over each file in the Event's (EventID) CSV folder
            for file in os.listdir(getpath("CSV_Files"+'/'+row["EventID"]+'/')):
                with open(getpath("CSV_Files"+"/"+row["EventID"]+"/"+file), 'r', encoding = 'ISO-8859-1') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for paper in reader:
                        TotalPapers += 1
                        insertTable += '<tr class="item"><td><a href="%s" target="_blank">%s</a></td><td>%s</td><td>%s</td></tr>\n' % (paper['PDF Link'],paper['Document Title'],paper['Authors'],paper['Publication_Year'])
            for line in eventTemp:
                CatDescription = ''
                Categories = row['Category'].split()
                for cats in Categories:
                    CatDescription += abbrevs['category'][cats]+", "
                #list of tags to parse and the variable to fill it.
                mapping = [('[tag_TotalPapers]', str(TotalPapers)), ('[tag_name]', row["Name"]), ('[tag_started]', row["Started"]), ('[tag_website]', row["Link"]), ('[tag_type]', abbrevs['type'][row['Type']]), ('[tag_categories]',CatDescription)]
                for i, j in mapping:
                    line = line.replace(i, j)
                line = line.replace('[tag_papers]', insertTable)
                fout.write(line)

    # #Iterate over each file in the Event's (EventID) folder
    # for file in os.listdir(getpath("CSV_Files"+row["EventID"]+'/')):
    #         with open(getpath(file), 'r') as csvfile:
    #             reader = csv.DictReader(csvfile)
    #             for row in reader:
    #                     insertTable += '<tr class="item"><td><a href="%s" target="_blank">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (link,row['Name'],row['Started'],row['Type'],row['Category'],row['Published'],row['Recorded'])
    #
    # #Copies insertTable into the proper place in the index.html file identified by [tag_events]
    # with open(getpath("HTML_Templates/index.html"), 'r') as indexTemp:
    #     with open("index.html", "w") as fout:
    #         for line in indexTemp:
    #             fout.write(line.replace('[tag_events]', insertTable))
    #
    #
    # with open(getpath("CSV_Files/events.csv"), 'r') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #
    #             #fout.write(line.replace('[tag_name]', row["Name"] ))
    # #
    # #
    # # <div class="w3-third w3-container w3-margin-bottom">
    # #   <h4>Name: [tag_name]</h4>
    # #   <p>Type: [tag_type]</p>
    # #   <p>Year Started: [tag_started]</p>
    # #   <p>[tag_website]</p>
    # # </div>
    # # <div class="w3-third w3-container w3-margin-bottom">
    # #   <h4>Category</h4>
    # #   <p>[tag_categories]</p>
    # # </div>
    # # <div class="w3-third w3-container w3-margin-bottom">
    # #   <h4>Stats </h4>
    # #   <p>Total Papers: [tag_TotalPapers]</p>

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
                link = "../events/"+row["EventID"]+'/'#getpath("../events/"+row["EventID"]+'/')
                SetupEventPage(row)
            insertTable += '<tr class="item"><td><a href="%s" target="_blank">%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (link,row['Name'],row['Started'],row['Type'],row['Category'],row['Published'],row['Recorded'])

    #Copies insertTable into the proper place in the index.html file identified by [tag_events]
    with open(getpath("HTML_Templates/index.html"), 'r') as indexTemp:
        with open("index.html", "w") as fout:
            for line in indexTemp:
                fout.write(line.replace('[tag_events]', insertTable))


if __name__ == "__main__":
    main()
