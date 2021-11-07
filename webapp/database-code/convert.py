'''
October 13th 2021
Simon Hempel-Costello
'''
import csv
class Converter:

    def __init__(self) -> None:
        self.tweet_line_list = []
        pass

    def read_in(self, tweet_file_name):

        with open(tweet_file_name) as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                self.tweet_line_list.append[row]

  

if __name__ == "__main__":             
    c = Converter()
    for i in range(1,14):
        c.read_in("~/simonhc/csrepo/cs257/cs257/webapp/russian-troll-tweet-data/IRAhandle_tweets_" + str(i) + ".csv")


