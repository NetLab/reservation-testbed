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
        self.arrivingBlocking   = 0

        self.debugFirstLink     = 0

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

    # Load in premade reservation
    def LoadRes(self, info):
        res = Reservation(1, self.GetNodes())
        res.Load(info[R_NodesIndex], info[R_ArrivIndex], info[R_StartIndex], info[R_HoldiIndex], info[R_NumSlIndex])
        src, dst = res.GetSrcDst()
        res.SetPath(self.FindShortestPath(src, dst))
        self.arrivingResList.append(res)

    # Load in list of multiple premade reservations
    def LoadMultRes(self, infoList):
        for i in range(0, len(infoList)):
            self.LoadRes(infoList[i])
        self.SortResByArrival()

    # Generate a reservation with random values
    def CreateRes(self, my_lambda, nodes):
        res = Reservation(my_lambda, nodes)
        src, dst = res.GetSrcDst()  # Get the source and destination nodes for the reservation
        res.SetPath(self.FindShortestPath(src, dst))  # Find and set the shortest path it can take
        self.arrivingResList.append(res)

    # Generate several reservations with random values
    def CreateMultRes(self, my_lambda, numRes):
        i = 0
        nodes = self.GetNodes()
        while i < numRes:
            self.CreateRes(my_lambda, nodes)
            i += 1
        self.SortResByArrival()

    # Sort res in arrivingResList by their arrival time
    def SortResByArrival(self):  # Sorts initial list based on arrival time, then bookahead time
        #self.arrivingResList.sort(key=attrgetter('arrival_t', 'sourceNode', 'destNode'))
        try:
            self.arrivingResList.sort(key=lambda res: (res.arrival_t, res.sourceNode, res.destNode))
        except:
            self.DEBUG_PrintTypesInList(self.arrivingResList)
            raise

    # Sort res in arrivingResList by their start time
    def SortResByStartT(self):
        #self.arrivingResList.sort(key=attrgetter('start_t', 'arrival_t', 'book_t'))
        self.arrivingResList.sort(key=lambda res: (res.start_t, res.sourceNode, res.destNode))

    # Print out arrivingResList
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
            print("Reservation from", res.GetSrcDst(), "with next path", res.GetNextPathLink(), "Arriving at", res.GetNextTime(), "for", res.GetHoldingTime(), "of width", res.GetNumSlots())

    def DEBUG_ERROR_CheckValidRes(self, resList): # ensure all objects in list are of type reservation
        for res in resList:
            if type(res) != Reservation:
                return False
        return True


    # Search arrivingResList for any reservations arriving at this time, initial or forwarded
    def AllocateArrivingRes(self):
        self.SortResByArrival()
        arrivingRes         = []
        arrivingResIndexes  = []
        for res in self.arrivingResList:
            if res.arrival_t == self.time:
                arrivingResIndexes.append(self.arrivingResList.index(res))
            elif res.arrival_t < self.time:
                ReportError("AllocateArrivingRes", "res arriving at link: {0} at time: {1} for passed time: {2}".format(res.GetNextPathLink(), self.time, res.arrival_t))
                raise NetworkError()
        arrivingResIndexes = sorted(arrivingResIndexes, reverse=True)
        for index in arrivingResIndexes:
            arrivingRes.append(self.arrivingResList.pop(index))

        return arrivingRes

    # For use upon reservations initial arrival at first node. Checks if a continuous space is open on its path right now.
    #   Returns the first index found. Blocks if none.
    def CheckInitialPathOpen(self, res):
        listLinks       = []  # List of links in path to check
        spaceOptions    = []  # Options for continuous blocks of space to check in path
        pathSpace       = None # The final decided continuous (persistent) start location for the reservation
        hasPath         = False
        DEBUG_index     = 0

        size            = res.GetNumSlots() # get the size in slots of the request
        listLinks       = res.GetAllPathLinks()
        print(listLinks)
        spacesFound, spaceOptions    = self.linkDict[listLinks[0]].GetListOfOpenSpaces(size) # Possible cont. spaces in init. link
#        print("DEBUG LIST OF SPACES", spaceOptions)

        print(listLinks[0], "has", len(spaceOptions), "spaces")
        if spacesFound == False:    # If no spaces are found
            print("Returned False 1")
            return False, pathSpace
        elif len(listLinks) == 1:  # If only one link in path
            return True, spaceOptions[0]    # Return that a path was found, and the first spot found
        for space in spaceOptions:  # For each possible space
            pathSpace = space
            for link in listLinks[1:]:  # For each link beyond the first in the path
                if self.linkDict[link].CheckContinuousSpace(space, size) == FULL:   # Check each possible space
                    hasPath = False
                    print("Conflict with", listLinks.index(link))
                    break                   # If the space is full in any link, move on to the next possible space
                else:
                    print("Success")
                    hasPath = True

            if hasPath == True:         # If any possible space is empty on every link
                return hasPath, pathSpace   # return True and the index of the space

        pathSpace = None    # set pathSapce as None
        if hasPath: # If hasPath is somehow True at this point, raise an error
            print("Oops, I did something wrong")
            raise

        print("Returned False 2")
        return hasPath, pathSpace

    # Get all arriving reservations, then load them to their corresponding link or complete them
    def UpdateLinkRes(self):

        arrivingRes     = self.AllocateArrivingRes()
        resToLinkDict   = {}    # Dictionary of each link, each entry contains list of res arriving at link
        resInstr        = [ERR_INSTR] * len(arrivingRes)    # List of instructions for processing res; default to all err

        for link in self.linkDict:  # For each link
            resToLinkDict[link]   = []    # Initialize an empty list of reservations to be loaded

        index = 0   # index of current res arriving
        for res in arrivingRes:
            isDone, nodes = res.IsResDone()
            if isDone:
                resInstr[index] = DON_INSTR

                if nodes is not None:
                    self.completedResList.append(nodes)
                    self.completedRes += 1
                else:
                    print("ERROR: UpdateLinkRes -> invalid completed node pair")
                    raise

            else:   # If reservation is not done

                if res.IsOnFirstLink(): # If this is the first link the res arrives on
                    hasSpace, slotIndex = self.CheckInitialPathOpen(res)    # Check if res can be continuous, and where

                    if hasSpace == False:   # If no continuous space was found
                        self.arrivingBlocking += 1  # increment number of arrival blocked res
                        print("BLOCKED on", res.sourceNode + res.destNode, "of size", res.num_slots)
                        resInstr[index] = BLK_INSTR # Record res as blocked
                        continue                    # continue to next res in arrivingRes
                    else:
                        res.SetLinkIndex(slotIndex) # Set the slot index that the res will continuously occupy

                for link in self.linkDict:
                    if FormatLinkName_String(res.GetNextPathLink()) == link:
                        resInstr[index] = PAS_INSTR
                        resToLinkDict[link].append(res)
            index += 1

        for link in resToLinkDict:  # For each link
            if len(resToLinkDict[link]) > 0:    # If any res to be loaded for the respective link
                self.linkDict[link].LoadArrivingRes(resToLinkDict[link])    # Load the list of res for that link

        for instr in resInstr:
            if instr < MIN_INSTR or instr > MAX_INSTR:
                print("Arriving Res List not Cleared")
                print("Arriving Res at", self.time)
                self.DEBUG_PrintListOfRes(arrivingRes)
                raise

    # For each link, run a time step and retrieve any reservations to be forwarded.
    def RunCurrentTimeStep(self):
        for link in self.linkDict:
            fwdedResList = self.linkDict[link].RunTimeStep()
            self.arrivingResList += fwdedResList

    # ======================================= M a i n   F u n c t i o n ==========================================

    def MainFunction(self, my_lambda, numRes):
        self.CreateMultRes(my_lambda, numRes)
        self.initialResList = deepcopy(self.arrivingResList)
        #print("Initial Reservations")
        #self.DEBUG_PrintListOfRes(self.initialResList)

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

#        print("Initial Reservations")
#        self.DEBUG_PrintListOfRes(self.initialResList)

        print("Of", numRes, "initial reservations")
        print("Reservations Completed", self.completedRes)
        localBlocking   = self.arrivingBlocking    # Get number of local blocks
        linkBlocking    = 0
        for link in self.linkDict:
            linkBlocking += self.linkDict[link].GetNumBlocks()  # Add the number of blocks occurring in each link
        totalBlocking = localBlocking + linkBlocking
#        for res in self.completedResList:
#            print(res)
        print("Total number of blocks:", totalBlocking, "\n", localBlocking, "blocked initially and", linkBlocking, "due to conflict")
        print("DEBUG", self.debugFirstLink)

        if(numRes != totalBlocking + self.completedRes):
            ReportError("MainFunction", "Not all of {0} reservations blocked: {1}, or completed: {2}".format(numRes, totalBlocking, self.completedRes))
            raise NetworkError



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
test.MainFunction(Lambda, NumRes)
