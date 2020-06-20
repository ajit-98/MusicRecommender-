import pandas as pd 
import os
import sys
import numpy as np
import pickle

CUTOFF = 10000

Echo_to_MSD_file = '..\\MSD Data\\EchoToMSD_ID.txt' # path to echo to MSD file
train_triplets_file = '..\\MSD Data\\train_triplets.txt' # path to train triplets file

def get_popular_songs(txtfile, num_subset_songs):
    
    df = pd.read_csv(txtfile, sep='\t', names=['user', 'song', 'play_count'])
    # sort songs and users by playcounts
    sorted_song = df.groupby(['song']).sum().sort_values('play_count', ascending=False)
    sorted_song.reset_index(level=['song'],inplace=True)
    #print(sorted_song)
    #sorted_song = df.groupby(level= 0).sum().sort_values('play_count', ascending=False)
    #subset_songs = sorted_song.ix[0:num_subset_songs].index.get_level_values('song').tolist()
    #sorted_user = df.groupby(['user'])[['play_count']].sum().sort_values('play_count', ascending=False)
    # take subset 
    subset_songs = sorted_song.loc[0:num_subset_songs,'song'].tolist()
    #subset_users = sorted_user.loc[0:num_subset_users,'user'].tolist()
    id_to_songname = pd.read_csv(Echo_to_MSD_file,sep='<SEP>',names=['track_id','echo_id','artist_name','song_name'],engine='python')
    id_to_songname['artist_song_name'] = id_to_songname['artist_name'].str.cat(id_to_songname['song_name'],sep='=')
    songname_to_trackid = dict(zip(id_to_songname.artist_song_name,id_to_songname.track_id))
    id_to_songname_dict = dict((zip(id_to_songname.echo_id,id_to_songname.artist_song_name)))
    song_artist_list = [id_to_songname_dict[ID] for ID in subset_songs]
    #print(song_srtist_list)
    with open('..\\Metadata\\id_to_songname.txt','w') as f:
        for song in song_artist_list:
            try:
                f.write(song+ '=' + songname_to_trackid[song] + '\n')
            except:
                pass

    	   
    f.close()




if __name__ == '__main__':
	get_popular_songs(train_triplets_file,384546)