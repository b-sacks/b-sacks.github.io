from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests


# user inputs an artist, formatting to match search query requirements
artist = input("Enter artist: ")
display_artist = artist # used for output
for i in range(len(artist)):
    if artist[i] == ' ':
        artist = artist[0:i] + '+' + artist[i + 1:len(artist)]

# setlist.fm search query of user inputted artist name
search_url = f"https://www.setlist.fm/search?query={artist}"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

# opening url
try:
    res = requests.get(search_url, headers=headers)
except HTTPError as e:
    print(e)


# beautiful soup used to find information from the url's html
bs = BeautifulSoup(res.text, features='lxml')

# using beautiful soup to find the url of the artist's page on the site
tail = bs.find_all('a')[23].get('href')
artist_url = f'https://www.setlist.fm/{tail}'

# opening artists page
try:
    res = requests.get(artist_url, headers=headers)
except HTTPError as e:
    print(e)

bs = BeautifulSoup(res.text, features='lxml')

# finds url of last show played by the artist and opens it
tail = bs.find_all('h2')[0].find('a').get('href')[3:]
set_url = f"https://www.setlist.fm/{tail}"

try:
    res = requests.get(set_url, headers=headers)
except HTTPError as e:
    print(e)

bs_set = BeautifulSoup(res.text, features='lxml')

# finds all song title objects on the page and adds them to a list
arr = bs_set.find_all("li", {"class": "setlistParts song"})
final_length = len(arr)
final_set_list = []
for item in arr:
    final_set_list.append(item.find('a').get_text())

# outputs a message containing the artist name and the length of the setlist followed by the full setlist
output_box = f"{display_artist} played {final_length} songs at their last show. Their was their setlist:"
print(output_box)
for song in final_set_list:
    print(song)