import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
KEY = os.getenv("OMDB_KEY")


class OMDB:
    def __init__(self):
        self.key = KEY
        self.url = "http://www.omdbapi.com/"

    def getMovie(self, movie):
        parameters = {"apikey": self.key, "type": "movie", "plot": "short"}

        if movie[:2] == "tt":
            parameters["i"] = movie
        else:
            parameters["t"] = movie

        return requests.get(self.url, params=parameters).json()
