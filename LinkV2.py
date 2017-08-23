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
        windowLength    = len(self.timeWindow)
        newFrames       = []
        newAvail        = []
        if windowLength < startT + depth:
            for x in range(10 * (startT+depth - windowLength)):
                row = [EMPTY] * MAX_NUM_FREQ
                newFrames.append(row)
                newAvail.append(MAX_NUM_FREQ)

            self.timeWindow += newFrames
            self.availSlots += newAvail

    # For checking if a space exists starting from a current start slot
    def CheckContinuousSpace(self, startSlot, size, startT, depth):
        crossSection = self.timeWindow[startT:startT+depth]
        endSlot = startSlot + size
        for column in range(startSlot,endSlot):
            if CheckLineFull(crossSection, column) == True:
                return True
            else:
                continue
        # for row in range(0, depth):
        #     for space in range(0, size):
        #         curSlot = self.timeWindow[startT + row][startSlot + space]
        #     if curSlot == FULL:
        #         return True
        #     elif curSlot == EMPTY:
        #         continue
        #     else:
        #         raise

        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current link
        endT            = startT + depth
        numAvail        = 0
        startIndex      = None
        numBlocked      = 0

        i = 0
        while (i + size - 1 < MAX_NUM_FREQ):
            if CheckLineFull(self.timeWindow[startT:endT], i) == False:
                numAvail += 1
                if startIndex == None:
                    startIndex = i
            else:
                numAvail    = 0
                startIndex  = None
                numBlocked += 1
            if numAvail >= size:
                listOfSpaces.append(startIndex)
                startIndex += 1
            i += 1

            #         checkContinuous = False
            #         for j in range(i+1, i + size):
            #             if CheckLineFull(self.timeWindow[startT:endT], j, depth) == False:
            #                 checkContinuous = True
            #                 continue
            #             else:
            #                 checkContinuous = False
            #                 i = j + i
            #                 break
            #         while checkContinuous == True:
            #             listOfSpaces.append(i)
            #             if len(listOfSpaces) > MAX_NUM_FREQ:
            #                 raise
            #             i += 1
            #             if (i + size - 1 < MAX_NUM_FREQ):
            #                 if CheckLineFull(self.timeWindow[startT:startT + depth], i + size - 1, depth) == False:
            #                     i = i + size
            #                     checkContinuous = False
            #                 else:
            #                     continue
            #             else:
            #                 break
            #     else:
            #         break
            # else:
            #     i += 1

#        if numBlocked >= 4:
#            self.PrintGraphic(startT, endT + 1)
#            print(listOfSpaces)
#            raise

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
                    if self.timeWindow[startDepth + i][startSlot + j] == EMPTY:
                        self.timeWindow[startDepth + i][startSlot + j] = FULL
                    else:
                        raise
                except:
                    self.PrintGraphic(startDepth, startDepth + depth + 1)
                    print(startSlot, startDepth, "size", size, "by", depth)
                    raise
                numSlotsFilled += 1
        if numSlotsFilled != (size*depth):
            print(numSlotsFilled, size, depth)
            raise

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, start, end):
        for row in self.timeWindow[start:end]:
            for column in row:
                if column == FULL:
                    print("X", end='')
                else:
                    print("-", end='')
            print('')

    def GetLinkNodes(self):
        return self.nodes[0], self.nodes[1]

def CheckLineFull(window, slot):
    for row in window:
        if row[slot] != EMPTY:
            return True
        else:
            continue
    return False

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

