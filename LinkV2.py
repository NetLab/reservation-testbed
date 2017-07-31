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

    def UpdateSize(self, startT, depth, windowSize):
        windowLength    = len(self.timeWindow)
        newFrames       = []
        newAvail        = []
        if windowLength < startT + depth + windowSize:
            for x in range(10 * (startT + depth + windowSize - windowLength)):
                row = [EMPTY] * MAX_NUM_FREQ
                newFrames.append(row)
                newAvail.append(MAX_NUM_FREQ)

            self.timeWindow += newFrames
            self.availSlots += newAvail

    # For checking if a space exists starting from a current start slot
    def CheckSpaceFull(self, startSlot, size, startT, depth):
        for row in range(0, depth):
            for space in range(0, size):
                curSlot = self.timeWindow[startT + row][startSlot + space]
                if curSlot == FULL:
                    return True
                elif curSlot == EMPTY:
                    continue
                else:
                    raise

        return False
#    def GetOpenSpaceAfter(self, size, startT, ):

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current link
        rowChecked = self.timeWindow[startT]
        i = 0
        while (i + size - 1 < MAX_NUM_FREQ):
            if rowChecked[i] == EMPTY:
                if rowChecked[i + size - 1] == EMPTY:
                    wasEmpty = True
                    for j in range(size - 2):
                        if rowChecked[i + j] == FULL:
                            wasEmpty = False
                            break
                        else:
                            wasEmpty = True
                    if wasEmpty:
                        listOfSpaces.append(i)
                        i += 1
                        while (i + size - 1 < MAX_NUM_FREQ):
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
                if self.timeWindow[startDepth + i][startSlot + j] != FULL:
                    self.timeWindow[startDepth + i][startSlot + j] = FULL
                    numSlotsFilled += 1
                else:
                    print("tried to fill slot that was aready full", startSlot, j, startDepth, i)
                    print("LINK", self.nodes)
                    #self.PrintGraphic(startSlot + depth)
                    raise
        if numSlotsFilled != (size*depth):
            print(numSlotsFilled, size, depth)
            raise

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, end):
        for row in self.timeWindow[0:end]:
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