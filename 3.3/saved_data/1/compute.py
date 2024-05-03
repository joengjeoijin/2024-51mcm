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
data2_path = "~/51/zou/3/3.3/data2.xlsx"
data2 = pd.read_excel(data2_path)
data3_path = "~/51/zou/3/3.3/data3.xlsx"
data3 = pd.read_excel(data3_path)

num_node = len(map2)
num_path = 0
for i in map2:
    num_path = num_path + len(i)

capacity = []
for i in range(num_node):
    temp = []
    for j in range(num_node):
        temp.append(0)
    capacity.append(temp);
for i in range(len(data3)):
    capacity[data3.iloc[i,0]][data3.iloc[i,1]] = data3.iloc[i,2]

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

max_val = 0
max_i = 0
max_j = 0
for i in range(num_node):
    for j in range(num_node):
        if volumn[i][j]>max_val:
            max_val = volumn[i][j]
            max_i = i
            max_j = j
print(max_val)
print(max_i)
print(max_j)
getchar = input()

def evaluate_total(volumn):
    temp_volumn = copy.deepcopy(volumn)
    sum_val = 0
    for step in range(5):
        max_val = 0
        max_i = 0
        max_j = 0
        for i in range(num_node):
            for j in range(num_node):
                if temp_volumn[i][j]>max_val:
                    max_val=temp_volumn[i][j]
                    max_i = i
                    max_j = j
        sum_val = sum_val + max_val
        for i in range(len(result)):
            for j in range(len(result[i])):
                flag = False
                for k in range(len(routine[i][j])-1):
                    if routine[i][j][k]==max_i and routine[i][j][k+1]==max_j:
                        flag = True
                if flag==True:
                    for k in range(len(routine[i][j])-1):
                        temp_volumn[routine[i][j][k]][routine[i][j][k+1]] = temp_volumn[routine[i][j][k]][routine[i][j][k+1]] - result[i][j]
    return sum_val

kkk = evaluate_total(volumn)
for i in range(num_node):
    for j in range(num_node):
        if volumn[i][j] - capacity[i][j] > 1:
            kkk = kkk + volumn[i][j] - capacity[i][j]
print(kkk)
getchar = input()
import math
def evaluate1(volumn):
    sum = 0
    average = 0
    max_val = 0
    for i in range(len(volumn)):
        for j in range(len(volumn[i])):
            average = average + volumn[i][j]
    average = average/num_path
    for i in range(len(volumn)):
        for j in range(len(volumn[j])):
            if(volumn[i][j]>average):
                sum = sum + pow(volumn[i][j]-average,2)
    return sum

def evaluate(volumn):
    sum_val = 0;
    for i in range(len(volumn)):
        for j in range(len(volumn[i])):
            sum_val = sum_val + pow(volumn[i][j],2)
            if volumn[i][j] > capacity[i][j]:
                sum_val = sum_val + 10000*pow(volumn[i][j]-capacity[i][j],2)
    sum_val = 1.2*sum_val + 0.8*pow(evaluate_total(volumn),2)
    return sum_val

#def evaluate(volumn):
#    sum = 0
#    for i in range(num_node):
#        for j in range(num_node):
#            if volumn[i][j]>capacity[i][j]:
#                sum = sum + pow(volumn[i][j]-capacity[i][j],2)
#    return sum

#退火
import random
T = 1000
cooling_rate = 0.95
min_num = 1
import os
for step in range(20000):
    #产生随机值
    temp_num = 1
    #while temp_num==1:
    #    temp_num = 0
    #    temp_path = random.randint(0,len(result)-1)
    #    for i in range(len(result[temp_path])):
    #        if result[temp_path][i]>=1:
    #            temp_num = temp_num + 1
    temp_path = random.randint(0,len(result)-1)
    temp_routine1 = 0 #这个流量增加
    temp_routine2 = 0 #这个流量减少
    #while temp_routine1==temp_routine2 or result[temp_path][temp_routine1]<=min_num or result[temp_path][temp_routine2]<=min_num:
    while temp_routine1==temp_routine2:
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

    if new_val<old_val or math.exp(-(new_val-old_val)/T)>random.uniform(0,1):
    #if new_val<old_val:
        result = copy.deepcopy(new_result)
        volumn = copy.deepcopy(new_volumn)

    print(step,end=' ')
    print(old_val)

#for i in range(num_node):
#    for j in range(num_node):
#        if volumn[i][j] > capacity[i][j]:
#            print(volumn[i][j] - capacity[i][j],end=' ')
#            print(i,end=' ')
#            print(j)


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
