import os

# This program is written to delete unwanted files in UKCP09 raw data.
# Raw data should be copied to ~/UKCP09data
currentdir = os.path.dirname(__file__)+'/UKCP09data'
dirList = [f for f in os.listdir(currentdir) if os.path.isdir(f)]
for dir in dirList:
    fileList = [f for f in os.listdir(currentdir+'/'+dir) if f[-3:] == '.nc']
    for file in fileList:
        if ('temp' in file) or ('precip' in file):
            pass
        else:
            os.remove('{}/{}/{}'.format(currentdir,dir,file))