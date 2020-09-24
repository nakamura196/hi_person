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

files = glob.glob("data/kotobank_kani/*.json")

arr = []

all = Graph()

t = "https://nakamura196.github.io/hi_person/term/type/Kani.json"

subject = URIRef(t)

stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal("官位"))

all.add(stmt)

stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef("http://www.w3.org/2000/01/rdf-schema#Class"))

all.add(stmt)

path = t.replace("https://nakamura196.github.io/hi_person", "../docs")

dirname = os.path.dirname(path)

os.makedirs(dirname, exist_ok=True)

all.serialize(destination=path, format='json-ld')

for file in files:
    filename = os.path.splitext(os.path.basename(file))[0]
    id = "https://nakamura196.github.io/hi_person/term/kani/" + filename + ".json"

    json_open = open(file, 'r')
    json_load = json.load(json_open)

    g = Graph()

    subject = URIRef(id)

    stmt = (subject, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(filename))

    g.add(stmt)
    all.add(stmt)

    stmt = (subject, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), URIRef(t))

    g.add(stmt)
    all.add(stmt)

    if "description" in json_load:

        stmt = (subject, URIRef("http://schema.org/description"), Literal(json_load["description"]))

        g.add(stmt)
        all.add(stmt)

        stmt = (subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(json_load["url"]))

        g.add(stmt)
        all.add(stmt)

        url = json_load["url"]

        if "-" in url:
            name = url.split("/")[-1].split("-")[0]

            stmt = (subject, URIRef("http://schema.org/name"), Literal(name))

            g.add(stmt)
            all.add(stmt)

    json_open = open(file, 'r')
    json_load2 = json.load(json_open)

    path2 = "data/wiki_kani/"+filename+".json"

    try:
        json_open = open(path2, 'r')
        json_load2 = json.load(json_open)


        if "http://dbpedia.org/ontology/abstract" in json_load2:

            stmt = (subject, URIRef("http://schema.org/description"), Literal(json_load2["http://dbpedia.org/ontology/abstract"][0]["value"]))

            g.add(stmt)
            all.add(stmt)

            uri2 = json_load2["http://xmlns.com/foaf/0.1/isPrimaryTopicOf"][0]["value"]
            stmt = (subject, URIRef("http://www.w3.org/2002/07/owl#sameAs"), URIRef(uri2))

            g.add(stmt)
            all.add(stmt)

            label2 = uri2.split("/")[-1]
            if label2 != filename:

                stmt = (subject, URIRef("http://schema.org/name"), Literal(label2))

                g.add(stmt)
                all.add(stmt)

    except Exception as e:
        print(e)

    path = id.replace("https://nakamura196.github.io/hi_person", "../docs")

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    g.serialize(destination=path, format='json-ld')



path = "data/kani.json"

all.serialize(destination=path.replace(".json", ".rdf"), format='pretty-xml')