from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = []
        for i in range(TIME_WNDW_SIZE):
            row = [EMPTY] * MAX_NUM_FREQ
            self.timeWindow.append(row)
        self.availSlots     = [MAX_NUM_FREQ] * TIME_WNDW_SIZE   # Number to track available slots in time row
        self.nodes          = nodes
        self.length         = length
        self.onFirstLink    = True
        self.initResList    = []
        self.currResList    = []
        self.fwdResList     = []
        self.curTime        = 0
        self.numBlocks      = 0

    # ===================================== R e s e r v a t i o n   W i n d o w ===================================

    def UpdateSize(self, startT, depth):
        if len(self.timeWindow) < startT + depth:
            for x in range((startT+depth - len(self.timeWindow))):
                row = [EMPTY] * MAX_NUM_FREQ
                self.timeWindow.append(row)
                self.availSlots.append(MAX_NUM_FREQ)

    # For checking if a space exists starting from a current start slot
    def CheckContinuousSpace(self, startSlot, size, startT, depth):
        if len(self.timeWindow) < startT + depth:
            raise
        for space in range(0, size):
            curSlot = self.timeWindow[startT][startSlot + space]
            if curSlot == FULL:
                return True
            elif curSlot == EMPTY:
                continue
            else:
                raise

        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current link
        if self.availSlots[startT] < size:  # If not enough slots for space to exist
            return listOfSpaces # return the empty list instantly
        if startT > len(self.timeWindow):
            print(startT)
            print(len(self.timeWindow))
            raise

        rowChecked = self.timeWindow[startT]
        i = 0
        while (i + size - 1 < MAX_NUM_FREQ):
            #print('1', i)
            if rowChecked[i] == EMPTY:
                #print('2', i)
                if rowChecked[i + size - 1] == EMPTY:
                    #print('3', i)
                    wasEmpty = True
                    for j in range(size - 2):
                        #print('4', i)
                        if rowChecked[i + j] == FULL:
                            #print('4-1', i)
                            wasEmpty = False
                            break
                        else:
                            #print('4-2', i)
                            wasEmpty = True
                    if wasEmpty:
                        #print('5', i)
                        listOfSpaces.append(i)
                        i += 1
                        while (i + size - 1 < MAX_NUM_FREQ):
                            #print('6', i)
                            if rowChecked[i + size - 1] == EMPTY:
                                listOfSpaces.append(i)
                                i += 1
                            else:
                                i = i + size + 1
                                break
                    else:
                        i = i + size
                else:
                    i = i + size
            else:
                i += 1
        return listOfSpaces  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startSlot, size, depth, startDepth):
        i = 0
        j = 0
        numSlotsFilled = 0

        for k in range(0, depth):
            self.availSlots[startDepth + k] -= size # Mark the time row as having less space

        for i in range(depth):
            for j in range(size):
                try:
                    self.timeWindow[startDepth + i][startSlot + j] = FULL
                except:
                    print(startDepth)
                    raise
                numSlotsFilled += 1
        if numSlotsFilled != (size*depth):
            print(numSlotsFilled, size, depth)
            raise

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self):
        for row in self.timeWindow:
            for column in row:
                if column == FULL:
                    print("[]", end='')
                else:
                    print("--", end='')
            print('')

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