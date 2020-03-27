# -*- coding:utf-8 -*-
import ee
import os
import numpy as np
from datetime import datetime
import pandas as pd
from xml.etree.ElementTree import parse

os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1080'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1080'

ee.Initialize()

doc = parse("./PEcAn_99000000001/pecan.CONFIGS.xml")

#L8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA")

Point = ee.Geometry.Point([-105.546, 40.0329])
L7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_RT_TOA")

myCollection = L7.filterBounds(Point) \
.filterMetadata('CLOUD_COVER','less_than',5) \
.filterDate('2002-01-01', '2005-12-31')

def reduceNDVI(image):
    selected = image.select('B3','B4')
    NDVI = selected.expression('(b(1)-b(0))/(b(1)+b(0))').select(['B4'], ['NDVI']);
    meanDict = NDVI.reduceRegion(reducer = ee.Reducer.mean(), scale = 90)
    return ee.Image(image.setMulti(meanDict))

reduced = myCollection.map(reduceNDVI)

NDVIList = reduced.aggregate_array('NDVI').getInfo()
dateList = reduced.aggregate_array('system:index').getInfo()
dateList = [d.split('_')[-1] for d in dateList]
dateList = [datetime(int(d[0:4]), int(d[4:6]), int(d[6:])) for d in dateList]

df_NDVI = pd.DataFrame(list(zip(dateList, NDVIList)), columns=['date','val'])
df_NDVI.sort_values(by=['date'], inplace=True)


fig, ax1 = plt.subplots()
ax1.xaxis.set_major_locator(mdates.YearLocator(1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax1.set_title(filename)

color = 'tab:red'
ax1.set_xlabel('YEAR')
ax1.set_ylabel('LVI', color=color)
ax1.set_ylim(-0.1, 1.1)
ax1.plot(df['date'], arr, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
ax2.xaxis.set_major_locator(mdates.YearLocator(1))
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

color = 'tab:blue'
ax2.set_ylabel('NDVI', color=color)
ax2.set_ylim(-0.05, 0.55)
ax2.plot(df_NDVI['date'], df_NDVI['val'], color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.savefig(filename.split('/')[0])