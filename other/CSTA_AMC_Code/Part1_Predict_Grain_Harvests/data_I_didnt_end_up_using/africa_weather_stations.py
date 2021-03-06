################################################################
# Finds two closest weather statioins to center of each county
################################################################
from pylab import *
import csv
from math import sqrt
from sys import exit
import pickle
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from mpl_toolkits.basemap import Basemap
import os
from scipy.stats import norm
import matplotlib as mpl
from matplotlib.patches import Polygon
import random

# cd Documents/Science_Fair_2017_Crop_Yields/
wd='/Users/lilllianpetersen/Google Drive/science_fair/'
wddata='/Users/lilllianpetersen/data/'

## Number of Years Wanted ##
years=20

###############################################
# Read in Station Names
###############################################
filename=wddata+'noaa_daily_data/ghcnd-stations.txt'
openStations=open(filename,'r')

cityName={}  #initialize a dictionary
stationLon=np.zeros(shape=(100))
stationLat=np.zeros(shape=(100))

i=-1
j=-1
for line in openStations:
    j+=1
    tmp=line[0:85]
    lat=float(tmp[13:21])
    lon=float(tmp[22:30])
    if 3.4<lat and lat<14.9 and 33.3<lon and lon<47.2:
    #if 0.<lat and lat<18. and 30.<lon and lon<50.:
        i+=1
        station=tmp[0:11]
        cityName[station]=tmp[41:70]
        stationLat[i]=lat
        stationLon[i]=lon

###############################################
# Read in Start and End Date Data
###############################################

# load the pickle files
#countyLat=pickle.load(open('pickle_files/county_lats.p','rb'))
#countyLon=pickle.load(open('pickle_files/county_lons.p','rb'))

#the inventory file to read in
fileOpen=open(wddata+'noaa_daily_data/ghcnd-inventory.txt','r') 

# a file I am going to write with Tmax for cities over however many years
f=open(wd+'written_files/tmax_cities_over_'+str(years)+'_years.txt','w')

# a file I am going to write with precip for cities over however many years
fprecip=open(wd+'written_files/precip_cities_over_'+str(years)+'_years_no.txt','w')

# a file I am going to write with the 2 closest stations to the county centers
fnearestStation=open(wd+'written_files/tmax_nearest_stations.txt','w')

fnearestStation2=open(wd+'written_files/tmax_second_nearest_stations.txt','w')

#fnearestStationsPrecip=open('written_files/precip_nearest_stations.txt','w')


#                      #
# initialize variables #
#                      #
k=0 #a counter of how many times the loop goes through
maxk=571434 # the maximum number of stations
startYear=zeros(shape=(maxk))
endYear=zeros(shape=(maxk))
length=zeros(shape=(maxk))
var=zeros(shape=(maxk))
stationLat=zeros(shape=(maxk))
stationLon=zeros(shape=(maxk))
stationLatTmax=zeros(shape=(50000))
stationLonTmax=zeros(shape=(50000))
kPlot=0
kPrecipPlot=0
stationLatPrecip=zeros(shape=(50000))
stationLonPrecip=zeros(shape=(50000))
longCity=zeros(shape=(maxk),dtype=bool)
stationCode=[]

#                                                                              #
# read in each the lat, lon, station name, startYear, endYear for each station #
#                                                                              #
for line in fileOpen: # loop through every station
    tmp=line[0:45]
    station=tmp[0:11]
    stationLat[k]=tmp[11:20]
    stationLon[k]=tmp[21:30]
    if 3.4<stationLat[k] and stationLat[k]<14.9 and 33.3<stationLon[k] and stationLon[k]<47.2:
        variable=tmp[31:35]
        startYear[k]=float(tmp[36:40])
        endYear[k]=float(tmp[41:45])
        
        stationCode.append(station)
        
        if variable=='TMAX':
            var[k]=0
        elif variable=='TMIN':
            var[k]=1
        else:
            var[k]=-1
        
        
        length[k]=endYear[k]-startYear[k] # find how many years of data the station has
                
        # find the cities that have atleast years worth of data, the var is Tmax, and ends after 2010
        if length[k]>=years and var[k]==0 and endYear[k]>2000: 
            longCity[k]=True
            stationLatTmax[kPlot]=stationLat[k] # put the latitude of the city into an array
            stationLonTmax[kPlot]=stationLon[k] # put the longitude of the city into an array
            kPlot+=1 # a counter of how many cities
            # write the station, lat, lon, var, startYear, endYear, and place where located into a document
            f.write(str(stationCode[k])+','+
                str(stationLat[k])+','+
                str(stationLon[k])+','+
                str(var[k])+','+
                str(startYear[k])+','+
                str(endYear[k])+','+
                cityName[stationCode[k]]+'\n')
            #f.write(tmp+' '+cityName[station]+'\n')
         
        # find the cities that have atleast nyears worth of data, the var is precip, and ends after 2010    
        if length[k]>=years and var[k]==2 and endYear[k]>2000:
            # write the station, lat, lon, var, startYear, endYear, and place where located into a document
            fprecip.write(tmp+' '+cityName[station]+'\n')
            stationLatPrecip[kPrecipPlot]=stationLat[k] # put the latitude of the city into an array
            stationLonPrecip[kPrecipPlot]=stationLon[k] # put the longitude of the city into an array
            kPrecipPlot+=1 # a counter of how many cities
                   

        k+=1 # add one to the counter of how many times the loop has gone through

f.close()
fprecip.close()

#print kPlot # print number of cities written into the Tmax file
#print kPrecipPlot # print number of cities written into the precip file

# initialize variables
nearestStationLat=-9999*ones(shape=(k))
nearestStationLon=-9999*ones(shape=(k))
nearestStationIndex=[-9999]*k

nearestStationLat2=-9999*ones(shape=(k))
nearestStationLon2=-9999*ones(shape=(k))
nearestStationIndex2=[-9999]*k

for c in range(1):
    print c, ' of ',k
    #lat=countyLat[c]
    #lon=countyLon[c]
    lat=8.966736
    lon=38.789822 #Addis Ababa, capital of Ethiopia
    for w in range(maxk):
        if w==0: # only if it is the first time running through
            shortestDist=dist
        if lat==-9999:
            continue
        if length[w]<years or endYear[w]<2000: # dont want weather stations too short
            continue   
        if var[w]!=0: #only want tmax
            continue 
        wsLat=stationLat[w]
        wsLon=stationLon[w]
        
        # find distance from county center to weather station
        dist=abs(sqrt((lon-wsLon)**2+(lat-wsLat)**2))
        
        if dist>3: # only look at the close ones
            continue
        
        if dist<shortestDist: # if its closer than the last closest one
            # make the last closest one the second to closest one
            shortestDist2=shortestDist
            nearestStationLat2[c]=nearestStationLat[c]
            nearestStationLon2[c]=nearestStationLon[c]
            nearestStationIndex2[c]=nearestStationIndex[c]
            
            # make this one the closest one
            shortestDist=dist
            nearestStationLat[c]=wsLat
            nearestStationLon[c]=wsLon  
            nearestStationIndex[c]=w
              
    # write the closest and second closest stations into a csv file      
    fnearestStation.write(str(stationCode[nearestStationIndex[c]])+','+
        '1,'+
        str(nearestStationLat[c])+','+
        str(nearestStationLon[c])+','+
        str(var[nearestStationIndex[c]])+','+
        str(startYear[nearestStationIndex[c]])+','+
        str(endYear[nearestStationIndex[c]])+','+
        cityName[stationCode[nearestStationIndex[c]]]+','+
        str(stationCode[nearestStationIndex2[c]])+','+
        '2,'+
        str(nearestStationLat2[c])+','+
        str(nearestStationLon2[c])+','+
        str(var[nearestStationIndex2[c]])+','+
        str(startYear[nearestStationIndex2[c]])+','+
        str(endYear[nearestStationIndex2[c]])+','+
        cityName[stationCode[nearestStationIndex2[c]]] +'\n')

fnearestStation.close()        
  
#plot the closest stations
figure(1,figsize=(20,20))
#m = Basemap(llcrnrlat=24,urcrnrlat=50,\
#            llcrnrlon=-125.5,urcrnrlon=-66.5,lat_ts=50,resolution='i',area_thresh=10000)
m = Basemap(llcrnrlat=-2,urcrnrlat=19,\
            llcrnrlon=30,urcrnrlon=50,lat_ts=50,resolution='i',area_thresh=10000)
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.drawcounties()
#x,y=m(nearestStationLon,nearestStationLat)
x,y=m(stationLon,stationLat)
plotHandle = m.scatter(x,y,c='r',zorder=10)    
savefig('figures/nearestWeatherStation')
show()
