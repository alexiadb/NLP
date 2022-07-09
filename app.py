import json, requests, pprint, yaml
from pymongo import MongoClient
from flask import Flask, jsonify, render_template, request
import random
from langdetect import detect, detect_langs

with open("config.yaml", "r") as f:
    conf = yaml.safe_load(f)['MOOC']
    client = MongoClient(conf['mongoUri'])
    collection = client[conf['db']][conf['collection']]


url = conf["cognitive"]+"/text/analytics/v3.0/sentiment?opinionMining=true"

headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': conf['key']}
doc = { "documents": [{ "id": "1", "text": "The customer service here is really good."}]}
x = requests.post(url, headers=headers, json = doc)
print(x.text)
pprint.pprint(x.json())

app = Flask(__name__)

@app.route("/")
def hello_world():
    course_id = request.args.get('course_id')
    docs = []
    resp=[]
    languages=[]
    if course_id:
        cur = collection.find({'content.course_id': course_id}, {'content.body': True}).limit(10)
        docs = { "documents": [{'id': x['_id'], "text": x['content']['body']} for x in cur]}
        resp = requests.post(url, headers=headers, json = docs)
        resp=resp.json()
        languages=[detect_langs(t['text']) for t in docs['documents']]
        print(languages)
    courses = collection.distinct('content.course_id')
    print(courses)
    return render_template('mooc.html', courses=courses, course_id=course_id, resp=resp, languages=languages)


#~ app.run(port=5000, host='0.0.0.0')
if __name__ == '__main__':
   app.run()


app.run(port=5000, host='0.0.0.0')