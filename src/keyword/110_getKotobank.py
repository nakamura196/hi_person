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
    time.sleep(1)
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return {}
    soup = bs4.BeautifulSoup(res.text)

    description = soup.find(class_="description")

    if "⇒<a" in str(description):
        a = description.find("a").get("href")
        url = "https://kotobank.jp" + a
        return main(url)
    else:
        return {
            "description" : description.text.strip(),
            "url" : urllib.parse.unquote(url.split("#")[0])
        }

def main2(term):
    url = "https://kotobank.jp/word/"+term

    path = "data/kotobank/"+term+".json"

    if os.path.exists(path):
        return

    description = main(url)

    if description == None:
        return

    f2 = open(path, 'w')
    json.dump(description, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

url = "https://diyhistory.org/c.php/http://3.91.74.60:8890/sparql?query=PREFIX+jps%3A+%3Chttps%3A%2F%2Fjpsearch.go.jp%2Fterm%2Fproperty%23%3E%0D%0APREFIX+schema%3A+%3Chttp%3A%2F%2Fschema.org%2F%3E%0D%0APREFIX+type%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fterm%2Ftype%2F%3E%0D%0APREFIX+chname%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fentity%2Fchname%2F%3E%0D%0APREFIX+time%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fentity%2Ftime%2F%3E%0D%0APREFIX+skos%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+dct%3A+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0D%0APREFIX+genji%3A+%3Chttps%3A%2F%2Fw3id.org%2Fkouigenjimonogatari%2Fapi%2Fproperty%2F%3E%0D%0APREFIX+prop-ja%3A+%3Chttp%3A%2F%2Fja.dbpedia.org%2Fproperty%2F%3E%0D%0APREFIX+emperor%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fentity%2Femperor%2F%3E%0D%0APREFIX+kani%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fterm%2Fkani%2F%3E%0D%0APREFIX+role%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fterm%2Frole%2F%3E%0D%0APREFIX+term%3A+%3Chttps%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fterm%2F%3E%0D%0ASELECT+DISTINCT+%3Fs+WHERE+%7B%0D%0A%09%3Fs+%3Fv+%3Fo.+FILTER%28regex%28str%28%3Fs%29%2C+%22%2Fkeyword%2F%22+%29+%29%0D%0A%7D%0D%0AORDER+BY+%3Fs&output=json"

results = requests.get(url).json()["results"]["bindings"]

arr = []

for row in results:
    label = row["s"]["value"].split("/keyword/")[1].split(".")[0]

    if label not in arr:

        arr.append(label)

for i in range(len(arr)):

    print(i+1, len(arr))

    label3 = arr[i]

    main2(label3)
    