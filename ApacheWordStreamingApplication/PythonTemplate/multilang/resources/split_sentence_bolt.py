import storm
import re


class SplitBolt(storm.BasicBolt):
    # There's nothing to initialize here,
    # since this is just a split and emit
    # Initialize this instance
    def initialize(self, conf, context):
        self._conf = conf
        self._context = context
        storm.logInfo("Split bolt instance starting...")

    def process(self, tup):
        # TODO
        # Task: split sentence and emit words
        # Hint: split on "[^a-zA-Z0-9-]"
        words=tup.values[0]
        word_list=re.split('[^a-zA-Z0-9-]',words)
        for w in word_list:
            if w !='':
                storm.logInfo("Emitting %s" % w)
                storm.emit([w])
        # End


# Start the bolt when it's invoked
SplitBolt().run()
