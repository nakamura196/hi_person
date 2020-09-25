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

rows.append(["Year", "Month", "Day", "Time", "Year", "Month", "Day", "Time", "Display Date", "Headline", "Text", "Media", "Media Credit", "Media Caption", "Media Thubmnail", "Type", "Group"])


files = glob.glob("../../docs/entity/shogunate/*.json")
for file in files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)[0]

    # print(json_load)

    label = json_load["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]

    start = json_load["https://jpsearch.go.jp/term/property#start"][0]["@value"]
    start_s = start.split("-")

    end = json_load["https://jpsearch.go.jp/term/property#end"][0]["@value"]
    end_s = end.split("-")

    image = ""

    if "http://schema.org/image" in json_load:
        image = json_load["http://schema.org/image"][0]["@id"]

    rows.append([start_s[0], start_s[1], start_s[2], "", end_s[0], end_s[1], end_s[2], "", "", label, "", image, "", "", image, "", "将軍"])

files = glob.glob("../../docs/entity/emperor/*.json")
for file in files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)[0]

    # print(json_load)

    label = json_load["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]

    start = json_load["https://jpsearch.go.jp/term/property#start"][0]["@value"]

    end = json_load["https://jpsearch.go.jp/term/property#end"][0]["@value"]

    image = ""

    rows.append([start, "", "", "", end, "", "", "", "", label, "", image, "", "", image, "", "天皇"])

files = glob.glob("../../docs/entity/time/*.json")
for file in files:
    json_open = open(file, 'r')
    json_load = json.load(json_open)[0]

    # print(json_load)

    descriptions = []
    
    for obj in json_load["http://schema.org/description"]:
        descriptions.append(obj["@value"])

    description = "<br/>".join(descriptions)

    start = json_load["https://jpsearch.go.jp/term/property#start"][0]["@value"]

    end = json_load["https://jpsearch.go.jp/term/property#end"][0]["@value"]

    image = ""

    rows.append([start, "", "", "", end, "", "", "", "", "", description, image, "", "", image, "", "出来事"])


with open('data/timeline.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows)