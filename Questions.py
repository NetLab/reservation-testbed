from random import *

class TestClass:
    def __init__(self):
        self.x = randint(0,10)
        self.y = randint(0,10)
    def PrintXY(self):
        print("[", self.x, self.y, "]")

def LambdaTest():
    testList = []
    for x in range(0,10):
        testList.append(TestClass())
    testList.sort(key=lambda test: (test.x, test.y), reverse=True)
    for x in testList:
        x.PrintXY()

LambdaTest()

# List of definite changes to be made:
# - Seperate the two types of blocking into their own counters
# - Confirm that each request completes or blocks (Same amount finish or fail as were created)

# Tentative
# - Check if reservation must occupy the same bandwith slot on each link it is a part of
#   -- I.E: must it be 1, or is 2 okay?
#               1                                               2
#   Link A      ->      Link B          or          Link A      ->      Link B
#   0110                0110                        0110                1100
#   0110                0110                        0110                1100
#   0110                0110                        0110                1100
#
# - Do nodes start on link the time unit they arrive, or the first one after?
