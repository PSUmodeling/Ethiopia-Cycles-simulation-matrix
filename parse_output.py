#!/usr/bin/env python3

import csv
import os
import glob
from itertools import *


'''
Load crop matrix
'''
with open('summary/matrix_summary.csv') as f:
    next(f)
    reader = csv.reader(f, delimiter=',')
    mat = list(reader)

with open('locations.txt') as fp:
    for line in fp:
        location = line.split()[0]
        weather_file = line.split()[1]
        soil_file = line.split()[2]

        with open('summary/output_summary_%s.csv' % (location), 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['simulation',
                                'crop',
                                'location',
                                'planting_date',
                                'nitrogen_rate',
                                'year',
                                'total_biomass',
                                'root_biomass',
                                'grain_yield',
                                'forage_yield',
                                'ag_residue',
                                'harvest_index',
                                'potential_tr',
                                'actual_tr',
                                'soil_evap',
                                'irrigation',
                                'total_n',
                                'root_n',
                                'grain_n',
                                'forage_n',
                                'n_stress',
                                'n_in_harvest',
                                'n_in_residue',
                                'n_conc_forage',
                                'n_fixation'
                               ])
            for sim in mat:
                print('%s%s' % (location, sim[0]))
                with open('output/%s/season.dat' % (location + sim[0])) as season_file:
                    csvreader = csv.reader(season_file, delimiter='\t')
                    next(csvreader)
                    next(csvreader)
                    for row in csvreader:
                        csvwriter.writerow([
                                            sim[0].strip(),
                                            row[1].strip(),
                                            location.strip(),
                                            sim[2].strip(),
                                            sim[3].strip(),
                                            row[0][:4].strip(),
                                            row[3].strip(),
                                            row[4].strip(),
                                            row[5].strip(),
                                            row[6].strip(),
                                            row[7].strip(),
                                            row[8].strip(),
                                            row[9].strip(),
                                            row[10].strip(),
                                            row[11].strip(),
                                            row[12].strip(),
                                            row[13].strip(),
                                            row[14].strip(),
                                            row[15].strip(),
                                            row[16].strip(),
                                            row[17].strip(),
                                            row[18].strip(),
                                            row[19].strip(),
                                            row[20].strip(),
                                            row[21].strip()
                                           ])

