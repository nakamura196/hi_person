import sys
import bs4
import hashlib
import json
import bs4
import requests
import time
import os
import urllib.parse
import csv
import glob
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace



rows = []

rows.append(["year", "count", "title", "text"])

files = glob.glob("../../docs/entity/time/*.json")

map = {}

for file in files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)[0]

    # print(json_load)

    descriptions = []
    
    for obj in json_load["http://schema.org/description"]:
        descriptions.append(obj["@value"])

    description = "<br/>".join(descriptions)

    start = json_load["https://jpsearch.go.jp/term/property#start"][0]["@value"]

    map[start] = description

import csv

with open('data/result.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    map2 = {}


    for row in reader:
        year = row[0]
        count = row[1]

        map2[year] = count

    for year in sorted(map2):
        count = map2[year]

        yearInt = int(year)

        if yearInt > 1300 or yearInt < 1226:
            continue

        title = ""
        text = ""

        if year in map:
            title = year
            text = map[year]

        rows.append([year, count, title, text])

with open('data/story.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows)