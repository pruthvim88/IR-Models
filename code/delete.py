import sys
import requests
parameter_url='http://localhost:8984/solr/_core_/update?'
commit_stub ='stream.body=%3Ccommit/%3E'
delete_stub ='stream.body=%3Cdelete%3E%3Cquery%3E*:*%3C/query%3E%3C/delete%3E'
if len(sys.argv)<2:
    argv='all'
else:
    argv=sys.argv[1]
if argv=='all':
    for core in ('vsm','dfr','bm25'):
        url=parameter_url.replace('_core_',core)+delete_stub
        data=requests.get(url)
        if(data.status_code!=200):
            print("could not delete docs in "+core)
            print("url ->"+url)
            continue
        data=requests.get(parameter_url.replace('_core_',core)+commit_stub)
        print("deleted "+core)
else:
    core=argv
    url=parameter_url.replace('_core_',core)+delete_stub
    data=requests.get(url)
    if(data.status_code!=200):
        print("could not delete docs in "+core)
        print("url ->"+url)
        sys.exit()
    data=requests.get(parameter_url.replace('_core_',core)+commit_stub)
    print ("deleted "+core)
