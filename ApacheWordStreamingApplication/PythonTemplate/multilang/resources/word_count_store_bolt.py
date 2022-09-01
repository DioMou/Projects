import storm
import redis

class WordCountStoreBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        self._redis = conf.get("redis")  # redis configuration converted into a dictonary
        storm.logInfo("Word Count Store bolt instance starting...")

        # TODO
        # Connect to Redis using redis.Redis() with redis configuration in self._redis dictionary
        # Hint: Add necessary instance variables and classes if needed
        #self.r=redis.Redis(self._redis)
        self.r = redis.Redis(host=self._redis.get('host'), 
                             port=self._redis.get('port'), 
                             db=self._redis.get('db'), 
                             password=self._redis.get('password')
                             )


    def process(self, tup):
        self.r.hset(self._redis.get('hashKey'),str(tup.values[0]),str(tup.values[1]))
        #storm.logInfo("Emitting %s" % self.r.hget("partAWordCount",str(tup.values[0])))
        # TODO 
        # Task: save word count pair to redis under the specified hash name
        #storm.emit([str(tup.values[0]),str(tup.values[1])])
        # End

# Start the bolt when it's invoked
WordCountStoreBolt().run()
