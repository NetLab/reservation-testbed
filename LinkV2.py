from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = []
        self.availSlots     = []

        for i in range(TIME_WNDW_SIZE):
            row = [EMPTY] * MAX_NUM_FREQ
            self.timeWindow.append(row)

            total = MAX_NUM_FREQ
            self.availSlots.append(total)

        self.nodes          = nodes
        self.length         = length
        self.onFirstLink    = True
        self.initResList    = []
        self.currResList    = []
        self.fwdResList     = []
        self.curTime        = 0
        self.numBlocks      = 0
        self.provResList    = []
        self.windowScale    = 0

    # ===================================== R e s e r v a t i o n   W i n d o w ===================================

    def UpdateSize(self, startT, depth):
        windowLength    = len(self.timeWindow)
        newFrames       = []
        newAvail        = []
        if windowLength < startT + depth + STRT_WNDW_SIZE:
            for x in range(10 * (startT + depth + STRT_WNDW_SIZE - windowLength)):
                row     = [EMPTY] * MAX_NUM_FREQ
                newFrames.append(row)
                total   = MAX_NUM_FREQ
                newAvail.append(total)

            self.timeWindow += newFrames
            self.availSlots += newAvail

    def ScaleStartTime(self, startT):
        return startT - self.windowScale

    # For checking if a space exists starting from a current start slot
    def CheckSpaceFull(self, startSlot, size, startT, depth):
        return CheckAreaIsFull(self.timeWindow[startT:startT+depth], startSlot, size)


    def GetTimeAvailSlots(self, startT, depth):
        self.UpdateSize(startT, depth)
        return self.availSlots[startT]

    def CheckLineFull(self, startT, slot, depth):
        for row in range(startT, startT + depth):
            if self.timeWindow[row][slot] != EMPTY:
                return True
            else:
                continue
        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        return GetListOfOpenSpaces(self.timeWindow[startT:startT+depth], size)  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startDepth, depth, startSlot, size, isProv, resNum, baseStartT = None):
        i = 0
        j = 0
        errorRaised = False
        numSlotsFilled = 0
        for row in range(startDepth,startDepth+depth):
            self.availSlots[row] -= size
        for i in range(depth):
            for j in range(size):
                curSlot = self.timeWindow[startDepth + i][startSlot + j]
                if curSlot == EMPTY:
                    if j == 0 and i == 0:
                        if isProv == False:
                            self.timeWindow[startDepth + i][startSlot + j] = START
                        else:
                            self.timeWindow[startDepth + i][startSlot + j] = PROV
                    else:
                        if isProv == False:
                            self.timeWindow[startDepth + i][startSlot + j] = FULL
                        else:
                            self.timeWindow[startDepth + i][startSlot + j] = PROV
                    numSlotsFilled += 1
                elif curSlot == PROV:
                    print("Error: PlaceRes, no provisioned slots should exist at this point: time,", startDepth, startSlot + j, startDepth + i)
                    self.PrintGraphic(startDepth, startDepth + depth, startOffset = startDepth)
                    errorRaised = True
                elif self.timeWindow[startDepth + i][startSlot + j] == FULL or self.timeWindow[startDepth + i][startSlot + j] == START:
                    print("LINK", self.nodes)
                    self.PrintGraphic(startDepth, startDepth + depth, startOffset = startDepth)
                    print("tried to fill slot that was aready full: StartSlot", startSlot, j, "StartDepth", startDepth, i)
                    print("Dimensions", size, "by", depth)
                    errorRaised = True
                else:
                    print(self.timeWindow[startDepth + i][startSlot + j])
                    errorRaised = True
                if(errorRaised):
                    print("StartDepth", startDepth, "StartSlot", startSlot)
                    print("depth", depth, "size", size)
                    raise

        if numSlotsFilled != (size*depth):
            print(numSlotsFilled, size, depth)
            raise

    # ================================= P r o v i s i o n i n g   F u n c t i o n s ===============================

    def RemoveProvFromWindow(self, startD, depth, startS, size):

        endD    = startD + depth
        endS    = startS + size

        for row in range(startD, endD):
            for column in range(startS, endS):
                if self.timeWindow[row][column] == PROV:
                    self.timeWindow[row][column] = EMPTY
                else:
                    print("Error: RemoveProv, slot",column, row, "was not PROV", self.timeWindow[row][column])
                    self.PrintGraphic(startD, endD, startOffset=startD)
                    print("From", startS, startD, "to", endS, endD)
                    raise

    def GetWindowCopy(self, startT, endT):
        return deepcopy(self.timeWindow[startT:endT])

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, start, end, startOffset = 0):
        PrintGraphic(self.timeWindow, start, end, startOffset)

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

def CheckLineIsFull(window, slot):
    for row in window:
        if row[slot] != EMPTY:
            return True
        else:
            continue
    return False

def CheckAreaIsFull(window, startSlot, size):
    for row in window:
        for column in range(startSlot, startSlot + size):
            if row[column] != EMPTY:
                return True
            else:
                continue
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

def GetListOfOpenSpaces(timeWindow, size):
    listOfSpaces = []  # List of spaces of size(size) in the current row

    i = 0
    numAvail = 0
    startSlotNum = 0
    startSlot = None
    while (i < MAX_NUM_FREQ):
        wasFull = CheckLineIsFull(timeWindow, i)
        if wasFull == False:
            numAvail += 1
            #if numAvail >= 1:
                #print(numAvail)
            if startSlot == None:
                startSlot = i
                startSlotNum += 1
        else:
            numAvail  = 0
            startSlot = None
        if numAvail >= size:
            listOfSpaces.append(startSlot)
            startSlot += 1
        i += 1

    return listOfSpaces  # If at least one suitable space is found, return true and the list of suitable spaces

def PrintGraphic(window, start, end, startOffset = 0):
    i = 0
    for row in window[start:end]:
        print("{:5} ".format(i+startOffset), end='')
        for column in row:
            if column == FULL:
                print("X", end='')
            elif column == START:
                print("O", end='')
            elif column == EMPTY:
                print("-", end='')
            elif column == PROV:
                print("P", end='')
            else:
                print(column)
                raise

        print('')
        i += 1
    print("      ", end='')
    for x in range(MAX_NUM_FREQ):
        print(str(int((x % 1000)/100)), end='')
    print("\n      ", end='')
    for x in range(MAX_NUM_FREQ):
        print(str(int((x % 100)/10)), end='')
    print("\n      ", end='')
    for x in range(MAX_NUM_FREQ):
        print(str(x % 10), end='')
    print('')