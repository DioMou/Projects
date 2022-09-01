#!/usr/bin/env python

#Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 
line=lines.map(lambda line:line.strip().split(' '))
link_only=line.flatMap(lambda x: x[1:])\
            .map(lambda x:(x,1))\
            .reduceByKey(lambda a,b:a+b)\
            

#TODO

leagueIds = sc.textFile(sys.argv[2], 1)
num_league=leagueIds.count()
leagues=leagueIds.map(lambda x:(x,0))
merged_leagueLink=leagues.leftOuterJoin(link_only)\
                        .filter(lambda x:x[1][1] !=None)\
                        .map(lambda x:(x[0],x[1][1]))\
                        .sortBy(lambda x:x[1])\
                        .map(lambda x:x[0])\
                        .zipWithIndex()\
                        .sortByKey()
                        #.takeOrdered(num_league)
                        # .map(lambda x:x[0])\
                        # .sortByKey()


#TODO

output = open(sys.argv[3], "w")
for l in merged_leagueLink.collect():
    #for l in link_only:
    output.write(str(l))
    output.write('\n')
#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()

