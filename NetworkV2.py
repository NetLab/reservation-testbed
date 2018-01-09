from LinkV2 import *
from copy import deepcopy, copy
from time import *
from argparse import *

# Routing and Network Assignment

class Network:
    def __init__(self, numNodes, linkVals):
        self.nodeDict           = {}
        self.pathDict           = {}
        self.linkDict           = {}

        self.DEBUG_SrcDstCount  = {}

        self.initialResList     = []
        self.provisionedResList = []
        self.tempProvResData    = []

        self.arrivingResList    = []  # Dictionary reservations that will arrive in the next time unit

        self.time               = 0
        self.completedRes       = 0
        self.immediateBlocking  = 0
        self.promisedBlocking   = 0
        self.successfulReprov   = 0
        self.unsuccessfulReprov = 0

        self.debugFirstLink     = 0
        self.DEBUG_ResNum       = []

        self.InitNodes(numNodes)
        self.InitLinkList(linkVals)

        self.D_Avg_1 = 0
        self.D_Num_1 = 0
        self.D_Avg_2 = 0
        self.D_Num_2 = 0
        self.D_Avg_3 = 0
        self.D_Num_3 = 0
        self.D_Avg_4 = 0
        self.D_Num_5 = 0

    # ========================================= N o d e   F u n c t i o n s =======================================
    # --------------------------- I n i t -------------------------
    def InitNodes(self, numNodes):      # Initiate a list of nodes on the network from a list of tuples
        self.nodeDict.clear()
        self.pathDict.clear()
        if numNodes > 26:
            ReportError("InitNodes", "Number of Nodes must be less than 26; Number given: {0}".format(numNodes))
            raise NetworkError
        tempList = NodeList[0:numNodes]
        for node in tempList:
            self.nodeDict[node] = {}
            self.pathDict[node] = {}
            self.DEBUG_SrcDstCount[node] = {}
            for node2 in tempList:
                if node != node2:
                    self.DEBUG_SrcDstCount[node][node2] = 0

    # ------------------------ G e t / S e t ----------------------
    def GetNodes(self):
        nodes = []
        for node in self.pathDict:
            nodes.append(node)
        return ''.join(nodes)

    def SetNodeLink(self, nodeSrc, nodeDst, cost):  # Tell the node it has a link to another node
        self.nodeDict[nodeSrc][nodeDst] = cost

    def SetNodePairLink(self, linkNodes, cost):     # Tell a pair of nodes they link with one another
        self.SetNodeLink(linkNodes[0], linkNodes[1], cost)
        self.SetNodeLink(linkNodes[1], linkNodes[0], cost)

    def GetNodeLinks(self, node):
        links = self.nodeDict[node]
        if len(links) == 0:
            print("ERROR: GetNodeLinks -> No Links on Node", node)
        return links

    # -------------------- C h e c k  V a l i d -------------------
    def CheckValidNode(self, node):
        for valid in self.nodeDict:     # Check each valid node in the listr
            if node == valid:               # If any match with the node given, return true
                return True
        return False                        # Else return false

    def CheckValidNodePair(self, node1, node2):
        if (self.CheckValidNode(node1) and self.CheckValidNode(node2)): # If both valid
            return True                                                     # Return True
        return False                                                    # Else Return False

    # -------------------------- P r i n t ------------------------
    def PrintNodes(self):    # Print a formatted list of all nodes on the network and their info
        print("Using Nodes:")
        for node in self.nodeDict:
            print(node, end="")
        print("")   # Print final newline

    def PrintNodeLinks(self):
        for node in self.nodeDict:
            self.nodeDict[node].PrintInfo()

    # ========================================= L i n k   F u n c t i o n s =======================================
    # --------------------------- I n i t -------------------------
    def InitLinkList(self, linkList):
        self.linkDict.clear()   # Clear any previously existing links
        for link in linkList:

            linkNodes = link[L_NodePrIndex]
            linkLength = link[L_LengthIndex]

            self.linkDict[linkNodes] = Link(linkNodes, linkLength)  # Create a Link object between nodes of a length
            reversePair = linkNodes[::-1]
            self.linkDict[reversePair] = Link(reversePair, linkLength)

            self.SetNodePairLink(linkNodes, linkLength)             # Update node objects to know their links

    # -------------------------- P r i n t ------------------------
    def PrintLinks(self):    # Print a formatted list of all links on the network and their info
        print("With Links:")
        for link in self.linkDict:      # Print each link in the link dictionary
            self.linkDict[link].PrintInfo()

    # ========================================= P a t h   F u n c t i o n s =======================================

    def FindShortestPath(self, src, dst):
        if (self.CheckValidNodePair(src, dst) == False):
            print("ERROR: FindShortestPath -> Invalid Source Node,", src, "or Destination Node,", dst)
            raise
        pathAndCost = self.PathDefinedTo(src, dst) # Check if a path has been found before
        pathCheck = pathAndCost[0]
        costCheck = pathAndCost[1]
        if pathCheck != None:    # If a path already exists to this node
            return pathCheck, costCheck     # Return it, otherwise find one here
        debugInfo   = False
        costDict    = {}
        solvedDict  = {}
        curNode     = src
        curPath     = src
        curCost     = 0
        pathFound   = False
        # Set up default values for each connection
        for node in self.nodeDict:
            costDict[node] = [node, float("inf")]   # Mark node with default path and infinite cost
            solvedDict[node] = False        # Mark each node as not solved
        # Initialize first node connection values
        costDict[src] = [src, 0]

        while(pathFound == False):
            curLeastCost = float("inf") # Reset 'least cost' to infinite
            solvedDict[curNode] = True  # Mark current node as "solved" (This goes here b/c of initial loop)

            if debugInfo:
                print("curNode", curNode)
            curLinksDict = self.GetNodeLinks(curNode)   # Get all connections to current node
            for node in curLinksDict:
                # If the combined cost of the current path and the link to a node is less than previously recorded path
                if curCost + curLinksDict[node] < costDict[node][P_CostIndex] and solvedDict[node] == False:
                    costDict[node] = [curPath + node, curLinksDict[node] + curCost]
            for node in costDict:
                if costDict[node][P_CostIndex] < curLeastCost and solvedDict[node] == False:
                    curLeastCost = costDict[node][P_CostIndex]
                    curNode = node
                    if debugInfo:
                        print("     curLeastCost: Node", curNode, "with", curLeastCost)

            curPath = costDict[curNode][P_PathIndex]
            curCost = costDict[curNode][P_CostIndex]
            for node in solvedDict:
                if solvedDict[node] == False:   # If any nodes are not solved, mark pathFound false and break
                    pathFound = False
                    break
                pathFound = True                # If loop allowed to fully complete, it marks the end of DSP
        self.pathDict[src][dst] = costDict[dst][P_PathIndex], costDict[dst][P_CostIndex]
        reversePath = costDict[dst][P_PathIndex][::-1]
        self.pathDict[dst][src] = reversePath, costDict[dst][P_CostIndex]
        if debugInfo:
            print("Path", costDict[dst][P_PathIndex], "of cost", costDict[dst][P_CostIndex], "from", src, "to", dst)
        return costDict[dst]

    def PathDefinedTo(self, src, dst):
        try:
            if dst in self.pathDict[src]:
                path, cost = self.pathDict[src][dst]
                return path, cost
            else:
                return None, None
        except:
            print(src, dst)
            print(self.pathDict[src])
            raise

    def VerifyPath(self, linkPath): # Verify that the listed path exists between links on the network
        i = 0
        pathLen = len(linkPath)
        while (i != pathLen - 1):   # Iterate through the charaacters in the path string
            if (self.linkDict.get(linkPath[i] + linkPath[i + 1]) is None):  # If a direct link between nodes in path DNE
                print("ERROR: VerifyPath -> with link:", linkPath[i] + linkPath[i+1])
                return False    #report an error and return false
            i += 1
        return True     # If all links present in correct direction, return true

    # ====================== B a n d w i t h   R e s e r v a t i o n   F u n c t i o n s =========================
    # ---------------- G e n e r a t e   R e s e r v a t i o n s -------------------

    # Generate a reservation with random values
    def CreateRes(self, my_lambda, nodes, resNum, prevArrivalT):
        res = Reservation(my_lambda, nodes, resNum, prevArrivalT)
        src, dst = res.GetSrcDst()  # Get the source and destination nodes for the reservation
        path, cost = self.FindShortestPath(src, dst)    # Find the shortest src/dst path, and the cost of that path
        self.DEBUG_SrcDstCount[src][dst] += 1
        res.SetPath(path)  # Set the shortest path for that reservation
        blocked = res.SetNumSlots(cost)   # Set the number of slots the reservation will take
        if res.num_slots == None:
            raise
        if blocked:
            self.immediateBlocking += 1
            print("M = 0?")
        else:
            self.initialResList.append(res)
        return res.arrival_t    # Return arrival time generated for this reservation

    # Generate several reservations with random values
    def CreateMultRes(self, my_lambda, numRes, seedInt):
        i = 0
        prevArrivalT = 0
        nodes = self.GetNodes()
        random.seed(a=seedInt)

        while i < numRes:
            prevArrivalT = self.CreateRes(my_lambda, nodes, i, prevArrivalT)
            i += 1
        self.SortInitResByArrivalT()

    def LoadRes(self, resVars, resNum):
        res = Reservation(1, NodeList, resNum, 0)
        res.sourceNode  = resVars[R_NodesIndex][0]
        res.destNode    = resVars[R_NodesIndex][1]
        res.arrival_t   = resVars[R_ArrivIndex]
        res.start_t     = resVars[R_StartIndex]
        res.holding_t   = resVars[R_HoldiIndex]
        res.num_slots   = resVars[R_NumSlIndex]
        src, dst = res.GetSrcDst()  # Get the source and destination nodes for the reservation
        path, cost = self.FindShortestPath(src, dst)  # Find the shortest src/dst path, and the cost of that path
        res.SetPath(path)  # Set the shortest path for that reservation

        self.initialResList.append(res)
        return res.path

    # Sort res in arrivingResList by their start time
    def SortInitResByArrivalT(self):
        self.initialResList.sort(key=lambda res: (res.arrival_t, res.resNum))

    # Sort res in arrivingResList by their start time
    def SortArrivingResByStartT(self):
        self.arrivingResList.sort(key=lambda res: (res.start_t, res.arrival_t, res.resNum))

    def PrintInitialResList(self):
        for res in self.initialResList:
            res.PrintInfo()

    # Print out arrivingResList
    def PrintArrivingResList(self):
        for res in self.arrivingResList:
            res.PrintInfo()

    # ------------------ H a n d l e   R e s e r v a t i o n s ---------------------
    # For use upon reservations initial arrival at first node. Checks if a continuous space is open on its path right now.
    #   Returns the first index found. Blocks if none.
    def FindContinuousSpace(self, res):
        hasPath         = False

        size            = res.GetNumSlots() # get the size in slots of the request
        listLinks       = res.GetPath()
        baseStartT      = res.GetStartT()

        holdT           = res.GetHoldingT()

        for offset in range(0, STRT_WNDW_RANGE):
            checkTime = baseStartT + offset
            leastAvail = 128
            linkToCheck = 0
            i = 0

            for link in listLinks:
                linkAvail = self.linkDict[link].GetTimeAvailSlots(checkTime)
                if linkAvail <= leastAvail:
                    leastAvail = linkAvail
                    linkToCheck = i
                i += 1

            spaceOptions    = self.linkDict[listLinks[linkToCheck]].GetListOfOpenSpaces(size, checkTime, holdT) # Possible cont. spaces in init. link

            if len(spaceOptions) == 0 :# If no spaces are found at this time
                continue    # Skip to the next time in window
            elif len(listLinks) == 1:  # If only one link in path
                return True, spaceOptions[0], checkTime     # Return that a path was found, and the first spot found

            for startSlot in spaceOptions:  # For each possible space
                pathSpace = startSlot
                for link in listLinks:  # For each link beyond the first in the path, as first link has already been confirmed
                    if link != listLinks[linkToCheck]:  # If link is not the one the list of space options was gotten from
                        isFull = self.linkDict[link].CheckSpaceFull(startSlot, size, checkTime, holdT)  # Check each possible space

                        if isFull:
                            hasPath = False     # If the space is full in any link, move on to the next possible space
                            break
                        else:
                            hasPath = True

                if hasPath:             # If any possible space is empty on every link
                    return True, pathSpace, checkTime   # return True and the index of the space

            if hasPath: # If hasPath is somehow True at this point, raise an error
                print("Oops, I did something wrong")
        return False, None, None

    def AddToProvList(self, startT, startDepth, startSlot, size, depth, path, resNum):
        self.tempProvResData.append(ReservationData(startT, startDepth, startSlot, size, depth, path, resNum))

    def GetPathTempProv(self, path):
        provList = []
        for tempProv in self.tempProvResData:
            for link in path:
                if link in tempProv.path:
                    provList.append(tempProv)
                    break
        provList.sort(key=lambda prov: (prov.bStartT, prov.resNum))
        return provList

    # Get a list of currently provisioned reservations along the incoming reservation's path
    #   as well as min/max values for the relevant start/end times
    def GetReproWindow(self, res):
        pathProvisions = []             # Currently provisioned reservations on res' path
        minTime                 = 0     # Minimum start time for reservation to be considered for reprov
        maxTime                 = 0     # Maximum start time for reservation to be considered for reprov
        minWindowBase           = 0     # Base of window to be copied from current link configuration
        maxWindowBound          = 0     # Bound of window to be copied from current link configuration
        provNotConsidered_Index = []    # Prov to be removed from pathProvision as they fall outside min/maxTime (index)

        resStartT       = res.GetStartT()
        linkList        = res.GetPath()
        pathProvisions  = self.GetPathTempProv(linkList)

        maxTime = resStartT + res.GetHoldingT() + STRT_WNDW_SIZE + 20

        if len(pathProvisions) > 0:
            if SMALL_OR_large_WINDOW:
                minTime = resStartT
            else:
                minTime = self.time
        else:
            return None, None, None, None, []   # Return Nones and an empty list if no provisions

        for provIndex in range(len(pathProvisions)):
            prov = pathProvisions[provIndex]
            if prov.rStartT < minTime or maxTime < prov.rStartT:
                provNotConsidered_Index.append(provIndex)

        provNotConsidered_Index.sort(reverse=True)
        for i in provNotConsidered_Index:       # Remove all provisions outside of reprov window
            pathProvisions.pop(i)

        minWindowBase   = minTime   # Set default window B/B to known values
        maxWindowBound  = maxTime
        for prov in pathProvisions:
            if prov.bStartT < minWindowBase:
                minWindowBase = prov.bStartT
            if prov.bStartT + prov.holdingT + STRT_WNDW_SIZE > maxWindowBound:
                maxWindowBound = prov.bStartT + prov.holdingT + STRT_WNDW_SIZE

        return minTime, minWindowBase, maxTime, maxWindowBound, pathProvisions

    def ClearProvAcrossTempLinks(self, pathProvisions, tempLinkDict, minWindowBase, minTime, maxWindowBound):
        for provIndex in range(len(pathProvisions)):
            prov        = pathProvisions[provIndex]
            provStartD  = prov.rStartT - minWindowBase # Get base startT relative to earliest startT
            provStartS  = prov.sSlot
            provDepth   = prov.holdingT
            provSize    = prov.nSlots
            provEndD    = provStartD + provDepth
            provEndS    = provStartS + provSize
            provPath    = prov.path
            for link in provPath:
                for i in range(provStartD, provEndD):
                    for j in range(provStartS, provEndS):
                        tempLinkDict[link][i][j] = EMPTY
                        #try:
                        #    if tempLinkDict[link][i][j] == PROV:
                        #        tempLinkDict[link][i][j] = EMPTY
                            #else:
                            #    PrintGraphic(tempLinkDict[link], 0, -1)
                            #    print(i+minTime,j, provSize)
                            #    print("Link", link, "on", provPath)
                            #    print("From ", provStartD, "to", provEndD, "and", provStartS, "to", provEndS)
                            #    print(tempLinkDict[link][i][j] )
                            #    print("Max window size", maxWindowBound)
                            #    raise
                        #except IndexError:  # DEBUG, REMOVE
                        #    print(i, j)
                        #    print("From ", provStartD, "to", provDepth, "and", provStartS, "to", provSize)
                        #    print("With window from", minTime, "to", maxWindowBound)
                        #    print(len(tempLinkDict[link]))
                        #    print(len(tempLinkDict[link][i]))
                        #    print(len(tempLinkDict[link][i][j]))
                        #    raise
        return tempLinkDict

    def PopProvisions(self, pathProvisions):
        reprovisionedResNum = []
        tempProvResList     = []
        provRes_Index       = []

        for resData in pathProvisions:  # Get a list of all unique resNum involved in this reprovisioning
            if resData.resNum in reprovisionedResNum:   # If it exists in the list already, pass
                continue
            else:
                reprovisionedResNum.append(resData.resNum)  # Else add it to the list

        for resNum in reprovisionedResNum:
            for i in range(len(self.provisionedResList)):
                if self.provisionedResList[i].resNum == resNum:
                    provRes_Index.append(i)
                    break

        if len(reprovisionedResNum) != len(provRes_Index):
            print("Mismatched List Length")
            raise

        provRes_Index.sort(reverse=True)
        for index in provRes_Index:
            tempProvResList.append(self.provisionedResList.pop(index))

        return tempProvResList

    def CheckEnoughSpace(self, res):
        startT  = res.GetStartT()
        depth   = res.GetHoldingT()
        size    = res.GetNumSlots()
        for link in res.path:
            numConcurrentRows = 0
            linkHasSpace = False
            for line in range(startT, startT + depth + STRT_WNDW_SIZE):
                if self.linkDict[link].GetTimeAvailSlots(line) < size:
                    numConcurrentRows = 0
                else:
                    numConcurrentRows += 1
                if numConcurrentRows >= depth:
                    linkHasSpace = True
                    break
            if linkHasSpace == False:
                return False
        return True

    def ClearProvAcrossLinks(self, resData):
        resID = resData.resNum
        foundProv = False
        i = 0
        for prov in self.tempProvResData:
            if prov.resNum == resID:
                foundProv = True
                break
            i += 1
        if foundProv == False:
            raise

        path    = prov.path
        startD  = prov.rStartT
        depth   = prov.holdingT
        startS  = prov.sSlot
        size    = prov.nSlots
        self.tempProvResData.pop(i)
        try:
            for link in path:
                self.linkDict[link].RemoveProvFromWindow_NoCheck(startD, depth, startS, size)
        except:
            print("HERE", startD, depth)
            raise

    def CheckReprovision(self, res, time):
        tempLinkDict    = {}
        listLinks       = res.GetPath()
        relevantLinks   = copy(listLinks)
        tempResCoords   = {}
        newReprovResList = []

        #if self.CheckEnoughSpace(res) == False:
        #    return False

        minTime, minWindowBase, maxTime, maxWindowBound, pathProvisions = self.GetReproWindow(res)
        if len(pathProvisions) <= 0: # minTime is set to "None" if no reservations may be reprovisioned at this time
            return False

        reprovResList = self.PopProvisions(pathProvisions)

        for rpRes in reprovResList:
            tempLinks = rpRes.GetPath()
            for link in tempLinks:
                if link in relevantLinks:
                    continue
                else:
                    relevantLinks.append(link)
        for link in relevantLinks:
            tempLinkDict[link]    = [None,None]
            tempLinkDict[link] = self.linkDict[link].GetWindowCopy(minWindowBase, maxWindowBound)
        reprovResList.append(res)   # Probationally add res to list
        reprovResList.sort(key=lambda rpRes: (rpRes.start_t, rpRes.resNum))

        tempLinkDict = self.ClearProvAcrossTempLinks(pathProvisions, tempLinkDict, minWindowBase, minTime, maxWindowBound)

        allResReprov = False
        #   Use temporary window to find possible rearrangement of provisions
        for rpRes in reprovResList:
            rpListLinks = rpRes.GetPath()
            curLink     = rpListLinks[0]
            rpStartT    = rpRes.GetStartT()
            rpSize      = rpRes.num_slots
            rpDepth     = rpRes.GetHoldingT()
            rpNum       = rpRes.resNum
            startBaseTime = 0  # The starting slot of the sliding window
            if self.time > rpStartT: # If it is already past the reservations original start time, the window is smaller
                startBaseTime = self.time - rpStartT        # Base of window is first non-past time in window
                if startBaseTime >= STRT_WNDW_RANGE:   # Bound of window is startT + STRT_WNDW_RANGE
                    raise
            for windowSpace in range(startBaseTime, STRT_WNDW_RANGE):
                curLink = rpListLinks[0]
                startT  = rpStartT + windowSpace - minWindowBase
                endT    = startT + rpDepth
                spaceOptions = GetListOfOpenSpaces(tempLinkDict[curLink][startT:endT], rpSize)
                spaceFound = False
                # If the path is only one link long, spaceOptions contains all valid spaces
                if len(rpListLinks) == 1 and len(spaceOptions) > 0:
                    spaceFound = True
                    space = spaceOptions[0]
                    tempResCoords[rpNum] = [startT + minTime, space]
                # Otherwise
                else:
                    # For each space available
                    for space in spaceOptions:
                        # In each link past the first
                        for curLink in rpListLinks[1:]:
                            # Check if that area is full, if so, spacefound is false and escape the link check loop
                            if CheckAreaIsFull(tempLinkDict[curLink][startT:endT], space, rpSize):
                                spaceFound = False
                                break
                            # If not, spaceFound is true and continue through the rest of the links
                            else:
                                spaceFound = True
                        # If none of the links has that space full and exited the loop, record those coords; exit space loop
                        if spaceFound == True:
                            foundStartT = startT
                            tempResCoords[rpNum] = [startT + minTime, space]    # Un-scale startT and record new coords
                            break
                        else:
                            continue
                if spaceFound:
                    for curLink in rpListLinks:
                        for i in range(startT, endT):
                            for j in range(space, space+rpSize):
                                if tempLinkDict[curLink][i][j] == EMPTY:
                                    tempLinkDict[curLink][i][j] = PROV
                                else:
                                    for testLink in rpListLinks:
                                        print("Link", testLink)
                                        PrintGraphic(tempLinkDict[testLink], 0, endT)
                                    print(foundStartT, startT)
                                    print("initial space options", spaceOptions)
                                    print("Error at", i, j)
                                    print("For Res from", startT,"to", endT, "and", space, "to", space+rpSize)
                                    print("Link", curLink, "of", rpListLinks)
                                    print("Links in rpListLinks")
                                    print(rpListLinks)
                                    raise
                    allResReprov = True
                    break
                else:
                    allResReprov = False
            if allResReprov == False:
                break

        if allResReprov:    # If all reservations could be reprovisioned without blocking
            numChanged          = 0
            removedRes_Index    = []
            for delProv in pathProvisions:
                self.ClearProvAcrossLinks(delProv)
            for resID in tempResCoords:
                for rpRes in range(len(reprovResList)):
                    if resID == reprovResList[rpRes].GetResNum():
                        numChanged += 1
                        rpTime  = tempResCoords[resID][0]
                        rpSlot  = tempResCoords[resID][1]
                        reprovResList[rpRes].SetProvSpace(rpTime, rpSlot)
                        if reprovResList[rpRes].GetProvTime() != rpTime or reprovResList[rpRes].GetProvSlot() != rpSlot:
                            raise
                        if time == rpTime:
                            self.AllocateAcrossLinks(rpSlot, rpTime, reprovResList[rpRes], False)
                            self.completedRes += 1
                            removedRes_Index.append(rpRes)  # If res completes, record its index so not put back in self.provResList
                        else:
                            try:
                                self.ProvisionAcrossLinks(reprovResList[rpRes], rpSlot, rpTime)
                            except:
                                print("CHECK", rpTime, reprovResList[rpRes].GetStartT())
                                raise

            if numChanged != len(tempResCoords):
                print("Some unacknowledged res", len(tempResCoords), numChanged)
                raise

            removedRes_Index.sort(reverse=True)
            for index in removedRes_Index:  # Remove any immediately starting (completed) reservations
                reprovResList.pop(index)

            for prov in reprovResList:
                if prov.provTime == None or prov.provSlot == None:
                    raise
        else:               # If not all reservations could be reprovisioned without blocking
            for rpRes in range(len(reprovResList)):
                if reprovResList[rpRes].resNum == res.GetResNum():
                    reprovResList.pop(rpRes)
                    break
        self.provisionedResList += reprovResList
        self.provisionedResList.sort(key=lambda rpRes: (rpRes.start_t, rpRes.resNum))
        if allResReprov == True:
            return True
        else:
            return False

    def ProvisionAcrossLinks(self, res, startSlot, startDepth):
        self.AllocateAcrossLinks(startSlot, startDepth, res, True)

    def AllocateAcrossLinks(self, startSlot, startDepth, res, isProv):
        startT      = startDepth
        size        = res.GetNumSlots()
        holdingT    = res.GetHoldingT()
        links       = res.GetPath()
        baseStartT  = res.GetStartT()
        resNum      = res.GetResNum()
        path        = res.GetPath()

        if isProv:
            self.AddToProvList(baseStartT, startT, startSlot, size, holdingT, path, resNum)

        for link in links:
            try:
                self.linkDict[link].PlaceRes_NoCheck(startT, holdingT, startSlot, size, isProv, resNum, baseStartT=baseStartT)
            except:
                print("On link", link, "of links", links)
                print("Error at", startT, startSlot, "of size", size, holdingT)
                print("res", res.GetResNum())
                raise

    # ======================================= M a i n   F u n c t i o n ==========================================

    def DEBUG_GetNodeFrequencies(self):
        for node in self.DEBUG_SrcDstCount:
            total = 0
            for node2 in self.DEBUG_SrcDstCount[node]:
                total += self.DEBUG_SrcDstCount[node][node2]
            print("Count", node, total)

        for node in self.pathDict:
            for node2 in self.pathDict[node]:
                try:
                    print(node, node2, self.pathDict[node][node2][0], self.pathDict[node][node2][1])
                except:
                    print(node, node2)
                    raise

    def TestRes(self):
        numRes = 100000
        avgAr = 0
        avgHo = 0
        avgBk = 0
        avgSR = 0
        avgSS = 0

        preAr = 0
        self.CreateMultRes(2, numRes)
        for res in self.initialResList:
            avgAr += res.arrival_t_pre - preAr
            preAr = res.arrival_t_pre

            avgHo += res.holding_t
            avgBk += res.book_t
            avgSR += res.size_req
            avgSS += res.num_slots

        print("Avg Arrival Time", avgAr/numRes)
        print("Avg Bookahead Time", avgBk/numRes)
        print("Avg Holding Time", avgHo/numRes)
        print("Avg Size Req", avgSR/numRes)
        print("Avg Slot Size", avgSS/numRes)

    def MainFunction(self, my_lambda, numRes, seedInt, genRes = True, info = False):
        allocated_Index             = []
        arrivedOrIBlocked_Index     = []

        DEBUG_Total_Time = clock()

        if genRes:
            self.CreateMultRes(my_lambda, numRes, seedInt)
        else:
            numRes = len(self.initialResList)
        self.SortInitResByArrivalT()

        linkNames = []
        for link in self.linkDict:
            linkNames.append(link)

        maxTime = self.initialResList[-1].GetStartT() + 100 + STRT_WNDW_RANGE
        for time in range(0, maxTime):
            try:
                if (time % UpdateTimeCheck) == 0 and time != 0:
                        for link in linkNames:
                            self.linkDict[link].UpdateSize(time)
            except:
                raise
            self.time = time
            i = 0
            allocated_Index.clear()
            # ============= A L L O C A T I O N   L O O P ================
            for res in self.provisionedResList:
                provStartT  = res.GetProvTime()
                provStartS  = res.GetProvSlot()
                if provStartT == time:
                    self.ClearProvAcrossLinks(res)
                    try:
                        self.AllocateAcrossLinks(provStartS, provStartT, res, False)
                    except RuntimeError:
                        print("Error with res", res.resNum)
                        print("Res intended for ", res.GetProvSlot(), res.GetProvTime())
                        raise
                    self.completedRes += 1
                    allocated_Index.append(i)
                elif res.GetProvTime() == None or res.GetProvSlot() == None:
                    raise
                i += 1

            # Sort indexes from high to low as deleting and index reindexes earlier entries
            allocated_Index.sort(reverse=True)
            for index in allocated_Index:
                self.provisionedResList.pop(index)

            arrivedOrIBlocked_Index.clear()
            # ---------- E N D   A L L O C A T I O N   L O O P -----------
            # =============== P R O V I S I O N   L O O P ================
            wasProvisioned = False
            for i in range(len(self.initialResList)):
                res = self.initialResList[i]
                if res.arrival_t == time:
                    hasSpace, spaceSlot, spaceTime = self.FindContinuousSpace(res)
                    if hasSpace and spaceTime > time:
                        self.initialResList[i].SetProvSpace(spaceTime, spaceSlot)
                        if (res.GetProvTime() == None or res.GetProvSlot() == None):
                            print(res.GetProvTime(), res.GetProvSlot())
                            raise
                        self.ProvisionAcrossLinks(res, spaceSlot, spaceTime)
                        self.provisionedResList.append(res)
                        wasProvisioned = True
                    elif hasSpace and spaceTime == time:
                        self.AllocateAcrossLinks(spaceSlot, spaceTime, res, False)
                        self.completedRes += 1
                    elif hasSpace and spaceTime < time:
                        print("ERROR: Invalid time")
                        raise
                    else:
                        wasReprovisioned = self.CheckReprovision(res, time)
                        if wasReprovisioned == False:
                            self.immediateBlocking += 1
                            self.unsuccessfulReprov += 1
                        else:
                            self.successfulReprov += 1

                    arrivedOrIBlocked_Index.append(i)
            # Sort indexes from high to low as deleting and index reindexes earlier entries
            arrivedOrIBlocked_Index.sort(reverse=True)
            for index in arrivedOrIBlocked_Index:
                self.initialResList.pop(index)
            if wasProvisioned:
                try:
                    self.provisionedResList.sort(key=lambda res: (res.provTime, res.resNum))
                except TypeError:
                    for prov in self.provisionedResList:
                        print("Prov", prov.resNum, prov.provTime, prov.provSlot)
                        print(wasReprovisioned)
                    raise

            # ============ E N D   P R O V I S I O N   L O O P =============

        localBlocking = self.immediateBlocking  # Get number of local blocks
        linkBlocking = self.promisedBlocking
        totalBlocking = localBlocking + linkBlocking

        if info:    # If printout of results wanted immediately
            print("Of", numRes, "initial reservations")
            print("Reservations Completed", self.completedRes)
            print("Total number of blocks:", totalBlocking, "\n", localBlocking, "blocked initially and", linkBlocking, "due to conflict")
            print("Number of attempted reprovisions:", self.unsuccessfulReprov + self.successfulReprov, "Number of success:", self.successfulReprov)

        if(numRes != totalBlocking + self.completedRes):
            ReportError("MainFunction", "Not all of {0} reservations blocked: {1}, or completed: {2}".format(numRes, totalBlocking, self.completedRes))
            print(len(self.initialResList), len(self.arrivingResList))
            raise NetworkError
        DEBUG_Total_Time = clock() - DEBUG_Total_Time

        return self.completedRes, localBlocking, linkBlocking, DEBUG_Total_Time

    def PrintGraphics(self, link, end, all=False):
        print("Link:", link)
        self.linkDict[link].PrintGraphic(end)

    def ReportError(self, errorMsg):
        self.errorQueue.puts(errorMsg)


class NetworkError(Exception):
    pass

def ReportError(funct, msg, info = None):
    print("========== ERROR:", funct, "->", msg)
    if info != None:
        for line in info:
            print("=====", line)

def DEBUG_print(msg):
    print(msg)

def DetermineSeed(mySeed):
    random.seed(a=mySeed)

def ReportResults(indexLambda, avgComp, avgImme, avgProm):
    report = open("Test"+ str(indexLambda) +".txt", 'w')
    report.write("Test for Lambda " + str(LambdaList[indexLambda]))
    if avgImme + avgProm == 0:
        avgImme = 1
    report.write("\nBlocked Vs Total Ratio " + str((avgImme + avgProm)/NumRes) +'\n\n')
#    report.write(str(LambdaList[indexLambda]) + ' ' + str(avgComp) + ' ' + str(avgImme) + ' ' + str(avgProm))
    report.close()

def RunTrial(args, detailed=False, debugGraphic = False):
    indexLambda = args[0]
    resultsQueue = args[1]

    avgTime = 0
    avgComp = 0
    avgImme = 0
    avgProm = 0
    myLambda = LambdaList[indexLambda]

    try:
        for x in range(NumTrials):
            seedInt = indexLambda * x ^x
            test = Network(NumNodes, LinkList)
            complete, immediate, promised, time = test.MainFunction(myLambda, NumRes, seedInt, info=True)
            avgTime += time
            avgComp += complete
            avgImme += immediate
            avgProm += promised
        avgTime = avgTime / NumTrials
        avgComp = avgComp / NumTrials
        avgImme = avgImme / NumTrials
        avgProm = avgProm / NumTrials

        if detailed:
            print("total time for lambda", myLambda, "was", avgTime * NumTrials, "with an average of", avgTime, "seconds")
        if debugGraphic:
            test.PrintGraphics()
        ReportResults(indexLambda, avgComp, avgImme, avgProm)
        if resultsQueue != None:
            resultsQueue.put([myLambda, (avgImme + avgProm)/NumRes, avgTime])
    except BaseException as errorMsg:
        if resultsQueue != None:
            resultsQueue.put([myLambda, "Failed on lambda {0}\n".format(myLambda) + str(errorMsg)])
        raise

def TestingRun( ResList):
    listOfInvolvedLinks = []
    test = Network(NumNodes, LinkList)
    i = 0
    for resVars in ResList:
        path = test.LoadRes(resVars, i)
        for link in path:
            if link in listOfInvolvedLinks:
                continue
            else:
                listOfInvolvedLinks.append(link)
        i += 1
    #test.PrintInitialResList()
    test.MainFunction(None, None, genRes=False)

    for link in listOfInvolvedLinks:
        print(link)
        test.PrintGraphics(link, 10)


if __name__ == '__main__':
    RunTrial([16, None], detailed=True, debugGraphic=False)
    #TestingRun(TestResList)
#    test = Network(NumNodes, LinkList)
#    test.TestRes()
#    test2 = Network(NumNodes, LinkList)
#    test2.TestRes()