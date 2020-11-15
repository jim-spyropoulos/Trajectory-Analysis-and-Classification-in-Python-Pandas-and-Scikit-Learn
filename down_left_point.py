import pandas as pd

df = pd.read_pickle('final_cleaned.df')
df_2 = pd.DataFrame(columns=['lon', 'the', 'timestamp_longitude_latitude'])
df_3 = pd.DataFrame(columns=['lat', 'the', 'timestamp_longitude_latitude'])


the_lst_lon = []
the_lst_lat = []

for index, row in df.iterrows():
    lst = df['timestamp_longitude_latitude'].iloc[index]
    min_lon = lst[0][1]
    min_lat = lst[0][2]
    the_lon = str(lst[0][1]) + ',' + str(lst[0][2])
    the_lat = str(lst[0][1]) + ',' + str(lst[0][2])
    for i in range(len(lst)):
        temp_lon = lst[i][1]
        temp_lat = lst[i][2]
        if temp_lon < min_lon:
            min_lon = temp_lon
            the_lon = str(lst[i][1]) + ',' + str(lst[i][2])  # the leftest diadromi point
            the_lst_lon = lst
        if temp_lat < min_lat:
            min_lat = temp_lat
            the_lat = str(lst[i][1]) + ',' + str(lst[i][2])
            the_lst_lat = lst

    print("found min lon and lat of traj")
    df_2 = df_2.append({'lon': str(min_lon)}, ignore_index=True)
    df_3 = df_3.append({'lat': str(min_lat)}, ignore_index=True)
print("ready to sort")
df_2 = df_2.sort_values(by=['lon'], ascending=False)
df_3 = df_3.sort_values(by=['lat'])

downleft_lon = df_2['lon'].iloc[0]
downleft_lat = df_3['lat'].iloc[0]

print(downleft_lon)
print(downleft_lat)
