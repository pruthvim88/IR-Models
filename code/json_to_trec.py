# -*- coding: utf-8 -*-
"""
Thanks to the author Ruhan Sa, who is the TA of IR project 3 in Fall 2015
"""

import json
import sys
# if you are using python 3, you should
#import urllib.request
import requests
import subprocess

# change the url according to your own koding username and query

parameter_url = 'http://localhost:8984/solr/_core_/select?fl=id%2Cscore&wt=json&indent=true&rows=20'
parameter_outfn = 'output_core_.txt'
import codecs
qf=codecs.open("queries.txt",'r',encoding='utf-8')
queries={}
while True:
	s=qf.readline().strip()
	if not len(s):
		break
	sp=s.split(" ",1)
	queries[sp[0]]=sp[1]
qids=queries.keys()
qids=sorted(qids)

# change query id and IRModel name accordingly

def sanatize(instr):
	for s in '+-!(){}[]^\"~*?:':
		instr=instr.replace(s,'\\'+s)
	return instr

def get_map(opList):
	return opList[opList.index("map")+2]

for core in ("VSM","BM25","DFR"):
	inurl=parameter_url.replace("_core_",core)
	outfn=parameter_outfn.replace("core_",core)
	outf =codecs.open(outfn,'w',encoding='utf-8')
	for qid in qids:
		query=sanatize(queries[qid])
		d={"q":query}
		data = requests.post(inurl,data=d)
		if data.status_code !=200:
			print(query)
			sys.exit()
		docs = data.json()['response']['docs']
		rank = 1
		for doc in docs:
			outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + core + '\n')
			rank += 1
	outf.close()
	opStr=subprocess.check_output("./trec_eval qrel.txt "+outfn,shell=True)
	map_measure=get_map(opStr.split())
	print("map for "+core+" -"+str(map_measure))
