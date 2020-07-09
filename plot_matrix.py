#!/usr/bin/env python3

import numpy as np
import csv
import matplotlib
import matplotlib.pyplot as plt
from statistics import mean
from matplotlib.legend import Legend

dir = 'summary_auto_irrig'

# Read simulation set-up summary to retrieve matrix
with open('%s/matrix_summary.csv' % (dir)) as f:
    next(f)
    reader = csv.reader(f, delimiter=',')
    mat = np.array(list(reader))

_crops = np.unique(mat[:, 1])

crops = {}
for c in _crops:
    crops[c] = (sorted([int(pd) for pd in np.unique(mat[mat[:, 1] == c, 2])]),
                sorted([int(fr) for fr in np.unique(mat[mat[:, 1] == c, 3])]))

summary = {}
with open('locations.txt') as fp:
    for line in fp:
        _location = line.split()[0]

        with open('%s/output_summary_%s.csv' % (dir, _location)) as f:
            next(f)
            reader = csv.reader(f, delimiter=',')
            _mat = np.array(list(reader))

            summary[_location] = (_mat[:, 1],
                                  np.array([int(pd) for pd in _mat[:, 3]]),
                                  np.array([int(fr) for fr in _mat[:, 4]]),
                                  np.array([int(y) for y in _mat[:, 5]]),
                                  np.array([float(yld) for yld in _mat[:, 8]]))


# Yield - planting dates
fig = plt.figure(figsize=(12, 8))
p = 1
for c in crops:
    ax = plt.subplot(2, 4, p)
    pd = crops[c][0]

    for l in summary:
        yields = [mean(summary[l][4][(summary[l][0] == c) & (summary[l][1] == d)]) for d in pd]
        ax.plot([float(d) for d in pd], yields, label=l)

    ax.tick_params(labelsize=11)
    plt.title(c, fontsize=12)

    p += 1

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel("Planting date (DOY)", fontsize=18)
plt.ylabel("Yield (Mg ha$^{-1})$", fontsize=18)

# Yield - fertilization rates
fig = plt.figure(figsize=(12, 8))
p = 1
for c in crops:
    ax = plt.subplot(2, 4, p)
    fr = crops[c][1]

    for l in summary:
        #print(summary[l][2], fr)
        yields = [mean(summary[l][4][(summary[l][0] == c) & (summary[l][2] == r)]) for r in fr]
        for yld in yields:
            if yld > 17.5:
                print(l)
        ax.plot([float(r) for r in fr], yields, label=l)

    ax.tick_params(labelsize=11)
    plt.title(c, fontsize=12)

    p += 1

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False, labelsize=15)
plt.xlabel("Fertilization rate (kg ha$^{-1}$)", fontsize=18)
plt.ylabel("Yield (Mg ha$^{-1})$", fontsize=18)

# Yield - fertilization rates
fig = plt.figure(figsize=(12, 8))
p = 1
for c in crops:
    ax = plt.subplot(2, 4, p)
    years = range(2000, 2018)

    for l in summary:
        yields = [mean(summary[l][4][(summary[l][0] == c) & (summary[l][3] == y)]) for y in years]
        ax.plot(years, yields, label=l)

    ax.tick_params(labelsize=11)
    plt.title(c, fontsize=12)

    p += 1

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False, labelsize=15)
plt.xlabel("Year", fontsize=18)
plt.ylabel("Yield (Mg ha$^{-1})$", fontsize=18)

plt.show()
