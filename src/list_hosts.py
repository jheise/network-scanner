#!/usr/bin/env python

import time
import elasticsearch
from datetime import datetime

es = elasticsearch.Elasticsearch("glados")

def get_timestamps():

    scantimes= []
    scans = es.search("network-scan", "scan")
    for scan in scans["hits"]["hits"]:
        scantimes.append(scan["_source"]["timestamp"])

    scantimes.sort()
    scantimes = set(scantimes)

    return scantimes

scantimes = get_timestamps()
query = {
        "size":256,
         "aggs": {
            "all_hosts" : {
                "cardinality" : {
                    "field" : "hostname"
                }
            }
        }
        }

data = es.search("network-scan", "host", body=query)
hosts = [ entry["_source"]["hostname"] for entry in data["hits"]["hits"] ]
hosts = list(set(hosts))

for i in range(len(hosts)):
    hosts[i] = tuple((int(x) for x in hosts[i].split(".")))

hosts.sort()

for i in range(len(hosts)):
    hosts[i] = ".".join((str(x) for x in hosts[i]))


#for entry in data["hits"]["hits"]:
for entry in hosts:
    #print entry["_source"]["hostname"]
    print entry
    query = {
                "query" : {
                    "term" : { "hostname": entry}
                }
            }
    host_data = es.search("network-scan", "host", body=query)
    timestamps = []
    for host_entry in host_data["hits"]["hits"]:
        timestamps.append( host_entry["_source"]["timestamp"])

    timestamps.sort()
    #for stamp in scantimes:
        #if stamp not in timestamps:
            #print "\t{0} - MISSING".format(stamp)
        #else:
            #print "\t{0}".format(stamp)
