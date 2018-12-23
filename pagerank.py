import numpy as np
import time

dir = "./hw3dataset/"
fileset = ["graph_1.txt", "graph_2.txt", "graph_3.txt", "graph_4.txt", "graph_5.txt", "graph_6.txt", "dirgenData.txt", "bidirgenData.txt"]
thre = 0.01
D = 0.15

def iteration(mat, value, threshold, count, init):
    prev_value = value.copy()
    result_sum = 0

    result = (1-D) * np.matmul(mat, value) + D * init
    for v in result:
        result_sum += v[0]
    # Notice that if all of rank value is zero, i.e. rank sink, return a zero vector to main function.
    if result_sum == 0:
        return result, count
    for i in range(len(result)):
        result[i][0] /= result_sum
    
    sub = np.subtract(prev_value, result)
    distance = 0
    for i in range(len(sub)):
        distance += abs(sub[i][0])

    if distance <= threshold:
        return result, count
    else:
        count += 1
        return iteration(mat, result, threshold, count, init)

output = open("pagerank_result.txt", "w")
for filename in fileset:
    data = []
    itemclass = {}
    inv_itemclass = {}
    itemcount = 0
    f = open(dir + filename, "r")
    print("For " + filename + " :")
    for itemstring in f:
        value = itemstring.rstrip("\n").split(",")
        if value[0] not in itemclass:
            itemclass[value[0]] = itemcount
            inv_itemclass[itemcount] = value[0]
            itemcount += 1
        if value[1] not in itemclass:
            itemclass[value[1]] = itemcount
            inv_itemclass[itemcount] = value[1]
            itemcount += 1

        data.append([value[0], value[1]])

    mat = np.zeros((itemcount, itemcount))
    init = np.zeros((itemcount,1))
    for d in data:
        x = itemclass[d[0]]
        y = itemclass[d[1]]
        mat[x][y] = 1
    for i in range(len(init)):
        init[i] = 1/len(init)
    
    mat = mat.transpose()
    # Normalize for matrix
    for col in mat:
        mat_sum = 0
        for item in col:
            mat_sum += item
        if mat_sum != 0:    
            col /= mat_sum
    print(mat)
    # Notice that if all of rank value is zero, i.e. rank sink, return a zero vector to main function.
    
    start = time.time()
    result, count = iteration(mat, init, thre, 1, init)
    end = time.time()
    print("Iterate over in %f sec..." %(end - start))
    print("After " + str(count) + " iteration, the result is in output.txt:")

    output.write("For " + filename + " :\n")
    output.write("Iterate over in %f sec...\n" %(end - start))
    
    output.write("After " + str(count) + " iteration, the result is:\n")
    for i in range(len(result)):
        output.write(str(inv_itemclass[i]) + ": " + str(result[i][0]) + "\n")
    output.write("\n")
    output.write("\n")

output.close()