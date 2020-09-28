from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import xml.etree.ElementTree as ET
import sys
import urllib
import json
import argparse
import urllib.request
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
import glob
import requests
import os

"""
Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = '1WxMz4mX9Cvr0NC7Ql35Mq7kx2jZCml4qdtbxhp4aI9c'

# Call the Sheets API
def read_data(spreadId, rangeName, service):
    SPREADSHEET_ID = spreadId
    RANGE_NAME = rangeName
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    return result

sheets = ["機関"] # , "abc"

all = Graph()

def bbb(value):

    flg = False

    if value.startswith("http"):
        flg = True

    if value.startswith("_:"):
        flg = True

    map = {
        "jps" : "https://jpsearch.go.jp/term/property#",
        "schema" : "http://schema.org/", 
        "prop-ja" : "http://ja.dbpedia.org/property/",
        
        "emperor" : "https://nakamura196.github.io/hi_person/entity/emperor/",
        "wiki": "https://ja.wikipedia.org/wiki/",
        "kani" : "https://nakamura196.github.io/hi_person/term/kani/",
        "person" : "https://nakamura196.github.io/hi_person/entity/chname/",
        "role" : "https://nakamura196.github.io/hi_person/term/role/",
        "skos" : "http://www.w3.org/2004/02/skos/core#",
        "level" : "https://nakamura196.github.io/hi_person/term/level/",
        "place" : "https://nakamura196.github.io/hi_person/entity/place/",
        "rdf" : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs" : "http://www.w3.org/2000/01/rdf-schema#",
        "type" : "https://nakamura196.github.io/hi_person/term/type/",
        "keyword" : "https://nakamura196.github.io/hi_person/term/keyword/",
        "word" : "https://kotobank.jp/word/",
    }

    for key in map:
        if key+":" in value:
            flg = True
            value = value.replace(key+":", map[key])

            if key in ["emperor", "kani", "person", "role", "level", "place", "type", "keyword"]:
                value += ".json"


    '''
    if flg:
        value = URIRef(value)
    else:
        value = Literal(value)
    '''

    return value

for sheetname in sheets:

    g = Graph()

    flg = False

    result = read_data(spreadsheet_id, sheetname + "!A1:Z1000", service)

    values = result["values"]

    subject_str = "https://nakamura196.github.io/hi_person/entity/chname/"+sheetname+".json"

    subject = URIRef(subject_str)

    map = {}

    arr = []

    c_count = len(values[0])
    r_count = len(values)

    for i in range(1, c_count):
        label = ""
        try:
            label = values[0][i]
        except Exception as e:
            print(e)

        uri = ""
        try:
            uri = values[1][i]
        except Exception as e:
            print(e)

        
        type = values[2][i]
        
        if type != "":
            obj = {}
            map[i] = obj
            obj["label"] = label
            obj["uri"] = uri
            obj["type"] = type

    for j in range(3, r_count):

        try:
            subject = values[j][0]
        except Exception as e:
            print(e)
            continue

        subject = bbb(subject)
        subject = URIRef(subject)

        for i in map:
            
            value = values[j][i]

            if value == "end":
                continue

            if value != "":

                obj = map[i]
                p = URIRef(obj["uri"])

                value = bbb(value)

                if obj["type"].upper() == "RESOURCE":
                    all.add((subject, p, URIRef(value)))
                else:
                    all.add((subject, p, Literal(value)))    

# print(all)
all.serialize(destination="data/org.rdf", format='pretty-xml')
# print(all.serialize(format="turtle").decode("utf-8"))