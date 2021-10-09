import feedparser
from datetime import datetime, timedelta
import json


class GnewsParser:
    __BASE_URL = "https://news.google.com/rss/search?q=<QUERY><DATERANGE><LOCALE>"
    __DATE_RANGE = "+after:<AFTER>+before:<BEFORE>"
    __EN_US_LOCALE = "&ceid=US:en&hl=en-US&gl=US"
    __SK_SK_LOCALE = "&ceid=SK:en&hl=sk-SK&gl=SK"

    def __init__(self):
        self.__url = GnewsParser.__BASE_URL
        self.__last_used_url = self.__url
        self.__start_date = None
        self.__end_date = None
        self.__current_window = None
        self.__days_step = 1

    def setup_search(self, query, from_date, to_date, days_step=1, locale="en-us"):
        self.__url = self.__url.replace("<QUERY>", query)
        self.__url = self.__url.replace("<DATERANGE>", GnewsParser.__DATE_RANGE)
        if locale == "en-us":
            self.__url = self.__url.replace("<LOCALE>", GnewsParser.__EN_US_LOCALE)
        elif locale == "sk":
            self.__url = self.__url.replace("<LOCALE>", GnewsParser.__SK_SK_LOCALE)
        self.__start_date = datetime.strptime(from_date, "%Y-%m-%d")
        self.__end_date = datetime.strptime(to_date, "%Y-%m-%d")
        self.__current_window = self.__start_date
        self.__days_step = days_step

    def get_results(self):
        if self.__current_window + timedelta(days=self.__days_step) > self.__end_date:
            return None
        time_from = self.__current_window.strftime("%Y-%m-%d")
        new_url = self.__url
        new_url = new_url.replace("<AFTER>", time_from)
        self.__current_window += timedelta(days=self.__days_step)
        time_to = self.__current_window.strftime("%Y-%m-%d")
        new_url = new_url.replace("<BEFORE>", time_to)

        res = feedparser.parse(new_url)
        self.__last_used_url = new_url
        if res["status"] != 200:
            print(res["status"])
            return None
        return res["entries"]

    def save_state(self, save_file):
        save = {
            "last_url": self.__last_used_url,
            "search_from": self.__start_date.strftime("%Y-%m-%d"),
            "search_to": self.__end_date.strftime("%Y-%m-%d"),
            "current_window_date": self.__current_window.strftime("%Y-%m-%d"),
            "days_step": self.__days_step
        }
        with open(save_file, "w") as fp:
            json.dump(save, fp)

    def setup_search_from_state(self, state):
        pass


