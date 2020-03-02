import urllib.request
from bs4 import BeautifulSoup
import sys
import config

inp = input("Choose table of winrates! (global, solo, duo, trio): ")
if inp == "global":
    url = config.global_url
    db = "all_winrates"
elif inp == "solo":
    url = config.solo_url
    db = "winrates_solo"
elif inp == "duo":
    url = config.duo_url
    db = "winrates_duo"
elif inp == "trio":
    url = config.trio_url
    db = "winrates_trio"
else:
    print("Url is invalid!")
    sys.exit()
    

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parce(html):
    soup = BeautifulSoup(html)
    table = soup.find("table", class_="table_dark")
    heroes = []

    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        heroes.append({
            'heroname_as_dotaname' : cols[0].text,
            "picks" : cols[1].text,
            "wins" : cols[2].text,
            "winrate" : cols[3].text.strip("%"),
            "pickrate" : cols[4].text.strip("%")
        })
    return heroes


def main():
    print(parce(get_html(url)))

if __name__ == "__main__":
    main()
