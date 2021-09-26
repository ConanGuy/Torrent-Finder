import datetime
from bs4 import BeautifulSoup
import requests

def get_age(date) -> int:
    return (datetime.datetime.today() - date).days

def scrap_Kickass(soup, maxRes) -> list:

    torrents_links = soup.find_all("tr", class_="odd")

    torrents = []

    for t in torrents_links[:min(len(torrents),maxRes)]:
        source = "Kickass"
        title = t.find("a", class_="cellMainLink").text
        link = "https://kickass.cd"+t.find("a", class_="cellMainLink")["href"]
        size = t.find("td", class_="nobr center").text[1:].replace(u'\xa0', " ").strip()
        seeds = t.find("td", class_="green center").text

        date = t.select("td[class='center']")[0].text[1:].replace("-", "/")
        if ':' in date:
            date = date[:5]+"/"+str(datetime.datetime.today().year)
        else:
            date = date.replace(u'\xa0', "/")
        age = str(get_age(datetime.datetime.strptime(date, "%m/%d/%Y")))+" days"

        torrent = t.find("a", title="Download torrent file")["href"]

        result = {
            "title": title,
            "link": link,
            "size": size,
            "age": age,
            "seeds": seeds,
            "source": source,
            "torrent": torrent
        }

        torrents.append(result)

    return torrents
    
def scrap_1337x(soup, maxRes) -> list:
    torrents_links = soup.find("table", class_="table-list table table-responsive table-striped").find_all("tr")[1:]

    torrents = []

    for t in torrents_links[:min(len(torrents),maxRes)]:
        source = "1337x"
        title = t.find("td", class_="coll-1 name").text[1:]
        link = "https://www.1377x.to/"+t.find("td", class_="coll-1 name").find_all("a")[1]["href"]
        size = t.find("td", class_="coll-4 size mob-uploader").text
        seeds = t.find("td", class_="coll-2 seeds").text
        date = t.find("td", class_="coll-date").text.replace("3rd ", "3th ").replace("2nd ", "2th ").replace("1st ", "1th ")
        age = str(get_age(datetime.datetime.strptime(date, "%b. %dth '%y")))+" days"

        t_soup = BeautifulSoup(requests.get(link).content, "lxml")
        torrent = t_soup.find("a", href=lambda x: "magnet:" in x)["href"]

        result = {
            "title": title,
            "link": link,
            "size": size,
            "age": age,
            "seeds": seeds,
            "source": source,
            "torrent": torrent
        }

        torrents.append(result)

    return torrents
    
def scrap_Torlock(soup, maxRes) -> list:

    torrents = []
    torrents_links = soup.find_all("table", class_="table-condensed")[-1].find_all("tr")

    for t in torrents_links[:maxRes]:
        source = "Torlock"
        title = t.find("td").text
        link = "https://www.torlock.com/"+t.find("td").a["href"]
        size = t.find("td", class_="ts").text
        seeds = t.find("td", class_="tul").text
        date = t.find("td", class_="td").text
        age = str(get_age((datetime.datetime.strptime(date, "%m/%d/%Y")) if "Today" not in date else datetime.datetime.today()))+" days"

        t_soup = BeautifulSoup(requests.get(link).content, "lxml")
        torrent = ""
        for tor in t_soup.find_all("a"):
            try:
                if "magnet:" in tor["href"]:
                    torrent = tor["href"]
                    break
            except:
                pass
            
        result = {
            "title": title,
            "link": link,
            "size": size,
            "age": age,
            "seeds": seeds,
            "source": source,
            "torrent": torrent
        }

        torrents.append(result)

    return torrents
