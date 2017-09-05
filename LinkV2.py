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

    # For checking if a space exists starting from a current start slot
    def CheckSpaceFull(self, startSlot, size, startT, depth, checkProv):

#        for row in self.availSlots[startT:startT+depth]:
#            if row < size:
#                return True

        # for row in range(0, depth):
        #     for space in range(0, size):
        #         curSlot = self.timeWindow[startT + row][startSlot + space]
        #         if curSlot != EMPTY:
        #             return True
        #         elif curSlot == EMPTY:
        #             continue
        #         else:
        #             raise

        return CheckAreaIsFull(self.timeWindow[startT:startT+depth], startSlot, size, checkProv)


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

    def GetListOfOpenSpaces(self, size, startT, depth, checkProv):
        listOfSpaces    = []    # List of spaces of size(size) in the current row
        endT = startT+depth

        i           = 0
        numAvail    = 0
        startSlot   = None
        canBeReprov = False
        for x in range(0, STRT_WNDW_RANGE):
            listOfSpaces = []
            while (i < MAX_NUM_FREQ):
                wasFull, preProvRows = CheckLineIsFull(self.timeWindow[startT:endT], i, checkProv, startT)
                if wasFull == False:
                    if checkProv:
                        canBeReprov = True
                        for row in preProvRows:
                            canBeReprov = self.CheckReprovision(row, depth, startT)
                            if canBeReprov == False:
                                break
                    if checkProv == False or canBeReprov == True:
                        numAvail += 1
                        if startSlot == None:
                            startSlot = i
                    else:
                        numAvail    = 0
                        startSlot   = None
                else:
                    numAvail    = 0
                    startSlot   = None
                if numAvail >= size:
                    listOfSpaces.append(startSlot)
                    startSlot += 1
                i += 1

        return listOfSpaces  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startSlot, size, depth, startDepth, isProv, resNum):
        i = 0
        j = 0
        numSlotsFilled = 0
        # Remove any overlapping provisions, both the reservations own as well as any previously scheduled that may be reprovisioned
        self.RemoveOverlappingProv(startSlot, size, depth, startDepth)
        for row in range(startDepth,startDepth+depth):
            self.availSlots[row] -= size
        if isProv:
            self.AddToProvList(startSlot, startDepth, startSlot+size, startDepth+depth, resNum)
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
                    print("Error: PlaceRes, no provisioned slots should exist at this point")
                    raise
                elif self.timeWindow[startDepth + i][startSlot + j] == FULL or self.timeWindow[startDepth + i][startSlot + j] == START:
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

    # ================================= P r o v i s i o n i n g   F u n c t i o n s ===============================
    def AddToProvList(self, startSlot, startDepth, endSlot, endDepth):
        self.provResList.append([startSlot, startDepth, endSlot, endDepth])

    def RemoveProv(self, provIndex):
        prov = self.provResList[provIndex]

        provSSlot   = prov[PRV_SSlotIndex]
        provSDepth  = prov[PRV_SDepthIndex]
        provESlot   = prov[PRV_ESlotIndex]
        provEDepth  = prov[PRV_EDepthIndex]

        for row in range(provSDepth, provEDepth):
            for column in range(provSSlot, provESlot):
                if self.timeWindow[row][column] == PROV:
                    self.timeWindow[row][column] = EMPTY
                else:
                    print("Error: RemoveProv, slot was not PROV")

        self.provResList.remove(provIndex)

    def FindProvInList(self, slot, depth):
        slotIndex = 0
        for prov in self.provResList:
            provSSlot   = prov[PRV_SSlotIndex]
            provSDepth  = prov[PRV_SDepthIndex]
            provESlot   = prov[PRV_ESlotIndex]
            provEDepth  = prov[PRV_EDepthIndex]
            if (provSSlot <= slot < provESlot) and (provSDepth <= depth < provEDepth):
                return True, slotIndex
            else:
                continue
            slotIndex += 1
        return False, None


    def CheckReprovision(self, slot, depth, startT):
        provExists, provIndex = self.FindProvInList(slot, depth)
        if provExists:
            if SMALL_OR_LARGE_WINDOW == SMALL:
                if startT >= self.provResList[provIndex]:
                    return True, provIndex
                else:
                    return False, None
            else:
                return True, provIndex
        else:
            return False, None

    # Find and remove any provisions overlapping with the space defined
    # for use in (tenative) PlaceRes (or some time right before it?)
    def RemoveOverlappingProv(self, startSlot, size, depth, startDepth):
        for row in range(startDepth, startDepth + depth):
            for column in range(startSlot, startSlot + size):
                provExists, provIndex = self.CheckReprovision(column, row, startDepth)
                if provExists:
                    self.RemoveProv(provIndex)
                else:
                    continue

    # =================================== O t h e r   L i n k   F u n c t i o n s =================================

    def PrintInfo(self):
        print("Link", self.nodes, "of cost", self.length)

    def PrintGraphic(self, end):
        i = 0
        for row in self.timeWindow[0:end]:
            print("{:5} ".format(i), end='')
            for column in row:
                if column == FULL:
                    print("X", end='')
                elif column == START:
                    print("O", end='')
                elif column == EMPTY:
                    print("-", end='')
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

def CheckLineIsFull(window, slot, checkProv, startT):
    preProvSlots = []   # List of rows that were preprovisioned. Each must be checked incase they are seperate provisions
    i = 0
    for row in window:
        if row[slot] != EMPTY:
            if checkProv == True and row[slot] == PROV:
                preProvSlots.append(startT + i)
                continue
            else:
                return True
        else:
            continue
        i += 1
    return False, preProvSlots

def CheckAreaIsFull(window, startSlot, size, checkProv):
    for row in window:
        for column in range(startSlot, startSlot + size):
            if row[column] != EMPTY:
                if checkProv == True and row[column] == PROV:
                    continue
                else:
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