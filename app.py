from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
import math

es = Elasticsearch()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    page_size = 10
    keyword = request.args.get('keyword')

    if request.args.get('page'):
        page_no = int(request.args.get('page'))
    else:
        page_no = 1

    body = {
        'size': page_size,
        'from': page_size * (page_no-1),
        'query': {
            'multi_match': {
                'query': keyword,
                'fields': ['name', 'description']
            }
        }
    }

    res = es.search(index='products', doc_type='', body=body)

    hits = [{'name': doc['_source']['name'], 'description': doc['_source']['description'], 'created': doc['_source']['created']} for doc in res['hits']['hits']]

    page_total = math.ceil(res['hits']['total']['value']/page_size)

    return render_template('search.html', keyword=keyword, hits=hits, page_no=page_no, page_total=page_total)