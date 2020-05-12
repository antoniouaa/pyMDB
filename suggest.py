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

TOP250 = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating"
TOP250_2 = "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&start=51&ref_=adv_nxt"

def fetch_():
    with requests.get(TOP250) as r:
        if r.status_code < 400:
            soup = BeautifulSoup(r.content, "lxml")
            try:
                item_pane = soup.find_all("div", class_="lister-item-content")
                titles = []
                for item in item_pane:
                    titles.extend(item.find("a"))
                return sample(titles, k=1)
            except Exception:
                print("BAD ELEMENT IN SOUP")

class SuggestionLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(SuggestionLayout, self).__init__(**kwargs)
        self.button = Button(text="Pick new suggestion", on_press=self.update_title, always_release=True)
        self.label = Label(text="Film Suggestion")
        self.add_widget(self.button)
        self.add_widget(self.label)

    def update_title(self, event):
        self.label.text = fetch_()[0]

class SuggestionApp(App):
    def build(self):
        return SuggestionLayout(orientation="vertical")

if __name__ == "__main__":
    SuggestionApp().run()