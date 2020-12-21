import os
from urllib.parse import urljoin
from urllib.request import Request, urlopen

BASE_URL = "https://purge.jsdelivr.net/gh/linepro6/PrincessConnectReDiveCharactersJson@release/"

def main():
    list = os.listdir("./release/")
    for name in list:
        print(f"flushing {name}...")
        resp = urlopen(Request(urljoin(BASE_URL, name))).read().decode('utf-8')
        print(resp)

if __name__ == "__main__":
    main()