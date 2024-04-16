import requests
import argparse
import os
import sys
import time
from huepy import *
from core import requester
from core import extractor
from core import crawler
from urllib.parse import unquote
from tqdm import tqdm

start_time = time.time()

def clear():
    if 'linux' in sys.platform:
        os.system('clear')
    elif 'darwin' in sys.platform:
        os.system('clear')
    else:
        os.system('cls')

def banner():
    ban = '''
███████╗███╗   ███╗ █████╗ ███████╗
██╔════╝████╗ ████║██╔══██╗██╔════╝
███████╗██╔████╔██║███████║███████╗
╚════██║██║╚██╔╝██║██╔══██║╚════██║
███████║██║ ╚═╝ ██║██║  ██║███████║
╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝        
                          by Zierax
    '''

    print(red(ban))

def concatenate_list_data(list_data, result):
    if result is None:
        result = ""
    for element in list_data:
        result = result + "\n" + str(element)
    return result

def main():
    try:
        parser = argparse.ArgumentParser(description='SMAS - a sqli scanner tool')
        parser.add_argument('-d', '--domain', help='Domain name of the target [ex. example.com]', required=True)
        parser.add_argument('-s', '--subs', help='Set false or true [ex: --subs False]', default=False)
        parser.add_argument('-p', '--proxy', help='Proxy server address (e.g., http://127.0.0.1:8080)', default=None)
        parser.add_argument('-v', '--verbose', help='Enable verbose output', action='store_true')
        args = parser.parse_args()

        if args.subs == True:
            url = f"http://web.archive.org/cdx/search/cdx?url=*.{args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"
        else:
            url = f"http://web.archive.org/cdx/search/cdx?url={args.domain}/*&output=txt&fl=original&collapse=urlkey&page=/"

        clear()
        banner()

        proxies = None
        if args.proxy:
            proxies = {'http': args.proxy, 'https': args.proxy}

        if args.verbose:
            print(f"Using Wayback Machine URL: {url}")
            print(f"Proxy settings: {proxies}")

        response = requester.get_wayback_data(url)
        crawled_urls = crawler.spider(f"http://{args.domain}", 10)
        response = concatenate_list_data(crawled_urls, response)

        if response == False:
            return

        response = unquote(response)

        print("\n" + "[" + blue("INF") + "] " + f" Scanning sqli for {args.domain}")

        file = open('payloads.txt', 'r')
        payloads = file.read().splitlines()

        vulnerable_urls = []

        for uri in tqdm(crawled_urls, desc="Scanning URLs", unit="URL"):
            for payload in payloads:
                final_url = uri + payload

                if not final_url.startswith("http://") and not final_url.startswith("https://"):
                    final_url = "http://" + final_url  # Assuming HTTP as default scheme

                try:
                    if args.verbose:
                        print(f"Sending request to: {final_url}")

                    req = requests.get(final_url, proxies=proxies)

                    res = req.text

                    if 'SQL' in res or 'sql' in res or 'Sql' in res:
                        print("[" + green("sql-injection") + "] " + final_url)
                        break

                except KeyboardInterrupt:
                    print(red("\nSee u Later"))
                    sys.exit(1)

                except requests.exceptions.ProxyError as e:
                    print(red("\nProxy Error:", str(e)))
                    sys.exit(1)

    except KeyboardInterrupt:
        print(red("\nSee u Later"))
        sys.exit(1)

if __name__ == "__main__":
    main()
