from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import requests
import sys
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Search for open ports on different IP ranges using masscan")
    parser.add_argument("-p", "--port", required=True)
    parser.add_argument("-c", "--c_parse", default=1, type=int, help="Number of URIs to be received")
    parser.add_argument("-d", "--date", default=datetime.now().date(), help="Scan date in yyyy-mm-dd format")
    parser.add_argument("-o", "--output", action="store_true")
    return parser.parse_args()

def fill_URI_list(URL, date):
    URI_list = []
    for tr in page.find_all('tr'):
        if (tr.find('a') == None):
            continue
        if (tr.find(align='right').get_text().find(str(date)) != -1):
            URI_list.append(URL + tr.find('a').get_text())
    print(f"Received {len(URI_list)} links")
    return URI_list

def c_parse(URI_list):
    for c in range(args.c_parse):
        print("Parse " + URI_list[c])
        parse(URI_list[c])

def parse(URI):
    req = requests.get(URI)
    for line in req.text.splitlines():
        if re.search('open tcp ' + args.port, line):
            print(line)

if __name__ == '__main__':
    URL = 'https://masspull.org/data/'
    args=parse_args()
    req_get = requests.get(URL)
    page = BeautifulSoup(req_get.content, 'html.parser')
    URI_list = fill_URI_list(URL, args.date)
    if args.c_parse > len(URI_list):
        print(f"Too many count. The number of links should not exceed {len(URI_list)}")
        sys.exit(1)
    if args.output:
        with open('result.txt', 'a') as res:
            sys.stdout = res
            c_parse(URI_list)
    else:
        c_parse(URI_list)
