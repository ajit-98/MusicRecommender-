# MusicRecommender-
A simple CNN based music recommendation system built on the million song dataset!
To use the recommender system
1. Clone this repository
2. Download the files 'Metadata.zip' and 'MSD Data.zip' from here <INSERT LINK>
3. Extract zip files to the directory of the cloned repo
4. Install Anaconda and all the dependencies

To find songs similar to each other
1. Find songids for songs in the msd dataset in Metadata\database_id_to_songname.csv
2. open anaconda prompt and run recommender.py --find_closest_songs msd --msd_id <msd id of song to find recommendations for>


The dependencies for the code are 
1. TensorFlow
2. annoy 
3. cv2
4. ml_metrics
5. rec_metrics

----Sidenote-----
The code only works for windows environments, updates for mac and linux in progress.

Enjoy
