import requests
from bs4 import BeautifulSoup
import time
import sqlite3

import concurrent.futures



conn = sqlite3.connect('Database.db')
sql_create_table = """ CREATE TABLE IF NOT EXISTS temp (
                        id integer PRIMARY KEY,
                        city text NOT NULL,
                        temperature text
                    ); """
cur = conn.cursor()
cur.execute(sql_create_table)
conn.commit()

STORY_LINKS=[]
file_url = requests.get('https://raw.githubusercontent.com/nshntarora/Indian-Cities-JSON/master/cities.json')
queryName = 'https://www.google.com/search?q='
for i in file_url.json():
    STORY_LINKS.append(queryName + i['name'] + ' tempterature')







USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
LANGUAGE = "en-US,en;q=0.5"
headers = {'User-Agent':USER_AGENT,
           'Accept-Language':LANGUAGE,
           'Content-Language':LANGUAGE }
           

MAX_THREADS = 30

def download_url(url):
    conn = sqlite3.connect('Database.db')
    #print(url)
    response=requests.get(url,headers=headers)
    city=url.split(' ')[0].split('=')[1]

    soup = BeautifulSoup(response.content,'lxml')
    temp = soup.find("span", attrs={"id": "wob_tm"}).text
    #print(temp)
    #print(i['name'],temp)
    sql = ''' INSERT INTO temp(city,temperature)
              VALUES(?,?) '''
    params = (city,temp)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    
    
def download_stories(story_urls):
    threads = min(MAX_THREADS, len(story_urls))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(download_url, story_urls)

def main(story_urls):
    t0 = time.time()
    download_stories(story_urls)
    t1 = time.time()
    print(f"{t1-t0} seconds to download {len(story_urls)} stories.")

main(STORY_LINKS)
