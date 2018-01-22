from bs4 import BeautifulSoup as bs4
import requests
from slackclient import SlackClient
import time

#Slack connection
slack_client = SlackClient('your slack bot token goes here. More info:https://api.slack.com/bot-users')

#searches CL for keyword and posts to Slack
def cl():    
    url_base = ('https://louisville.craigslist.org/search/sss')
    params = dict(query=keyword, sort='date', search_distance=30, postal=40243, hasPic=1)
    rsp = requests.get(url_base, params=params)
    html = bs4(rsp.text, 'html.parser')
    shit = []
    shit = html.find_all('p', attrs={'class': 'result-info'})	
    for s in shit:
        price = s.find('span', attrs={'class': 'result-price'})
        if price == None:
            price = 'unknown'
        else:
            price = str(price.text)
        date = s.find('time', attrs={'class': 'result-date'})
        date = date.text
        link = s.find('a', attrs={'class': 'result-title'})
        text = link.text
        link = link.get('href')	
        link = str("\n"+link)
        desc = text+"\n"+price+", "+date+link
        slack_client.api_call(
                'chat.postMessage',
                channel=channel,
                text=desc,
                as_user='true:')
       
if slack_client.rtm_connect():
    while True:
        events = slack_client.rtm_read()
        for event in events:
            if (
                'channel' in event and
                'text' in event and
                event.get('type') == 'message'
            ):
               
                channel = event['channel']
                text = event['text']
                #define text to call bot
                if 'CL Bot:' in text:
                    print(text)
                    #pops bot's name 
                    keyword = text.replace("CL Bot:","")
                    cl()
                    #to exit loop
                    time.sleep(2)
else:
    print('Connection failed, invalid token?')
    
    
    
