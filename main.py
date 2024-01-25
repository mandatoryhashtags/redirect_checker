import requests
import logging
import argparse
from datetime import datetime
from http.client import HTTPConnection


def write_to_file(data, file_path):
    with open(file_path, 'a') as file:
        file.write(data)
        file.write('\n')


def main():
    global last_url
    parser = argparse.ArgumentParser(description='URL Checker')
    parser.add_argument(
        'debug', help='Enable debug mode (0 for No, 1 for Yes)', type=int)
    parser.add_argument('read_file', help='File to read URLs from', type=str)
    parser.add_argument(
        'write_file', help='File to write results to', type=str)
    args = parser.parse_args()

    if args.debug == 1:
        print('In Debug Mode')
        log = logging.getLogger('urllib3')
        log.setLevel(logging.DEBUG)
        HTTPConnection.debuglevel = 1
    else:
        print('Not in Debug Mode')
        HTTPConnection.debuglevel = 0
        log = logging.getLogger('urllib3')
        log.setLevel(logging.CRITICAL)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG if args.debug == 1 else logging.CRITICAL)
    log.addHandler(ch)

    start_time = datetime.now()

    print(f'{start_time} Starting Now')

    with open(args.read_file, 'r') as url_entries:
        headers = {
            'User-Agent': 'curl/8.4.0',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'cookie': ''
        }

        for url in url_entries:
            url = url.strip()  # Remove newline characters
            last_url = url
            session = requests.Session()
            r = session.get(url, timeout=60, headers=headers,
                            allow_redirects=True)

            if args.debug == 1:
                print(f"Testing {url}")
                print(r.status_code)

            if r.status_code == 404:
                write_to_file(url + '\n', args.write_file)

    print('Finished running URLs')
    print(datetime.now() - start_time)


def exit_gracefully():
    print(f'The last URL touched was {last_url}')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        exit_gracefully()
