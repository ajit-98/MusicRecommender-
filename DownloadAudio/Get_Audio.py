from __future__ import unicode_literals
from selenium import webdriver 
import pandas as pd 
import numpy as np
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse 
import youtube_dl
import os
from pydub import AudioSegment
from pydub.utils import make_chunks
import librosa
import librosa.display
import matplotlib.pyplot as plt
import pylab
import argparse

#Code to download songs in the million song dataset from youtube and extract spectrograms for each of them

VIDEO_FILTER_QUERY = '&sp=EgIQAQ%253D%253D' #append to search to filter only videos
BASE_URL = 'http://youtube.com/results?search_query='
spectrogram_dir = '..\\Mel Specs' #Change to directory where spectrograms are to be stored 
chromedriver_path = 'C:\\Users\\ajitrao\\ChromeDriver\\chromedriver' #change to path to chromedriver


def get_search_url(song,base_url):
	query = urllib.parse.quote_plus(song)
	return BASE_URL+query+VIDEO_FILTER_QUERY


def get_id_from_filename(name):
	filename = name.split('_')[0]
	filename = filename.split('.')[0]
	return filename

#https://accounts.google.com/

# input a list of tuples containing song name and id to
def get_songs(song_id_list,start_index,end_index):
	options = webdriver.ChromeOptions()
	options.add_argument('--headless') #instantiate headless browsing
	for root,dirs,files in os.walk(spectrogram_dir):
		root = root
		filenames = files
	downloaded_song_ids = [get_id_from_filename(x) for x in filenames]
	downloaded_song_ids = set(downloaded_song_ids)
	#print(downloaded_song_ids)
		
	count = 0 

	for song_id in song_id_list[start_index:end_index]:
		if song_id[1] not in downloaded_song_ids:
			url = get_search_url(song_id[0],BASE_URL) #get youtubeurl for the given searched song
			driver = webdriver.Chrome(chromedriver_path,options=options)    
			driver.get(url) #search for song
			driver.add_cookie({'name':'SameSite','value':'None'})
			driver.add_cookie({'name':'Secure','value':'True'})

			user_data = driver.find_elements_by_xpath('//*[@id="video-title"]') #get all video elements
			links = []
			for i in user_data:
				links.append(i.get_attribute('href')) # get links for each song search
			#print(links)
			df = pd.DataFrame(columns = ['id','title','link'])
			wait = WebDriverWait(driver,10) # timeout if a NotFoundException is thrown while fetching the songlinks
			v_category = 'CATEGORY_NAME'
			download_flag = 0
			for x in links[0:3]: #try downloading only first three links returned during search
				try:
					driver.get(x)
					v_id = x.strip('https://www.youtube.com/watch?v=')
					v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
					filename = song_id[1] + '.mp3'
					success = download(x,filename)
					if(success):
						print('{} - {} - {} - successful'.format(v_id,v_title,x))
						driver.close()
						get_audio_specs(filename,spectrogram_dir)
						df.loc[len(df)] = [v_id,v_title,x]
						count +=1

						break
					else:
						pass
				except KeyboardInterrupt:
					print('Quitting....')
					break
				except:
					pass

	driver.quit()
	return df #return df of successfully dowloaded songs

def get_audio_specs(mp3_file,export_dir):
    myaudio = AudioSegment.from_file(mp3_file) 
    chunk_length_ms = 30000 # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms) #Make chunks of one sec

#Export all of the individual chunks as mp3 files 

    for i, chunk in enumerate(chunks):
        mp3_file_name = os.path.join(export_dir,mp3_file)           
        spec_name = ((mp3_file_name + "_{0}.png").format(i)) 
        print ("exporting", spec_name)
        sig = np.array(chunk.get_array_of_samples(),dtype='float64')
        Generate_Mel(sig,44100,spec_name)


def Generate_Mel(sig,fs,filename) :     
# make pictures name 
#save_path = 'test.jpg'

    pylab.axis('off') # no axis
    pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) # Remove the white edge
    S = librosa.feature.melspectrogram(y=sig, sr=fs)
    librosa.display.specshow(librosa.power_to_db(S, ref=np.max))

    pylab.savefig(filename, bbox_inches=None, pad_inches=0)
    plt.close()
        #plt.savefig(mp3_file_name + ".png")#Change this line


def download(url,filepath):
	ydl_opts = {
	    'format': 'bestaudio/best',
	    'outtmpl': filepath,
	    'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}
	try:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([url])
		return True
	except:
		return False



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = 'Script for downloading audio spectrograms for songs in the million song dataset')
	parser.add_argument('--index',nargs =2, type = int, default='False',help='Specify the start and end indexes of songs in Metadata\\id_to_songname.txt to be downloaded')
	arguments = parser.parse_args()
	song_df = pd.read_csv('..\\Metadata\\id_to_songname.txt',sep='=',names= ['artist_name','song_name','msd_id'],encoding = "ISO-8859-1") #change the popular_songs.txt to the file you wanna download
	song_df['search_query'] = song_df['artist_name'].str.cat(song_df['song_name'],sep=' ')
	song_id_list = list(zip(song_df.search_query,song_df.msd_id))
	get_songs(song_id_list,arguments.index[0],arguments.index[1])








