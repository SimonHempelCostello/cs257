CREATE TABLE tweets(
    tweet_content text,
    tweet_language text,
    publish_date DATETIME, 
    post_type text,
    is_retweet integer,
    tweet_id integer
);
CREATE TABLE authors(
    external_author_id integer,
    author_name text,
    account_type text,
    account_category text,
    alt_external_id text
);

CREATE table tweet_instance(
    tweet_id integer,
    author_id integer,
    accounts_followed integer,
    followers integer
);