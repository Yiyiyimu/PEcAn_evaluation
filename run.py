import ee
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import rpy2.robjects as robjects
from datetime import datetime, timedelta
from xml.etree.ElementTree import parse

def getLVI():
    robjects.r['load']("./PEcAn_99000000001/ensemble.ts.99000000001.LAI.2002.2005.RData")

    arr = np.array(robjects.r['ensemble.ts'][0]).flatten()

    def valid_time(x):
        init_time = datetime(int(x['year']), 1, 1)
        offset = timedelta(days=int(x['day']), hours=x['time'])
        return init_time + offset

    df = pd.read_csv('./PEcAn_99000000001/out/99000000001/sipnet.out', skiprows=1, sep = '\s+')
    df['date'] = df.apply(valid_time, axis=1)
    df = pd.DataFrame(list(zip(df['date'].values, arr)), columns=['date', 'val'])
    return df

def getNDVI(doc, cloud_threhold):
    ####SET_PROXY, to connect GEE from China####
    os.environ['HTTP_PROXY'] = 'http://127.0.0.1:1080'
    os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:1080'

    ee.Initialize()
    #not use Landsat 8 for older time needed
    #L8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_RT_TOA")
    L7 = ee.ImageCollection("LANDSAT/LE07/C01/T1_RT_TOA")

    if(doc):
        #extract information from xml file of PEcAn output
        lat = doc.find('run/site/lat').text
        lon = doc.find('run/site/lon').text
        start = doc.find('run/site/met.start').text.split(' ')[0]
        end = doc.find('run/site/met.end').text.split(' ')[0]
        Point = ee.Geometry.Point([float(lon), float(lat)])
        myCollection = L7.filterBounds(Point) \
        .filterMetadata('CLOUD_COVER','less_than',cloud_threhold) \
        .filterDate(start, end)
    else:
        Point = ee.Geometry.Point([-105.70, 40.0329])#original longitute is -105.546
        myCollection = L7.filterBounds(Point) \
        .filterMetadata('CLOUD_COVER','less_than',cloud_threhold) \
        .filterDate('2002-01-01', '2005-12-31')

    def reduceNDVI(image):
        selected = image.select('B3','B4')
        NDVI = selected.expression('(b(1)-b(0))/(b(1)+b(0))').select(['B4'], ['NDVI'])
        #extract mean value of the whole image
        meanDict = NDVI.reduceRegion(reducer = ee.Reducer.mean(), scale = 90)
        return ee.Image(image.setMulti(meanDict))

    reduced = myCollection.map(reduceNDVI)

    NDVIList = reduced.aggregate_array('NDVI').getInfo()
    dateList = reduced.aggregate_array('system:index').getInfo()
    dateList = [d.split('_')[-1] for d in dateList]
    dateList = [datetime(int(d[0:4]), int(d[4:6]), int(d[6:])) for d in dateList]

    df = pd.DataFrame(list(zip(dateList, NDVIList)), columns=['date','val'])
    df.sort_values(by=['date'], inplace=True)

    return df

def makeplot(filename, df_LVI, df_NDVI):
    fig, ax1 = plt.subplots()
    ax1.xaxis.set_major_locator(mdates.YearLocator(1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.set_title(filename)

    color = 'tab:red'
    ax1.set_xlabel('YEAR')
    ax1.set_ylabel('LVI', color=color)
    ax1.set_ylim(-0.1, 1.1)
    ax1.plot(df_LVI['date'], df_LVI['val'], color=color)
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


if __name__ == '__main__':
    cloud_threhold = 50

    try:
        doc = parse("./PEcAn_99000000001/pecan.CONFIGS.xml")
        df_NDVI = getNDVI(doc, cloud_threhold)
        filename = doc.find('run/site/name').text
    #if failed to find certain xml or try different coordinates
    except:
        df_NDVI = getNDVI(None,cloud_threhold)
        filename = ""

    df_LVI = getLVI()
    makeplot(filename, df_LVI, df_NDVI)
