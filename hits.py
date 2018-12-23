import time

dir = "./hw3dataset/"
fileset = ["graph_1.txt", "graph_2.txt", "graph_3.txt", "graph_4.txt", "graph_5.txt", "graph_6.txt", "dirgenData.txt", "bidirgenData.txt"]
thre = 0.1

def iteration(data, record, threshold, itercount):
    prev_record = record.copy()
    autcount = 0
    hubcount = 0
    for d in record:
        authority = 0
        hubness = 0
        for itempair in data:
            if itempair[0] == str(d):
                hubness += prev_record[itempair[1]][0]
            if itempair[1] == str(d):
                authority += prev_record[itempair[0]][1]
        record[d] = [authority, hubness]
        autcount += authority
        hubcount += hubness
    if autcount == 0:
        autcount = 1
    if hubcount ==0:
        hubcount = 1
    for d in record:
        record[d] = [record[d][0] / autcount, record[d][1] / hubcount]
    
    again = False
    for d in record:
        if abs(record[d][0] - prev_record[d][0]) > threshold:
            again = True
            break
        if abs(record[d][1] - prev_record[d][1]) > threshold:
            again = True
            break
    if again:
        itercount += 1
        return iteration(data, record, threshold, itercount)
    else:
        return record, itercount

output = open("hits_result.txt", "w")

for filename in fileset:
    data = []
    itemclass = {}
    f = open(dir + filename, "r")
    print("For " + filename + " :")
    for itemstring in f:
        value = itemstring.rstrip("\n").split(",")
        # let the pair be [authority, hubness]
        if value[0] not in itemclass:
            itemclass[value[0]] = [1,1]
        if value[1] not in itemclass:
            itemclass[value[1]] = [1,1]

        data.append([value[0], value[1]])
    start = time.time()
    result, count = iteration(data, itemclass, thre, 1)
    end = time.time()
    print("Iterate over in %f sec..." %(end - start))
    print("After " + str(count) + " iteration, the result is in output.txt:")

    output.write("For " + filename + " :\n")
    output.write("Iterate over in %f sec...\n" %(end - start))
    
    output.write("After " + str(count) + " iteration, the result is:\n")
    output.write(str(result))
    output.write("\n")
    output.write("\n")

output.close()
