import os
import errno
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# This program is written to visualise the difference between UKCP09 and UKCP18.
# You should have run Data_Collator.py before running this code.

dirname = os.path.dirname(__file__)
newdirList = {'temp', 'precip'}
for newdir in newdirList:
    try:
        os.makedirs(dirname + '/Plots/' +newdir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# The following dictionary defines the colourmap
# Format: (pivot (x-axis) value, color value left, color value right)
# For continuous colourmap, colour value left == colour value right
cdict = {'red':  ((0.0, 0.3882, 0.3882),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.9725, 0.9725)),

        'green': ((0.0, 0.7451, 0.7451),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.4118, 0.4118)),

        'blue':  ((0.0, 0.4824, 0.4824),
                  (0.5, 1.0, 1.0),
                  (1.0, 0.4196, 0.4196))
       }
# The above colour map corresponds to #63BE7B at minimum, white at middle and #F8696B at maximum
# You are advised to take maximum = - minimum to have white at zero
GnRd = colors.LinearSegmentedColormap('GnRd', cdict)  # Create the colormap using the dictionary

# File name dictionary
vardict = {'temp': 'air temperature', 'precip': 'precipitation rate'}
avgdict = {'dmin': 'minimum', 'dmean': 'mean', 'dmax': 'maximum'}
periodict = {"jan": 'January', "feb": 'February', "mar": 'March', "apr": 'April', "may": 'May', "jun": 'June', "jul": 'July', "aug": 'August', "sep": 'September', "oct": 'October', "nov": 'November', "dec": 'December', "mam": 'spring', "jja": 'summer', "son": 'autumn', "djf": 'winter', "ann": 'annual'}

# Data file name (put them in the same folder as the script)
shapefile_path = dirname+"/shapefile/ukcp18-uk-land-region-lowres.shp"
datafile_path = dirname+"/summary_tranc.csv"

# Import and data
shapefile = gpd.read_file(shapefile_path)  # Map Shape Data
datafile = pd.read_csv(datafile_path, header=0)  # UKCP Data

# Change Region Name to match csv file
shapefile['Region'] = shapefile['Region'].replace('East Scotland', 'Eastern Scotland')
shapefile['Region'] = shapefile['Region'].replace('North Scotland', 'Northern Scotland')
shapefile['Region'] = shapefile['Region'].replace('West Scotland', 'Western Scotland')
shapefile['Region'] = shapefile['Region'].replace('Yorkshire and Humber', 'Yorkshire and Humberside')

# merge data
mergefile = shapefile.set_index('Region').join(datafile.set_index('region'))  # Combine Two Sets of Data

# Lists of all possible parameters
timesliceList = {"2020-2049"}
variableList = {'temp'}
periodList = {"jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "mam", "jja", "son", "djf", "ann"}
percentileList = {'10%', '50%', '90%'}

for variable in variableList:
    if variable == 'temp':
        averageList = {'dmax', 'dmean', 'dmin'}
    else:
        averageList = {'dmean'}
    # Separate temperature and precipitation data
    variablefile = mergefile[mergefile['variable'] == variable]

    # Find the appropriate colour mapping scheme
    vmin = variablefile[percentileList].min().min()
    vmax = variablefile[percentileList].max().max()
    if -vmin > vmax:
        vmax = -vmin
    else:
        vmin = -vmax

    fig, ax = plt.subplots(1, figsize=(10, 6))  # Create plot canvas
    ax.axis('off')  # Do not display axis

    # Color bar settings (shrink = size, pad = position)
    sm = plt.cm.ScalarMappable(cmap=GnRd, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm, shrink=0.5)
    cbar.outline.set_linewidth(0.1)
    for timeslice in timesliceList:
        for average in averageList:
            for period in periodList:
                try:
                    for percentile in percentileList:
                        # Filter data under selected parameters
                        trancfile = variablefile.loc[(variablefile.timeslice == timeslice) & (variablefile.average == average) & (variablefile.period == period)]
                        # Check data not empty
                        if len(trancfile) == 0:
                            break

                        # Define Map Title
                        ax.set_title('Projection difference on\n' + periodict[period] + ' ' + avgdict[average] + ' ' + vardict[variable] + '\n over ' + timeslice + ' at ' + percentile + ' probability level')

                        # Plot and save map
                        trancfile.plot(column=percentile, cmap=GnRd, vmin=vmin, vmax=vmax, linewidth=0.2, ax=ax, edgecolor='0.8')
                        fig.savefig(dirname + '/Plots/' + variable + '/' + period + '_' + timeslice + '_' + variable + '_' + average + '_' + percentile + '.png', dpi=300, bbox_inches="tight")  # Save plot
                        print('Success: ' + period + '_' + timeslice + '_' + variable + '_' + average + '_' + percentile + '.png')
                except OSError as e:
                    print('Error: ' + period + '_' + timeslice + '_' + variable + '_' + average + '_' + percentile + '.png')
                    print(e)
    plt.close('all')



