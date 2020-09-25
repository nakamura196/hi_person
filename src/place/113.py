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

import geohash2

all = Graph()

aaa = URIRef("https://nakamura196.github.io/hi_person/term/type/Place.json")

stmt = (aaa, RDF.type, RDFS.Class)
all.add(stmt)

stmt = (aaa, RDFS.label, Literal("Place"))
all.add(stmt)

stmt = (aaa, RDFS.comment, Literal("場所を表す実体。"))
all.add(stmt)

url = "https://raw.githubusercontent.com/utda/kunshujo/master/src/data/map.json"

data = requests.get(url).json()

rows = []
rows.append(["Name", "Location"])

for obj in data:
    lat = obj["http://www.w3.org/2003/01/geo/wgs84_pos#lat"][0]["@value"]
    ln = obj["http://www.w3.org/2003/01/geo/wgs84_pos#long"][0]["@value"]

    print(lat, ln)

    uri = "http://geohash.org/" + (geohash2.encode(lat, ln))

    lat = str(lat)
    ln = str(ln)

    subject = URIRef(uri)

    stmt = (subject, URIRef("http://schema.org/latitude"), Literal(lat))

    all.add(stmt)

    stmt = (subject, URIRef("http://schema.org/longitude"), Literal(ln))

    all.add(stmt)

    label = obj["http://www.w3.org/2000/01/rdf-schema#label"][0]["@value"]

    rows.append([label, lat+","+ln])

    uri2 = "https://nakamura196.github.io/hi_person/entity/place/" + label + ".json"

    subject2 = URIRef(uri2)

    stmt = (subject2, URIRef("http://schema.org/geo"), subject)

    all.add(stmt)

    stmt = (subject2, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label))
    all.add(stmt)

    stmt = (subject2, URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso"), URIRef(obj["@id"]))
    all.add(stmt)

    stmt = (subject2, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), aaa)
    all.add(stmt)

path = "data/all.rdf"
all.serialize(destination=path, format='pretty-xml')

with open('data/p.csv', 'w') as f:
    writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
    writer.writerows(rows)