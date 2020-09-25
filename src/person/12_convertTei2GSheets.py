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

spreadsheet_id = '1FX92zyp916uZBwoosE4oaXNBR0MeGay0l30SvHl5PFQ'

# Call the Sheets API
def read_data(spreadId, rangeName, service):
    SPREADSHEET_ID = spreadId
    RANGE_NAME = rangeName
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=RANGE_NAME).execute()
    return result

sheets = ["藤原経光"] # , "abc"

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
        "word" : "https://kotobank.jp/word/",
        "emperor" : "https://nakamura196.github.io/hi_person/entity/emperor/",
        "wiki": "https://ja.wikipedia.org/wiki/",
        "kani" : "https://nakamura196.github.io/hi_person/term/kani/",
        "person" : "https://nakamura196.github.io/hi_person/entity/chname/",
        "role" : "https://nakamura196.github.io/hi_person/term/role/"
    }

    for key in map:
        if key+":" in value:
            flg = True
            value = value.replace(key+":", map[key])

            if key in ["emperor", "kani", "person", "role"]:
                value += ".json"



    if flg:
        value = URIRef(value)
    else:
        value = Literal(value)

    return value

for sheetname in sheets:

    flg = False

    result = read_data(spreadsheet_id, sheetname + "!A1:D1000", service)

    values = result["values"]

    subject_str = "https://nakamura196.github.io/hi_person/entity/chname/"+sheetname+".json"

    subject = URIRef(subject_str)

    map = {}

    for i in range(1, len(values)):
        row = values[i]


        v = row[0]

        if v == "":
            continue

        if v == "prop-ja:官位":
            flg = True

        v = bbb(v)
        o = row[1]
        

        v2 = None
        o2 = None

        if not flg:
            o = bbb(o)
            all.add((subject, v, o))

        else:
            o = values[i][1]

            map[o] = []

            for j in range(0, 6):
                row1 = values[i+j]

                if len(row1) < 4:
                    continue

                p = row1[2]

                values1 = row1[3].split("|")

                for value1 in values1:
                    map[o].append({
                        "v" : bbb(p),
                        "o" : bbb(value1)
                    })

    for key in map:
        b = BNode()
        v = URIRef(bbb("prop-ja:官位"))
        # v = URIRef(bbb("jps:agential"))
        # b = URIRef(bbb(subject_str+"#"+str(key).zfill(2)))
        b = URIRef(bbb("_:"+sheetname+"_官位_"+str(key).zfill(3)))
        all.add((subject, v, b))

        for obj in map[key]:
            all.add((b, obj["v"], obj["o"]))

    # print(result)

# print(all)
all.serialize(destination="data/person.rdf", format='pretty-xml')
# print(all.serialize(format="turtle").decode("utf-8"))