#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests
from random import sample

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

BASE_URL = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating"
next_page_url = ",desc&start="
next_page_url_ = "&ref_=adv_nxt"

def fetch_list():
    films = {}
    for page_number in range(0, 252, 50):
        url = f"{BASE_URL}{next_page_url}{page_number}{next_page_url_}"
        with requests.get(url) as r:
            soup = BeautifulSoup(r.content, "lxml")
            try:
                item_pane = soup.find_all("div", class_="lister-item-content")
                for item in item_pane:
                    film_title = item.find("a").text
                    film_desc = item.find_all("p", class_="text-muted")[-1].text.strip()
                    films[film_title] = film_desc
            except Exception:
                print("BAD ELEMENT IN SOUP")
    return films

def suggest_film(films):
    title = sample(list(films), k=1)[0]
    return title, films[title]

class SuggestionLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SuggestionLayout, self).__init__(**kwargs)
        self.films = films
        self.button = Button(text="Pick new suggestion", 
            on_press=self.update_title, 
            always_release=True,
            size=[800, 150],
            size_hint=[None, None])   
        self.button.font_size = "25dp"
        self.label = Label(text="Film Suggestion", 
            markup=True,
            halign="center", 
            valign="center", 
            text_size=[400, 400])
        self.label.font_size = "25dp"
        self.add_widget(self.label)
        self.add_widget(self.button)

    def update_title(self, event):
        title, desc = suggest_film(self.films)
        self.label.text = f"[b]{title}[/b]\n\n{desc}"

class SuggestionApp(App):
    def build(self):
        return SuggestionLayout(films, orientation="vertical")

if __name__ == "__main__":
    films = fetch_list()
    SuggestionApp().run()