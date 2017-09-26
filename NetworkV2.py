from LinkV2 import *
from copy import deepcopy
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
        self.resToBeSlotted     = []
        self.completedResList   = []

        self.arrivingResList    = []  # Dictionary reservations that will arrive in the next time unit

        self.time               = 0
        self.completedRes       = 0
        self.immediateBlocking  = 0
        self.promisedBlocking   = 0

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
    def CreateMultRes(self, my_lambda, numRes):
        i = 0
        prevArrivalT = 0
        nodes = self.GetNodes()
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

        holdT           = res.GetHoldingTime()

        for offset in range(0, STRT_WNDW_RANGE):
            checkTime = baseStartT + offset
            leastAvail = 128
            linkToCheck = 0
            i = 0

            for link in listLinks:
                linkAvail = self.linkDict[link].GetTimeAvailSlots(checkTime, holdT)
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

    def GetReproWindow(self, res):
        pathProvisions = []
        provNotConsidered_Index = []
        linkList = res.GetPath()

        for link in linkList:
            pathProvisions += self.linkDict[link].GetProvisionList()
        pathProvisions.sort(key=lambda prov: (prov.bStartT, prov.resNum))

        minTime         = pathProvisions[0].bStartT
        # Default maxTime is the max time the res can go to
        maxTime         = res.GetStartT() + res.GetHoldingT() # Time after which reservations may not be considered.
        maxWindowSize   = maxTime + STRT_WNDW_RANGE # Maximum depth of time window needed to reprovision
        i = 0
        for prov in pathProvisions:
            if prov.rStartT > maxTime:
                provNotConsidered_Index.append(i)
            elif prov.bStartT + prov.holdingT + STRT_WNDW_RANGE > maxWindowSize:  # If larger time window needed
                maxWindowSize = prov.bStartT + prov.holdingT + STRT_WNDW_RANGE  # Set new time window size
            i += 1
        provNotConsidered_Index.sort(reverse=True)  # Sort indexes to be removed in high->low as to not reindex
        for prov_Index in provNotConsidered_Index:
            pathProvisions.pop(prov_Index)  # Remove each index

        return minTime, maxTime, maxWindowSize, pathProvisions

    def PopProvisions(self, pathProvisions, time):
        reprovisionedResNum = []
        tempProvResList     = []
        provRes_Index       = []


        for resData in pathProvisions:  # Get a list of all unique resNum involved in this reprovisioning
            if resData.resNum in reprovisionedResNum:   # If it exists in the list already, pass
                continue
            else:
                reprovisionedResNum.append(resData.resNum)  # Else add it to the list

        for resNum in reprovisionedResNum:
            i = 0
            for res in self.provisionedResList:
                if res.resNum == resNum:
                    provRes_Index.append(i)
                    break
                i += 1
        if len(resprovisionedResNum) != len(provRes_Index):
            print("Mismatched List Length")
            raise

        for index in provRes_Index:
            tempProvResList.append(self.provisionedResList.pop(index))

        return tempProvResList

    def ClearProvAcrossLinks(self, res):
        linkList = res.GetPath()
        resID = res.resNum
        for link in linkList:
            self.linkDict[link].ClearProv(resID)

    def CheckReprovision(self, res):
        tempLinkDict    = {}
        listLinks       = res.GetPath()
        tempResCoords   = {}

        minTime, maxTime, maxWindowSize, pathProvisions = self.GetReproWindow(res)
        reprovResList = self.PopProvisions(pathProvisions)

        for rpRes in reprovResList:
            relevantLinks = rpRes.GetPath()
            for link in relevantLinks:
                if link in listLinks:
                    continue
                else:
                    listLinks.append(link)
        for link in listLinks:
            tempLinkDict[link][0] = self.linkDict[link].GetWindowCopy(minTime, maxWindowSize)
            tempLinkDict[link][1] = self.linkDict[link].GetProvisionList()

        reprovResList.append(res)   # Probationally add res to list
        reprovResList.sort(key=lambda rpRes: (rpRes.StartT, rpRes.resNum))

        # Clear out all reservation spots in the tempWindows
        for link in tempLinkDict:
            for prov in tempLinkDict[link][1]:
                provStartT  = prov.bStartT - minTime # Get base startT relative to earliest startT
                provStartD  = prov.sSlot
                provSize    = prov.nSlots
                provDepth   = prov.holdingT
                for i in range(provStartD, provDepth):
                    for j in range(provStartT, provSize):
                        if tempLinkDict[link][0][i][j] == PROV:
                            tempLinkDict[link][0][i][j] = EMPTY
                        else:
                            raise
        allResReprov = False
        for rpRes in reprovResList:
            listLinks   = rpRes.GetPath()
            rpStartT    = rpRes.GetStartT()
            rpSize      = rpRes.num_slots
            rpDepth     = rpRes.holdingT
            rpNum       = rpRes.resNum

            windowBaseTime = 0  # The starting slot of the sliding window
            if time > rpStartT: # If it is already past the reservations original start time, the window is smaller
                windowBaseTime = time - rpStartT    # Base of window is first non-past time in window
                                                    # Bound of window is startT + STRT_WNDW_RANGE
            for windowSpace in range(windowBaseTime,STRT_WNDW_RANGE):
                startT  = rpStartT + windowSpace - minTime
                endT    = startT + rpDepth
                spaceOptions = GetListOfOpenSpaces(tempLinkDict[link][0][startT:endT], rpSize)
                spaceFound = False
                for space in spaceOptions:
                    for link in listLinks[1:]:
                        if CheckAreaIsFull(tempLinkDict[link][0][startT:endT], space, rpSize):
                            spaceFound = False
                            break
                        else:
                            spaceFound = True
                    if spaceFound == True:
                        tempResCoords[rpNum] = [startT + minTime, space]    # Un-scale startT and record new coords
                        break
                    else:
                        continue
                if spaceFound:
                    for link in listLinks:
                        for i in range(startT, endT):
                            for j in range(space, space+rpSize):
                                if tempLinkDict[link][0][i][j] == EMPTY:
                                    tempLinkDict[link][0][i][j] = PROV
                                else:
                                    raise
                    break
                else:
                    continue
            if spaceFound == True:
                allResReprov = True
            else:
                allResReprov = False
                break

        if allResReprov:    # If all reservations could be reprovisioned without blocking
            i                   = 0
            numChanged          = 0
            removedRes_Index    = []
            for resID in tempResCoords:
                for rpRes in reprovResList:
                    if resID == rpRes.numRes:
                        self.ClearProvAcrossLinks(rpRes)
                        numChanged += 1
                        rpTime  = tempResCoords[resID][0]
                        rpSlot  = tempResCoords[resID][1]
                        reprovResList[i].SetProvSpace(rpTime, rpSlot)
                        if time == rpTime:
                            self.AllocateAcrossLinks(rpSlot, rpTime, rpRes, False)
                            self.completedRes += 1
                            removedRes_Index.append(i)  # If res completes, record its index so not put back in self.provResList
                        else:
                            self.ProvisionAcrossLinks(rpRes, rpSlot, rpTime)
                i += 1

            if numChanged != len(tempResCoords):
                print("Some unacknowledged res", len(tempResCoords), numChanged)
                raise

            removedRes_Index.sort(reverse=True)
            for index in removedRes_Index:  # Remove any immediately starting (completed) reservations
                reprovResList.pop(index)

        else:               # If not all reservations could be reprovisioned without blocking
            i = 0
            for rpRes in reprovResList:
                if rpRes.resNum == res.GetResNum():
                    reprovResList.pop(i)
                    break
                i += 1
        self.provisionedResList += reprovResList
        self.provisionedResList.sort(key=lambda rpRes: (rpRes.start_t, rpRes.resNum))

        #CHECK 1. Add res to reprov Res List
        #2. Run simulation of possible reres
        #3. If fail, block and remove res from rRL. If success, rewrite the startSlot and startTime of each res in rRL to its new space
        #4. If success, clear and reprovision all res in rRL in all links (dont forget to edit link provision lists).
        #5. Reappend reprovResList to self.provisionedResList.

    def ProvisionAcrossLinks(self, res, startSlot, startDepth):
        self.AllocateAcrossLinks(startSlot, startDepth, res, True)

    def AllocProvAcrossLinks(self, res):
        startSlot = res

    def AllocateAcrossLinks(self, startSlot, startDepth, res, isProv):
        startT      = startDepth
        size        = res.GetNumSlots()
        holdingT    = res.GetHoldingTime()
        links       = res.GetPath()
        baseStartT  = res.GetStartT()
        resNum      = res.GetResNum()

        for link in links:
            try:
                self.linkDict[link].PlaceRes(startSlot, size, holdingT, startT, isProv, resNum, baseStartT=baseStartT)
            except:
                print("On link", link, "of links", links)
                print("Error at", startT, startSlot, "of size", size, holdingT, "offset")
                print(isProv)
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

    def MainFunction(self, my_lambda, numRes, genRes = True, info = False):
        allocated_Index             = []
        arrivedOrIBlocked_Index     = []

        DEBUG_Total_Time = clock()

        if genRes:
            self.CreateMultRes(my_lambda, numRes)
        else:
            numRes = len(self.initialResList)
        self.SortInitResByArrivalT()

        maxTime = self.initialResList[-1].GetStartT() + 100 + STRT_WNDW_RANGE
        for time in range(0, maxTime):
            print("Time", time)
            i = 0
            allocated_Index.clear()
            # ============= A L L O C A T I O N   L O O P ================
            for res in self.provisionedResList:
                provStartT  = res.GetProvTime()
                provStartS  = res.GetProvSlot()
                if provStartT == time:
                    print("Allocating res", res.GetResNum())
                    self.ClearProvAcrossLinks(res)
                    self.AllocateAcrossLinks(provStartS, provStartT, res, False)
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
            i = 0
            wasProvisioned = False
            for res in self.initialResList:
                if res.arrival_t == time:
                    print("Provisioning res", res.GetResNum())
                    hasSpace, spaceSlot, spaceTime = self.FindContinuousSpace(res)
                    if hasSpace and spaceTime > time:
                        res.SetProvSpace(spaceTime, spaceSlot)
                        self.ProvisionAcrossLinks(res, spaceSlot, spaceTime)
                        self.provisionedResList.append(res)
                        wasProvisioned = True
                        arrivedOrIBlocked_Index.append(i)
                    elif hasSpace and spaceTime == time:
                        self.AllocateAcrossLinks(spaceSlot, spaceTime, res, False)
                        self.completedRes += 1
                        arrivedOrIBlocked_Index.append(i)
                    elif hasSpace and spaceTime < time:
                        print("ERROR: Invalid time")
                    else:
                        wasReprovisioned = self.CheckReprovision(res)
                        if wasReprovisioned == False:
                            self.immediateBlocking += 1
                            arrivedOrIBlocked_Index.append(i)
                        else:
                            print("Reprovisioning for res", res.GetResNum())
                            wasProvisioned = True
                            self.provisionedResList.append(res)
                i += 1
            # Sort indexes from high to low as deleting and index reindexes earlier entries
            arrivedOrIBlocked_Index.sort(reverse=True)
            for index in arrivedOrIBlocked_Index:
                self.initialResList.pop(index)
            if wasProvisioned:
                self.provisionedResList.sort(key=lambda res: (res.provTime, res.resNum))

            print("A-Res-List:")
            for res in self.provisionedResList:
                print(res.GetResNum())
            print("P-Res-List:")
            for res in self.initialResList:
                print(res.GetResNum())


        localBlocking = self.immediateBlocking  # Get number of local blocks
        linkBlocking = self.promisedBlocking
        totalBlocking = localBlocking + linkBlocking

        if info:    # If printout of results wanted immediately
            print("Of", numRes, "initial reservations")
            print("Reservations Completed", self.completedRes)
            print("Total number of blocks:", totalBlocking, "\n", localBlocking, "blocked initially and", linkBlocking, "due to conflict")

        if(numRes != totalBlocking + self.completedRes):
            ReportError("MainFunction", "Not all of {0} reservations blocked: {1}, or completed: {2}".format(numRes, totalBlocking, self.completedRes))
            print(len(self.initialResList), len(self.arrivingResList))
            raise NetworkError
        DEBUG_Total_Time = clock() - DEBUG_Total_Time

        return self.completedRes, localBlocking, linkBlocking, DEBUG_Total_Time

    def PrintGraphics(self, link, end, all=False):
        self.linkDict[link].PrintGraphic(end)


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

def RunTrial(indexLambda, detailed=False, debugGraphic = False):
    avgTime = 0
    avgComp = 0
    avgImme = 0
    avgProm = 0
    myLambda = LambdaList[indexLambda]
    for x in range(NumTrials):
        DetermineSeed(indexLambda * x ^ x)
        test = Network(NumNodes, LinkList)
        complete, immediate, promised, time = test.MainFunction(myLambda, NumRes, info=True)
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
    test.PrintInitialResList()
    test.MainFunction(None, None, genRes=False)

    for link in listOfInvolvedLinks:
        print(link)
        test.PrintGraphics(link, 10)


if __name__ == '__main__':
    #RunTrial(0, detailed=True, debugGraphic=False)
    TestingRun(TestResList)
#    test = Network(NumNodes, LinkList)
#    test.TestRes()
#    test2 = Network(NumNodes, LinkList)
#    test2.TestRes()