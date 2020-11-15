import os
import random

import pandas as pd

from auxiliaryfunctions import *

df = pd.read_csv('train_set.csv')
df = df[pd.notnull(df['journeyPatternId'])]  # deletes null values from dataset

pd.set_option('display.max_rows', 1000000000)

df['route'] = df['vehicleID'].map(str) + df['timestamp'].map(str)
df = df.sort_values(by=['route'])

df = df.reset_index(drop=True)  # re index elements of df

print("ready for cleaning.(completed sorting and creation of route)")

df['timestamp_longitude_latitude'] = df[['timestamp', 'longitude', 'latitude']].values.tolist()

df_2 = pd.DataFrame(columns=['TripId', 'JourneyPatternId', 'timestamp_longitude_latitude'])

TripId_LOCS = []

count = 0

for index, row in df.iterrows():

    TripId_LOCS.append(df['timestamp_longitude_latitude'][index])

    if (index + 1) == df.shape[0]:  # 1484821
        break

    if df['journeyPatternId'][index] != df['journeyPatternId'][index + 1]:
        a = TripId_LOCS
        df_2 = df_2.append(
            {'TripId': count, 'JourneyPatternId': df['journeyPatternId'][index], 'timestamp_longitude_latitude': a},
            ignore_index=True)
        count = count + 1
        TripId_LOCS = []  # make the list empty
    # print count

df_2.to_pickle('TripId.df')

# Data cleaning segment


df3 = pd.read_pickle('./TripId.df')
init_counter = len(df3.index)
print('initially we had ' + str(init_counter) + ' trajectories')
df_final = pd.DataFrame(
    columns=['TripId', 'JourneyPatternId', 'timestamp_longitude_latitude', 'total_distance', 'max_distance'])

totaldrop = 0
maxdrop = 0
for index, row in df3.iterrows():
    td = compute_distances(df3['timestamp_longitude_latitude'][index])  # for each traj compute whole havershine in kms.
    if (td[0] <= 2):  # total distance smaller than 2kms
        totaldrop = totaldrop + 1
        continue
    if (td[1] >= 2):  # max distance bigger than 2kms
        maxdrop = maxdrop + 1
        continue
    else:  # write info in new_final_cleaned dataframe
        df_final = df_final.append({'TripId': df3['TripId'][index], 'JourneyPatternId': df3['JourneyPatternId'][index],
                                    'timestamp_longitude_latitude': df3['timestamp_longitude_latitude'][index],
                                    'total_distance': td[0], 'max_distance': td[1]}, ignore_index=True)

final_counter = len(df_final.index)
print('we dropped ' + str(totaldrop) + ' trajectories from totaldistance.')
print('we dropped ' + str(maxdrop) + ' trajectories from maxdistance.')
print('finally,we have ' + str(final_counter) + ' trajectories')
df_final.to_csv('final_cleaned.csv')
df_final.to_pickle('final_cleaned.df')

# Random Plotting Segment

df_gm = pd.read_pickle('./final_cleaned.df')

first_traj = df_gm['timestamp_longitude_latitude'].iloc[0]

# randomly choose 5 trajectories
r5 = random.sample(range(0, len(df_gm)), 5)
i = 1
# create output directory
os.mkdir("Random_Images")
for elem in r5:
    print
    "i chose traj : " + df_gm["JourneyPatternId"].iloc[elem]
    traj = df_gm['timestamp_longitude_latitude'].iloc[elem]
    plot_traj(traj, "./Random_Images/RandomImage" + str(i))
    i = i + 1
