from bs4 import BeautifulSoup
import requests
import pandas as pd
from scraps import *
from consts import *

def main():
    results = pd.DataFrame(columns=['title', 'link','size','age','seeds','source','torrent'])
    search = input("Rechercher: ")

    # for site in sitesStructures:
    for site in SITE_STRUCTURE:
        print(site)

        siteDict = SITE_STRUCTURE[site]

        url_base = siteDict["url_base"]
        url_preffix = siteDict["url_preffix"]
        url_suffix = siteDict["url_suffix"]
        space_string = siteDict["space_string"]

        url = url_base+url_preffix+search.replace(" ", space_string)+url_suffix
        result = requests.get(url)

        soup = BeautifulSoup(result.content, "lxml")

        for t in eval("scrap_"+site+"(soup, MAX_RESULTS_PER_SITE)"):
            results = results.append(t, ignore_index=True)

    print(results)

if __name__ == "__main__":
    results = main()
    print(results)