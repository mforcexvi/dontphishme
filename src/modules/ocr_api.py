import requests
import json
import re
from dotenv import load_dotenv
import os
load_dotenv()


def run_ocr(image_uri):
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    data_payload = json.loads('{ "requests": [ { "image": { "source": { "imageUri": "%s" } }, "features": [ { "type": "TEXT_DETECTION" } ] } ] } ' % (image_uri))
    KEY = os.getenv("myKey")
    print(KEY)
    # os.go()
    target_url = "https://vision.googleapis.com/v1/images:annotate?key=" + os.getenv("myKey")

    try:
        r = requests.post(target_url, headers=headers, json = data_payload)
        results = r.text
        results = json.loads(results)
        results = results["responses"][0]["textAnnotations"][0]["description"]
    except KeyError:
        # For some reason, the first API call sometimes returns nothing, but when the API is called again everything is fine
        r = requests.post(target_url, headers=headers, json = data_payload)
        results = r.text
        results = json.loads(results)
        results = results["responses"][0]["textAnnotations"][0]["description"]

    urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', results)
    return(urls)
