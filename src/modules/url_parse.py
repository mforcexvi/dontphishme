from dotenv import load_dotenv
import requests
import os
import json
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
EMPTY  = 0
DATA = 1

def get_url_params(url) :
    r = requests.get(url, allow_redirects=False)
    r.raise_for_status()
    if r.status_code//100 == 3 :
        return (r.status_code, r.headers['Location'])
    else :
        return (r.status_code, url)

def unshorten_url(url) :
    statusCode, link  = get_url_params(url)
    while statusCode//100 == 3 :
        statusCode, link = get_url_params(url)
        url = link
    return link

def get_headers(url) :
    r = requests.get(url, allow_redirects=False)
    print(r.headers)
    return

def check_google_safebrowsing (url) :
    google_url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key='+str(GOOGLE_API_KEY)
    payload = {"client" : {
      "clientId" : "Check-URL" ,
      "clientVersion" : "1.5.2"} ,
      "threatInfo" : {
      "threatTypes" :      ["MALWARE", "SOCIAL_ENGINEERING"],
      "platformTypes" :    ["ANY_PLATFORM"],
      "threatEntryTypes" : ["URL"],
      "threatEntries" : [
        {"url" : str(url)}
        ]
      }
     }
    header = {'Content-Type' : 'application/json'}
    r = requests.post(google_url, data = json.dumps(payload), headers = header)
    r.raise_for_status()
    if r.status_code == 200:
        response_data = json.loads(r.text)
        return response_data
    return json.dumps('{}')

def check_json_google (data) :
    if data == json.loads('{}') :
        print('NO MATCH WITH GOOGLE BLACKLIST - Probably Safe :P')
        return EMPTY
    # print(data["matches"][-1]["threatType"])
    result = "Threat Type: " + data["matches"][-1]["threatType"]
    return result
