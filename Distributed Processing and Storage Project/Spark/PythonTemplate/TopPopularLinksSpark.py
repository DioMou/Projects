#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext
import re

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

delim=': '
exp = '|'.join(map(re.escape, delim))

lines = sc.textFile(sys.argv[1], 1) 
line=lines.map(lambda line:line.strip().split(' '))
#page_only=line.map(lambda x :x[0].split(':')[0])
link_only=line.flatMap(lambda x: x[1:])\
            .map(lambda x:(x,1))\
            .reduceByKey(lambda a,b:a+b)\
            .sortBy(lambda x:-x[1])\
            .take(10)
            #.takeOrdered(10,key=lambda x:-x[1])
top_link=sc.parallelize(link_only)\
            .sortByKey()
            

#TODO

output = open(sys.argv[2], "w")
for l in top_link.collect():
#for l in link_only:
    output.write(str(l[0]))
    output.write('\t')
    output.write(str(l[1]))
    output.write('\n')

#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()

