from url_parse import *
import sys

def main():
    shortenedUrl = sys.argv[1]
    print('shortened url : ' + shortenedUrl)
    match1 = check_google_safebrowsing(shortenedUrl)
    check_json_google(match1)
    fullUrl = unshorten_url(shortenedUrl)
    print('full url : ' + fullUrl)
    match2 = check_google_safebrowsing(fullUrl)
    check_json_google(match2)


if __name__ == "__main__":
    main()

'''
Instruction :

$ python3 test_url.py <url here>

'''
