from operator import attrgetter
from Constants import *
from Reservation import *

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = [[EMPTY] * MAX_NUM_FREQ] * TIME_WNDW_SIZE  ## Declare 2D array of Empty (False) time periods and frequencies
        self.nodes          = nodes
        self.length         = length
        self.initResList    = []
        self.currResList    = []
        self.fwdResList     = []
        self.curTime        = 0
        self.numBlocks      = 0


    # ======================================== R e s e r v a t i o n s ===========================================
    # ----------------- C u r r e n t   R e s e r v a t i o n s --------------------
    def LoadArrivingRes(self, arrivingRes):
        for res in arrivingRes:
            if res.arrival_t == self.curTime:
                avail, startIndex = self.CheckOpenSpace(res.num_slots)
                if avail:
                    self.currResList.append(res)
                else:
                    self.numBlocks += 1
        self.SortCurrResList()

    def SortCurrResList(self):
        self.currResList.sort(key=attrgetter('start_t', 'arrival_t', 'book_t'))

    def ClearCurrResList(self):
        self.currResList = []

    def CheckNeedUpdate(self):
        if (len(self.currResList) != 0):
            if (self.currResList[0].start_t == self.curTime):
                return True
        return False

    def UpdateCurrReservations(self):
        update = self.CheckNeedUpdate()

        while(update):
            tempRes = self.currResList.pop(0)
            spaceOpen, spaceIndex = self.CheckOpenSpace(tempRes.num_slots)  # See if window can fit the res, if so where
            if spaceOpen:
                self.PlaceRes(spaceIndex, tempRes.num_slots, tempRes.holding_t) # Place the reservation in the window
                self.AddToFwdList(tempRes)      # Only once the reservation is actually placed do we add to fwdList
            else:
                self.numBlocks += 1
            update = self.CheckNeedUpdate()

    # -------------- F o r w a r d i n g   R e s e r v a t i o n s -----------------
    #   Add a reservation to the links forwarding list
    def AddToFwdList(self, res):
        res.IncrementPath() # Mark the reservation to continue to next step of its path when it is called
        res.SetNextTime(res.start_t + res.holding_t)    # Set arrival/start of next step to after current completes
#        print("Next start time", res.start_t + res.holding_t)
        self.fwdResList.append(res)
        self.fwdResList.sort(key=lambda x: x.arrival_t)    # Sort the list by the first item of each sublist (end time)

    def GetFwdingRes(self):
        fwdingRes = []
        for res in self.fwdResList:
            if res.arrival_t - 1 == self.curTime:   # If the end time of the reservation = 1 + current time:
                resToRemove = self.fwdResList.index(res)    # Get index of forwarded reservation to move
                fwdingRes.append(self.fwdResList.pop(resToRemove))  # Move res to the list to a list to be returned
        return fwdingRes

    def GetFwdResList(self):
        return self.fwdResList

    # ===================================== R e s e r v a t i o n   W i n d o w ===================================
    def CheckOpenSpace(self, size):
        avail       = 0
        index       = 0
        startIndex  = None

        for space in self.timeWindow[0]:    # For each space in the current row
            if space == EMPTY:  # If space is empty
                if avail == 0:      # If start of new space to be checked
                    startIndex = index  # Record the start index of the space
                avail += 1          # Increment the counter of available space
            elif space == FULL: # Else if its full
                avail = 0           # Reset the counter of available space
                startIndex = None   # Reset the start index of the space
            else:   # Should not get here
                print("ERROR: CheckOpenSpace -> Time Window Space =", space)
                raise

            if avail >= size:   # If a space of suitable size is found
                return True, startIndex # Return that there is a suitable open space, and its start index
            index += 1  # Increment the index
        print("*********************HERE***************")
        print(self.nodes)
        return False, startIndex    # If no suitable space is found, return False and None

    def PlaceRes(self, startIndex, size, depth):
        i = 0
        j = 0
        while(i < size):
            while(j < depth):
                try:
                    self.timeWindow[j][startIndex + i] = FULL
                except:
                    print("Size", size)
                    print("Depth", depth)
                    print("PlaceRes Error:")
                    print("Time Index   = ", j)
                    print("Time Max     = ", len(self.timeWindow))
                    print("Freq Index   = ", i)
                    print("Freq Max     = ", len(self.timeWindow[j]))
                    raise
                j += 1
            j  = 0
            i += 1

    def IncrementTime(self):
        self.timeWindow = self.timeWindow[1:]
        self.timeWindow.append([EMPTY] * MAX_NUM_FREQ)
        self.curTime += 1

    # =========================================== M a i n   P r o c e s s =========================================
    def RunTimeStep(self):
        self.UpdateCurrReservations()
        self.IncrementTime()

        return self.GetFwdingRes()  # Return any reservations that are forwarded at this time
        #print("Total Number of Blocks with lambda", my_lambda, "equal to:", self.numBlocks)

    def GetNumBlocks(self):
        return self.numBlocks

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def NodeInLink(self, node):
        for myNode in self.nodes:
            if node == myNode:  # If either node is one belonging to the link
                return True         # Return True
        return False            # Else return false

    def GetLinkNodes(self):
        return self.nodes[0], self.nodes[1]



def FormatLinkName_List(node1, node2):
    return "".join(sorted(node1 + node2))

def FormatLinkName_String(nodes):
    return "".join(sorted(nodes))




# testNode = Network()
# i = 1
# total = 0
# while(i < 21):
#     for x in range(0,20):
#         total += testNode.RunProcess(i)
#
#     print("Total Number of Blocks with lambda", i, "equal to:", total/20)
#     i += 1
#
#
# print("done")