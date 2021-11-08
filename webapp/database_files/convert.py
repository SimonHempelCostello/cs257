'''
October 13th 2021
Simon Hempel-Costello
'''
import csv
from datetime import datetime
class Converter:

    def __init__(self) -> None:
        pass

    def read_and_write(self, tweet_file_name):
    #this is really ugly, but these lists are so big that I am trying to minimise iterations and this seemed like the best way
        with open(tweet_file_name) as input, open('converted_csv/tweets.csv', 'a', encoding = 'UTF8') as tweets_output, open('converted_csv/authors.csv', 'a', encoding = 'UTF8') as authors_output, open('converted_csv/tweets_authors.csv', 'a', encoding = 'UTF8') as tweets_authors_output:
            csvreader = csv.reader(input)
            tweet_writer = csv.writer(tweets_output)
            authors_writer = csv.writer(authors_output)
            tweets_authors_writer = csv.writer(tweets_authors_output)
            heading = False
            last_author_id = 0
            for row in csvreader:
                if heading:
                    tweets_row = self.get_tweets_output(row)
                    authors_row = self.get_authors_output(row)
                    tweets_authors_row = self.get_tweets_authors_output(row)
                    tweet_writer.writerow(tweets_row)
                    if(authors_row[0]!= last_author_id):
                        authors_writer.writerow(authors_row)
                        last_author_id = authors_row[0]
                    tweets_authors_writer.writerow(tweets_authors_row)
                heading = True
    def get_tweets_output(self, input):
        content = input[2].replace(',','')
        content = content.replace('\\', '')
        content = content.replace('/', '')
        language = input[4]
        date_string = input[6]
        date_time = datetime.strptime(date_string, "%m/%d/%Y %H:%M")
        output_date = str(date_time.year) +  "/" + str(date_time.month) + "/" + str(date_time.day)
        is_retweet = input[12]
        tweet_id = input[16]
        output = [content, language, output_date, is_retweet, tweet_id]
        return output
    def get_authors_output(self, input):
        external_author_id = input[0]
        author_name = input[1]
        output = [external_author_id, author_name]
        return output
    def get_tweets_authors_output(self, input):
        author_id = input[0]
        tweet_id = input[16]
        following = input[7]
        followers = input[8]
        output = [author_id, tweet_id, following, followers]
        return output

  

if __name__ == "__main__":             
    c = Converter()
    for i in range(1,14):
        c.read_and_write("IRAhandle_tweets_" + str(i) + ".csv")
        print(i)


