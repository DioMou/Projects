import storm
import redis


class TopNStoreBolt(storm.BasicBolt):
    # Initialize this instance
    def initialize(self, conf, context):
        # redis configuration converted into a dictonary
        self._redis = conf.get("redis")
        storm.logInfo("Top N Store bolt instance starting...")

        # TODO
        # Connect to Redis using redis.Redis() with redis configuration in self._redis dictionary
        # Hint: Add necessary instance variables and classes if needed
        self.r = redis.Redis(host=self._redis.get('host'), 
                             port=self._redis.get('port'), 
                             db=self._redis.get('db'), 
                             password=self._redis.get('password')
                             )

    def process(self, tup):
        # TODO
        # Task: save the top-N word to redis under the specified hash name
        #storm.logInfo(str(tup.values[0]))
        self.r.hset(self._redis.get('hashKey'),"top-N",tup.values[0])
        # End


# Start the bolt when it's invoked
TopNStoreBolt().run()
