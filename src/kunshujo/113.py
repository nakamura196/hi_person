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

import json

json_open = open('data/data.json', 'r')
d = json.load(json_open)

for obj in d:
    if "http://purl.org/dc/terms/spatial" in obj:
        value = obj["http://purl.org/dc/terms/spatial"][0]["@id"]
        value = value.replace("http://ja.dbpedia.org/resource/", "https://nakamura196.github.io/hi_person/entity/place/") + ".json"
        obj["http://purl.org/dc/terms/spatial"][0]["@id"] = value

    title = obj["http://purl.org/dc/terms/title"][0]["@value"]
    obj["http://www.w3.org/2000/01/rdf-schema#label"] = [{
        "@value" : title
    }]

    title = obj["http://xmlns.com/foaf/0.1/thumbnail"][0]["@id"]
    obj["http://schema.org/image"] = [{
        "@id" : title
    }]

'''
f2 = open("data/new.json", 'w')
json.dump(d, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))
'''

all = Graph()
all.parse("data/new.json", format="json-ld")
all.serialize(destination="data/new.rdf", format='pretty-xml')
