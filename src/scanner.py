#!/usr/bin/env python

import nmap
import time
import elasticsearch
from datetime import datetime

nm = nmap.PortScanner()
es = elasticsearch.Elasticsearch("glados")
#nm.scan('10.0.42.0/24', '22')
for x in range(1):
    scantime = datetime.utcnow()
    nm.scan('10.0.42.0/24', arguments='-sP')
    es.create(index="network-scan", doc_type="scan", body={"timestamp":scantime})
    for host in nm.all_hosts():
        print "reporting on", host
        print nm[host]
        data = {"hostname":host,
                "timestamp":scantime}
        es.create(index="network-scan", doc_type="host", body=data)

    print "Sleeping..."
    time.sleep(10)
