#!/usr/bin/env python
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)
value_pair = lines.map(lambda x: (x.split("\t")[0],int(x.split("\t")[1])))
value_only = value_pair.map(lambda x: x[1]).variance()
value_only_with_count = value_pair.map(lambda x: (x[1],1))
(sum,count)=value_only_with_count.reduce(lambda a,b: (a[0]+b[0],a[1]+b[1]))
# value_pair=lines.flatMap(lambda line: filter(None,line.split("\t"))) \
#     .filter(lambda word:word.strip()) \
#     .map(lambda word:(word[0],word[1])) 
    
#value_max=value_pair.takeOrdered(1,key=lambda x:-x[1])

#TODO

outputFile = open(sys.argv[2], "w")
outputFile.write('Mean\t%s\n' % int(sum/count))
outputFile.write('Sum\t%s\n' % sum)
for i in value_pair.takeOrdered(1,key=lambda x:x[1]):
    outputFile.write('Min\t%s\n' % i[1])
for i in value_pair.takeOrdered(1,key=lambda x:-x[1]):
    outputFile.write('Max\t%s\n' % i[1])
outputFile.write('Var\t%s\n' % int(value_only))
    #outputFile.write('Max\t%s\n' % i)
'''
TODO write your output here
write results to output file. Format
outputFile.write('Mean\t%s\n' % ans1)
outputFile.write('Sum\t%s\n' % ans2)
outputFile.write('Min\t%s\n' % ans3)
outputFile.write('Max\t%s\n' % ans4)
outputFile.write('Var\t%s\n' % ans5)
'''

sc.stop()

