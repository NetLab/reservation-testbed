from operator import attrgetter
from ReservationV2 import *
from copy import deepcopy

class Link:
    def __init__(self, nodes, length):
        self.timeWindow     = []
        self.availSlots     = []

        for i in range(InitWindowSize):
            row = [EMPTY] * MAX_NUM_FREQ
            self.timeWindow.append(row)

            total = MAX_NUM_FREQ
            self.availSlots.append(total)

        self.nodes          = nodes
        self.length         = length
        self.windowScale    = 0

    # ===================================== R e s e r v a t i o n   W i n d o w ===================================

    def UpdateSize(self, time):
        newFrames       = []
        newAvail        = []

        scaledTime = self.ScaleStartTime(time)
        self.timeWindow = self.timeWindow[scaledTime:]
        self.availSlots = self.availSlots[scaledTime:]
        self.windowScale = time

        for x in range(UpdateTimeToAdd):
            row     = [EMPTY] * MAX_NUM_FREQ
            newFrames.append(row)
            newAvail.append(MAX_NUM_FREQ)

        self.timeWindow += newFrames
        self.availSlots += newAvail

    def ScaleStartTime(self, startT):
        return startT - self.windowScale

    # For checking if a space exists starting from a current start slot
    def CheckSpaceFull(self, startSlot, size, startT, depth):
        startT = self.ScaleStartTime(startT)
        return CheckAreaIsFull(self.timeWindow[startT:startT+depth], startSlot, size)

    def GetTimeAvailSlots(self, time):
        scaledTime = self.ScaleStartTime(time)
        return self.availSlots[scaledTime]

    def CheckLineFull(self, startT, slot, depth):
        startT = self.ScaleStartTime(startT)
        for row in range(startT, startT + depth):
            if self.timeWindow[row][slot] != EMPTY:
                return True
            else:
                continue
        return False

    def GetListOfOpenSpaces(self, size, startT, depth):
        startT = self.ScaleStartTime(startT)
        return GetListOfOpenSpaces(self.timeWindow[startT:startT+depth], size)  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startDepth, depth, startSlot, size, isProv, resNum, baseStartT = None):
        errorRaised = False
        numSlotsFilled = 0
        startDepth = self.ScaleStartTime(startDepth)
        for row in range(startDepth,startDepth+depth):
            try:
                self.availSlots[row] -= size
            except IndexError:
                print("Link", self.nodes, "is of invalid length", len(self.timeWindow), "for res from", startDepth, "to", startDepth + depth)
                raise
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

    def PlaceRes_NoCheck(self, startDepth, depth, startSlot, size, isProv, resNum, baseStartT=None):
        numSlotsFilled = 0
        startDepth = self.ScaleStartTime(startDepth)
        for row in range(startDepth, startDepth + depth):
            try:
                self.availSlots[row] -= size
            except IndexError:
                print("Link", self.nodes, "is of invalid length", len(self.timeWindow), "for res from", startDepth,
                      "to", startDepth + depth)
                raise
        for i in range(depth):
            for j in range(size):
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

    # ================================= P r o v i s i o n i n g   F u n c t i o n s ===============================

    def RemoveProvFromWindow(self, startDepth, depth, startSlot, size):

        scaledStart = self.ScaleStartTime(startDepth)
        endD    = scaledStart + depth
        endS    = startSlot + size

        for row in range(scaledStart, endD):
            for column in range(startSlot, endS):
                if self.timeWindow[row][column] == PROV:
                    self.timeWindow[row][column] = EMPTY
                else:
                    print("Error: RemoveProv, slot",column, row, "was not PROV", self.timeWindow[row][column])
                    self.PrintGraphic(0, -1, startOffset=scaledStart)
                    print("From", startSlot, scaledStart, "to", endS, endD)
                    print("Window Scale", self.windowScale)
                    raise

    def RemoveProvFromWindow_NoCheck(self, startDepth, depth, startSlot, size):

        scaledStart = self.ScaleStartTime(startDepth)
        endD = scaledStart + depth
        endS = startSlot + size

        for row in range(scaledStart, endD):
            for column in range(startSlot, endS):
                self.timeWindow[row][column] = EMPTY

    def GetWindowCopy(self, startT, endT):
        startT = self.ScaleStartTime(startT)
        endT = self.ScaleStartTime(endT)
        return deepcopy(self.timeWindow[startT:endT])

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, start, end, startOffset = 0):
        startT = self.ScaleStartTime(start)
        end = self.ScaleStartTime(start)
        PrintGraphic(self.timeWindow, start, end, startOffset)

    def GetLinkNodes(self):
        return self.nodes[0], self.nodes[1]

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

def GetListOfOpenSpaces(timeWindow, size, scale=0):
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