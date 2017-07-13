from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = [[EMPTY] * MAX_NUM_FREQ] * TIME_WNDW_SIZE ## Declare 2D array of Empty (False) time periods and frequencies
        self.availSlots     = [MAX_NUM_FREQ] * TIME_WNDW_SIZE   # Number to track available slots in time row
        self.nodes          = nodes
        self.length         = length
        self.onFirstLink    = True
        self.initResList    = []
        self.currResList    = []
        self.fwdResList     = []
        self.curTime        = 0
        self.numBlocks      = 0


    # ======================================== R e s e r v a t i o n s ===========================================


    # ===================================== R e s e r v a t i o n   W i n d o w ===================================

    # For checking if a space exists starting from a current start slot
    def CheckContinuousSpace(self, startSlot, size):
        for space in range(0, size):
            if self.timeWindow[startSlot + space] == FULL:
                return FULL

        return EMPTY

    def FindOpenSpace(self, size, time):
        avail       = 0
        i           = 0
        startSlot   = None

        for space in self.timeWindow[time]:    # For each space in the current row
            if space == EMPTY:  # If space is empty
                if avail == 0:      # If start of new space to be checked
                    startSlot = i       # Record the start slot of the space
                avail += 1          # Increment the counter of available space
            elif space == FULL: # Else if its full
                avail = 0           # Reset the counter of available space
                startSlot = None   # Reset the start slot of the space
            else:   # Should not get here
                print("ERROR: CheckOpenSpace -> Time Window Space =", space)
                raise

            if avail >= size:   # If a space of suitable size is found
                return True, startSlot # Return that there is a suitable open space, and its start index
            i += 1      # Increment the index
        return False, startSlot    # If no suitable space is found, return False and None

    def GetListOfOpenSpaces(self, size, startT):
        listOfSpaces    = []    # List of spaces of size(size) in the current link
        avail           = 0
        i               = 0
        startSlot       = None

        #if self.availSlots[startT] < size:  # If not enough slots for space to exist
        #    return listOfSpaces # return the empty list instantly

        for space in self.timeWindow[startT]:    # For each space in the current row
            if space == EMPTY:  # If space is empty
                if avail == 0:      # If start of new space to be checked
                    startSlot = i       # Record the start slot of the space
                avail += 1          # Increment the counter of available space
            elif space == FULL: # Else if its full
                avail       = 0     # Reset the counter of available space
                startSlot   = None  # Reset the start slot of the space
            else:   # Should not get here
                print("ERROR: CheckOpenSpace -> Time Window Space =", space)
                raise

            if avail >= size:   # If a space of suitable size or greater is found
                # startIndex + (avail - size0 is appended as to get first available space, plus each following space
                listOfSpaces.append(startSlot + (avail - size))    # append the index of the open space (first or subsequent)
            i += 1      # Increment the index

        return listOfSpaces   # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startSlot, size, depth, startDepth):
        i = 0
        j = 0

        for k in range(0, depth):
            self.availSlots[startDepth + k] -= size # Mark the time row as having less space

        while(i < size):
            while(j < depth):
                try:
                    self.timeWindow[startDepth + j][startSlot + i] = FULL
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

    # -------------------------- D e b u g   T o o l s -----------------------------
    def DEBUG_PrintFirstWindowLine(self):
        print("Node", self.nodes)
        for value in self.timeWindow[0]:
            if value == EMPTY:
                print('-', end='')
            else:
                print('X', end='')
        print('')   # Print a final newline

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