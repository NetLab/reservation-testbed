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

        self.initialResList     = []
        self.arrivingResList    = []
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

    # ------------------------ G e t / S e t ----------------------
    def GetNodes(self):
        nodes = []
        for node in self.nodeDict:
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
            self.SetNodePairLink(linkNodes, linkLength)             # Update node objects to know their links

    # def InitRandLinks(self):  # Initiate a list of links between nodes on the network from a list of tuples
    #     self.linkDict.clear()   # Clear any previously existing links
    #
    #     for node in self.nodeList:
    #         i = 0
    #         numLinks = randint(1,4) # Create between 1 and 3 links for each
    #
    #         while(i < numLinks):
    #             otherNode = self.nodeList[randint(0,NumNodes)]          # Get a random node from the list
    #             linkNodes = FormatLinkName_List(node + otherNode)  # Get the formatted (ex: AB, not BA) link name
    #
    #             if(otherNode == node):  # If both nodes the same
    #                 pass
    #             elif(self.linkDict[linkNodes] != None):  # If the link already exists
    #                 pass
    #             else:                                                   # Otherwise
    #                 linkLength = randint(LINK_RAND_MIN, LINK_RAND_MAX)
    #                 self.linkDict[linkNodes] = Link(linkNodes, linkLength) # Append the link to the list

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
                if debugInfo:
                    print("     node:", node)
                    print("     costDict:", costDict)
                    print("     costDict[node]:", costDict[node])
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
#        self.nodeDict[src].SetPath(dst, costDict[dst][P_PathIndex], costDict[dst][P_CostIndex]) # Record the path to save time in future lookups
        if debugInfo:
            print("Path", costDict[dst][P_PathIndex], "of cost", costDict[dst][P_CostIndex], "from", src, "to", dst)
        returnPath = costDict[dst][P_PathIndex]
        returnCost = costDict[dst][P_CostIndex]
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
        res.SetPath(path)  # Set the shortest path for that reservation
        blocked = res.SetNumSlots(cost)   # Set the number of slots the reservation will take
        if res.num_slots == None:
            raise
        if blocked:
            self.immediateBlocking += 1
            print("M = 0?")
        else:
            self.initialResList.append(res)
        return res.arrival_t_pre    # Return arrival time generated for this reservation

    # Generate several reservations with random values
    def CreateMultRes(self, my_lambda, numRes):
        i = 0
        prevArrivalT = 0
        nodes = self.GetNodes()
        while i < numRes:
            prevArrivalT = self.CreateRes(my_lambda, nodes, i, prevArrivalT)
            i += 1
        self.SortInitResByArrivalT()


    # Sort res in arrivingResList by their start time
    def SortInitResByArrivalT(self):
        self.initialResList.sort(key=lambda res: (res.arrival_t, res.resNum))

    # Sort res in arrivingResList by their start time
    def SortArrivingResByStartT(self):
        self.arrivingResList.sort(key=lambda res: (res.start_t, res.arrival_t, res.resNum))

    # Print out arrivingResList
    def PrintArrivingResList(self):
        for res in self.arrivingResList:
            print(
                "Reservation arriving at {0:1d}, Bookahead for {1:3d}; Start time at {2:2d} and size of {3:2d}".format(
                    res.arrival_t, res.book_t, res.start_t, res.num_slots))

    # ------------------ H a n d l e   R e s e r v a t i o n s ---------------------
    # For use upon reservations initial arrival at first node. Checks if a continuous space is open on its path right now.
    #   Returns the first index found. Blocks if none.
    def CheckInitialPathOpen(self, res, arrivalcheck):
        listLinks       = []  # List of links in path to check
        spaceOptions    = []  # Options for continuous blocks of space to check in path
        pathSpace       = None # The final decided continuous (persistent) start location for the reservation
        hasPath         = False

        size            = res.GetNumSlots() # get the size in slots of the request
        listLinks       = res.GetPath()
        if arrivalcheck:
            checkTime   = res.arrival_t
        else:
            checkTime   = res.GetStartT()
        holdT           = res.GetHoldingTime()

        self.D_Num_2 += 1
        D_Time_2 = clock()
        spaceOptions    = self.linkDict[listLinks[0]].GetListOfOpenSpaces(size, checkTime, holdT) # Possible cont. spaces in init. link
        if len(spaceOptions) > 0:
            spacesFound = True
        else:
            spacesFound = False
        D_Time_2 = clock() - D_Time_2
        self.D_Avg_2 += D_Time_2

        if spacesFound == False:    # If no spaces are found
            return False, pathSpace
        elif len(listLinks) == 1:  # If only one link in path
            return True, spaceOptions[0]    # Return that a path was found, and the first spot found
        for space in spaceOptions:  # For each possible space
            pathSpace = space
            for link in listLinks[1:]:  # For each link beyond the first in the path
                self.D_Num_1 += 1
                D_Time_1 = clock()
                isFull = self.linkDict[link].CheckContinuousSpace(space, size, checkTime)  # Check each possible space
                D_Time_1 = clock() - D_Time_1
                self.D_Avg_1 += D_Time_1
                if isFull == FULL:
                    hasPath = False
                    break                   # If the space is full in any link, move on to the next possible space
                else:
                    hasPath = True

            if hasPath == True:         # If any possible space is empty on every link
                return hasPath, pathSpace   # return True and the index of the space

        pathSpace = None    # set pathSapce as None
        if hasPath: # If hasPath is somehow True at this point, raise an error
            print("Oops, I did something wrong")
            raise

        return hasPath, pathSpace

    def AllocateAcrossLinks(self, startIndex, res):
        startT      = res.GetStartT()
        size        = res.GetNumSlots()
        holdingT    = res.GetHoldingTime()
        links       = res.GetPath()

        self.DEBUG_ResNum.append(res.resNum)

        for link in links:
            self.linkDict[link].PlaceRes(startIndex, size, holdingT, startT)

    # ======================================= M a i n   F u n c t i o n ==========================================

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

    def MainFunction(self, my_lambda, numRes, info = False):
        # Reservations cannot be deleted in the middle of a list search, so their indexes are saved to be deleted after
        arrivedOrIBlocked_Index     = []
        completeOrPBlocked_Index    = []
        DEBUG_CIPO1_Avg     = 0
        DEBUG_CIPO1_Num     = 0
        DEBUG_Init_Avg      = 0
        DEBUG_Init_Num      = 0
        DEBUG_Arri_Avg      = 0
        DEBUG_Arri_Num      = 0
        DEBUG_Check_Avg     = 0
        DEBUG_Check_Num     = 0
        DEBUG_HasP_Avg      = 0
        DEBUG_HasP_Num      = 0
        DEBUG_NoP_Avg       = 0
        DEBUG_NoP_Num       = 0

        DEBUG_Total_Time    = clock()

        self.CreateMultRes(my_lambda, numRes)
        self.SortInitResByArrivalT()

        for time in range(0, TIME_WNDW_SIZE):

            newResArrived   =   False   # Each time, t, set newResArrived to false; check if need to re-sort arrivedResList
            arrivedOrIBlocked_Index.clear()


            DEBUG_Init_Num += 1
            DEBUG_Init_Time = clock()
            for res in self.initialResList:
                i = 0
                if res.arrival_t == time:   # If the Res arrives at this time
                    DEBUG_CIPO1_Num     += 1
                    DEBUG_CIPO1_Time    = clock()
                    hasPath, pathSpace = self.CheckInitialPathOpen(res, True) # Check to see if there is an opening
                    DEBUG_CIPO1_Time    = clock() - DEBUG_CIPO1_Time
                    DEBUG_CIPO1_Avg     += DEBUG_CIPO1_Time

                    DEBUG_Check_Num     += 1
                    DEBUG_Check_Time    = clock()
                    if hasPath:
                        DEBUG_HasP_Num += 1
                        DEBUG_HasP_Time = clock()
                        self.arrivingResList.append(res)
                        arrivedOrIBlocked_Index.append(i) # Queue the res for deletion
                        newResArrived = True    # Set to true if any new res arrive
                        DEBUG_HasP_Time = clock() - DEBUG_HasP_Time
                        DEBUG_HasP_Avg += DEBUG_HasP_Time
                    else:
                        DEBUG_NoP_Num += 1
                        DEBUG_NoP_Time = clock()
                        self.immediateBlocking += 1
                        arrivedOrIBlocked_Index.append(i) # Queue the res for deletion
                        DEBUG_NoP_Time = clock() - DEBUG_NoP_Time
                        DEBUG_NoP_Avg += DEBUG_NoP_Time

                    DEBUG_Check_Time    = clock() - DEBUG_Check_Time
                    DEBUG_Check_Avg     += DEBUG_Check_Time
                else:
                    break   # As the lsit is ordered by time: if any do not match, move on to the next step; Checking arrived res
                i += 1


            DEBUG_Init_Time = clock() - DEBUG_Init_Time
            DEBUG_Init_Avg += DEBUG_Init_Time
            # Clear out res that arrive or immediately block
            arrivedOrIBlocked_Index.sort(reverse=True) # Sort indexes from low to high as deleting reindexes later entries
            for index in arrivedOrIBlocked_Index:
                self.initialResList.pop(index)

            completeOrPBlocked_Index.clear()
            if newResArrived:   # If any new reservations have arrived
                self.SortArrivingResByStartT()  # Sort arriving res list if new res have arrived

            DEBUG_Arri_Num += 1
            DEBUG_Arri_Time = clock()
            for res in self.arrivingResList:
                i = 0
                if res.GetStartT() == time:
                    hasPath, pathSpace = self.CheckInitialPathOpen(res, False)  # Check to see if there is an opening
                    if hasPath:
                        self.AllocateAcrossLinks(pathSpace, res)
                        completeOrPBlocked_Index.append(i)
                        self.completedRes += 1
                    else:
                        self.promisedBlocking += 1
                        completeOrPBlocked_Index.append(i)
                else:
                    break   # As the lsit is ordered by time: if any do not match, move on to the next step
                i += 1

            # Clear out res that complete or promise block
            completeOrPBlocked_Index.sort(reverse=True)  # Sort indexes from low to high as deleting reindexes later entries
            for index in completeOrPBlocked_Index:
                self.arrivingResList.pop(index)

            DEBUG_Arri_Time = clock() - DEBUG_Arri_Time
            DEBUG_Arri_Avg += DEBUG_Arri_Time


        localBlocking = self.immediateBlocking  # Get number of local blocks
        linkBlocking = self.promisedBlocking
        totalBlocking = localBlocking + linkBlocking

        if info:    # If printout of results wanted immediately
            print("Of", numRes, "initial reservations")
            print("Reservations Completed", self.completedRes)
            print("Total number of blocks:", totalBlocking, "\n", localBlocking, "blocked initially and", linkBlocking, "due to conflict")

        if(numRes != totalBlocking + self.completedRes):
            ReportError("MainFunction", "Not all of {0} reservations blocked: {1}, or completed: {2}".format(numRes, totalBlocking, self.completedRes))
            raise NetworkError
        DEBUG_Total_Time = clock() - DEBUG_Total_Time

        if(False):
            print("DEBUG_CIPO1 Average", DEBUG_CIPO1_Avg/DEBUG_CIPO1_Num, "Total", DEBUG_CIPO1_Avg)
            print("DEBUG_Check Average", DEBUG_Check_Avg/DEBUG_Check_Num, "Total", DEBUG_Check_Avg)
            print("DEBUG_Init Average", DEBUG_Init_Avg / DEBUG_Init_Num, "Total", DEBUG_Init_Avg)
            print("DEBUG_Arri Average", DEBUG_Arri_Avg / DEBUG_Arri_Num, "Total", DEBUG_Arri_Avg)
            print("DEBUG_HasPath Average", DEBUG_HasP_Avg / DEBUG_HasP_Num, "Total", DEBUG_HasP_Avg)
            print("DEBUG_HasNoPath Average", DEBUG_NoP_Avg / DEBUG_NoP_Num, "Total", DEBUG_NoP_Avg)
            print("DEBUG Continuous Open", self.D_Avg_1/ self.D_Num_1, "Total", self.D_Avg_1)
            print("DEBUG Get List of Open", self.D_Avg_2/ self.D_Num_2, "Total", self.D_Avg_2)
            print("Total Time", DEBUG_Total_Time)
#        return(self.completedRes, localBlocking, linkBlocking, totalBlocking)

        return self.completedRes, localBlocking, linkBlocking, DEBUG_Total_Time

    def PrintGraphics(self, all=False):
        self.linkDict["AB"].PrintGraphic()


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

def RunTrial(indexLambda, detailed=True, debugGraphic = False):
    avgTime = 0
    avgComp = 0
    avgImme = 0
    avgProm = 0
    myLambda = LambdaList[indexLambda]
    for x in range(NumTrials):
        DetermineSeed(indexLambda * x)
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

if __name__ == '__main__':
    RunTrial(0, detailed=True, debugGraphic=False)
#    test = Network(NumNodes, LinkList)
#    test.TestRes()
#    test2 = Network(NumNodes, LinkList)
#    test2.TestRes()