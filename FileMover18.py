import os
import shutil

# This program is written to move netCDF files into a single folder.
# Raw data should be copied to ~/UKCP18data
dirname = os.path.dirname(__file__)+'UKCP18data'
variableList = [f for f in os.listdir(dirname) if os.path.isdir(dirname+'/'+f)]
for variable in variableList:
    periodList = [f for f in os.listdir(dirname+'/'+variable) if os.path.isdir(dirname+'/'+variable+'/'+f)]
    for period in periodList:
        fileList = [f for f in os.listdir(dirname+'/'+variable+'/'+period+'/latest') if (dirname+'/'+variable+'/'+period+'/latest/'+f)[-3:] == '.nc']
        for file in fileList:
            print(dirname+'/'+variable+'/'+period+'/latest/'+file)
            shutil.move(dirname+'/'+variable+'/'+period+'/latest/'+file, dirname+'/'+file)