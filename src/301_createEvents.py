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

with open('data/events.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    # arr = []

    map = {}

    for row in reader:
        year = row[0]
        desc = row[3]

        if year not in map:
            map[year] = []

        map[year].append(desc)

all = Graph()

t = "https://nakamura196.github.io/hi_person/term/type/Time.json"

subject = URIRef(t)

stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal("Time"))

all.add(stmt)

stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/2000/01/rdf-schema#Class"))

all.add(stmt)

path = t.replace("https://nakamura196.github.io/hi_person", "../docs")

dirname = os.path.dirname(path)

os.makedirs(dirname, exist_ok=True)

all.serialize(destination=path, format='json-ld')
        

for year in map:

    id = "https://nakamura196.github.io/hi_person/entity/time/" + year + ".json"

    g = Graph()

    subject = URIRef(id)

    stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(year+"年"))

    g.add(stmt)
    all.add(stmt)
    
    stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(t))

    g.add(stmt)
    all.add(stmt)

    stmt = (subject, URIRef("http://schema.org/startDate"), Literal(year, datatype=XSD.gYear))

    g.add(stmt)
    all.add(stmt)

    stmt = (subject, URIRef("http://schema.org/endDate"), Literal(year, datatype=XSD.gYear))

    g.add(stmt)
    all.add(stmt)

    stmt = (subject, URIRef("https://jpsearch.go.jp/term/property#start"), Literal(year))

    g.add(stmt)
    all.add(stmt)

    stmt = (subject, URIRef("https://jpsearch.go.jp/term/property#end"), Literal(year))

    g.add(stmt)
    all.add(stmt)

    arr = map[year]

    for value in arr:

        stmt = (subject, URIRef("http://schema.org/description"), Literal(value))

        g.add(stmt)
        all.add(stmt)

    path = id.replace("https://nakamura196.github.io/hi_person", "../docs")

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    g.serialize(destination=path, format='json-ld')



path = "data/time.json"


all.serialize(destination=path.replace(".json", ".rdf"), format='pretty-xml')