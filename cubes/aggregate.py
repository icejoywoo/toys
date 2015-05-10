#!/bin/env python
# encoding: utf-8
from __future__ import print_function
from cubes import Workspace, Cell, PointCut

# 1. Create a workspace
workspace = Workspace()
workspace.register_default_store("sql", url="sqlite:///data.sqlite")

# import model可以是dict或json配置文件
workspace.import_model("model.json")

# 2. Get a browser
browser = workspace.browser("test_data")

# 3. Play with aggregates
result = browser.aggregate()

print("Total\n"
      "----------------------")

print("Record count : %8d" % result.summary["record_count"])
print("Total amount : %8d" % result.summary["amount_sum"])

#
# 4. Drill-down through a dimension
#

print("\n"
      "Drill Down by Region (top-level Item hierarchy)\n"
      "==================================================")
#
result = browser.aggregate(drilldown=["region"])
#
print(("%-20s%10s%10s\n"+"-"*50) % ("Region", "Count", "Total"))
#
for row in result.table_rows("region"):
    print("%-20s%10d%10d" % (row.label,
                             row.record["record_count"],
                             row.record["amount_sum"]
                             ))

print("\n"
      "Slice where region = BR\n"
      "==================================================")

cuts = [
    PointCut("region", ["BR"]),
    PointCut("channel", ["web|br|official|direct"]),
]
cell = Cell(browser.cube, cuts=cuts)

result = browser.aggregate(cell, drilldown=["channel", "version", "region"])

print(("%-20s%-20s%10s%10s\n"+"-"*50) % ("version", "channel", "Count", "Total"))

for row in result.table_rows("version"):
    print("%-20s%-20s%10d%10d" % (row.record['version'],
                                  row.record['channel'],
                                  row.record["record_count"],
                                  row.record["amount_sum"]))
