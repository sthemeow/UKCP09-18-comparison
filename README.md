# UKCP09/UKCP18 Comparison
This repository is intended to compare the prediction results between UKCP18 and UKCP09 under the same baseline.

<p align="center"><img src="/samples/difference-plot-sample.png" height="300">     <img src="/samples/threshold-plot-sample.png" height="300"></p>

## Required Python Packages
* netCDF4
* pandas
* geopandas
* matplotlib
## How to use the codes
#### Retrive UKCP09 and UKCP18 raw data
1. Register Centre for Environmental Data Analysis (CEDA) account here *https://services.ceda.ac.uk/cedasite/register/info*
1. Download UKCP09 data from *ftp://ftp.ceda.ac.uk/badc/UKCP09* to local directory *~/UKCP09data*
1. Download UKCP18 data from *ftp://ftp.ceda.ac.uk/badc/UKCP18* to local directory *~/UKCP18data* 
#### Read and reformat raw data
1. Run **DeleteFiles.py** to delete irrelevant UKCP09 data files.
1. Run **Decoder09.py** to convert netCDF4 UKCP09 file to multiple csv files.
1. Run **FileMover18.py** to move UKCP18 data files to corresponding folders.
1. Run **Decoder18.py** to convert netCDF4 UKCP18 file to multiple csv files.
#### Compare UKCP18/UKCP09 and visualise data
1. Run **Data_Collator.py** to combine all data into a summary csv file. 
1. Run **Mapdrawer.py** to plot coloured maps.
#### Threshold analysis
1. Tweak and Run **Threshold_datacollator.py** to produce a threshold summary csv file for your purpose.
1. Run **Threshold_mapdrawer.py** to plot coloured maps under the following colour scheme.
<p align="center"><img src="/samples/colour-scheme.png" width="306"></p>

## Notes
1. Sample output may be found in *~/Samples*.
1. The default admin region names are slightly different in UKCP09, in UKCP18 and in shapefile. If anyone is to replicate the work, make sure the names are identical to the sample files.
1. Mapdrawer.py is a single-threaded program. It would take a long time (hours) to plot all maps. You may divide workloads by running multiple instances (easy work-around) or write a multi-threaded program to reduce the rendering time.
1. The colour code for current colour scheme:
   1. Red: 248,105,107 (RGB); F8696B (Hex)
   1. Green: 99,190,123 (RGB); 63BE7B (Hex)
1.	The only overlapping emission scenario is SRES A1B (Medium case in UKCP09). Use this setting for comparison.
