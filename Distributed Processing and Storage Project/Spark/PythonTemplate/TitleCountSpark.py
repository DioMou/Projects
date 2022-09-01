#!/usr/bin/env python

'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
import re
from pyspark import SparkConf, SparkContext

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

stopWords=[]
with open(stopWordsPath) as f:
    stopWords=f.readlines()
stopWords=[s.strip() for s in stopWords]

	#TODO
delim=[]
with open(delimitersPath) as f:
    delim=f.read()
    #TODO

conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[3], 1)
exp = '|'.join(map(re.escape, delim))
# counts = lines.flatMap(lambda line: filter(None,re.split(exp, line))) \
#             .filter(lambda word:word.lower().strip() not in stopWords)\
#             .collect() \
#             .map(lambda word: (word, 1)) \
#             .reduceByKey(lambda a, b: a + b)
counts = lines.flatMap(lambda line: filter(None,re.split(exp, line))) 
filter_counts=counts.filter(lambda word:word.lower().strip() not in stopWords)
filter_pair=filter_counts.map(lambda word: (word.lower().strip(), 1)) \
            .reduceByKey(lambda a, b: a + b) \
            .takeOrdered(10, key = lambda x: -x[1])

#TODO
def print_rdd(x):
    print(x)

outputFile = open(sys.argv[4],"w")

for x in sorted(filter_pair, key = lambda x: x[0]):
    print(x)
    outputFile.write(x[0])
    outputFile.write('\t')
    outputFile.write(str(x[1]))
    outputFile.write('\n')

# for i in range(10):
#     print('%s\t%s\n' % (  sort_orders[9-i][0],  sort_orders[9-i][1]))


#TODO
#write results to output file. Foramt for each line: (line +"\n")

sc.stop()
