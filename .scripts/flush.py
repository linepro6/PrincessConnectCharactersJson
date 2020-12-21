import os
import requests
from urllib.parse import urljoin

BASE_URL = "https://purge.jsdelivr.net/gh/linepro6/PrincessConnectReDiveCharactersJson@release/"

def main():
    list = os.listdir("./release/")
    for name in list:
        print(f"flushing {name}...")
        resp = requests.get(urljoin(BASE_URL, name))
        print(resp.json())

if __name__ == "__main__":
    main()