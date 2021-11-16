AUTHORS: Simon Hempel Costello and Lev Shuster 

DATA: 300,000 tweets from bot accounts.

FEATURES CURRENTLY WORKING:
- Graph of follower count over time for any bot account (access through the results of rank or search page)
- Search: searches the contents of tweets for matching strings and displays the first few results
- Rank: ranks the most successful bots
- I'm Feeling lucky - take a random archived tweet then displays the results in a form meant to mirror the twitter interface.

FEATURES NOT YET WORKING:
- Search and ranking filters have graphical elements but do not affect the SQL calls
    - This means that date filters, ascending/descending sort, number of results, etc. remain at default values
- Most buttons on website do not interact when hovered over.