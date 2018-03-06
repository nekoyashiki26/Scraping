import tweepy
import json
import re
import subprocess 
import sys
import inspect
from config import *

def trend(api):
    # トレンドを検索
    result = api.trends_place('23424856')
    #f = open('output.json', 'w')
    text = json.dumps(result, sort_keys=True, ensure_ascii=False)
    trends_list = re.split('[{},\[\]]',text)
    f = open('trend.html', 'w')
    for trend_str in trends_list:
        trend_list = trend_str.split()
        if len(trend_list) != 2:
            continue
        elif(trend_list[0] in '\"name\":'):
            f.write("<p>"+trend_list[1]+"</p>")
        elif(trend_list[0] in '\"url\":'):
            f.write("<p><a href="+trend_list[1]+" target=\"_blank\">"+trend_list[1]+"</a></p>")
            f.write("")
        else:
            continue

    f.close()
    subprocess.check_output(["open","trend.html"])

def serch_tweet(api,topic):
    f = open('search_result.html', 'w')
    search_result = api.search(q=topic, lang='ja', count=100)
    for result in search_result:
        #リツイートかチェック
        retweet = result.retweet_count
        #リツイートを除外
        if retweet == 0:
            #ツイートIDを取得
            tweet_id = result.id
            #ユーザーIDを取得
            screen_id = result.user.screen_name
            f.write(f"<p><a href=https://twitter.com/{screen_id}/status/{tweet_id}"+" target=\"_blank\">"
                +result.text+"</a></p>")
            f.write("")
    f.close()
    subprocess.check_output(["open","search_result.html"])
if __name__ == "__main__":
    argvs = sys.argv
    argc = len(argvs)
    # Twitter APIの認証情報
    # Twitterの開発者向けのページで取得したキーとトークンを使う

    # 認証情報の設定
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    if argc == 2:
        serch_tweet(api,argvs[1])
    else:
        trend(api)