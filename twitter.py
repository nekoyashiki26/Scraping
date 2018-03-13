import tweepy
import json
import re
import subprocess 
import sys
import inspect
from config import *
import datetime

argv = sys.argv
argc = len(argv)

def trend(api):
  now = datetime.datetime.today()
  f_name = str(now.date())+'-'+str(now.time())+'-'+'trend.html'
  f= open(f_name, 'w')
  with open('bootstrap-head.txt') as temp:
    for line in temp:
      f.write(line)
    # トレンドを検索
  result = api.trends_place('23424856')
  text = json.dumps(result, sort_keys=True, ensure_ascii=False)
  trends_list = re.split('[{},\[\]]',text)
  trends_list = filter(lambda str:str != '', trends_list)
  list = []
  for trend_str in trends_list:
    trend = trend_str.replace(' ','')
    trend = trend_str.replace('"','').split(': ')
    if len(trend) != 2:
      continue
    elif(trend[0] in 'name' or trend[0] in ' url'):
      list.append(trend[1])
    else:
      continue

  cnt = 0
  for i in range(int((len(list) - 1) / 2)):
    if i != 0:
      cnt+=1
      f.writelines(f'{tab(4)}<tr>{new_line()}')
      f.writelines(f'{tab(5)}<th scope="row">{cnt}</th>{new_line()}')
      f.writelines(f'{tab(5)}<td>{list[i * 2  -1]}</td>{new_line()}')
      f.writelines(f'{tab(5)}<td>{new_line()}')
      f.writelines(f'{tab(6)}<a href={list[i * 2]} class="list-group-item list-group-item-action" target="_blank">{list[i * 2]}</a>{new_line()}')
      f.writelines(f'{tab(5)}</td>{new_line()}')
      f.writelines(f'{tab(4)}</tr>{new_line()}')

  with open('bootstrap-bottom.txt') as temp:
    for line in temp:
      f.write(line)

  f.close()
  if argc == 2 and argv[1] == '-s':
    subprocess.check_output(["mv",f_name,"trend"])
    subprocess.check_output(["open",'./trend/'+f_name])
  else:
    subprocess.check_output(["mv",f_name,"trend"])
    subprocess.check_output(["open",'./trend/'+f_name])
    subprocess.check_output(["rm",'./trend/'+f_name])

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
  return ' ' * num * 2

def new_line():
  return '\n'

if __name__ == "__main__":
  # Twitter APIの認証情報
  # Twitterの開発者向けのページで取得したキーとトークンを使う

  # 認証情報の設定
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
  auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  api = tweepy.API(auth)
  if argc == 3:
    serch_tweet(api,argv[2])
  else:
    trend(api)
