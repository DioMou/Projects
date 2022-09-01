#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark import SparkContext
import re

conf = SparkConf().setMaster("local").setAppName("OrphanPages")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)
spark=SparkSession(sc)

delim=': '
exp = '|'.join(map(re.escape, delim))


lines = sc.textFile(sys.argv[1], 1) 

pagelink=lines.map(lambda line: line.strip().split(" "))
page_only=pagelink.map(lambda line:(line[0].split(':')[0],0))
link_only=pagelink.flatMap(lambda line:line[1:])
link_only_pair=link_only.map(lambda x:(x,1))
merge_linkpage=link_only_pair.union(page_only)
orphan=merge_linkpage.reduceByKey(lambda a,b:a+b)\
                    .filter(lambda x:x[1] ==0)\
                    .sortByKey()
    
output = open(sys.argv[2], "w")
for p in orphan.collect():
    output.write(str(p[0]))
    output.write('\n')
sc.stop()
#TODO
#write results to output file. Foramt for each line: (line + "\n")



