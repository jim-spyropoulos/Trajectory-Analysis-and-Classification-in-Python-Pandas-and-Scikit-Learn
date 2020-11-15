import pandas as pd

from auxiliaryfunctions import *

df = pd.read_pickle('final_cleaned.df')
df_final = pd.DataFrame(columns=['TripId', 'Grids'])

cell_size = 0.2  ########################## CELL SIZE ################
zero_point = [0, -6.61505, 53.07045]  ################ zero point

for index, row in df.iterrows():
    grid = ''
    trajectory = df['timestamp_longitude_latitude'][index]

    last = ' '  # value that stores last element on the list
    for i in range(0, len(trajectory)):

        on_longitute_axis = []
        on_latitute_axis = []

        on_longitute_axis.append(zero_point[0])
        on_longitute_axis.append(trajectory[i][1])
        on_longitute_axis.append(zero_point[2])
        dist_of_longitute_axis = haversine_np(on_longitute_axis, zero_point)

        grid_lon = int(dist_of_longitute_axis // cell_size)

        on_latitute_axis.append(zero_point[0])
        on_latitute_axis.append(zero_point[1])
        on_latitute_axis.append(trajectory[i][2])
        dist_of_latitute_axis = haversine_np(on_latitute_axis, zero_point)

        grid_lat = int(dist_of_latitute_axis // cell_size)

        current_cell = str(grid_lat) + ',' + str(grid_lon)

        if current_cell == last:
            continue

        grid = grid + 'C' + current_cell + ';'  ######################## grid formation. Every time it stores grid value of a point

        last = current_cell

    df_final = df_final.append({'TripId': df['TripId'][index], 'Grids': grid}, ignore_index=True)

df_final.to_csv('grids.csv')
