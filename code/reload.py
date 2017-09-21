import subprocess
import sys
import requests
parameter_url='http://localhost:8984/solr/admin/cores?action=RELOAD&core=_core_'
if len(sys.argv)<2:
    argv='all'
else:
    argv=sys.argv[1]
if argv=='all':
    for core in ('vsm','dfr','bm25'):
        url=parameter_url.replace('_core_',core)
        data=requests.get(url)
        if(data.status_code!=200):
            print("could not reload "+core)
            print("url ->"+url)
            continue
        subprocess.call("post -c "+core+" train.json",shell=True)
else:
    print("reloaded "+core)
    core=argv
    url=parameter_url.replace('_core_',core)
    data=requests.get(url)
    if(data.status_code!=200):
        print("could not reload "+core)
        print("url ->"+url)
        sys.exit()
    subprocess.call("post -c "+core+" train.json",shell=True)
    print("reloaded "+core)
