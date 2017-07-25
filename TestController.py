import multiprocessing
import os
import random
from math import *
from NetworkV2 import *

# def calculate(value):
#     return value * 10
#
# if __name__ == '__main__':
#     pool = multiprocessing.Pool(None)
#     tasks = range(10000)
#     results = []
#     r = pool.map_async(calculate, tasks, callback=results.append)
#     r.wait() # Wait on the results
#     print results

#for x in range (23, 99, 2):
def CompileReport():
    reports = []
    for x in range(0,NumLambdas):
        try:
            report = open("Test" + str(x) + ".txt", 'r')
            for line in report:
                reports.append(line)
            report.close()
        except:
            print("Report", x, "Not Found")
    finalReport = open("FinalReport.txt", 'w')
    for rLine in reports:
        finalReport.write(rLine)
        finalReport.write('\n')
    finalReport.close()
    for x in range(0, NumLambdas):
        try:
            os.remove("Test" + str(x) + ".txt")
        except:
            pass



def WorkerInit():
    pass

def InitRun(myLambdaIndex):
    RandSeed(myLambdaIndex)
    RunTrial(myLambdaIndex)

def RandSeed(mySeed):
    random.seed(a=mySeed)

alt = False
if __name__ == '__main__':
    if alt == False:
        results = []
        timer = clock()

        procPool = multiprocessing.Pool(initializer=WorkerInit)

        numCores    = multiprocessing.cpu_count()
        rangeLambda = range(NumLambdas)
        numChunks   = ceil(NumLambdas/numCores)

        results = procPool.map_async(InitRun, rangeLambda, chunksize=numChunks)
        procPool.close()  # Wait on the results
        procPool.join()
        timer = clock() - timer
        print("Took", timer, "seconds")
        CompileReport()
    else:
        CompileReport()
