#!/usr/bin/env python3

import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.legend import Legend

matplotlib.rcParams.update({'font.size': 14})
fig = plt.figure(figsize=(12, 8))
ax = plt.subplot2grid((1, 5), (0, 0), colspan=3)

fig1 = plt.figure(figsize=(12, 8))
ax1 = plt.subplot2grid((1, 5), (0, 0), colspan=3)
'''
Create control files and run simulation matrix
'''
with open('locations.txt') as fp:
    for line in fp:
        location = line.split()[0]
        weather_file = line.split()[1]
        _doy = []
        _tmp = []
        doy_tmp = []
        doy_tmp_ma = []
        _prcp = []
        doy_prcp = []
        doy_prcp_ma = []
        with open('input/%s' % (weather_file)) as weather_fp:
            next(weather_fp)
            next(weather_fp)
            next(weather_fp)
            next(weather_fp)
            for weather in weather_fp:
                _doy.append(int(weather.split()[1]))
                _tmp.append(0.5 * float(weather.split()[3]) +
                            0.5 * float(weather.split()[4]))
                _prcp.append(float(weather.split()[2]))

            _tmp = np.array(_tmp)
            _prcp = np.array(_prcp)
            _doy = np.array(_doy)

            for d in range(365):
                doy_tmp.append(np.average(_tmp[_doy == d + 1]))
                doy_prcp.append(np.average(_prcp[_doy == d + 1]))

            for d in range(365):
                if d - 7 < 0:
                    start = 0
                else:
                    start = d - 7
                if d + 8 > 365:
                    end = 365
                else:
                    end = d + 8
                doy_tmp_ma.append(np.average(doy_tmp[start:end]))
                doy_prcp_ma.append(np.average(doy_prcp[start:end]))


            ax.plot(range(1, 366), doy_tmp_ma, label=location)
            ax1.plot(range(1, 366), doy_prcp_ma, label=location)

ax.set_xlim((1, 366))
ax.set_xlabel('Day of year', fontsize=16)
ax.set_ylabel('Temperature ($^\circ$C)', fontsize=18)
ax.legend(loc='center left', ncol=3, fontsize=13, bbox_to_anchor=(1.05, 0.5)) #fontsize=16,
            #handletextpad=0)
ax1.set_xlim((1, 366))
ax1.set_xlabel('Day of year', fontsize=16)
ax1.set_ylabel('Precipitation (mm)', fontsize=18)
ax1.legend(loc='center left', ncol=3, fontsize=13, bbox_to_anchor=(1.05, 0.5)) #fontsize=16,
            #handletextpad=0)

plt.show()