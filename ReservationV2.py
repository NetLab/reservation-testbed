import random
from time import sleep
from math import floor, ceil, log
from ConstantsV2 import *

class Reservation:
    def __init__(self, my_lambda, nodes, resNum, prevArrivalT):
        self.sourceNode = nodes[random.randint(0,len(nodes) - 1)]  # Randomly assign source node from list
        randDst = nodes[random.randint(0,len(nodes) - 1)]
        while(randDst == self.sourceNode):   # Ensure dest node is not equal to source
            randDst = nodes[random.randint(0, len(nodes) - 1)]  # Randomly assign dest node from list
        self.destNode       = randDst

        self.resNum         = resNum

        self.path           = None
        self.arrival_t      = prevArrivalT + self.GenArrivalTime(my_lambda)
        self.book_t         = self.GenBkAheadTime()
        self.holding_t      = self.GenHoldingTime()
        self.start_t        = self.arrival_t + self.book_t
        self.size_req       = self.GenSizeRequest()
        self.num_slots      = None

    def LoadRes(self, resVars):
        self.arrival_t = resVars[0]
        self.start_t = resVars[0] + resVars[1]
        self.holding_t = resVars[2]
        self.num_slots = resVars[3]

    def SetNumSlots(self, cost):
        blocked, num_slots = self.GenNumberSlots(cost)
        if blocked:
            return True
        else:
            self.num_slots = num_slots
            return False

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
        self.path = []
        for nodeIndex in range(0,len(path) - 1):
            self.path.append(path[nodeIndex:nodeIndex + 2]) # append each link (Ex: AB, GH, etc.) to path list
        if len(self.path) < 1:
            print("ERROR: Reservation.SetPath -> Path of incorrect length", len(self.path))
            raise

    # =========================== G e n e r a t i o n ==============================

    def GetArrivalTime(self):
        return self.arrival_t

    def GenArrivalTime(self, my_lambda):
        #seed()
        randNum = random.uniform(0.0000000000000001, 1)
        return round((-1 * log(randNum))/my_lambda)

    def GetHoldingTime(self):
        return self.holding_t

    def GenHoldingTime(self):
        #seed()
        return ceil((-1 * log(random.uniform(0.0000000000000001, 1)))/Mu)

    def GenBkAheadTime(self):
        #seed()
        return random.randint(1,100)

    def GetStartT(self):
        return self.start_t

    # ---------------------- N u m b e r   o f   S l o t s -------------------------

    def GenSizeRequest(self):
        #seed()
        #return 200 - (random.randint(1,16) * MAX_SLOT_SIZE)
        return random.randint(1, MAX_REQ_SIZE)

    def GetNumSlots(self):
        return self.num_slots

    def GenNumberSlots(self, dist):
        if dist <= 5000 and dist > 2500:
            M = 1
        elif dist <= 2500 and dist > 1250:
            M = 2
        elif dist <= 1250 and dist > 625:
            M = 3
        elif dist <= 625:
            M = 4
        else:
            M = 0
            return True, None
        return False, ceil((self.size_req/(MAX_SLOT_SIZE * M)) + guard_band)

    def PrintInfo(self):
        print("Arrival time", self.arrival_t)
        print("SD", self.sourceNode, self.destNode)
        print("Size Request", self.size_req)
        print("Holding time", self.holding_t)
        print("Bookahead time", self.holding_t)
        print("Slot size", self.num_slots)

#Theoretical Maximums with lambda 1:
# Arrival = 15
# Start = 110
# numslots = 16
# holding time  = 298 (actual 320)

def FormatLinkName_List(node1, node2):
    return "".join(sorted(node1 + node2))

def FormatLinkName_String(nodes):
    return "".join(sorted(nodes))

if __name__ == '__main__':
    random.seed(12345)
    test = Reservation(2, "AB", 1, 0)
    test.SetNumSlots(500)
    test.PrintInfo()
    print('\n')