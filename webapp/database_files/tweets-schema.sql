CREATE TABLE tweets(
    tweet_content text,
    tweet_language text,
    publish_date text, 
    is_retweet integer,
    tweet_id BIGINT
);
CREATE TABLE authors(
    external_author_id BIGINT,
    author_name text
);

CREATE table tweet_instance(
    tweet_id BIGINT,
    author_id BIGINT,
    accounts_followed integer,
    followers integer
);