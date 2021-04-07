import json
import urllib.request
import tweepy
import time

url = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.json"
response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))

data = {}
total1 = {}
total2 = {}

with open('pop_regioni.json') as json_file:
    data = json.load(json_file)
    
    sumPop = 0
    sum1Dos = 0
    sum2Dos = 0

    for key in data.keys():

        dosi = 0 
        area = ''
        pop = data[key]['popolazione']
        sumPop += pop
        
        for i in range(len(response['data'])):
            area = response['data'][i]['nome_area']
            primadose = response['data'][i] ['prima_dose']
            secondadose = response['data'][i]['seconda_dose']
            
            if key in area:
                dosi += secondadose
                sum1Dos += primadose
                sum2Dos += secondadose

        data[key] = {'value' : str(round(((dosi * 100) / pop), 2 ))}
        
total1['total'] = {'value' : sum1Dos * 100 / sumPop}
total2['total'] = {'value' : sum2Dos * 100 / sumPop}

empty = '░'
fill = '█'
customrange = 20

# Authenticate to Twitter
auth = tweepy.OAuthHandler(os.environ['TWITTER_API_KEY'], os.environ['TWITTER_API_SECRET'])
auth.set_access_token(os.environ['TWITTER_TOKEN'], os.environ['TWITTER_TOKEN_SECRET'])

# Create API object
api = tweepy.API(auth)

value = round(total1['total']['value'],1)
normalised = round((value * customrange) / 100 ) 
diff = round((customrange - normalised))
status1 = fill * normalised + empty * diff + ' ' +  str(value) + '% prima dose'
print(status1)

value = round(total2['total']['value'],1)
normalised = round((value * customrange) / 100 ) 
diff = round((customrange - normalised))
status2 = fill * normalised + empty * diff + ' ' +  str(value) + '% seconda dose'
print(status2)

tweet = api.update_status(status1 + '\n' + status2)
time.sleep(2)

for region in data.keys():
    value = float(data[region]['value'])
    
    normalised = round(customrange / value ) 
    diff = round((customrange - normalised))
    
    print(fill * normalised + empty * diff + ' ' + region + ' ' + str(value) + '%')