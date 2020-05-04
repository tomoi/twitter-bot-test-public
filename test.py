import twitter #Twitter
import json
import os
from requests_oauthlib import OAuth1Session #Oauth

import urllib.error
import urllib.request
import glob
import tempfile
from time import sleep 
import datetime  


CK = os.environ["TWITTER_CONSUMER_KEY"]
CS = os.environ["TWITTER_CONSUMER_SECRET"]
AT = os.environ["TWITTER_ACCESS_TOKEN_KEY"]
ATS = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
twitter = OAuth1Session(CK, CS, AT, ATS)
user_id = os.environ["TWITTER_USER_ID"]

def get_favorites():
    url = "https://api.twitter.com/1.1/favorites/list.json"
    params ={'user_id' : user_id,'count' : 7} 
    res = twitter.get(url, params = params)

    if res.status_code == 200: 
        favorites = json.loads(res.text)
        for favorites_list in favorites:
            print(favorites_list['user']['name']+'::'+favorites_list['text'])
            print(favorites_list['created_at'])
            print('--------------------------------------------')
            if 'media' in favorites_list['entities']:
                print('-------------true-------')
                i = 0
                print('--------------------------------------------')
                if 'photo' in favorites_list['entities']['media'][0]['type'] :
                    for media in favorites_list['extended_entities']['media']:
                        i += 1
                        download_file(media['media_url'],media['url'],i)
                        print('--------------------------------------------')
                    print('--------------------------------------------')
                else:
                    pass
    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)


def download_file(url,path,number):
    try:
        with urllib.request.urlopen(url) as web_file:
            print(url)
            extension = url.split(".")[-1]
            print(number)
            Updated_path = path.split("/")[-1]
            file_path = Updated_path + "-" + str(number) + "." + extension
            #if DBにfile_pathの名前が存在するか確かめる:
            urllib.request.urlretrieve(url,os.path.join("tmp",file_path))
            print("アップロード完了")
            #sleep(0.5)
    except urllib.error.URLError as e:
        print(e)
#get_favorites()