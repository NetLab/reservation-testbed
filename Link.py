from operator import attrgetter
from Constants import *
from Reservation import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = [[EMPTY] * MAX_NUM_FREQ] * TIME_WNDW_SIZE  ## Declare 2D array of Empty (False) time periods and frequencies
        self.nodes          = nodes
        self.length         = length
        self.onFirstLink    = True
        self.initResList    = []
        self.currResList    = []
        self.fwdResList     = []
        self.curTime        = 0
        self.numBlocks      = 0


    # ======================================== R e s e r v a t i o n s ===========================================
    # ----------------- C u r r e n t   R e s e r v a t i o n s --------------------
    def LoadResToLink(self, arrivingRes):
        for res in arrivingRes:
            self.currResList.append(res)

    def SortCurrResList(self):
        self.currResList.sort(key=attrgetter('start_t', 'arrival_t', 'book_t'))

    def ClearCurrResList(self):
        self.currResList = []

    def CheckNeedUpdate(self):
        self.SortCurrResList()  # Before anything else, sort the current list of reservations by start time
        if (len(self.currResList) != 0):
            if (self.currResList[0].start_t == self.curTime):
                return True
        return False

    def UpdateCurrReservations(self):
        update = self.CheckNeedUpdate()
        while(update):
            if self.currResList[0].start_t == self.curTime:
                tempRes     = self.currResList.pop(0)
            else:
                print("ERROR->UpdateCurrReservations first res in list invalid start_t", self.currResList[0].start_t, "at time", self.curTime)
                raise
            resSpace    = tempRes.GetLinkIndex()
            resSize     = tempRes.GetNumSlots()
            resTime     = tempRes.GetHoldingTime()
            if resSpace == None or resSize == None or resTime == None:
                print("ERROR->UpdateCurrReservations one of following is not set: resSpace = {0} resSize = {1} resTime = {2}".format(resSpace, resSize, resTime))
                print(tempRes.start_t, tempRes.path, tempRes.nextLink, self.curTime)
                raise
            #spaceOpen, spaceIndex = self.CheckOpenSpace(tempRes.num_slots)  # See if window can fit the res, if so where
            if self.CheckContinuousSpace(resSpace, resSize) == EMPTY:
                self.PlaceRes(resSpace, resSize, resTime) # Place the reservation in the window
                self.AddToFwdList(tempRes)      # Only once the reservation is actually placed do we add to fwdList
            else:
                self.numBlocks += 1
            update = self.CheckNeedUpdate()

    # -------------- F o r w a r d i n g   R e s e r v a t i o n s -----------------
    #   Add a reservation to the links forwarding list
    def AddToFwdList(self, res):
        res.IncrementPath() # Mark the reservation to continue to next step of its path when it is called
        res.SetNextTime(res.start_t + res.holding_t + 1)    # Set arrival/start of next step to after current completes
        self.fwdResList.append(res)
        self.fwdResList.sort(key=lambda x: x.arrival_t)    # Sort the list by the first item of each sublist (end time)

    def GetFwdingRes(self):
        fwdingRes = deepcopy(self.fwdResList)
#        for res in self.fwdResList:
#            if res.arrival_t - 1 == self.curTime:   # If the end time of the reservation = 1 + current time:
#                resToRemove = self.fwdResList.index(res)    # Get index of forwarded reservation to move
#                fwdingRes.append(self.fwdResList.pop(resToRemove))  # Move res to the list to a list to be returned
        self.fwdResList.clear()
        return fwdingRes

    def GetFwdResList(self):
        return self.fwdResList

    # ---------------- I n d e x i n g   R e s e r v a t i o n s -------------------

    # Removes reservations that start next time unit and returns a list of them. Allows network to index them for a continuous path.
    def GetSlottableRes(self):
        slottableRes    = []
        indexList       = []    # indexes of resevations to be locally removed and returned by this function
        i           = 0     # Current index of self.currResList

        for res in self.currResList:
            if res.linkIndex == None:   # If the res has not been slotted previously
                if res.start_t == self.curTime + 1: # If the reservation must be slotted next time unit
                    indexList.append(i)             # add to list of reservations to be popped
            i += 1

        indexList = sorted(indexList, reverse=True) # sort list of reservations to be popped
        for i in indexList:
            slottableRes.append(self.currResList.pop(i))

        return slottableRes

    # ===================================== R e s e r v a t i o n   W i n d o w ===================================
    def CheckOpenSpace(self, size):
        avail       = 0
        i           = 0
        startSlot   = None

        for space in self.timeWindow[0]:    # For each space in the current row
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

    def GetListOfOpenSpaces(self, size):
        listOfSpaces    = []    # List of spaces of size(size) in the current link
        avail           = 0
        i               = 0
        startSlot       = None

        for space in self.timeWindow[0]:    # For each space in the current row
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

        if len(listOfSpaces) <= 0:  # If no available spaces of size(size)
            return False, listOfSpaces  # Return false
        else:
            return True, listOfSpaces   # If at least one suitable space is found, return true and the list of suitable spaces

    # For checking if a space exists starting from a current start slot
    def CheckContinuousSpace(self, startSlot, size):
        for space in range(0, size):
            if self.timeWindow[startSlot + space] == FULL:
                return FULL

        return EMPTY

    def PlaceRes(self, startSlot, size, depth):
        i = 0
        j = 0
        while(i < size):
            while(j < depth):
                try:
                    self.timeWindow[j][startSlot + i] = FULL
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