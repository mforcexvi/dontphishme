import requests
import json
import re
from dotenv import load_dotenv
import os
from pyzbar.pyzbar import decode
from PIL import Image
load_dotenv()
import time


def run_ocr(image_uri):
    headers = {'Accept': 'application/json', 'Content-type': 'application/json'}
    print(image_uri)
    data_payload = json.loads('{ "requests": [ { "image": { "source": { "imageUri": "%s" } }, "features": [ { "type": "TEXT_DETECTION" } ] } ] } ' % (image_uri))
    # data_payload = json.loads('{ "requests": [ { "image": { "content": "%s" }, "features": [ { "type": "TEXT_DETECTION" } ] } ] } ' % (image_uri))

    KEY = os.getenv("myKey")
    print(KEY)
    # os.go()
    target_url = "https://vision.googleapis.com/v1/images:annotate?key=" + os.getenv("myKey")

    time.sleep(10)

    try:
        r = requests.post(target_url, headers=headers, json = data_payload)
        results = r.text
        results = json.loads(results)
        results = results["responses"][0]["textAnnotations"][0]["description"]
    except:
        # For some reason, the first API call sometimes returns nothing, but when the API is called again everything is fine
        r = requests.post(target_url, headers=headers, json = data_payload)
        results = r.text
        results = json.loads(results)
        try:
            results = results["responses"][0]["textAnnotations"][0]["description"]
        except:
            print(results)
            return([None])

    urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', results)
    print(urls)
    return(urls)

def decode_qr(filepath):
    results_list = decode(Image.open(filepath))
    print(results_list)
    try:
        result_string = results_list[0][0].decode("utf-8")
        return result_string
    except:
        return "None"
