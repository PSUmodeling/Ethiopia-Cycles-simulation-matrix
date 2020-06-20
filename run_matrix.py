#!/usr/bin/env python3

import os
import csv
from itertools import product
from pathlib import Path
from crop_matrix import crop_matrix

def crop_matrix():
    '''
    Matrix configuration
    '''
    crops = {}
    crops['Teff'] = (
        (182, 189, 196, 203, 210, 217, 224, 231),
        (0, 30, 60),
        'PD1FR2')
    crops['SpringBarley'] = (
        (135, 142, 149, 156, 163, 170, 177, 184, 191),
        (0, 25, 50, 100, 200),
        'PD1FR3')
    crops['SpringWheat'] = (
        (135, 142, 149, 156, 163, 170, 177, 184, 191),
        (0, 25, 50, 100, 200),
        'PD1FR3')
    crops['CornRM.110'] = (
        (121, 128, 135, 142, 149, 156, 163, 170, 177, 184, 191),
        (0, 25, 50, 100, 200, 400),
        'PD1FR3')
    crops['SorghumLS'] = (
        (121, 128, 135, 142, 149, 156, 163, 170, 177, 184, 191),
        (0, 25, 50, 100, 200, 400),
        'PD1FR3')
    crops['Millet'] = (
        (182, 189, 196, 203, 210, 217, 224, 231),
        (0, 25, 50, 100, 200, 400),
        'PD1FR3')
    crops['Chickpea'] = (
        (182, 189, 196, 203, 210, 217, 224, 231),
        (0,),
        'PD1FR1')
    crops['SpringLentils'] = (
        (182, 189, 196, 203, 210, 217, 224, 231),
        (0,),
        'PD1FR1')

    return crops


def WriteCtrl(simulation, base,
              start_year, end_year,
              crop_file, soil_file, weather_file):

    file_name = 'input/' + simulation + '.ctrl'
    with open(file_name, 'w') as fp:
        fp.write('SIMULATION_START_YEAR   %s\n' % (start_year))
        fp.write('SIMULATION_END_YEAR     %s\n' % (end_year))
        fp.write('ROTATION_SIZE           1\n\n')
        fp.write('## SIMULATION OPTIONS ##\n')
        fp.write('USE_REINITIALIZATION    0\n')
        fp.write('ADJUSTED_YIELDS         0\n')
        fp.write('HOURLY_INFILTRATION     1\n')
        fp.write('AUTOMATIC_NITROGEN      0\n')
        fp.write('AUTOMATIC_PHOSPHORUS    0\n')
        fp.write('AUTOMATIC_SULFUR        0\n')
        fp.write('DAILY_WEATHER_OUT       0\n')
        fp.write('DAILY_CROP_OUT          0\n')
        fp.write('DAILY_RESIDUE_OUT       0\n')
        fp.write('DAILY_WATER_OUT         1\n')
        fp.write('DAILY_NITROGEN_OUT      0\n')
        fp.write('DAILY_SOIL_CARBON_OUT   0\n')
        fp.write('DAILY_SOIL_LYR_CN_OUT   0\n')
        fp.write('ANNUAL_SOIL_OUT         0\n')
        fp.write('ANNUAL_PROFILE_OUT      0\n')
        fp.write('ANNUAL_NFLUX_OUT        0\n\n')
        fp.write('## OTHER INPUT FILES ##\n')
        fp.write('CROP_FILE               %s\n' % (crop_file))
        fp.write('OPERATION_FILE          %s.operation\n' % (base))
        fp.write('SOIL_FILE               %s\n' % (soil_file))
        fp.write('WEATHER_FILE            %s\n' % (weather_file))
        fp.write('REINIT_FILE             N/A\n')


def WriteMulti(location, kcrop, crop, start_year, end_year, crop_file,
               soil_file, weather_file):

    simulation = location + 'CROP' + str(kcrop + 1)
    file_name = 'input/' + simulation + '.multi'

    num_pd = len(crop[0])
    num_fr = len(crop[1])

    with open(file_name, 'w') as fp:
        fp.write('%-20s' % ('SIM_CODE'))
        fp.write('%-16s' % ('ROTATION_YEARS'))
        fp.write('%-12s' % ('START_YEAR'))
        fp.write('%-12s' % ('END_YEAR'))
        fp.write('%-12s' % ('USE_REINIT'))
        fp.write('%-20s' % ('CROP_FILE'))
        fp.write('%-24s' % ('OPERATION_FILE'))
        fp.write('%-40s' % ('SOIL_FILE'))
        fp.write('%-28s' % ('WEATHER_FILE'))
        fp.write('%-20s' % ('REINIT_FILE'))
        fp.write('%-20s' % ('HOURLY_INFILTRATION'))
        fp.write('%-20s\n' % ('AUTOMATIC_NITROGEN'))

        for kpd in range(num_pd):
            for kfr in range(num_fr):
                fp.write('%-20s' % ('%sPD%dFR%d' % (simulation, kpd + 1,
                                                    kfr + 1)))
                fp.write('%-16s' % ('1'))
                fp.write('%-12s' % (start_year))
                fp.write('%-12s' % (end_year))
                fp.write('%-12s' % ('1'))
                fp.write('%-20s' % (crop_file))
                fp.write('%-24s' % ('CROP%dPD%dFR%d.operation' % (kcrop + 1,
                                                                  kpd + 1,
                                                                  kfr + 1)))
                fp.write('%-40s' % (soil_file))
                fp.write('%-28s' % (weather_file))
                fp.write('%-20s' % (simulation + '.reinit'))
                fp.write('%-20s' % ('1'))
                fp.write('%-20s\n' % ('0'))


def main():

    '''
    Set up simulation parameters
    '''
    start_year = '2000'
    end_year = '2017'
    crop_file = 'Ethiopia.crop'

    '''
    Load crop matrix
    '''
    crops = crop_matrix()

    Path('summary').mkdir(exist_ok=True)

    with open('summary/matrix_summary.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['simulation', 'crop', 'planting_date',
                            'nitrogen_rate'])
        '''
        Create operation files by replacing variables in a template operation
        file
        '''
        num_crops = len(crops)
        for c, kcrop in zip(crops, range(num_crops)):
            num_pd = len(crops[c][0])
            num_fr = len(crops[c][1])

            mat_ind = list(product([kcrop + 1],
                                list(range(1, num_pd + 1)),
                                list(range(1, num_fr + 1))))

            mat = list(product([c], crops[c][0], crops[c][1]))

            for ind, config in zip(mat_ind, mat):
                simulation = 'CROP%dPD%dFR%d' % (ind[0], ind[1], ind[2])
                pd = config[1]
                fr = config[2]

                # Write to matrix summary
                csvwriter.writerow([simulation, config[0], pd, fr])

                # Write operation file
                filen = 'input/%s.operation' % (simulation)
                replacements = {'$CP':config[0], '$PD':str(pd), '$FR':str(fr),
                                '$FD':str(pd - 10), '$TD':str(pd + 20)}

                with open('base.operation') as infile, open(filen, 'w') as outfile:
                    for line in infile:
                        for src, target in replacements.items():
                            line = line.replace(src, target)
                        outfile.write(line)

        '''
        Create control files and run simulation matrix
        '''
        with open('locations.txt') as fp:
            for line in fp:
                location = line.split()[0]
                weather_file = line.split()[1]
                soil_file = line.split()[2]

                for c, kcrop in zip(crops, range(num_crops)):
                    simulation = '%sCROP%d' % (location, kcrop + 1)
                    base = 'CROP%d%s' % (kcrop + 1, crops[c][2])

                    # Write control files for the baseline simulation
                    WriteCtrl(simulation, base,
                            start_year, end_year,
                            crop_file, soil_file, weather_file)

                    # Write multi-mode files for matrix
                    WriteMulti(location, kcrop, crops[c],
                            start_year, end_year,
                            crop_file, soil_file, weather_file)

                    # Run baseline simulation in baseline model with spin-up
                    print('Run baseline simulation in spin-up mode and '
                          'generate re-initialization file')
                    os.system('./Cycles -bs -l 1 ' + simulation)

                    #Copy generated re-initialization file into input directory
                    os.system('mv output/%s/reinit.dat input/%s.reinit'
                              % (simulation, simulation))

                    # Run batch simulation with re-initialization
                    print('Run batch simulations using re-initialization')
                    os.system('./Cycles -b -m ' + simulation + '.multi')


if __name__ == '__main__':
    main()
