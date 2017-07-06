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

        self.path           = None
        self.nextLink       = None
        self.linkIndex      = None

        self.arrival_t      = self.GenArrivalTime(my_lambda)
        self.book_t         = self.GenBkAheadTime()
        self.holding_t      = self.GenHoldingTime()
        self.start_t        = self.arrival_t + self.book_t
        self.size_req       = self.GenSizeRequest()
        self.num_slots      = self.GenNumberSlots(self.size_req)

    # Used for overloading randomly generated reservations (load in specific attributes for a reservation)
    def Load(self, nodes, arrival_t, start_t, holding_t, num_slots):
        self.sourceNode = nodes[0]
        self.destNode   = nodes[1]
        self.arrival_t  = arrival_t
        self.start_t    = start_t
        self.holding_t  = holding_t
        self.num_slots  = num_slots

    # --------------- S o u r c e   a n d   D e s t i n a t i o n ------------------
    # Get the source and destination nodes and return them as a list
    def GetSrcDst(self):
        return self.sourceNode, self.destNode

    # --------------------------------- P a t h ------------------------------------
    # Get the path of the reservation
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

    # For use in CheckInitialPathOpen in Network. Used to get list of links to verify res does not block at first arrival
    def GetAllPathLinks(self):
        if self.path == None:       # Raise error if res has no path at this point
            raise

        listLinks = []

        for index in range(0, len(self.path) - 2):
            listLinks.append(FormatLinkName_String(self.path[index:index+2]))  # Get each link name that the path will go through

        return listLinks

    def IsOnFirstLink(self):
        return self.path[0:2] == self.nextLink

    def IsResDone(self):
        try:
            if self.nextLink[1] == TERMINATE_CHAR:
                #print("Reservation", self.sourceNode, self.destNode, "complete")
                return True, (self.sourceNode, self.destNode)
            else:
                return False, None
        except:
            print(self.nextLink, self.path)
            raise

    # ----------------------------- I n d e x i n g --------------------------------
    # Get the slot index where the reservation is continuously allocated
    def GetLinkIndex(self):
        return self.linkIndex

    # Set the slot index where the reservation is to be continuously allocated
    def SetLinkIndex(self, linkIndex):
        self.linkIndex = linkIndex

    # --------------------------------- T i m e ------------------------------------
    def SetNextTime(self, nextTime):    # Sets time for link to next immediately start. Used for telling
        self.arrival_t  = nextTime      # res arrives at next link after it completes current step
        self.start_t    = nextTime      # res does not wait upon arriving, so starts as it arrives

    def GetNextTime(self):
        return self.arrival_t

    def GenArrivalTime(self, my_lambda):
        #seed()
        randNum = uniform(0.0000000000000001, 1)
        return round((-1 * log(randNum))/my_lambda)

    def GetHoldingTime(self):
        return self.holding_t

    def GenHoldingTime(self):
        #seed()
        return ceil((-1 * log(uniform(0.0000000000000001, 1)))/Mu)

    def GenBkAheadTime(self):
        #seed()
        return randint(1,100)

    # ---------------------- N u m b e r   o f   S l o t s -------------------------

    def GenSizeRequest(self):
        #seed()
        return 200 - (randint(1,16) * 12.5)

    def GetNumSlots(self):
        return self.num_slots

    def GenNumberSlots(self, size_req):
        return ceil((size_req/12.5) + guard_band)

#Theoretical Maximums with lambda 1:
# Arrival = 15
# Start = 110
# numslots = 16
# holding time  = 298 (actual 320)

def FormatLinkName_List(node1, node2):
    return "".join(sorted(node1 + node2))

def FormatLinkName_String(nodes):
    return "".join(sorted(nodes))

