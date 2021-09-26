from bs4 import BeautifulSoup
import requests
import pandas as pd
from scraps import *

results = pd.DataFrame(columns=['title', 'link','size','age','seeds','source','torrent'])

sitesStructures = {
    "Kickass" :
    {
        "url_base": "https://kickass.cd",
        "url_preffix": "/usearch/",
        "url_suffix": "/",
        "space_string": "%20"
    },
    "1337x" :
    {
        "url_base": "https://www.1377x.to",
        "url_preffix": "/search/",
        "url_suffix": "/1/",
        "space_string": "%20"
    }}

search = input("Rechercher: ")

for site in sitesStructures:
    print(site)
    url_base = sitesStructures[site]["url_base"]
    url_preffix = sitesStructures[site]["url_preffix"]
    url_suffix = sitesStructures[site]["url_suffix"]
    space_string = sitesStructures[site]["space_string"]

    url = url_base+url_preffix+search.replace(" ", space_string)+url_suffix
    result = requests.get(url)

    soup = BeautifulSoup(result.content, "lxml")

    for t in eval("scrap_"+site+"(soup)"):
        results = results.append(t, ignore_index=True)

print(results)