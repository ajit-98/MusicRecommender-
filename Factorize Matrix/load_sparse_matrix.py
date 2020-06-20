import pandas as pd 
import os
import sys
import numpy as np
import pickle
import scipy.sparse as sparse
import gzip
import argparse

train_triplets_file = '..\\MSD Data\\train_triplets.txt'
echo_to_msd_file = '..\\MSD Data\\EchotoMSD_ID.txt'
#create sparse taste profile matrix out of filtered_train_triplets
def create_sparse_matrix(txtfile, num_subset_songs =0, num_subset_users=0):
    ''' Creates a csr matrix of user data from csvfile 
    Params :
        txtfile : path to taste profile textfile
        num_subset_songs : number of subset songs
        num_subset_users : number of subset users
    Return :
        subset_matrix : sorted itemwise sparse matrix of item x user
        song_list : list of unique song ids sorted by popularity
        user_list : list of unique user ids
    '''
    
    df = pd.read_csv(txtfile, sep='\t', names=['user', 'song', 'play_count'])
    ID_df = pd.read_csv(echo_to_msd_file,sep='<SEP>',names = ['track_id','echo_id','artist_name','song_name'],engine='python')
    echonest_id_to_track_id = dict(zip(ID_df.echo_id,ID_df.track_id))

    # sort songs and users by playcounts
    sorted_song = df.groupby(['song']).sum().sort_values('play_count', ascending=False)
    sorted_song.reset_index(level=['song'],inplace=True)
    sorted_user = df.groupby(['user']).sum().sort_values('play_count',ascending=False)
    sorted_user.reset_index(level=['user'],inplace=True)

    # take subset 
    subset_songs = sorted_song.loc[0:num_subset_songs,'song'].tolist()
    print(len(subset_songs))
    subset_users = sorted_user.loc[0:num_subset_users,'user'].tolist()
    filtered_df = df[df['song'].isin(subset_songs) & df['user'].isin(subset_users)]

    # map index to songs and index to users for sparse matrix 
    idx_songs = np.arange(num_subset_songs)
    idx_users = np.arange(num_subset_users)
    song_to_idx = dict(zip(subset_songs, idx_songs))
    user_to_idx = dict(zip(subset_users, idx_users))
    filtered_df.loc[:,'user'] = filtered_df['user'].map(user_to_idx)
    filtered_df.loc[:,'song'] = filtered_df['song'].map(song_to_idx)
    #print(user_to_idx)
    # replace df values to indices s
    #print(filtered_df)
    #filtered_df = filtered_df.replace({'user':user_to_idx})
    #filtered_df = filtered_df.replace({'song':song_to_idx})

    # rows : songs, cols : users 
    song_user_matrix = sparse.csr_matrix((filtered_df.values[:, 2], (filtered_df.values[:, 1], filtered_df.values[:, 0])))

    print (song_user_matrix.shape)

    idx_to_song = dict(zip(song_to_idx.values(), song_to_idx.keys()))
    idx_to_user = dict(zip(user_to_idx.values(), user_to_idx.keys()))
    
    song_list = list()
    user_list = list()
    song_list_msd_id = list()
    for s in range(len(song_to_idx)) : 
        song_list.append(idx_to_song[s])
    for u in range(len(user_to_idx)) :
        user_list.append(idx_to_user[u])
    for song in song_list:
        song_list_msd_id.append(echonest_id_to_track_id[song][0])
    print(song_list)
    
    return song_user_matrix, song_list, user_list,song_list_msd_id 


if __name__ == '__main__':
    total_users = 1019318 
    total_songs = 384546
    song_user_matrix, songs, users,msd_ids = create_sparse_matrix(train_triplets_file, total_songs, total_users)
    print(len(songs),len(users))
	#save outputs 
	#filename_tag = '_' + str(args.users) + '_'+ str(args.songs)
    #sparse.save_npz('song_user_matrix' +'.npz', song_user_matrix)
    #np.save('subset_songs' + '.npy', np.array(songs))
    #np.save('subset_users' + '.npy', np.array(users))
    #np.save('subset_songs_msd_id' + '.npy', np.array(msd_ids))