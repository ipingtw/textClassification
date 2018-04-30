#import packages
import xmltodict, json
import pickle
import sys
import json
import gc
import os

project_file_path = os.path.dirname(os.path.abspath(__file__))
#open file
f =  open(os.path.join(project_file_path,'../data/news_sohusite_xml.dat')) 

doc = "" #buffer for current document
docs = [] #buffer fo all documents
file_counter = 0 #number of file output files, post-fix for the next oput file


for line in f:
	#urls have many & symbols which makes xmltodict fail, so replace them with empty string
	line = line.replace('&','')
	#add current line to current doc
	doc += line
	#if current line is close tag for doc, this means this is the end for current doc. we 
	#need to parse this doc and push the parsed result into document list
	if line.rstrip() == "</doc>":
		try:
			#strip all new line characters in current doc
			doc = doc.rstrip()
            #parse doc from xml into json
			dic= xmltodict.parse(doc)
			#append doc to document
			docs.append(dic['doc'])
			#reset doc
			doc = ""
		except:
			print('exception')
			break

	#dump each 500,000 documents to separate files. jason.dump will fail if all documents 
	#were to be dumped in the same file
	if len(docs) == 500000:
		with open(os.path.join(project_file_path,'../data/news_json'+str(file_counter)+'.txt'), 'w') as outfile:
			json.dump(docs, outfile)
		docs = []
		gc.collect()
		file_counter += 1

#if docs not empyt, which means there's still data to be dumped, dump data
if len(docs) != 0:
	with open(os.path.join(project_file_path,'../data/news_json'+str(file_counter)+'.txt'), 'w') as outfile:
	    json.dump(docs, outfile)

