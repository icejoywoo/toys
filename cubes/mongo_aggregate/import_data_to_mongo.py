__author__ = 'icejoywoo'

import pymongo

mongo = pymongo.MongoClient(host="localhost", port=27017)

query_result = mongo.test.query_result

field_names = ['userid', 'count', 'channel', 'region', 'version']

buffer = []

for line in open("data.csv"):
    item = dict(zip(field_names, line.rstrip('\n').split(',')))
    item['count'] = int(item['count'])
    buffer.append(item)
    if len(buffer) >= 10000:
        query_result.insert(buffer)
        buffer = []

if buffer:
    query_result.insert(buffer)
