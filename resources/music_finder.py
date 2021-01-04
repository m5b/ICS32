import spotify_credentials
import spotipy, sys
from collections import namedtuple
from spotipy import SpotifyClientCredentials

Artist = namedtuple('Artist', ['id','name'])
Album = namedtuple('Album', ['id','name'])

class MusicFinder:

    """
    Init the MusicFinder class by passing a client id and client secret 
    required by the Spotify API.
    """ 
    def __init__(self, client_id:str, client_secret:str):
        self._sp = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(
                    client_id=spotify_credentials.client_id,
                    client_secret=spotify_credentials.client_secret
                )
    )

    """
    returns a dict of Artist namedtuple's containing the id and name
    of the artists found using the name parameter search criteria
    """
    def find_artists(self, name: str) -> dict:
        results = self._sp.search(q='artist:' + name, type='artist')
        print(results)
        artists = {}
        for i, item in enumerate(results['artists']['items']):
            artists[i] = Artist(item['id'], item['name'])

        return artists

    """
    returns a dict of Album namedtuple's containing the id and name of the albums 
    found for the supplied Artist nametuple.
    """
    def get_artist_albums(self, artist:Artist) -> dict:
        results = self._sp.artist_albums(artist.id, album_type='album')
        albums = {}
        dups = []
        for i, item in enumerate(results['items']):
            if item['name'] not in dups:
                albums[i] = Album(item['id'], item['name'])
                dups.append(item['name'])
        
        return albums

def main():
    search = input("What is the name of the artist you would like to find (Q to quit)? ")
    if(search == 'Q'):
        sys.exit()

    mf = MusicFinder(spotify_credentials.client_id, spotify_credentials.client_secret)
    
    artists = mf.find_artists(search)

    print("Here are the artists that I found: \r\n")    
    for i in artists:
        print("{}. {}".format(i+1,artists[i].name))


    r = input("If you like see the albums for one of these artists, enter the number: ")
    sel = int(r) - 1

    albums = mf.get_artist_albums(artists[sel])
    print("\r\n")    
    print("Great, here are the albums for " + artists[sel].name + "\r\n")    

    for i in albums:
        print("{}. {}".format(i+1,albums[i].name))

    print("\r\n")    
    main()


if __name__ == '__main__':
    main()
