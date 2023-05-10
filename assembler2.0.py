from sys import exit
d={"add":"00000","sub":"00001","mov":"00010","mov_":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
d_={"R1":"000","R2":"001","R3":"010","R4":"011","R5":"100","R6":"101","R7":"110","FlAGS":"111"}
f=open("assembler_code.txt","r")
data=f.readlines()
data=[i.split(" ") for i in data if i!=""]
data=data[1:]
for i in range(len(data)):
    if i!=len(data)-1:
        data[i][-1]=data[i][-1][:-1]
var_dic={};count_=0
for i in data:
    if i[0]!="var":count_+=1
for i in data:
    if i[0]=="var":
        t=bin(count_)[2:]
        t="0"*(7-len(t))+t
        var_dic[i[1]]=t
        count_+=1
label_dic={}#storing labels in the dictionary
count_=0
for i in range(len(data)):
    if data[i][0][-1]==":":
        t=bin(count_)[2:]
        t="0"*(7-len(t))+t
        label_dic[data[i][0][:-1]]=t
        count_+=1
    elif data[i][0]!="var":
        count_+=1
for i in range(len(data)):
    if data[i][0][-1]==":":
        data[i]=data[i][1:]

print(data)
print(var_dic)
print(label_dic)
def hlt_end(data):
    if data[-1][-1]=="hlt":
        return True
    else:
        print("hlt not found at the end")
        return False
def hlt_not_found(data):
    flag=True
    for i in data:
        for j in i:
            if j=="hlt":
                flag=False
            break
    if flag:
        print("No hlt instruction found")
        return True
        
    else:
        return False
def var_found_in_btw(data):
    flag=True;count_=0
    for i in data:
        if count_==0:
            if i[0]!="var":
                count_+=1
        if count_==1:
            if i[0]=="var":
                flag=False
                break
    if flag:
        return False
    else:
        print("Variable found in between")
        return True
def immediate(data):
    flag=True
    for i in data:
        for j in range(len(i)):
            if i[j][0]=="$":
                z=len(bin(i[j][1:])[2:])
                if z>7:
                    flag=False
                    break
    if flag:
        return flag
    else:
        print("Immediate value greater than 7 bit")
        return flag
 f.close() 

