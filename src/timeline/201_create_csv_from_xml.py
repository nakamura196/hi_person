import sys
import bs4
import hashlib
import json

inputpath = "../../../hi_kokiroku/data/tei/E16 - 民経記.xml"

soup = bs4.BeautifulSoup(open(inputpath), 'xml')

divs = soup.find("body").find_all("div")

rows = []
rows.append(["year", "vol", "count"])

map = {}

for div in divs:
    rend = div.get("rend")

    if rend == None:
        continue

    date = rend.split(";")[0].split(": ")[1]

    vol = rend.split(";")[1].split(": ")[1]

    year = date[0:4]

    if year not in map:
        map[year] = {
            "count" : 0,
            "words" : 0
        }

    count = len(div.text)

    map[year]["count"] += 1
    map[year]["words"] += count

    

    # rows.append([year, vol, count])

for year in map:
    obj = map[year]
    rows.append([year,obj["count"] , obj["words"]])

import csv

with open('data/result.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows) # 2次元配列も書き込める