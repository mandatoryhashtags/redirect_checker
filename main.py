import requests
import logging
import argparse
from datetime import datetime
from http.client import HTTPConnection

parser = argparse.ArgumentParser('main')
parser.add_argument(
    "debug", help="Needs debug mode. 0 No, 1", type=int)
parser.add_argument(
    "read_file", help="File to read urls from", type=str)
parser.add_argument(
    "write_file", help="File to write to", type=str)

args = parser.parse_args()
ch = logging.StreamHandler()
log = logging.getLogger('urllib3')
start_time = datetime.now()
url_entries = open(args.read_file, 'r')


def write_to_file(data):
    file = open(args.write_file, 'a')
    file.write(data)
    file.close()


if args.debug == 1:
    print('In Debug Mode')
    log.setLevel(logging.DEBUG)
    HTTPConnection.debuglevel = 1
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
else:
    print('Not in Debug Mode')
    HTTPConnection.debuglevel = 0
    log.setLevel(logging.CRITICAL)
    ch.setLevel(logging.CRITICAL)


print(f'{start_time} Starting Now')
for url in url_entries:
    url = url.replace('\n', '')
    headers = {'User-Agent': 'curl/8.4.0',
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
               "accept-language": "en-US,en;q=0.9",
               "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
               "sec-ch-ua-mobile": "?0",
               "sec-ch-ua-platform": "\"macOS\"",
               "sec-fetch-dest": "document",
               "sec-fetch-mode": "navigate",
               "sec-fetch-site": "none",
               "sec-fetch-user": "?1",
               "upgrade-insecure-requests": "1",
               "cookie": ""
               }
    session = requests.Session()
    r = session.get(url, timeout=60, headers=headers, allow_redirects=True)

    if args.debug == 1:
        print(f"Testing {url}")
        print(r.status_code)

    if r.status_code == 404:
        write_to_file(url)

print('Finished running URLs')
print(datetime.now() - start_time)
