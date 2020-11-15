import csv
import os
import re

import numpy as np
import pandas as pd
import time

from auxiliaryfunctions import *

df = pd.read_pickle('./final_cleaned.df')

with open('test_set_a2.csv', 'r') as f:
    reader = csv.reader(f)
    data = (list(rec) for rec in csv.reader(f, delimiter=','))
    i = 0
    count = 0
    trajectories_read = []  # list with all trajectories read
    for row in data:
        if (i != 0):
            tmp_list = []  # to read triples
            trajectory = []  # here will be the final trajectory
            j = 0
            while (j != len(row)):
                tmp_list = [float(re.sub('[[]', '', row[j])), float(row[j + 1]), float(re.sub('[]]', '', row[j + 2]))]
                j = j + 3
                trajectory.append(tmp_list)
                tmp_list = []
            trajectories_read.append(trajectory)
        i = i + 1

print("Dataset read successfully.")

os.mkdir("LCSSresults")
k = 0

for traj in trajectories_read:
    start_time = time.time()
    k = k + 1
    matching_points = lcss_trigger(traj, df, 1, 0)
    distancesnp = np.array(matching_points)
    sorted_ind = np.argsort(-distancesnp)
    m = 1
    for elem in sorted_ind[:5]:  # for each of the trajectories with the most matching points do
        print("Nearest trajectory " + str(df['JourneyPatternId'].iloc[elem]) + " Matching points : %d." % distancesnp[
            elem])
        # we find again which are the common points for the top 5 traj neighbors, in order to be printed red
        common_points = lcss_trigger(traj, df, 2, elem)

        plot_traj_red(common_points, df['timestamp_longitude_latitude'].iloc[elem],
                      "./LCSSresults/trajectory" + str(k) + "matchingpointsneighb: " + str(m))
        m = m + 1

    end_time = time.time()
    print("Took %.3f mins for traj %d to finish" % ((float)((end_time - start_time) / 60), k))
