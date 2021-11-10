CREATE TABLE tweets(
    tweet_content text,
    tweet_language text,
    publish_date text, 
    is_retweet smallint,
    tweet_id text
);
CREATE TABLE authors(
    external_author_id text,
    author_name text
);

CREATE table tweet_instance(
    author_id text,
    tweet_id text,
    accounts_followed integer,
    followers integer
);