import heapq
from heapq import heapify, heappush, heappop
from collections import Counter
import copy

import storm


class TopNFinderBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context

        storm.logInfo("Counter bolt instance starting...")

        # TODO:
        # Task: set N
        self.N=10#self._conf['']
        self.heap=[]
        heapify(self.heap)
        self.wordCount_dict={}
        # End

        # Hint: Add necessary instance variables and classes if needed

    def process(self, tup):
        '''
        TODO:
        Task: keep track of the top N words
        Hint: implement efficient algorithm so that it won't be shutdown before task finished
              the algorithm we used when we developed the auto-grader is maintaining a N size min-heap
        '''
        word=tup.values[0]
        count=tup.values[1]

        self.wordCount_dict[word]=count
        self.heap=[(-v, k) for k,v in self.wordCount_dict.items()]
        heapify(self.heap)
        #heappush(self.heap,(-count,word))
        #temp=copy.copy(self.heap)
        if len(self.heap)<10:
            result=[heappop(self.heap)[1] for _ in range(len(self.heap))]
        else:
            result=[heappop(self.heap)[1] for _ in range(10)]
        #result=[heappop(self.heap)[1] for _ in range(len(self.heap))]#[v for k,v in self.heap]
        # if word in["far", "oh", "yet", "up", "get", "ye", "no", "sir", "mr", "day"]:
        #     #sir,no,yet,day,oh,bed,mr,met,ask,ye
        #     storm.logInfo(str(self.heap[0:30])+"correct words")
        #     storm.logInfo("%s is %s"%(word,str(count)))
        # if word in ["bed","met","ask"]:#bed:4,met:3,ask:3
        #     storm.logInfo(str(self.heap[0:30])+"wrong words before")
        #     storm.logInfo("wrong %s is %s"%(word,str(count)))
        #storm.logInfo(", ".join(result[0:30]))
        result = list(dict.fromkeys(result))[0:10]
        result=", ".join(result)
        #self.heap=temp
        storm.logInfo(result)
        storm.emit([result])
        # End


# Start the bolt when it's invoked
TopNFinderBolt().run()
