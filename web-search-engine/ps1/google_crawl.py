#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Google Web Search Engine Crawler
'''

class GoogleWebCrawler(object):
  ''' Google Web Search Engine Crawler '''

  def __init__(self, keywords):
    self.queries = keywords

  def make_query_string(self):
    ''' make google web search query string based on keywords '''
    return "+".join(self.queries)  

  def query(self):
    my_referer='http://www.google.com'
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'referer': 'http://www.google.com'
    }

    cookies = {'RMME' : 'true',
           'ACCOUNT_CHOOSER' : 'AFx_qI6OWWcK4lZkpm70smCu2vbXPvpWFYcNBdNhibVdzkv88pKgneocw6ntYtHwqLXu109UvrhsvGLnp1FQhBwrOlyhfwrkqI_GgMbRpw1yiItKIFFO0n96IaDp54IFmMg9eBBwJYmM6c2bWExMwwyx_a1lE2Oq7yYqZyn3SJ5E32225rOh9nxn44gyKJAwQBqVvp8OSmwG',
          'PREF=ID' : '1111111111111111:FF=0:LD=en:NW=1:TM=1401696336:LM=1436847603:GM=1:V=1:S=JgA9IbCS_lH526TJ',
          'GoogleAccountsLocale_session':'en',
          'HSID' : 'AZ3F7F-vAhJ3lOcjO',
          'SSID' : 'AQXEKaqhhWbqjg-9-',
          'APISID' : 'Pe5W9L-OC7USE12y/ATepiwz-VQY4Mn2tp',
          'SAPISID' : 'U-Xvy_On3VILcpuX/AcJH8gcWkDlFdKiIq',
          'SID' : 'DQAAANIBAAA2_a5lmy2EUCsdATBItw6m_fkRpYmT0QSGcoEbJVd-64vPS_SzbMZXuL3CKPudhPH4xhALJlHMx_MrMUGdCyY0XpZt9rGL5yZpscBe06zj9qVqjiprbQ5FvcWV84Ms88jA8e9TPD2BLDmAiZMQgqxJ_08A07TJYgRzUMHZ64N95YQzBS6KeWH3Rse3RyGwae9FDJnmNGw8wMmJItKNPQyUsC2KCbE8KV_DM0yo1SmBIVCDi9CZbBH8vu_gBE8L_9EbOEPHgifojxD1FQBLDZ5Sz8okRtgwfbKMokhOzJmh_OGMgD1fBEs88a98KisOpzvW3uUugCwHt6brkD6rboZ3df2hFTnprMhHB1I1nUtpMR4r8d7-KQhwtuq2m3TlFHaqlBh3OFU7nxuNpiDTCtm3ZcXozesc9CsQbo3P3oPjMuQwA3mzNwoNYgH1wyX7iCCYe0Z1xGTwTrXsxV_pj3UYYFIvt1wqTi1hV7pF6a7D257PfO4ZEx4jyCSbXaCd7GomKWb1Py6SYSfbYkp_rEAePhVHngoXnUvUIErMgvOmaEXJZa_XtXe6vVvyYy2CeoUmOESUOap3w3DR_vXf6tLGBtsO386jPr_tdSZunGhFlWJHOlgYVMeiFOrodMdH4c0',
          'LSID' : 'cl|doritos|lso|mail|o.mail.google.com|s.blogger|s.youtube|ss|writely:DQAAANQBAADsPK5Rrhw0mPIV2TIoYMRZj_BcggDxodWtVL2rrKpIxr6o6-g1NnHgR_r-zH_68Bocq5-3PGeF4bndz7yZdp5wvW4YhAW8JiUcA6cMZK54_b5vYrCD-yPpPMVHtE4ghFYA5ZT5zYW3FPC8v9Mvj_gV01eQDUhIFF101l2mmCNV79HtH0Xw0c-HkybSSuGsMtzXNtg_1QhXpzap9qCFnOB8tDebpg3Wa9CSTUmxOj5-yBGvKH7ovZTcU3U3u2qCUIG8Ft9sdQN20ktvJwnRiYQg4s-u8xpQZ5x1KCptRxN4X8dOC6vAFLhyz_cmKAOotA79P2SrmbDdo2sCy6WjGzUf0SQt0-dMgSbWlO9pt-52di2xVzQ4pvnyCBERdaDhLjFOqqyDpYR5nAMRSbVGXGuM22Da65hKHHpRVWKuahYV58_cR6p6PiwbQ_43J5ktUeSnHAr3WifuZBFhAtEO2RLBLl1cb7ixNUwcMHiKjQLoy3uYOlfrHFSJ4QaEX6K1YiHqd9mAeSPIFGT2FDiXttVWOZtqH1RyI85chJpaUVDR1zW8cFWxrvmQXGXBrKzJW1nucPrniLf8LerXw2e3p4_VPHSnSbkReRSyoOBUDfO1UEF8-62YQeny3gf6MGQcHHA',
          'NID' : '71=FaHimDyTfSsilZ6kBG-02eBYFr_AtuWv4GZ4gV_Uj7MbwxIvJbfZRW371nyKeV0cq8qbe5Ey91gJV2yraqFmtEVldh7DzEx9dfQNzGV20vp3Z_vMD0ADfS81Dx-waWpoA3iVGjv7XIkwYlIZvXdfmZZKavKEu-09h9TZgmLa9ttcaiLuKssGDFJswL7tbNZVJLU_jClF3Z33X6Kn33LdIBxg6riWCZkvqaDzr3HZ60XTj76epDI',
          'GAPS' : '1:it2phkvQDW2lMEgZrCdPr_kBDn8nwQ:A77aLzproh-O7DJU'}

    ''' send query and return list of URLs '''
    query_string = self.make_query_string()
    params = {'q':query_string}

    # make google HTTP request
    google_url = "http://www.google.com/search?"
    response = requests.get(google_url, params=params, headers = headers, cookies = cookies)

    # parse page contents
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    ret = []

    for link in soup.find_all('h3'):
      for linka in link.find_all('a'):
        if not linka.get('style'):
          ret.append(linka.get('href'))

    # return array of URls in an array
    return list(set(ret))[:10]

