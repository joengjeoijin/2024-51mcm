import pickle
import pandas as pd
myfile = open("mymap",'rb')
map2 = pickle.load(myfile)
myfile.close()
myfile = open("myroutine",'rb')
routine = pickle.load(myfile)
myfile.close()
myfile = open("temp_result",'rb')
result = pickle.load(myfile)
myfile.close()
data2_path = "~/51/zou/3/3.1/data1.xlsx"
data2 = pd.read_excel(data2_path)

#去除小值
for i in range(len(result)):
    max_val = max(result[i])
    index = result[i].index(max_val)
    for j in range(len(result[i])):
        if result[i][j]<1:
            result[i][index] = result[i][index] + result[i][j]
            result[i][j] = 0
print(result)       

#保留五个最大值
min_num = 0.0000001
for i in range(len(result)):
    array = sorted(result[i],reverse=True)[0:5]
    index = []
    total = sum(array)
    for j in range(len(array)):
        index.append(result[i].index(array[j]))
    other = 0
    for j in range(len(array)):
        if j in index:
            continue
        else:
            other = other + result[i][j]
            result[i][j] = 0
    for j in range(len(array)):
        if j in index:
            if result[i][j]>min_num:
                result[i][j] = result[i][j] + result[i][j]/total*other
print(result)

myfile = open("temp_result",'wb')
pickle.dump(result,myfile)
myfile.close()
