#!/bin/env python
# encoding: utf-8
"""
    author: Eric.W
"""

# http://docs.mongodb.org/manual/reference/operator/aggregation/group/

import pymongo

mongo = pymongo.MongoClient(host="localhost", port=27017)

query_result = mongo.test.query_result

cursor = query_result.aggregate([
    {
        "$group": {
            "_id": {
                "region": "$region",
                "version": "$version",
            },
            "account": {
                "$sum": "$count",
            }
        }
    }
])

for item in cursor:
    print item