#读取临时文件
import copy
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

num_node = len(map2)
num_path = 0
for i in map2:
    num_path = num_path + len(i)

volumn = []
for i in range(num_node):
    temp = []
    for j in range(num_node):
        temp.append(0)
    volumn.append(temp)
for i in range(len(result)):
    for j in range(len(result[i])):
        for k in range(len(routine[i][j][0:-1])):
            volumn[routine[i][j][k]][routine[i][j][k+1]] = volumn[routine[i][j][k]][routine[i][j][k+1]] + result[i][j]
            
import math
def evaluate(volumn,p):
    sum = 0
    max_val = 0;
    for i in range(len(volumn)):
        for j in range(len(volumn[i])):
            sum = sum + math.pow(volumn[i][j],2)
            if volumn[i][j]>max_val:
                max_val = 
    sum = sum*(1-p)

    return sum

print(volumn)
getchar = input()

#退火
import random
T = 1000
cooling_rate = 0.9
min_num = 1
for step in range(10000):
    #产生随机值
    temp_num = 1
    while temp_num==1:
        temp_num = 0
        temp_path = random.randint(0,len(result)-1)
        for i in range(len(result[temp_path])):
            if result[temp_path][i]>=1:
                temp_num = temp_num + 1
    temp_routine1 = 0 #这个流量增加
    temp_routine2 = 0 #这个流量减少
    while temp_routine1==temp_routine2 or result[temp_path][temp_routine1]<=min_num or result[temp_path][temp_routine2]<=min_num:
        temp_routine1 = random.randint(0,len(result[temp_path])-1)
        temp_routine2 = random.randint(0,len(result[temp_path])-1)
    val_change = random.uniform(0,result[temp_path][temp_routine2])

    old_val = evaluate(volumn)
    new_result = copy.deepcopy(result)
    new_result[temp_path][temp_routine1] = new_result[temp_path][temp_routine1] + val_change
    new_result[temp_path][temp_routine2] = new_result[temp_path][temp_routine2] - val_change
    new_volumn = []
    for i in range(num_node):
        temp = []
        for j in range(num_node):
            temp.append(0)
        new_volumn.append(temp)
    for i in range(len(result)):
        for j in range(len(result[i])):
            for k in range(len(routine[i][j][0:-1])):
                new_volumn[routine[i][j][k]][routine[i][j][k+1]] = new_volumn[routine[i][j][k]][routine[i][j][k+1]] + new_result[i][j]
    new_val = evaluate(new_volumn)

    if math.exp(-(new_val-old_val)/T)>random.uniform(0,1):
        result = copy.deepcopy(new_result)
        volumn = copy.deepcopy(new_volumn)

print(volumn)
print(result)


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
