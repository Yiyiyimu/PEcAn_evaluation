import rpy2.robjects as robjects
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta

robjects.r['load']("./PEcAn_99000000001/ensemble.ts.99000000001.LAI.2002.2005.RData")

arr = np.array(robjects.r['ensemble.ts'][0]).flatten()

plt.plot(arr)

df = pd.read_table('./PEcAn_99000000001/out/99000000001/sipnet.out', skiprows=1, sep = '\s+')
df['date'] = df.apply(valid_time, axis=1)

def valid_time(x):
    init_time = datetime(int(x['year']), 1, 1)
    offset = timedelta(days=int(x['day']), hours=x['time'])
    return init_time + offset

fig, ax = plt.subplots()
ax.xaxis.set_tick_params(reset=True)
ax.xaxis.set_major_locator(mdates.YearLocator(1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.plot(df['date'], arr)