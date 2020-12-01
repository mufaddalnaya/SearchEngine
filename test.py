
from bs4 import BeautifulSoup
import requests
from string import ascii_lowercase
import json

agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"


def getArtists(letter):
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base + letter + ".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return data
    else:
        raise Exception("Unexpected Input")


def getSongs(artist):
    artist = artist.lower().replace(" ", "")
    first_char = artist[0]
    url = base + first_char + "/" + artist + ".html"
    req = requests.get(url, headers=headers)

    artist = {
        'artist': artist,
        'albums': {}
    }

    soup = BeautifulSoup(req.content, 'html.parser')

    all_albums = soup.find('div', id='listAlbum')
    first_album = all_albums.find('div', class_='album')
    album_name = first_album.b.text
    s = []

    for tag in first_album.find_next_siblings(['a', 'div']):
        if tag.a == None:
            # print(tag.a)
            artist['albums'][album_name] = s
            s = []
            if tag.b is None:
                pass
            elif tag.b:
                album_name = tag.b.text

        else:
            if tag.text is "":
                pass
            elif tag.text:
                s.append(tag.text)

    artist['albums'][album_name] = s

    return artist


def getLyrics(artist, song):
    artist = artist.lower().replace(" ", "")
    song = song.lower().replace(" ", "")
    url = base + "lyrics/" + artist + "/" + song + ".html"

    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    l = soup.find_all("div", attrs={"class": None, "id": None})
    if not l:
        return {'Error': 'Unable to find ' + song + ' by ' + artist}
    elif l:
        l = [x.getText() for x in l]
        return l

print(getArtists("b"))

# id = 1
# for char in ascii_lowercase:
#     print(char)
#     artists = getArtists(char)
#     print(artists)
#     for artist in artists:
#         all_songs = getSongs(artist)
#         for album, songs in all_songs['albums'].items():
#             for song in songs:
#                 wd = getLyrics(artist, song)
#                 f = open("doc"+str(id)+".py", "w")
#                 f.write("def getLyrics():\n")
#                 f.write("\tartist='"+artist+"'\n")
#                 f.write("\talbum='"+album+"'\n")
#                 f.write("\tlyrics=[")
#                 for line in wd:
#                     f.write("'"+line+"',")
#                 f.write("]")    
#                 id = id + 1
                    




# print(artists("a"))
# print(songs("Aaliyah")['albums'][0])
# for k, v in songs("Aaliyah")['albums'].iteritems():
#     print(k,v);
# # print(songs("Aaliyah"))

# f = open("doc1.py","a")
# f.write("getLyrics():\n")
# f.write("\talbum='"+"Aaliyah"+"'")

# print(lyrics("Aaliyah","Intro"))