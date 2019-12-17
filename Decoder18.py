from netCDF4 import Dataset
import csv
import os
import errno

# This program is written to convert UKCP18 raw data to a series of csv files.
# You should have run FileMover18.py before running this code.

dirname = os.path.dirname(__file__)  # Obtain this file's path

variableList = ["prAnom", "tasAnom", "tasmaxAnom", "tasminAnom"]
timesliceList = ["2010-2039", "2020-2049", "2030-2059", "2040-2069", "2050-2079", "2060-2089", "2070-2099"]
periodfileList = ["ann", "seas", "mon"]

axis = ["East Midlands", "East of England", "Eastern Scotland", "London", "North East England", "Northern Scotland", "North West England", "South East England", "South West England", "West Midlands", "Western Scotland", "Yorkshire and Humberside", "Channel Islands", "Isle of Man", "Northern Ireland", "Wales"]
periodList = [["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], ["mam", "jja", "son", "djf"], ["ann"]]

# Create directory if non-exist
for newdir in ["temp", "precip"]:
    try:
        os.makedirs(dirname+"/UKCP18data/"+newdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

for periodfile in periodfileList:
    if periodfile == "mon":
        periodnum = 12
        periodindex = 0
    elif periodfile == "seas":
        periodnum = 4
        periodindex = 1
    else:
        periodnum = 1
        periodindex = 2
    for variable in variableList:
        if "tas" in variable:
            vardir = "temp"
        else:
            vardir = "precip"
        if "max" in variable:
            pathaverage = "dmax"
        elif "min" in variable:
            pathaverage = "dmin"
        else:
            pathaverage = "dmean"
        path = "{0}_sres-a1b_land-prob_uk_region_cdf_b6190_30y_{1)_20091201-20991130".format(variable,periodfile)
        rootgrp = Dataset("{0}/data/{1}.nc".format(dirname,path), "r")
        vars = rootgrp.variables
        data = vars[variable]
        for num in range(7):
            pathyearstart = 10*num+2010
            pathyearend = 10*num+2039
            pathyear = str(pathyearstart)+'-'+str(pathyearend)
            for period in range(periodnum):
                tabledata = data[num*periodnum+period]
                pathperiod = periodList[periodindex][period]
                newpath = pathperiod+'_'+pathyear+'_'+vardir+'_'+pathaverage
                with open('{0}/UKCP18data/{1}/{2}.csv'.format(dirname,vardir,newpath), 'w', newline='') as csvFile:
                    writer = csv.writer(csvFile, dialect="excel")
                    writer.writerow(["region", "10%", "50%", "90%"])
                    for georegion in range(16):
                        header = axis[georegion]
                        tenth = tabledata[georegion][15]
                        fiftieth = tabledata[georegion][55]
                        ninetieth = tabledata[georegion][95]
                        writer.writerow([header, tenth, fiftieth, ninetieth])
                csvFile.close()