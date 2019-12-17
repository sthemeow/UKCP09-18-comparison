import os
import csv
import pandas as pd

# This program is written to collate all generated csv data files into a summary file.
# You should have run Decoder09.py and Decoder18.py before running this code.

dirname = os.path.dirname(__file__)

projectionList = ["UKCP09data", "UKCP18data"]
variableList = ["temp", "precip"]
timesliceList = ["2010-2039", "2020-2049", "2030-2059", "2040-2069", "2050-2079", "2060-2089", "2070-2099"]
periodList = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "mam", "jja", "son", "djf", "ann"]
areaList = ["Channel Islands", "East Midlands", "East of England", "Eastern Scotland", "Isle of Man", "London", "North East England", "North West England", "Northern Ireland", "Northern Scotland", "South East England", "South West England", "Wales", "West Midlands", "Western Scotland", "Yorkshire and Humberside"]
dictList = [12, 0, 1, 2, 13, 3, 4, 6, 14, 5, 7, 8, 15, 9, 10, 11]

with open(dirname + '/summary.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(["", "", "", "", "", "UKCP09", "", "", "UKCP18", "", "","Difference","",""])
    writer.writerow(["timeslice", "variable", "average", "period", "region", "10%", "50%", "90%", "10%", "50%", "90%", "10%", "50%", "90%"])
csvFile.close()
with open(dirname + '/summary_tranc.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(["timeslice", "variable", "average", "period", "region", "10%", "50%", "90%"])
csvFile.close()

for period in periodList:
    for timeslice in timesliceList:
        for variable in variableList:
            if variable == 'temp':
                averageList = ["dmax", "dmean", "dmin"]
            else:
                averageList = ["dmean"]
            for average in averageList:
                filename = period + '_' + timeslice + '_' + variable + '_' + average + '.csv'
                data = []
                for projection in projectionList:
                    with open('{0}/{1}/{2}/{3}'.format(dirname,projection,variable,filename)) as csvFile:
                        csvdata = list(csv.reader(csvFile, delimiter=','))
                        data.append(csvdata)
                    csvFile.close()
                with open(dirname+'/summary.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile, dialect='excel')
                    for num in range(16):
                        dictindex = dictList[num]
                        UKCP09_10 = data[0][num+1][1]
                        UKCP09_50 = data[0][num+1][2]
                        UKCP09_90 = data[0][num+1][3]
                        UKCP18_10 = data[1][dictindex+1][1]
                        UKCP18_50 = data[1][dictindex+1][2]
                        UKCP18_90 = data[1][dictindex+1][3]
                        Diff_10 = UKCP18_10 - UKCP09_10
                        Diff_50 = UKCP18_50 - UKCP09_50
                        Diff_90 = UKCP18_90 - UKCP09_90
                        writer.writerow([timeslice, variable, average, period, areaList[num], UKCP09_10, UKCP09_50, UKCP09_90, UKCP18_10, UKCP18_50, UKCP18_90, Diff_10, Diff_50, Diff_90])
                csvFile.close()
                with open(dirname+'/summary_tranc.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile, dialect='excel')
                    for num in range(16):
                        dictindex = dictList[num]
                        UKCP09_10 = data[0][num+1][1]
                        UKCP09_50 = data[0][num+1][2]
                        UKCP09_90 = data[0][num+1][3]
                        UKCP18_10 = data[1][dictindex+1][1]
                        UKCP18_50 = data[1][dictindex+1][2]
                        UKCP18_90 = data[1][dictindex+1][3]
                        Diff_10 = UKCP18_10 - UKCP09_10
                        Diff_50 = UKCP18_50 - UKCP09_50
                        Diff_90 = UKCP18_90 - UKCP09_90
                        writer.writerow([timeslice, variable, average, period, areaList[num], Diff_10, Diff_50, Diff_90])
                csvFile.close()
