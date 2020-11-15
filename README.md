<b>Trajectory Analysis and Classification in Python (Pandas and Scikit Learn) </b>

A university project  for the postgraduate class of Data Mining.

We were given a train_set with geographical points paired with the time interval. Firstly, we cleaned the dataset and then we formed the trajectories (with the corresponding route id). The last step of this part was to filter out some trajectories based on _their total_distance and max distance (between two of their points).

The goal of this project was firstly to compute trajectory similarity between trajectories of test_set_a1/a2.csv and the train_set.csv. 

The algorithms used for that were :
1) <b>Fast Dynamic Time Warping (Fast-DTW)</b>, taken from https://github.com/slaypni/fastdtw
2) <b>Longest Common Subsequence algorithm</b>, which i implemented.

The distance taken into account each time, was the Havershine distance of the points. Files lcss_neighbors.py and fast_dtw_neighbors.py read the corresponding trajectories from test_set_a1/a2.csv and find the 5 most 'similar' trajectories from the cleaned dataset. Finally, they plot them with some specific metrics of similarity.

The second part of the project was to train KNN,Random Forest, and Logistic Regression classifiers and predict the routes of trajectories of the test_set.csv . The first step was to assign each trajectory to a string (composed of cell codes) via a grid representation. In the second step, 10-cross-fold-validation was used to train the classifiers with grid strings of the dataset with accuracy metric . I conducted various experiments, by changing each classifier's parameters. 

Lastly,the classifiers with the best accuracy were bunched together in the Voting Classifier. The final classifier was used to find labels for the trajectories of the test_set.csv .
