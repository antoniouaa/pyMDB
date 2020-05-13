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
    titles = []
    for page_number in range(51, 252, 50):
        url = f"{BASE_URL}{next_page_url}{page_number}{next_page_url_}"
        with requests.get(url) as r:
            soup = BeautifulSoup(r.content, "lxml")
            try:
                item_pane = soup.find_all("div", class_="lister-item-content")
                for item in item_pane:
                    titles.extend(item.find("a"))
            except Exception:
                print("BAD ELEMENT IN SOUP")
    return titles

def suggest_film(titles):
    return sample(titles, k=1)[0]

class SuggestionLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SuggestionLayout, self).__init__(**kwargs)
        self.titles = titles
        self.button = Button(text="Pick new suggestion", on_press=self.update_title, always_release=True)
        self.button.font_size = "25dp"
        self.label = Label(text="Film Suggestion")
        self.label.font_size = "25dp"
        self.add_widget(self.label)
        self.add_widget(self.button)

    def update_title(self, event):
        self.label.text = suggest_film(self.titles)

class SuggestionApp(App):
    def build(self):
        return SuggestionLayout(titles, orientation="vertical")

if __name__ == "__main__":
    titles = fetch_list()
    SuggestionApp().run()