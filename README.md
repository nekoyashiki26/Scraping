## Scraping

## Description
- Twitter scraping tool

## Requirement
- python 3.6
- tweepy 3.6.0

## Usage
``` shll
#change directory
$ cd "your project directory"

#search trend
$ python3 twitter.py

#seach word in twitter
$ python3 twitter.py "word"    
```

## Installation 
``` shll
 $ git clone https://github.com/nekoyashiki26/Scraping.git
 $ cd Scraping
 $ pip3 install tweepy
 $ echo "CONSUMER_KEY = 'edit your CONSUMER_KEY'" > config.py
 $ echo "CONSUMER_SECRET = 'edit your CONSUMER_SECRET'" > config.py
 $ echo "ACCESS_TOKEN = 'edit your ACCESS_TOKEN'" > config.py
 $ echo "ACCESS_TOKEN_SECRET = 'edit your ACCESS_TOKEN_SECRET'" > config.py 
 ```
 
 ## Example
 ``` shll
# search twitter trends in tokyo
$ python3 twitter.py

# search word in twitter 
$ python3 twitter.py python
 ```