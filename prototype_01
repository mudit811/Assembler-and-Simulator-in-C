ins={"add":"00000","sub":"00001","mov":"00010","mov_":"00011","ld":"00100","st":"00101","mul":"00110","div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101","cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010"}
reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
ins_type={"add":1,"sub":1,"mov":2,"mov_":3,"ld":4,"st":4,"mul":1,"div":3,"rs":2,"ls":2,"xor":1,"or":1,"and":1,"not":3,"cmp":3,"jmp":5,"jlt":5,"jgt":5,"je":5,"hlt":6}
var_dec_perm, var_dec_error, input_ovrflw_error, imm_ovrflw_error = 1,0,0,0

def convert_A(s):
   global reg
   global ins
   x= f"{ins[s[0]]}00{reg[s[1]]}{reg[s[2]]}{reg[s[3]]}"
   return(x)

def convert_B(s):
    global reg
    global ins
    global imm_ovrflw_error
    imm=(str(bin(int(s[2].strip("$"))))).strip("0b")
    if len(imm)<8:
        imm="0"*(7-len(imm))+imm
        x=f"{ins[s[0]]}0{reg[s[1]]}{imm}"
        return(x)

def convert_C(s):
    global reg
    global ins
    x= f"{ins[s[0]]}00000{reg[s[1]]}{reg[s[2]]}"
    return(x)

def convert_D(s):  
    global reg
    global ins
    global var_dic
    x=f"{ins[s[0]]}0{reg[s[1]]}{var_dic[s[2]]}"
    return(x)
    

def convert_E(s):   
    global reg
    global ins
    global label_dic
    x=f"{ins[s[0]]}0000{label_dic[s[1]]}"
    return(x)

def convert_F(s):
    global ins
    x=f"{ins[s[0]]}00000000000"
    return(x)

func_dic={1: convert_A, 2: convert_B, 3: convert_C, 4: convert_D, 5: convert_E, 6: convert_F}

def func_call(s):
    t=ins_type[s[0]]
    x=func_dic[t](s)
    return(x)

f=open("stdin.txt","r")
data=f.readlines()
data=[i.split(" ") for i in data if i!=""]
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

for i in data:
    if (i[0]!="var"):
        x=func_call(i)
        print(x)
