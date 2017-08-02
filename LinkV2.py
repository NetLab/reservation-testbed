from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = []
        for i in range(TIME_WNDW_SIZE):
            row = []
            row.append(MAX_NUM_FREQ)
            row.append([EMPTY] * MAX_NUM_FREQ)
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
        if windowLength < startT + depth + windowSize:
            for x in range(10 * (startT + depth + windowSize - windowLength)):
                row     = []
                row.append(MAX_NUM_FREQ)
                row.append([EMPTY] * MAX_NUM_FREQ)
                newFrames.append(row)

            self.timeWindow += newFrames

    # For checking if a space exists starting from a current start slot
    def CheckSpaceFull(self, startSlot, size, startT, depth):

        for row in self.timeWindow[startT:startT+depth]:
            if row[AVAIL_SLOTS_INDEX] < size:
                return True

        for row in range(0, depth):
            for space in range(0, size):
                curSlot = self.timeWindow[startT + row][TIME_WINDOW_INDEX][startSlot + space]
                if curSlot == FULL:
                    return True
                elif curSlot == EMPTY:
                    continue
                else:
                    raise

        return False

    def GetTimeAvailSlots(self, startT, depth):
        updateWindow = UpdateSizeOuter(len(self.timeWindow), startT, depth)
        if updateWindow is not None:
            self.timeWindow += updateWindow
        return self.timeWindow[startT][AVAIL_SLOTS_INDEX]

    def CheckLineFull(self, startT, slot, depth):
        for row in range(startT, startT + depth):
            if self.timeWindow[row][TIME_WINDOW_INDEX][slot] == FULL:
                return True
            else:
                continue
        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current row
        endT = startT+depth
        i = 0

        for row in self.timeWindow[startT:endT]:
            total = row[AVAIL_SLOTS_INDEX]
            if total < size:
                return listOfSpaces

        while (i + size - 1 < MAX_NUM_FREQ):
            #print(1, i)
#            if self.CheckLineFull(startT, i, depth) == False:
            if CheckLineIsFull(self.timeWindow[startT:endT], i) == False:
                if(i + size - 1) < MAX_NUM_FREQ:
                    checkContinuous = False
                    for j in range(i+1, i + size):
                        #print(2, i)
#                        if self.CheckLineFull(startT, j, depth) == False:
                        if CheckLineIsFull(self.timeWindow[startT:endT], j) == False:
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
#                            if self.CheckLineFull(startT, i + size - 1, depth) == True:
                            if CheckLineIsFull(self.timeWindow[startT:endT], i + size - 1) == True:
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

        for row in range(startDepth,startDepth+depth):
            self.timeWindow[row][AVAIL_SLOTS_INDEX] -= size

        for i in range(depth):
            for j in range(size):
                if self.timeWindow[startDepth + i][TIME_WINDOW_INDEX][startSlot + j] == EMPTY:
                    self.timeWindow[startDepth + i][TIME_WINDOW_INDEX][startSlot + j] = FULL
                    numSlotsFilled += 1
                elif self.timeWindow[startDepth + i][TIME_WINDOW_INDEX][startSlot + j] == FULL:
                    print("LINK", self.nodes)
                    self.PrintGraphic(startDepth + depth + 10)
                    print("tried to fill slot that was aready full: StartSlot", startSlot, j, "StartDepth", startDepth, i)
                    print("Dimensions", size, "by", depth)
                    raise
                else:
                    print(self.timeWindow[startDepth + i][TIME_WINDOW_INDEX][startSlot + j])
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
            window = row[TIME_WINDOW_INDEX]
            for column in window:
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

def CheckLineIsFull(row, slot):
    for line in row:
        try:
            if line[TIME_WINDOW_INDEX][slot] == FULL:
                return True
            else:
                continue
        except:
            print(line, slot)
            print(row)
            print(row[TIME_WINDOW_INDEX])
            raise
    return False

def CheckAvailSlots(row):
    return row[AVAIL_SLOTS_INDEX]

def UpdateSizeOuter(length, startT, depth):
    windowLength    = length
    newFrames       = []
    if windowLength < startT + depth + STRT_WNDW_SIZE:
        for x in range(10 * (startT + depth + STRT_WNDW_SIZE - windowLength)):
            row     = []
            row.append(MAX_NUM_FREQ)
            row.append([EMPTY] * MAX_NUM_FREQ)
            newFrames.append(row)

        return newFrames