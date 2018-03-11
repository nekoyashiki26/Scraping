import tweepy
import json
import re
import subprocess 
import sys
import inspect
from config import *
import datetime

def trend(api):
  now = datetime.datetime.today()
  f_name = str(now.date())+'-'+str(now.time())+'-'+'trend.html'
  f= open(f_name, 'w')
  with open('bootstrap.txt') as temp:
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
      cnt+=1
      f.writelines(f'{tab(4)}<tr>{new_line()}')
      f.writelines(f'{tab(5)}<th scope="row">{cnt}</th>{new_line()}')
      f.writelines(f'{tab(5)}<td>{list[i * 2  -1]}</td>{new_line()}')
      f.writelines(f'{tab(5)}<td>{new_line()}')
      f.writelines(f'{tab(6)}<a href={list[i * 2]} class="list-group-item list-group-item-action" target="_blank">{list[i * 2]}</a>{new_line()}')
      f.writelines(f'{tab(5)}</td>{new_line()}')
      f.writelines(f'{tab(4)}</tr>{new_line()}')
    
  f.writelines(f'{tab(3)}</tbody>{new_line()}')
  f.writelines(f'{tab(2)}</table>{new_line()}')
  f.writelines(f'{tab(1)}</body>{new_line()}')
  f.writelines('</html>')
  f.close()
  subprocess.check_output(["mv",f_name,"trend"])
  subprocess.check_output(["open",'./trend/'+f_name])
