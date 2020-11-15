import gmplot
from math import sin, cos, sqrt, atan2, radians


def haversine_np(pointa, pointb):
    # approximate radius of earth in km

    R = 6373.0

    lat1 = radians(pointa[2])
    lon1 = radians(pointa[1])
    lat2 = radians(pointb[2])
    lon2 = radians(pointb[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    # print("Result:", distance)
    return distance


def compute_distances(trajectory):
    maxel = 0.0
    total_dst = 0.0

    for i in range(0, len(trajectory) - 1):
        dist = 0.0
        dist = haversine_np(trajectory[i], trajectory[i + 1])
        if dist > maxel:
            maxel = dist
        total_dst += dist
    return [total_dst, maxel]


def plot_traj(df_traj, plotname):
    longtitudes = []
    latitudes = []
    for elem2 in df_traj:
        longtitudes.append(elem2[1])
        latitudes.append(elem2[2])
    # now let's plot:
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longtitudes[0], len(df_traj))
    gmap.plot(latitudes, longtitudes, 'cornflowerblue', edge_width=10)
    gmap.draw(plotname + ".html")


def plot_traj_red(com_points, df_traj, plotname):
    longtitudes = []
    latitudes = []
    for elem2 in df_traj:
        longtitudes.append(elem2[1])
        latitudes.append(elem2[2])
    # now let's plot:
    gmap = gmplot.GoogleMapPlotter(latitudes[0], longtitudes[0], 12)
    gmap.plot(latitudes, longtitudes, 'cornflowerblue', edge_width=10)


    longtitudes = []
    latitudes = []
    for elem2 in com_points:
        longtitudes.append(elem2[1])
        latitudes.append(elem2[2])
    # now let's plot:
    gmap.plot(latitudes, longtitudes, 'red', edge_width=10)

    gmap.draw(plotname + ".html")


def print_results(df_traj, distances, index, name):
    target_traj_coordinates = df_traj['timestamp_longitude_latitude'].iloc[index]  # get target trajectory
    target_journeypattid = df_traj['JourneyPatternId'].iloc[index]  # get target journey pattern id

    print
    "Traj: " + str(target_journeypattid) + "Distance is %.4f km's." % distances[index]
    plot_traj(target_traj_coordinates, name)


def lcss_trigger(traj, df, trigger, index):
    # if trigger==1 then it returns the # of matching points
    if (trigger == 1):
        matching_points = []
        count = 0;
        for elem in df['timestamp_longitude_latitude']:
            n0 = len(traj)
            n1 = len(elem)
            # An (m+1) times (n+1) matrix
            C = [[0] * (n1 + 1) for _ in range(n0 + 1)]
            for i in range(1, n0 + 1):
                for j in range(1, n1 + 1):
                    if haversine_np(traj[i - 1], elem[j - 1]) <= 0.2:
                        C[i][j] = C[i - 1][j - 1] + 1
                    else:
                        C[i][j] = max(C[i][j - 1], C[i - 1][j])
            matching_points.append(C[n0][n1])
            count = count + 1
    elif (trigger == 2):  # else it returns the list of common points of traj with df[index] traj
        common_points = []
        elem = df['timestamp_longitude_latitude'].iloc[index]
        n0 = len(traj)
    n1 = len(elem)
    # An (m+1) times (n+1) matrix
    C = [[0] * (n1 + 1) for _ in range(n0 + 1)]
    for i in range(1, n0 + 1):
        for j in range(1, n1 + 1):
            if haversine_np(traj[i - 1], elem[j - 1]) <= 0.2:
                C[i][j] = C[i - 1][j - 1] + 1
                if (elem[j - 1] not in common_points):
                    common_points.append(elem[j - 1])
            else:
                C[i][j] = max(C[i][j - 1], C[i - 1][j])
    if (trigger == 1):
        return matching_points
    else:
        return common_points
