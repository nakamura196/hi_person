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



all = Graph()

t = "https://nakamura196.github.io/hi_person/term/type/Emperor.json"

subject = URIRef(t)

stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal("Emperor"))

all.add(stmt)

stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/2000/01/rdf-schema#Class"))

all.add(stmt)

path = t.replace("https://nakamura196.github.io/hi_person", "../docs")

dirname = os.path.dirname(path)

os.makedirs(dirname, exist_ok=True)

all.serialize(destination=path, format='json-ld')
        
with open('data/emperor.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    # arr = []

    map = {}

    for row in reader:
        label = row[0]
        image = row[1]
        start = row[2]
        end = row[3]

        id = "https://nakamura196.github.io/hi_person/entity/emperor/" + label + ".json"

        g = Graph()

        subject = URIRef(id)

        stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label))

        g.add(stmt)
        all.add(stmt)
        
        stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(t))

        g.add(stmt)
        all.add(stmt)

        stmt = (subject, URIRef("https://jpsearch.go.jp/term/property#start"), Literal(start))

        g.add(stmt)
        all.add(stmt)

        stmt = (subject, URIRef("https://jpsearch.go.jp/term/property#end"), Literal(end))

        g.add(stmt)
        all.add(stmt)

        if image != "":
            stmt = (subject, URIRef("http://schema.org/image"), URIRef(image))

            g.add(stmt)
            all.add(stmt)

        path = id.replace("https://nakamura196.github.io/hi_person", "../docs")

        dirname = os.path.dirname(path)

        os.makedirs(dirname, exist_ok=True)

        g.serialize(destination=path, format='json-ld')



path = "data/emperor.json"


all.serialize(destination=path.replace(".json", ".rdf"), format='pretty-xml')