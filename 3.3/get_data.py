import copy
import pandas as pd
import xlrd
data2_path = "~/51/zou/3/3.3/data2.xlsx"
data2 = pd.read_excel(data2_path)
map2_path = "~/51/zou/3/3.3/map2.xlsx"
map2_info = pd.read_excel(map2_path)

temp_map2 = []
map2 = []
for i in range(len(map2_info)):
    temp_map2.append(map2_info.iloc[i,1].split(","))
for i in temp_map2:
    temp = []
    for j in i:
        temp.append(int(j))
    map2.append(temp)

#routine与datax的顺序一致
routine = []
for i in range(len(data2)):
    #运行问题1的时候再以下两行后面加 -1
    start_node = data2.iloc[i,0]
    end_node = data2.iloc[i,1]
    num_routines = 0
    temp_len = 0

    queue = []
    temp = []
    temp.append(start_node)
    queue.append(temp)
    temp_routines = []

    #print(start_node)
    #print(end_node)

    while num_routines < 5:
        temp_queue = copy.deepcopy(queue);
        queue = [];
        #print(temp_queue)
        #getchar = input()
        for i in temp_queue:
            for j in map2[i[-1]]:
                temp = copy.deepcopy(i)
                if j in temp:
                    continue
                else:
                    temp.append(j)
                    if len(temp)>temp_len:
                        temp_len=len(temp)
                    if j==end_node:
                        temp_routines.append(temp)
                        num_routines = num_routines + 1
                    else:
                        queue.append(temp)
    routine.append(temp_routines)
    #print(temp_routines)

result = []
for i in range(len(routine)):
    x = data2.iloc[i,2]/len(routine[i])
    temp = []
    for j in range(len(routine[i])):
        temp.append(x)
    result.append(temp)

#保存数据
import pickle
myfile = open("mymap",'wb')
pickle.dump(map2,myfile)
myfile.close()
myfile = open("myroutine",'wb')
pickle.dump(routine,myfile)
myfile.close()
myfile = open("temp_result",'wb')
pickle.dump(result,myfile)
myfile.close()
