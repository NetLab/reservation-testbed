from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = []
        for i in range(TIME_WNDW_SIZE):
            row = [EMPTY] * MAX_NUM_FREQ
            self.timeWindow.append(row)
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
    def CheckLineFull(self, startT, slot, depth):
        for row in range(startT, startT + depth):
            if self.timeWindow[row][slot] == FULL:
                return True
            else:
                continue
        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current row

        rowChecked = self.timeWindow[startT]
        i = 0
        while (i + size - 1 < MAX_NUM_FREQ):
            #print(1, i)
            if self.CheckLineFull(startT, i, depth) == False:
                if(i + size - 1) < MAX_NUM_FREQ:
                    checkContinuous = False
                    for j in range(i+1, i + size):
                        #print(2, i)
                        if self.CheckLineFull(startT, j, depth) == False:
                            checkContinuous = True
                            continue
                        else:
                            checkContinuous = False
                            i = j + 1
                            break
                    while checkContinuous == True:
                        #print(3)
                        listOfSpaces.append(i)
                        i += 1
                        if (i + size - 1 < MAX_NUM_FREQ):
                            if self.CheckLineFull(startT, i + size - 1, depth) == True:
                                i = i + size
                                checkContinuous = False
                            else:
                                continue
                        else:
                            break
                else:
                    break

            else:
                i += 1
        return listOfSpaces  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startSlot, size, depth, startDepth):
        i = 0
        j = 0
        numSlotsFilled = 0

        for i in range(depth):
            for j in range(size):
                if self.timeWindow[startDepth + i][startSlot + j] == EMPTY:
                    self.timeWindow[startDepth + i][startSlot + j] = FULL
                    numSlotsFilled += 1
                elif self.timeWindow[startDepth + i][startSlot + j] == FULL:
                    print("LINK", self.nodes)
                    self.PrintGraphic(startDepth + depth + 10)
                    print("tried to fill slot that was aready full: StartSlot", startSlot, j, "StartDepth", startDepth, i)
                    print("Dimensions", size, "by", depth)
                    raise
                else:
                    print(self.timeWindow[startDepth + i][startSlot + j])
                    raise

        if numSlotsFilled != (size*depth):
            print(numSlotsFilled, size, depth)
            raise

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, end):
        i = 0
        for row in self.timeWindow[0:end]:
            print("{:5} ".format(i), end='')
            for column in row:
                if column == FULL:
                    print("[]", end='')
                else:
                    print("--", end='')
            print('')
            i += 1
        print("      ", end='')
        for x in range(MAX_NUM_FREQ):
            print(str(int((x % 1000)/100)) + ' ', end='')
        print("\n      ", end='')
        for x in range(MAX_NUM_FREQ):
            print(str(int((x % 100)/10)) + ' ', end='')
        print("\n      ", end='')
        for x in range(MAX_NUM_FREQ):
            print(str(x % 10) + ' ', end='')
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
