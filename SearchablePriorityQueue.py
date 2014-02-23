import Queue
from time import time as _time
try:
    import threading as _threading
except ImportError:
    import dummy_threading as _threading
from collections import deque
import heapq
import types

__all__ = ['SearchablePriorityQueue']

class SearchablePriorityQueue(Queue.Queue):
    '''Variant of Queue that retrieves open entries in priority order (lowest first) and has the ability to find elements in the queue.
    Entries are typically tuples of the form:  (priority number, data).
    '''
    def _init(self, maxsize):
        self.queue       = []
        self.searchQDict = dict()

    def _qsize(self, len=len):
        return len(self.queue)

    def _put(self, item, heappush=heapq.heappush):
        if(item[0] in self.searchQDict):
            raise Exception("Error: SearchablePriorityQueue already has this priority index[%s]. Indexes need to be unique!"%(item[0]))
        else:
            self.searchQDict[item[0]] = item[1]
        heappush(self.queue, item)

    def _get(self, heappop=heapq.heappop):
        rtnVal = heappop(self.queue)
        del self.searchQDict[rtnVal[0]]
        return rtnVal

    def printDict(self):
        print self.searchQDict

    def getDict(self):
        return self.searchQDict

    def inQueue(self,check):
        if( isinstance(check, types.TupleType) ):
            if(check[0] in self.searchQDict):
                if(check[1] == self.searchQDict[check[0]]):
                    return True
        elif( isinstance(check, types.StringType) ):
            for d in self.searchQDict.values():
                if(check in d):
                    return True
        return False


if __name__ == "__main__":
    q = SearchablePriorityQueue()
    q.put( (1.1,"first") )
    q.put( (2.2,"second") )
    q.put( (3.3,"third") )
    # q.printDict()
    # q.put( (2.2,"second_2") )
    # q.put( (2.2,"fourth_with_2_priorirty") )
    q.printDict()
    # q.put( (2.2,"second_3") )
    q.printDict()
    print "'first' is in queue: [%s, expect True]"%(q.inQueue('first'))
    print "'second' is in queue: [%s, expect True]"%(q.inQueue('second'))
    print "'third' is in queue: [%s, expect True]"%(q.inQueue('third'))
    print "'fourth_with_2_priorirty' is in queue: [%s, expect False]"%(q.inQueue('fourth_with_2_priorirty'))
    print "(1.1,'first') is in queue: [%s, expect True]"%(q.inQueue( (1.1,'first') ))
    print "(2.2,'second') is in queue: [%s, expect True]"%(q.inQueue( (2.2,'second') ))
    print "(3.3,'third') is in queue: [%s, expect True]"%(q.inQueue( (3.3,'third') ))
    print "(3.3,'fourth_with_2_priorirty') is in queue: [%s, expect False]"%(q.inQueue( (3.3,'fourth_with_2_priorirty') ))
    # print "(2.2,'fourth_with_2_priorirty') is in queue: [%s, expect True]"%(q.inQueue( (2.2,'fourth_with_2_priorirty') ))
    # print "less 'first'",q.get() # should return first
    # print "less 'second'",q.get() # should return second
    # # q.printDict()
    # print "less 'second_2'",q.get() # should return second
    # print "less 'fourth_with_2_priorirty'",q.get() # should return second
    # print "less 'second_3'",q.get() # should return second
    # print "less 'third'",q.get() # should return second
    # q.printDict()