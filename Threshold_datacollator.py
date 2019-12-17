import os
import csv
import pandas as pd

# This program is written to analyse whether the threshold is exceeded in two prediction cases repectively.
# You should have run Data_Collator.py before running this code.

dirname = os.path.dirname(__file__)

projectionList = ["UKCP09", "UKCP18"]
variableList = ["temp"]
timesliceList = ["2010-2039", "2020-2049", "2030-2059", "2040-2069", "2050-2079", "2060-2089", "2070-2099"]
periodList = ["ann"]
averageList = ['dmean']
areaList = ["East Midlands", "East of England", "Eastern Scotland", "London", "North East England", "North West England", "Northern Ireland", "Northern Scotland", "South East England", "South West England", "Wales", "West Midlands", "Western Scotland", "Yorkshire and Humberside"]
dictList = [12, 0, 1, 2, 13, 3, 4, 6, 14, 5, 7, 8, 15, 9, 10, 11]

with open(dirname + '/1961-1990 baseline/temp_baseline_1960-1990.csv', 'r') as csvFile:
    baselinedata = list(csv.reader(csvFile, delimiter=','))
csvFile.close()

with open(dirname + '/Threshold_summary.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile, dialect='excel')
    writer.writerow(["", "", "UKCP09", "", "", "UKCP18", "", ""])
    writer.writerow(["timeslice", "region", "10%", "50%", "90%", "10%", "50%", "90%"])
csvFile.close()

for period in periodList:
    baselineindex = baselinedata[0].index(period)
    for timeslice in timesliceList:
        for variable in variableList:
            for average in averageList:
                filename = period + '_' + timeslice + '_' + variable + '_' + average + '.csv'
                data = []
                for projection in projectionList:
                    with open(rootpath+projection+'/'+variable+'/'+filename) as csvFile:
                        csvdata = list(csv.reader(csvFile, delimiter=','))
                        data.append(csvdata)
                    csvFile.close()
                with open(dirname+'/Threshold_summary.csv', 'a', newline='') as csvFile:
                    writer = csv.writer(csvFile, dialect='excel')
                    for num in range(14):
                        baseline = float(baselinedata[num+1][baselineindex])
                        dictindex = dictList[num]
                        writer.writerow([timeslice, areaList[num], float(data[0][num+1][1])+baseline, float(data[0][num+1][2])+baseline, float(data[0][num+1][3])+baseline, float(data[1][dictindex+1][1])+baseline, float(data[1][dictindex+1][2])+baseline, float(data[1][dictindex+1][3])+baseline])
                csvFile.close()
