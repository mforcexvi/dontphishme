from modules.url_parse import *
# import url_parse
import sys
import base64

def main():
    shortenedUrl = sys.argv[1]
    print('shortened url : ' + shortenedUrl)
    match1 = check_google_safebrowsing(shortenedUrl)
    check_json_google(match1)
    fullUrl = unshorten_url(shortenedUrl)
    print('full url : ' + fullUrl)
    match2 = check_google_safebrowsing(fullUrl)
    return check_json_google(match2)

def expand_url(input_string):
    fullUrl = unshorten_url(input_string)
    return str(fullUrl)

def test_long_url(input_string):
    fullUrl = input_string
    print('full url : ' + fullUrl)
    match2 = check_google_safebrowsing(fullUrl)
    return check_json_google(match2)

def test_url(input_string):
    # shortenedUrl = input_string
    # # shortenedUrl = base64.b64decode(input_string).decode("utf-8")
    # print('shortened url : ' + shortenedUrl)
    # match1 = check_google_safebrowsing(shortenedUrl)
    # check_json_google(match1)
    fullUrl = input_string
    print('full url : ' + fullUrl)
    match2 = check_google_safebrowsing(fullUrl)
    return check_json_google(match2)

if __name__ == "__main__":
    main()

'''
Instruction :

$ python3 test_url.py <url here>

'''
