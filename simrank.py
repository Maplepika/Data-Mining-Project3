import numpy as np
import time

dir = "./hw3dataset/"
fileset = ["graph_1.txt", "graph_2.txt", "graph_3.txt", "graph_4.txt", "graph_5.txt"]
# fileset = ["graph_1.txt", "graph_2.txt", "graph_3.txt", "graph_4.txt", "graph_5.txt", "dirgenData.txt", "bidirgenData.txt"]
C = 0.4 # dacay factor for simrank
thre = 0.1

itemclass = {}
itemorder = {}
inv_itemorder= {}
ret_mat = np.zeros((1,1))

def simrank(a, b, C, threshold, count):
    if ret_mat[a][b] >= 0:
        return ret_mat[a][b]
    elif a == b:
        return 1
    elif len(itemclass[itemorder[a]]) == 0 or len(itemclass[itemorder[b]]) == 0:
        return 0
    elif pow(C, count) <= threshold:
        return 0
    else:
        sum = 0
        for i in range(len(itemclass[itemorder[a]])):
            for j in range(len(itemclass[itemorder[b]])):
                sum += simrank(inv_itemorder[itemclass[itemorder[a]][i]], inv_itemorder[itemclass[itemorder[b]][j]], C, threshold, count+1)        
        return C / (len(itemclass[itemorder[a]]) * len(itemclass[itemorder[b]])) * sum
        
output = open("simrank_result.txt", "w")

for filename in fileset:
    itemclass = {}
    itemorder = {}
    inv_itemorder= {}
    itemcount = 0
    f = open(dir + filename, "r")
    print("For " + filename + " :")
    for itemstring in f:
        value = itemstring.rstrip("\n").split(",")
        # Notice that the front number of pair don't need give value
        if value[0] not in itemclass:
            itemclass[value[0]] = []
            itemorder[itemcount] = value[0]
            inv_itemorder[value[0]] = itemcount
            itemcount += 1
        if value[1] not in itemclass:
            itemclass[value[1]] = [value[0]]
            itemorder[itemcount] = value[1]
            inv_itemorder[value[1]] = itemcount
            itemcount += 1
        else:
            itemclass[value[1]].append(value[0])
    
    print(len(itemclass))
    
    ret_mat = np.zeros((len(itemclass), len(itemclass)))
    for i in range(len(itemclass)):
        for j in range(len(itemclass)):
            ret_mat[i][j] = -1.0
    start = time.time()
    for i in range(len(itemclass)):
        for j in range(len(itemclass)):
            ret_mat[i][j] = simrank(i, j, C, thre, 1)
    end = time.time()
    print("Iterate over in %f sec..." %(end - start))
    print("The result is in output.txt:")
    print(ret_mat)

    output.write("For " + filename + " :\n")
    output.write("Iterate over in %f sec...\n" %(end - start))
    for row in range(len(ret_mat)):
        for col in range(len(ret_mat[row])):
            output.write("S(" + str(itemorder[row]) + "," + (itemorder[col]) + "): " + str(ret_mat[row][col]) + "\n")
    output.write("\n")
    output.write("\n")

output.close()