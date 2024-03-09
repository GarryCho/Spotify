from operator import truediv
from pickle import FALSE
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import json
import pandas as pd 
# import matplotlib as plt 
from datetime import date, datetime
import requests
import os



def authenication():
    global sp
    global a

    a=spotipy.oauth2.SpotifyPKCE(client_id=client_id,redirect_uri=redirect_uri,open_browser=False,scope=scope)
    sp=spotipy.client.Spotify(auth_manager=a)

def get_user():
    global sp_user
    global user

    sp_user1=spotipy.oauth2.SpotifyPKCE(client_id=client_id,redirect_uri=redirect_uri,open_browser=True,scope="user-read-private, user-top-read")
    sp_user=spotipy.client.Spotify(auth_manager=sp_user1)
    user=sp_user.current_user()
    print(user['id'])

def get_tracks():
    results = sp_user.current_user_top_tracks(limit=50, offset=0, time_range='long_term')

    for idx, item in enumerate(results['items']):
        idx=idx+1
        artists=item['artists'][0]['name']
        song=item['name']
        album=item['album']['name']
        year=item['album']['release_date'][0:4]
        artist_uri=item['artists'][0]['uri'][15:]

        idx1.append(idx)
        Title1.append(song)
        Artists1.append(artists)
        Album1.append(album)
        Year_rel1.append(year)
        artists_uri.append(artist_uri)
def recommendations():
    recs=sp_user.recommendations(seed_artists=artists_uri[0:4],limit=100)
    recs_1=json.dumps(recs, indent = 4)
   

    for idx, track in enumerate(recs['tracks']):
        idx=idx+1
        artists=track['artists'][0]['name']
        song=track['name']
        link=track['album']['external_urls']['spotify']
        link=track['album']['id']
        uri=track['uri']
        idno=track['id']


        idx1.append(idx)
        rec_artist.append(artists)
        rec_song.append(song)
        rec_link.append(link)
        rec_uri.append(uri)
        rec_id.append(idno)

    
def read_playlist():
    global sp_read
    #Checks whether the playlist exists; adds to existing playlist but will create if it doesn't exist..
    # playlist_read_scope='playlist-read-private'
    # sp_read=spotipy.Spotify(auth_manager=SpotifyOAuth(scope=playlist_read_scope))
    sp_read=spotipy.oauth2.SpotifyPKCE(client_id=client_id,redirect_uri=redirect_uri,open_browser=True,scope="playlist-read-private,playlist-modify-private")
    sp_read=spotipy.client.Spotify(auth_manager=sp_read)
    # input(sp_read.get_authorize_url())
    playlist_names=sp_read.current_user_playlists(limit=50)
    
    for i in range(len(playlist_names['items'])):
        p_names=playlist_names['items'][i]['name']
        # if p_names=="API-Recs_shorts":
        #     continue
        if p_names=="G.CHO SPOTIFY API":
            print('it exists'+"\n"+"adding to the existing playlist")
            existing_playlist_id=playlist_names['items'][i]['id']
            add_2_playlist(existing_playlist_id)
            break
        else:
            make_playlist()
            break

def make_playlist():
   
    playlist_name="G.CHO SPOTIFY API"
    descrip="using API"
    new_playlist=sp_read.user_playlist_create(user=str(user['id']),name=playlist_name,public=True,description=descrip)

    playlist_id=new_playlist["id"]
    sp_read.user_playlist_add_tracks(user=str(user['id']),playlist_id=playlist_id,tracks=rec_uri,position=None)
    print("Playlist created!!")

def add_2_playlist(existing_playlist_id):
    # playlist_scope='playlist-modify-private'
    # sp1=spotipy.Spotify(auth_manager=SpotifyOAuth(scope=playlist_scope))

    sp_read.user_playlist_add_tracks(user=str(user['id']),playlist_id=existing_playlist_id,tracks=rec_uri,position=None)



# ****************************************
#            Start of Script             #
# ****************************************


client_id='c0252fa649a940d89ed6324c9bf8c242'
client_secret='1a51802e5d9e4c3987be1f37c12b4509'
redirect_uri='http://localhost:8000/'


os.environ['SPOTIPY_CLIENT_ID']=client_id
os.environ['SPOTIPY_CLIENT_SECRET']=client_secret
os.environ['SPOTIPY_REDIRECT_URI']=redirect_uri


idx1=[]
Title1=[]
Artists1=[]
Album1=[]
Year_rel1=[]
artists_uri=[]
rec_artist=[]
rec_song=[]
rec_link=[]
rec_uri=[]
rec_id=[]

""" Scope refers to the type of information and call you want. (Reading playlist/tracks/user info) """
scope="playlist_read_scope"
authenication()
get_user()
get_tracks()
recommendations()
read_playlist()


"""
Now to read the recommendations to make more recommendations!
"""