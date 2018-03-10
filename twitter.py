import tweepy
import json
import re
import subprocess 
import sys
import inspect
from config import *

def trend(api):
    f= open('trend.html', 'w')
    with open('bootstrap.txt') as temp:
        for line in temp:
            f.write(line)
    # トレンドを検索
    result = api.trends_place('23424856')
    text = json.dumps(result, sort_keys=True, ensure_ascii=False)
    trends_list = re.split('[{},\[\]]',text)
    list = []
    for trend_str in trends_list:
        trend_list = trend_str.split()
        print(trend_list)        
        if len(trend_list) != 2:
            continue
        elif(trend_list[0] in '\"name\":' or trend_list[0] in '\"url\":'):
            list.append(trend_list[1])
        else:
            continue

    cnt = 0
    for i in range(int((len(list) - 1) / 2)):
        if i == 0:
            f.writelines(f'{tab(3)}<thead>{new_line()}')
            f.writelines(f'{tab(4)}<tr>{new_line()}')
            f.writelines(f'{tab(5)}<th>#</th>{new_line()}')
            f.writelines(f'{tab(5)}<th>trend</th>{new_line()}')
            f.writelines(f'{tab(5)}<th>url</th>{new_line()}')
            f.writelines(f'{tab(4)}</tr>{new_line()}')
            f.writelines(f'{tab(3)}</thead>{new_line()}')
            f.writelines(f'{tab(3)}<tbody>{new_line()}')
        else:
            f.writelines(f'{tab(4)}<tr>{new_line()}')
            f.writelines(f'{tab(5)}<th scope="row">{cnt}</th>{new_line()}')
            f.writelines(f'{tab(5)}<td>{list[i * 2  -1]}</td>{new_line()}')
            f.writelines(f'{tab(5)}<td>{new_line()}')
            f.writelines(f'{tab(6)}<a href={list[i * 2]} class="list-group-item list-group-item-action">{list[i * 2]}</a>{new_line()}')
            f.writelines(f'{tab(5)}</td>{new_line()}')
            f.writelines(f'{tab(4)}</tr>{new_line()}')
    
    f.writelines(f'{tab(3)}</tbody>{new_line()}')
    f.writelines(f'{tab(2)}</table>{new_line()}')
    f.writelines(f'{tab(1)}</body>{new_line()}')
    f.writelines('</html>')
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

def tab(num):
    return '\t' * num

def new_line():
    return '\n'

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