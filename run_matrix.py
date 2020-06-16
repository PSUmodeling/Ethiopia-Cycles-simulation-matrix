#!/usr/bin/env python3

import os

'''
Matrix configuration
'''
crops = ('Maize', 'Sorghum', 'SpringBarley', 'Teff')

# Configuration with planting dates, fertilization rates, and baseline operation
configs = {}
configs['Maize'] = ((121, 128, 135, 142, 149, 156, 163, 170, 177, 184, 191),
                    (0, 25, 50, 100, 200, 400), 'PD1FR3')
configs['Sorghum'] = ((121, 128, 135, 142, 149, 156, 163, 170, 177, 184, 191),
                      (0, 25, 50, 100, 200, 400), 'PD1FR3')
configs['SpringBarley'] = ((135, 142, 149, 156, 163, 170, 177, 184, 191),
                     (0, 25, 50, 100, 200), 'PD1FR3')
configs['Teff'] = ((182, 189, 196, 203, 210, 217, 224, 231),
                   (0, 30, 60), 'PD1FR2')

start_year = '2000'
end_year = '2017'
crop_file = 'GenericCrops.crop'

def WriteCtrl(simulation, base, soil_file, weather_file):

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


def WriteMulti(location, kcrop, config, start_year, end_year, crop_file,
               soil_file, weather_file):

    simulation = location + 'CROP' + str(kcrop + 1)

    file_name = 'input/' + simulation + '.multi'

    num_pd = len(config[0])
    num_fr = len(config[1])

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


'''
Create operation files by replacing variables in a template operation file
'''
num_crops = len(crops)
for kcrop in range(num_crops):
    for kpd in range(len(configs[crops[kcrop]][0])):
        pd = configs[crops[kcrop]][0][kpd]

        for kfr in range(len(configs[crops[kcrop]][1])):
            fr = configs[crops[kcrop]][1][kfr]

            filen = 'input/CROP%dPD%dFR%d.operation' % (kcrop + 1, kpd + 1,
                                                        kfr + 1)
            replacements = {'$CP':crops[kcrop], '$PD':str(pd), '$FR':str(fr),
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

        for kcrop in range(num_crops):
            simulation = '%sCROP%d' % (location, kcrop + 1)
            base = 'CROP%d%s' % (kcrop + 1, configs[crops[kcrop]][2])

            WriteCtrl(simulation, base, soil_file, weather_file)
            WriteMulti(location, kcrop, configs[crops[kcrop]], start_year,
                       end_year, crop_file, soil_file, weather_file)

            # Run baseline simulation in baseline model with spin-up
            print('Run baseline simulation in spin-up mode and generate re-initialization file')

            cmd = './Cycles -bs -l 1 ' + simulation
            os.system(cmd)

            #Copy generated re-initialization file into input directory
            cmd = 'mv output/%s/reinit.dat input/%s.reinit' % (simulation,
                                                               simulation)
            os.system(cmd)

            # Run batch simulation with re-initialization
            print('Run batch simulations using re-initialization')
            cmd = './Cycles -b -m ' + simulation + '.multi'
            os.system(cmd)
