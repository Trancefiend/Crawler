
# coding: utf-8

# In[1]:


import urllib3
import certifi
import re
from bs4 import BeautifulSoup


# In[2]:


artist = input("Artist's name: ")
url_artist = re.sub(r'\W+', '', artist)
url = 'https://www.1001tracklists.com/dj/' + url_artist + '/index.html'


# In[3]:


http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

response = http.request('GET', url)
soup = BeautifulSoup(response.data, 'html.parser')


# In[4]:


link_box = soup.find_all('div', attrs={'class', 'tlLink'})


# In[5]:


link_list = []
for links in link_box:
    links = str(links)
    head, sep, tail = links.rpartition('">')
    head1, sep1, tail1 = head.partition('href="')
    url_tracks = 'https://www.1001tracklists.com' + tail1
    link_list.append(url_tracks)


# In[6]:


name_list = []
for link in link_list:
    tracklist_response = http.request('GET', link)
    track_soup = BeautifulSoup(tracklist_response.data, 'html.parser')
    name_box = track_soup.find_all('div', attrs={'class', 'tlToogleData'})
    for names in name_box:
        name_list.append(names.text.strip())


# In[7]:


song_list = []
song_edits = []
for name in name_list:
    head, sep, tail = name.partition('  [')
    song_list.append(head)

for songs in song_list:
    head, sep, tail = songs.partition('   \n')
    song_edits.append(head)
    
song_edits = [f.replace('\xa0', ' ') for f in song_edits]


# In[8]:


file = open(str(artist)+'.txt', 'w')
for val in song_edits:
    var1 = val.split(',');
    file.write('%s\n' % var1)
file.close()

