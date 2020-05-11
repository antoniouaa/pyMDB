#!/usr/bin/env python
# coding: utf-8

# In[27]:


from bs4 import BeautifulSoup
import requests

top250 = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating"
top250_2 = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt"

def fetch_(query):
    with requests.get(top250) as r:
        if r.status_code < 400:
            soup = BeautifulSoup(r.content, "lxml")
            try:
                item_pane = soup.find_all("div", class_="lister-item-content")
                title = []
                for item in item_pane:
                    title.extend(item.find("a"))
                return title
            except e:
                print("BAD ELEMENT IN SOUP")


# In[37]:


titles = fetch_("i=tt0111161")

from random import sample

print(sample(titles, k=1))


# In[ ]:




