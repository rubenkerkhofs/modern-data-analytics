from datetime import datetime
import time
import pandas as pd
import requests
import random

class RedditData:
    def __init__(self):
        self.dataframe = pd.DataFrame()
        self.datalist = []
    
    ##################
    # Helper functions
    ##################
    def __dt2unix(self, before: str, after: str, format: str = "%Y/%m/%d") -> tuple:
        # input: two strings in the form yyyy/mm/dd
        # returns: tuple (before, after) as unix times
        beforeUnix = time.mktime(datetime.strptime(before, format).timetuple())
        afterUnix = time.mktime(datetime.strptime(after, format).timetuple())
        return int(beforeUnix), int(afterUnix)

    def __extractData(self, data):
        dataDF = pd.DataFrame(data)
        toExtract = ['author',
                     'subreddit',
                      'created_utc',
                      'full_link', 
                      'id', 'is_self', 
                      'is_video', 
                      'locked', 
                      'num_comments', 
                      'num_crossposts', 
                      'pinned', 
                      'score',
                     'selftext',
                      'title',
                    'body']
        outDF = pd.DataFrame([])
        for query in toExtract:
            try:
                outDF[query] = dataDF[query]
            except:
                pass
        return outDF

    def __getPushshiftData(self, query, after, before, score, sub, endpoint = 'submission', size = 25):
        url = 'https://api.pushshift.io/reddit/search/' + endpoint
        parameters = {'subreddit': sub, 'title' : query, 'after' : str(after), 'before' : str(before), 'size': 500, 'score': score}
        r = requests.get(url, parameters)
        try:
            data = r.json()
        except:
            data = {'data':[]}
        return data['data']

    def __getNews(self, query: str, after: int, before: int, 
                  endpoint: str, score: str, 
                  sublist: list = ['news','worldnews','gunpolitics']):
        combinedDF = pd.DataFrame()
        after0 = after
        for sub in sublist:
            datai = self.__getPushshiftData(query, after0, before, score, sub, endpoint)
            while(len(datai) > 0):
                dataj = self.__extractData(datai)
                combinedDF = combinedDF.append(dataj)
                after = datai[-1]['created_utc']
                datai = self.__getPushshiftData(query, after, before, score, sub, endpoint)
                time.sleep(random.random())
        return combinedDF


    ##################
    # Public functions
    ##################
    def collect(self, subs: list, terms: list, startdate: str, enddate: str, 
                endpoint: str = 'submission', score: str = '>0') -> pd.DataFrame:
        # assert that subs, dates, and terms are nonempty
        assert(len(subs) > 0), "Search a Subreddit"
        assert(len(terms) > 0), "Pick a searchterm"

        after, before = self.__dt2unix(startdate, enddate)
        for term in terms:
            self.datalist.append(term)
            stories = self.__getNews(term, after, before, endpoint, score, subs)
            stories.insert(0, "Search Term", term)
            self.dataframe = self.dataframe.append(stories)  
        return self.dataframe

            
    def getdata(self) -> pd.DataFrame:
        return(self.dataframe)





if __name__ == "__main__":
    stories = RedditData()
    start = '2018/1/1'
    stop = '2020/1/1'
    collected = stories.collect(['news','worldnews','TrueNews', "InDepthStories"], "heat wave", start,stop, 'submission', '>9')
    stockstories = stories.getdata()[stories.getdata()['Search Term'] != "heat wave"]