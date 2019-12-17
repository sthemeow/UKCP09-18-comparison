from netCDF4 import Dataset
import csv
import os
import errno

# This program is written to convert UKCP09 raw data to a series of csv files.
# You should have run DeleteFiles09.py before running this code.

dirname = os.path.dirname(__file__)  # Obtain this file's path

percentile = "tmean"
variableList = ["temp", "precip"]
timesliceList = ["2010-2039", "2020-2049", "2030-2059", "2040-2069", "2050-2079", "2060-2089", "2070-2099"]
periodList = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "mam", "jja", "son", "djf", "ann"]

axis = ["Channel Islands", "East Midlands", "East of England", "Eastern Scotland", "Isle of Man",
        "London", "North East England", "North West England", "Northern Ireland", "Northern Scotland",
        "South East England", "South West England", "Wales", "West Midlands", "Western Scotland",
        "Yorkshire and Humberside"]

# Create directory if non-exist
for newdir in variableList:
    try:
        os.makedirs(dirname+"/UKCP09data/"+newdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

for timeslice in timesliceList:
    for period in periodList:
        for variable in variableList:
            if variable == "temp":
                attributes = "abs"
                propertyList = ["dmin", "dmean", "dmax"]
            else:
                attributes = "perc"
                propertyList = ["dmean"]
            for property in propertyList:
                rootgrp = Dataset("{0}/UKCP09data/{1}/{2}.nc".format(dirname,timeslice,path), "r")  # Source data path
                path = "prob_land_cc_region_{0}_{1}_{2}_{3}_{4}_{5}".format(period, timeslice, variable, property, percentile, attributes)
                vars = rootgrp.variables
                data = vars["cdf_{0}_{1}_{2}_{3}".format(variable,property,percentile,attributes)]
                # data.dimensions = ('meaning_period', 'time', 'em_scen', 'georegion', 'percentile')

                tabledata = data[0][0][1]
                with open("{0}/UKCP09data/{1}/{2}_{3}_{4}_{5}.csv".format(dirname,variable,period,timeslice,variable,property), 'w', newline='') as csvFile:
                    writer = csv.writer(csvFile, dialect="excel")
                    writer.writerow(["region", "10%", "50%", "90%"])
                    for georegion in range(16):
                        header = axis[georegion]
                        tenth = tabledata[georegion][13]
                        fiftieth = tabledata[georegion][53]
                        ninetieth = tabledata[georegion][93]
                        writer.writerow([header, tenth, fiftieth, ninetieth])
                csvFile.close()