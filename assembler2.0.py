from sys import exit
d={"add":"00000","sub":"00001","mov":"00010","mov_":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
d_={"R1":"000","R2":"001","R3":"010","R4":"011","R5":"100","R6":"101","R7":"110","FlAGS":"111"}
f=open("assembler_code.txt","r")
data=f.readlines()
f.close()
data=[i.split(" ") for i in data if i!=""]
data=data[1:];flag=True
if data[-1][-1]!="hlt":
    flag=False
if len(data)>127:
    flag=False
for i in range(len(data)):
    data[i][-1]=data[i][-1][:-1]
d1={};count_=len(data)+1 # storing variable in the dictionary
for i in data:
    if i[0]=="var":
        if count_>127:
            flag=False
        d1[i[1]]=bin(count_)[2:]
        count_+=1
d2={}#storing labels in the dictionary
for i in range(len(data)):
    if data[i][0][-1]==":":
        d2[data[i][0]]=bin(i)[2:]
