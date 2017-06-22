from random import *
from time import sleep
from math import floor, ceil, log
from Constants import *

class Reservation:
    def __init__(self, my_lambda, nodes):
        self.sourceNode = nodes[randint(0,len(nodes) - 1)]  # Randomly assign source node from list

        randDst = nodes[randint(0,len(nodes) - 1)]
        while(randDst == self.sourceNode):   # Ensure dest node is not equal to source
            randDst = nodes[randint(0, len(nodes) - 1)]  # Randomly assign dest node from list
        self.destNode   = randDst

        self.path       = None
        self.nextLink   = None
        self.arrival_t  = GetArrivalTime(my_lambda)
        self.book_t     = GetBkAheadTime()
        self.holding_t  = GetHoldingTime()
        self.start_t    = self.arrival_t + self.book_t
        self.size_req   = GetSizeRequest()
        self.num_slots  = GetNumberSlots(self.size_req)

    def Load(self, nodes, arrival_t, start_t, holding_t, num_slots):
        self.sourceNode = nodes[0]
        self.destNode   = nodes[1]
        self.arrival_t  = arrival_t
        self.start_t    = start_t
        self.holding_t  = holding_t
        self.num_slots  = num_slots

    def GetSrcDst(self):
        return self.sourceNode, self.destNode

    def GetPath(self):
        return self.path

    def SetPath(self, path):
        self.path = path + TERMINATE_CHAR
        if self.path[1] == TERMINATE_CHAR or len(self.path) < 2:
            print("ERROR: Reservation.SetPath -> Path of incorrect length", self.path[0:-1])
            raise
        self.nextLink   = path[0:2]

    def IncrementPath(self):
        for node in self.path:
            if node == self.nextLink[0]:
                index = self.path.index(node)
        self.nextLink   = self.path[index+1:index+3]
        if len(self.nextLink) < 2:
            print("ERROR: Reservation.IncrementPath -> path", self.path, "with nextLink", self.nextLink, "of incorrect length", len(self.nextLink))
            raise

    def GetNextPathLink(self):
        return self.nextLink

    def SetNextTime(self, nextTime):    # Sets time for link to next immediately start. Used for telling
        self.arrival_t  = nextTime      # res arrives at next link after it completes current step
        self.start_t    = nextTime      # res does not wait upon arriving, so starts as it arrives

    def GetNextTime(self):
        return self.arrival_t

    def GetHoldingTime(self):
        return self.holding_t

    def GetNumBlocks(self):
        return self.num_slots

    def IsResDone(self):
        try:
            if self.nextLink[1] == TERMINATE_CHAR:
                print("Reservation", self.sourceNode, self.destNode, "complete")
                return True, (self.sourceNode, self.destNode)
            else:
                return False, None
        except:
            print(self.nextLink, self.path)
            raise

def GetArrivalTime(my_lambda):
    #seed()
    randNum = uniform(0.0000000000000001, 1)
    return round((-1 * log(randNum))/my_lambda)

def GetHoldingTime():
    #seed()
    return ceil((-1 * log(uniform(0.0000000000000001, 1)))/Mu)

def GetBkAheadTime():
    #seed()
    return randint(1,100)

def GetSizeRequest():
    #seed()
    return 200 - (randint(1,16) * 12.5)

def GetNumberSlots(size_req):
    return ceil((size_req/12.5) + guard_band)

#Theoretical Maximums with lambda 1:
# Arrival = 15
# Start = 110
# numslots = 16
# holding time  = 298 (actual 320)


