#!/bin/env python
# encoding: utf-8
"""
    author: Eric.W
"""
from __future__ import print_function
from cubes import Workspace, Cell, PointCut

# cubes根本没实现mongodb backend
workspace = Workspace()
workspace.register_default_store("sql", "mongodb",
                                 url="mongodb://localhost:27017/",
                                 database="test", collection="query_result")

workspace.import_model("model.json")

browser = workspace.browser("query")