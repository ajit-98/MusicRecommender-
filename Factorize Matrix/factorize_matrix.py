import numpy as np  
import pandas as pd  
import scipy.sparse as sparse
import json
import wmf




if __name__ == "__main__":
	song_user_sparse_matrix = sparse.load_npz('..\\Metadata\\song_user_matrix.npz')
	#dense_matrix = song_user_sparse_matrix.todense()
	confidence_matrix = wmf.log_surplus_confidence_matrix(song_user_sparse_matrix,alpha=40,epsilon=10**-8)
	song_latent_factors,user_latent_factors = wmf.factorize(confidence_matrix,num_factors=100)
	np.savez_compressed('..\\Metadata\\song_latent_factors.npz',song_latent_factors)
	np.savez_compressed('..\\Metadata\\user_latent_factors.npz',user_latent_factors)
	print(user_latent_factors.shape,song_latent_factors.shape)
	#print(user_latent_factors)






