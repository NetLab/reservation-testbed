from Constants import *

class Node:
    def __init__(self, name):
        self.name       = name
        self.pathDict   = {}    # Dictionary containing shortest paths to other nodes
        self.linkDict   = {}    # Any links shared with other nodes and the cost of that link
        self.linkDict[name] = 0 # Sets distance to self to 0

    def SetLink(self, node, cost):
        self.linkDict[node] = cost

    def SetDefaultLinks(self, nodeList):
        for node in nodeList:
            if node != self.name:
                self.SetLink(node, LINK_DNE)
            else:
                self.SetLink(node, LINK_SELF)

    def GetLinks(self):
        return self.linkDict

    def SetPath(self, dst, path):
        self.pathDict[dst] = path

    def GetPaths(self):
        paths = []
        for path in self.pathDict:
            paths.append(self.pathDict[path])
        return paths

    def CheckPaths(self, dst):
        if dst in self.pathDict:
            return self.pathDict[dst]
        else:
            return None

    def PrintInfo(self):
        print("On Node", self.name, ":")
        for link in self.linkDict:
            print("Link to", link, "of length", self.linkDict[link])