import multiprocessing
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

if __name__ == '__main__':
    timer = clock()
    procPool = multiprocessing.Pool(None)
    myLambdas = []
    results = []
    numCores = multiprocessing.cpu_count()
    rangeLambda = range(NumLambdas)
    for _ in procPool.imap_unordered(RunTrial, rangeLambda, chunksize=numCores):
        pass
    procPool.close()  # Wait on the results
    procPool.join()
    timer = clock() - timer
    print("Took", timer, "seconds")
    print(results)
