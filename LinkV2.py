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
    def CheckSpaceFull(self, startSlot, size, checkTime, depth):

#        for row in self.availSlots[startT:startT+depth]:
#            if row < size:
#                return True

        for row in range(0, depth):
            for space in range(0, size):
                try:
                    curSlot = self.timeWindow[checkTime + row][startSlot + space]
                except:
                    print(checkTime, startSlot)
                    raise
                if curSlot != EMPTY:
                    return True
                elif curSlot == EMPTY:
                    continue
                else:
                    raise

        return False

    def GetTimeAvailSlots(self, startT, depth):
        self.UpdateSize(startT, depth)
        return self.availSlots[startT]

    def GetListOfOpenSpaces(self, size, startT, depth):
        listOfSpaces    = []    # List of spaces of size(size) in the current row
        numAvail        = []
        startSlot       = []
        for x in range(STRT_WNDW_RANGE):
            listOfSpaces.append([])
            numAvail.append(0)
            startSlot.append(None)
        endT = startT+depth + STRT_WNDW_SIZE
        i           = 0
        while (i < MAX_NUM_FREQ):
            spaceList = []
            for x in range(STRT_WNDW_RANGE):
                spaceList.append(EMPTY)
            numEmpty = STRT_WNDW_RANGE
            for row in range(startT,endT):
                if self.timeWindow[row][i] != EMPTY:
                    for space in range(STRT_WNDW_RANGE):
                        if startT + space <= row and row < startT + space + depth:
                            if spaceList[space] == EMPTY:  # If space was not already invalidated
                                numEmpty -= 1  # Deincrement the number of possible valid spaces
                                spaceList[space] = FULL  # Mark space Full
                if numEmpty == 0:  # If no spaces can be empty after this point
                    break
#            freeSpaces = CheckLineIsFull(self.timeWindow[startT:endT], i, depth, STRT_WNDW_RANGE)
            for space in range(STRT_WNDW_RANGE):
                if spaceList[space] == EMPTY:
                    numAvail[space] += 1
                    if startSlot[space] == None:
                        startSlot[space] = i
                    if numAvail[space] >= size:
                        listOfSpaces[space].append(startSlot[space])
                        startSlot[space] += 1
                else:
                    numAvail[space]     = 0
                    startSlot[space]    = None
            #print("For Column", i)
            #print(freeSpaces)
            #input()
            i += 1

        return listOfSpaces  # If at least one suitable space is found, return true and the list of suitable spaces

    def PlaceRes(self, startSlot, size, depth, startDepth):
        i = 0
        j = 0
        numSlotsFilled = 0

        for row in range(startDepth,startDepth+depth):
            self.availSlots[row] -= size

        for i in range(depth):
            for j in range(size):
                if self.timeWindow[startDepth + i][startSlot + j] == EMPTY:
                    if j == 0 and i == 0:
                        self.timeWindow[startDepth + i][startSlot + j] = START
                    else:
                        self.timeWindow[startDepth + i][startSlot + j] = FULL
                    numSlotsFilled += 1
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

def CheckLineIsFull(window, slot, depth, slideSize):
    spaceList   = []
    for x in range(slideSize):
        spaceList.append(EMPTY)
    numEmpty    = slideSize
    for row in range(0,len(window)):
        if window[row][slot] != EMPTY:
            for space in range(slideSize):
                if space <= row and row < space + depth:
                    if spaceList[space] == EMPTY:    # If space was not already invalidated
                        numEmpty -= 1                  # Deincrement the number of possible valid spaces
                        spaceList[space] = FULL         # Mark space Full
        if numEmpty == 0:  # If no spaces can be empty after this point
            break
    return spaceList

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

if __name__ == '__main__':
    link = Link('AB', 500)
    #link.PlaceRes(startSlot, size, depth, startDepth)
    link.PlaceRes(0, 4, 6, 0)
    link.PlaceRes(6, 6, 2, 0)
    link.PlaceRes(4, 2, 3, 4)
    #link.PlaceRes(5, 1, 1, 2)
    link.PrintGraphic(7)
    #link.GetListOfOpenSpaces(size, startT, depth)
    listOf = link.GetListOfOpenSpaces(2, 0, 4)
    for thing in listOf:
        print(thing)
