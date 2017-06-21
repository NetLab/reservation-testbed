from Link import *
from Node import *
from copy import deepcopy

# Routing and Network Assignment

class Network:
    def __init__(self, numNodes, linkVals):
        self.nodeDict           = {}
        self.linkDict           = {}

        self.initialResList     = []
        self.completedResList   = []

        self.arrivingResList    = []  # Dictionary reservations that will arrive in the next time unit

        self.time               = 0
        self.completedRes       = 0

        self.InitNodes(numNodes)
        self.InitLinkList(linkVals)

    # ========================================= N o d e   F u n c t i o n s =======================================
    # --------------------------- I n i t -------------------------
    def InitNodes(self, numNodes):      # Initiate a list of nodes on the network from a list of tuples
        self.nodeDict.clear()
        if numNodes > 26:
            print("ERROR: InitNodes -> Number of Nodes must be less than 26; Number given:", numNodes)
        tempList = NodeList[0:numNodes]
        for node in tempList:
            self.nodeDict[node] = Node(node)

    # ------------------------ G e t / S e t ----------------------
    def GetNodes(self):
        nodes = []
        for node in self.nodeDict:
            nodes.append(node)
        return ''.join(nodes)

    def SetNodeLink(self, nodeSrc, nodeDst, cost):  # Tell the node it has a link to another node
        self.nodeDict[nodeSrc].SetLink(nodeDst, cost)

    def SetNodePairLink(self, linkNodes, cost):     # Tell a pair of nodes they link with one another
        self.SetNodeLink(linkNodes[0], linkNodes[1], cost)
        self.SetNodeLink(linkNodes[1], linkNodes[0], cost)

    def GetNodeLinks(self, node):
        links = self.nodeDict[node].GetLinks()
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
        path = self.PathDefinedTo(src, dst) # Check if a path has been found before
        if path != None:    # If a path already exists to this node
            return path     # Return it, otherwise find one here

        debugInfo = False
        costDict = {}
        solvedDict = {}
        curNode = src
        curPath = src
        curCost = 0
        pathFound = False
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
        self.nodeDict[src].SetPath(dst, costDict[dst][P_PathIndex]) # Record the path to save time in future lookups
        if debugInfo:
            print("Path", costDict[dst][P_PathIndex], "of cost", costDict[dst][P_CostIndex], "from", src, "to", dst)
        return costDict[dst][P_PathIndex]

    def PathDefinedTo(self, src, dst):
        return self.nodeDict[src].CheckPaths(dst)

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
    def LoadRes(self, info):
        res = Reservation(1, self.GetNodes())
        res.Load(info[R_NodesIndex], info[R_ArrivIndex], info[R_StartIndex], info[R_HoldiIndex], info[R_NumSlIndex])
        src, dst = res.GetSrcDst()
        res.SetPath(self.FindShortestPath(src, dst))
        self.arrivingResList.append(res)

    def LoadMultRes(self, infoList):
        for i in range(0, len(infoList)):
            self.LoadRes(infoList[i])
        self.SortResByArrival()

    def CreateRes(self, my_lambda, nodes):
        res = Reservation(my_lambda, nodes)
        src, dst = res.GetSrcDst()  # Get the source and destination nodes for the reservation
        res.SetPath(self.FindShortestPath(src, dst))  # Find and set the shortest path it can take
        self.arrivingResList.append(res)

    def CreateMultRes(self, my_lambda):
        i = 0
        nodes = self.GetNodes()
        while i < NumRes:
            self.CreateRes(my_lambda, nodes)
            i += 1
        self.SortResByArrival()

    def SortResByArrival(self):  # Sorts initial list based on arrival time, then bookahead time
        #self.arrivingResList.sort(key=attrgetter('arrival_t', 'sourceNode', 'destNode'))
        try:
            self.arrivingResList.sort(key=lambda res: (res.arrival_t, res.sourceNode, res.destNode))
        except:
            self.DEBUG_PrintTypesInList(self.arrivingResList)
            raise

    def SortResByStartT(self):
        #self.arrivingResList.sort(key=attrgetter('start_t', 'arrival_t', 'book_t'))
        self.arrivingResList.sort(key=lambda res: (res.start_t, res.sourceNode, res.destNode))

    def PrintArrivingResList(self):
        for res in self.arrivingResList:
            print(
                "Reservation arriving at {0:1d}, Bookahead for {1:3d}; Start time at {2:2d} and size of {3:2d}".format(
                    res.arrival_t, res.book_t, res.start_t, res.num_slots))

    # ------------------ H a n d l e   R e s e r v a t i o n s ---------------------
    #def FwdResToLink(self, res, link):
    def DEBUG_PrintTypesInList(self, list):
        for obj in list:
            print("Object type", type(obj))

    def DEBUG_PrintListOfRes(self, resList):
        for res in resList:
            print("Reservation from", res.GetSrcDst(), "with next path", res.GetNextPathLink(), "Arriving at", res.GetNextTime(), "for", res.GetHoldingTime(), "of width", res.GetNumBlocks())

    def DEBUG_ERROR_CheckValidRes(self, resList): # ensure all objects in list are of type reservation
        for res in resList:
            if type(res) != Reservation:
                return False
        return True

    def AllocateArrivingRes(self):
        self.SortResByArrival()
        arrivingRes         = []
        arrivingResIndexes  = []
        for res in self.arrivingResList:
            if res.arrival_t == self.time:
                arrivingResIndexes.append(self.arrivingResList.index(res))
            elif res.arrival_t < self.time:
                print (self.time, res.arrival_t, res.start_t, res.sourceNode, res.destNode)
                raise
        arrivingResIndexes = sorted(arrivingResIndexes, reverse=True)
        for index in arrivingResIndexes:
            arrivingRes.append(self.arrivingResList.pop(index))

        return arrivingRes

    def UpdateLinkRes(self):
        arrivingRes         = self.AllocateArrivingRes()

        for link in self.linkDict:
            linkRes = []  # List of reservations for this link in this step
            for res in arrivingRes:
                isDone, nodes = res.IsResDone()
                if isDone:                 # If the reservation has reached its final node
                    arrivingRes.pop(arrivingRes.index(res)) # Delete it
                    if nodes is not None:
                        self.completedResList.append(nodes)
                    else:
                        print("ERROR: UpdateLinkRes -> invalid completed node pair")
                        raise
                    self.completedRes += 1                  # Record that the reservation has reached end of path
                elif FormatLinkName_String(res.GetNextPathLink()) == link: # If not completed, check if res belongs to current link
                    linkRes.append(
                        arrivingRes.pop(arrivingRes.index(res)) # Move res from arriving res list
                    )                                           ## to reservations for current link
            self.linkDict[link].LoadArrivingRes(linkRes)  # Load reservations into current links waiting list

        if len(arrivingRes) > 0:
                print("Arriving Res at", self.time)
                self.DEBUG_PrintListOfRes(arrivingRes)
                for link in self.linkDict:
                    print(link)
                for res in arrivingRes:
                    print("FM", FormatLinkName_String(res.GetNextPathLink()))
                raise

        if len(arrivingRes) != 0:
            print("ERROR: UpdateLinkRes -> Some Reservations Not Allocated:")
            print(self.DEBUG_PrintListOfRes(arrivingRes))
            raise

    def RunCurrentTimeStep(self):
        for link in self.linkDict:
            fwdedResList = self.linkDict[link].RunTimeStep()
#            if len(fwdedResList) > 0:
#                print("Forwarded Res at", self.time)
#                self.DEBUG_PrintListOfRes(fwdedResList)
            #self.DEBUG_ERROR_CheckValidRes(self.arrivingResList)
            self.arrivingResList += fwdedResList

    # ======================================= M a i n   F u n c t i o n ==========================================

    def MainFunction(self, my_lambda):
        self.CreateMultRes(my_lambda)
        self.initialResList = deepcopy(self.arrivingResList)

        for time in range(0,1000):
            self.UpdateLinkRes()
            self.RunCurrentTimeStep()
            self.time += 1
#            if(len(self.arrivingResList) > 0):
#                print("Res List at", self.time)
#                self.DEBUG_PrintListOfRes(self.arrivingResList)

        for link in self.linkDict:
            unforwardedResList = self.linkDict[link].GetFwdResList()
            if len(unforwardedResList) > 0:
                errMsg = "Reservations not Forwarded in link {0}:".format(link)
                errInfo = []
                for res in unforwardedResList:
                    errInfo.append("Reservation {0} with next link {1} arriving at {2}".format(res.GetSrcDst(), res.GetNextPathLink(), res.GetNextTime()))

                ReportError("MainFunction", errMsg, info=errInfo)
                #raise NetworkError

        if len(self.arrivingResList) > 0:
            errMsg = "Reservations never addressed:"
            errInfo = []
            for res in self.arrivingResList:
                errInfo.append(
                    "Reservation {0} with next link {1} arriving at {2}".format(res.GetSrcDst(), res.GetNextPathLink(), res.GetNextTime()))
            ReportError("MainFuction", errMsg, info = errInfo)
            #raise NetworkError

        print("Initial Reservations")
        self.DEBUG_PrintListOfRes(self.initialResList)

        print("Reservations Completed", self.completedRes)
        blocking = 0
        for link in self.linkDict:
            blocking += self.linkDict[link].GetNumBlocks()
        for res in self.completedResList:
            print(res)
        print("Total number of blocks:", blocking)

class NetworkError(Exception):
    pass

def ReportError(funct, msg, info = None):
    print("========== ERROR:", funct, "->", msg)
    if info != None:
        for line in info:
            print("=====", line)

def DEBUG_print(msg):
    print(msg)

test = Network(NumNodes, LinkList)
#test.PrintNodes()
#test.PrintLinks()
#test.PrintNodeLinks()
#print(test.FindShortestPath("M","C"))
test.MainFunction(1)
