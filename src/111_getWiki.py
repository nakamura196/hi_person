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

def main(url):
    time.sleep(0.5)
    res = requests.get(url).json()

    print(url)

    obj = {}

    uri = url.replace("/data/", "/resource/").replace(".json", "")

    for key in res:
        if uri == key:
            obj = res[key]

    if "http://dbpedia.org/ontology/wikiPageRedirects" in obj:
        link = obj["http://dbpedia.org/ontology/wikiPageRedirects"][0]["value"]
        link = link.replace("/resource/", "/data/") + ".json"
        obj = main(link)

    return obj

def main2(term):
    url = "http://ja.dbpedia.org/data/"+term + ".json"

    path = "data/wiki/"+term+".json"

    if os.path.exists(path):
        return

    description = main(url)

    if description == None:
        return

    f2 = open(path, 'w')
    json.dump(description, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

with open('../../hi_kokiroku/test/data/person.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    arr = []

    for row in reader:
        label = row[2]

        if "、" not in label:
            continue

        if label == "":
            continue

        labelSpl = label.split("、")

        label2 = labelSpl[0] + "（" + labelSpl[1] + "）"

        label3 = labelSpl[1] + labelSpl[0] 
        label3 = label3.replace(" ", "").replace("?", "_")

        if label3 not in arr:

            arr.append(label3)

    for i in range(len(arr)):

        print(i+1, len(arr))

        label3 = arr[i]

        main2(label3)
    