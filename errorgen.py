from sys import exit
d={"add":"00000","sub":"00001","mov":"00010","mov_":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
d_={"R1":"000","R2":"001","R3":"010","R4":"011","R5":"100","R6":"101","R7":"110","FlAGS":"111"}
f=open("sample.txt","r")
data=f.readlines()
data=[i.split(" ") for i in data if i!=""]

for i in range(len(data)):
    if i!=len(data)-1:
     data[i][-1]=data[i][-1][:-1]
var_dic={};count_=len(data)+1
                                                        # storing variable in the dictionary
for i in data:
    if i[0]=="var":
        t=bin(count_)[2:]
        t="0"*(7-len(t))+t
        var_dic[i[1]]=t
label_dic={}                                  #storing labels in the dictionary
for i in range(len(data)):
    if data[i][0][-1]==":":
        t=bin(i+1)[2:]
        t="0"*(7-len(t))+t
        label_dic[data[i][0]]=t
for i in range(len(data)):
    if data[i][0][-1]==":":
        data[i]=data[i][1:]
print(data)
print(var_dic)
print(label_dic)
f.close() 

def typos(data,d):
    flag=True
    for i in range(len(data)):
        if data[i][0] not in d:
            line=i
            flag=False  
            break
    if flag==False:
        print("Syntax Error: Error at line:",i)
    return flag

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


def var_dec_error(data,var_dic):
    flag=True
    for i in range(len(data)):
        if data[i][0]!="var":
            for j in data[i]:
                if j[:3] =="var":
                    print(j,var_dic)
                    if j not in var_dic:
                        undec=j
                        line=i
                        flag=False
                        break
        if flag==False:
            break
    print(f"Undefined variable {undec}: Error at line:",i)
    return flag




var_dec_error(data,var_dic)

typos(data,d)
    
    


