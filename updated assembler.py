from sys import exit


# For all the error generator functions a return of False, indicates an error and True indicates there is no error.

def typo_opcode(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] not in l:
            line = i
            flag = False
            break
    if flag:
        return True
    else:
        f.write(f"Syntax Error: Operation code not correct; Error at line: {line}\n")
        return False


def typo_reg(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] in ["add", "sub", "mul", "xor", "or", "and"]:
            if data[i][1] not in reg or data[i][2] not in reg or data[i][3] not in reg:
                flag = False
                break
        elif data[i][0] in ["div", "not", "cmp"]:
            if data[i][1] not in reg or data[i][2] not in reg:
                flag = False
                break

        elif data[i][0] in ["ld", "st", "rs", "ls"]:
            if data[i][1] not in reg:
                flag = False
                break

        elif data[i][0] == "mov":
            if data[i][2][0] == "$":
                if data[i][1] not in reg:
                    flag = False
                    break

            else:
                if data[i][1] not in reg or data[i][2] not in reg:
                    flag = False
                    break

    if flag:
        return True
    else:
        f.write(f"Syntax Error: Register name not correct: Error at line {i}\n")
        return False


def hlt_end(data):
    if data[-1][-1] == "hlt":
        return True
    else:
        f.write(f"hlt not found at the end\n")
        return False


def hlt_not_found(data):
    flag = True
    for i in data:
        for j in i:
            if j == "hlt":
                flag = True
            break
    if flag:
        return True

    else:
        f.write(f"No halt instruction found\n")
        return False


def immediate(data):
    flag = True
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j][0] == "$":
                z = len(bin(int(data[i][j][1:]))[2:])
                if z > 7:
                    line = i
                    flag = False
                    break
        if flag == False:
            break
    if flag:
        return True
    else:
        f.write(f"Error at line {i} :Immediate value greater than 7 bit\n")
        return False


def var_found_in_btw_error(data):
    flag = True
    count_ = 0
    for i in range(len(data)):
        if count_ == 0:
            if data[i][0] != "var":
                count_ += 1
        if count_ == 1:
            if data[i][0] == "var":
                flag = False
                break
    if flag:
        return flag
    else:
        f.write(f"Variable found in between:Error at line {i}\n")
        return flag


def undefined_label(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] in jump_lst:
            j = data[i][1]
            if j not in label_dic:
                undec = j
                line = i
                flag = False
                break
    if flag:
        return True
    else:
        f.write(f"Undefined label {undec}: Error at line {i}\n")
        return False


def undefined_variable(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] in ["ld", "st"]:
            j = data[i][2]
            if j not in var_dic:
                undec = j
                line = i
                flag = False
                break
    if flag:
        return True
    else:
        f.write(f"Undefined variable {undec}: Error at line {i}\n")
        return False


def misuse_labels_n_var(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] in jump_lst and data[i][1] in var_dic:
            flag = False
            f.write(f"Using variable instead of label: Error at line: {i}\n")

        if data[i][0] in ["ld", "st"] and data[i][2] in label_dic:
            flag = False
            f.write(f"Using label instead of variable: Error at line: {i}\n")
    return flag


def flag_reg_misuse(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] != "mov" and "FLAGS" in data[i]:
            flag = False
            f.write(
                f"{data[i][0]} operation cannot have FLAGS in the instruction: Error at line {i}\n"
            )
            break
    return flag


def imm_misuse(data):
    flag = True
    for i in range(len(data)):
        if data[i][0] not in ["mov", "rs", "ls"]:
            for j in range(len(data[i])):
                if data[i][j][0] == "$":
                    flag = False
                    f.write(
                        f"{data[i][0]} operation cannot have immediate value in the instruction: Error at line {i}\n"
                    )
                    break
            if flag == False:
                break
    return flag
def var_already_dec(data):
    vd=[]
    for i in range(len(data)):
        if data[i][0]=='var':
            if data[i][1] not in vd:
                vd.append(data[i][1])
            else:
                f.write(f"variable {data[i][0]} already defined. Error at line {i}")
                return False
    return True

def label_already_dec(label_freq,label_dic):
    for i in label_freq:
        if label_freq[i]!=1:
            f.write(f"Used {i} label more than once. Error at line {int(label_dic[i],2)+len(var_dic)}")
            return False
    return True
def correct_instruction_length(data):
    flag = True
 
    for i in range(len(data)):

        if ins_type[data[i][0]] == 1:
            if len(data[i]) != 4:
                num=4
                flag = False
                break
        elif ins_type[data[i][0]] == 2:
            if len(data[i]) != 3:
                num=3
                flag = False
                break
        elif ins_type[data[i][0]] == 3:
            if len(data[i]) != 3:
                num=3
                flag = False
                break
        elif ins_type[data[i][0]] == 4:
            if len(data[i]) != 3:
                num=3
                flag = False
                break
        elif ins_type[data[i][0]] == 5:
            if len(data[i]) != 2:
                num=2
                flag = False
                break
        elif ins_type[data[i][0]] == 6:
            if len(data[i]) != 1:
                num=1
                flag = False
                break
    if flag:
        return True
    else:
        f.write(f"General Synatx Error-{data[i][0]} operation expects {num-1} arguments after opcode: Error at line {i}\n")
        return False

def ERRORS(data):
    isErrorfree = True
    # isERRORfree=typo_opcode(data) and hlt_end(data) and hlt_not_found(data) and immediate(data) and var_found_in_btw_error(data) and undefined_label(data) and undefined_variable(data) and misuse_labels_n_var(data) and flag_reg_misuse(data) and imm_misuse(data)
    if typo_opcode(data) == False:
        isErrorfree = False
    elif correct_instruction_length(data)==False:
        isErrorfree =False
    elif typo_reg(data) == False:
        isErrorfree = False
    elif var_already_dec(data) == False:
        isErrorfree=False
    elif label_already_dec(label_freq,label_dic)==False:
        isErrorfree=False
    elif hlt_not_found(data) == False:
        isErrorfree = False
    elif hlt_end(data) == False:
        isErrorfree = False
    elif imm_misuse(data) == False:
        isErrorfree = False
    elif var_found_in_btw_error(data) == False:
        isErrorfree = False
    elif undefined_label(data) == False:
        isErrorfree = False
    elif undefined_variable(data) == False:
        isErrorfree = False
    elif misuse_labels_n_var(data) == False:
        isErrorfree = False
    elif flag_reg_misuse(data) == False:
        isErrorfree = False
    elif immediate(data) == False:
        isErrorfree = False
    

    return isErrorfree


ins = {
    "add" : "00000",
    "sub" : "00001",
    "mov" : "00010",
    "ld"  : "00100",
    "st"  : "00101",
    "mul" : "00110",
    "div" : "00111",
    "rs"  : "01000",
    "ls"  : "01001",
    "xor" : "01010",
    "or"  : "01011",
    "and" : "01100",
    "not" : "01101",
    "cmp" : "01110",
    "jmp" : "01111",
    "jlt" : "11100",
    "jgt" : "11101",
    "je"  : "11111",
    "hlt" : "11010",
}
reg = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111",
}
ins_type = {
    "add": 1,
    "sub": 1,
    "mov": 7,
    "ld": 4,
    "st": 4,
    "mul": 1,
    "div": 3,
    "rs": 2,
    "ls": 2,
    "xor": 1,
    "or": 1,
    "and": 1,
    "not": 3,
    "cmp": 3,
    "jmp": 5,
    "jlt": 5,
    "jgt": 5,
    "je": 5,
    "hlt": 6,
    "var":-1
}
var_dec_perm, var_dec_error, input_ovrflw_error, imm_ovrflw_error = 1, 0, 0, 0
l = list(ins.keys()) + ["var"]
jump_lst = ["jmp", "jlt", "jgt", "je"]


def convert_A(s):
    global reg
    global ins
    x = f"{ins[s[0]]}00{reg[s[1]]}{reg[s[2]]}{reg[s[3]]}"
    return x

def convert_B(s):
    global reg
    global ins
    global imm_ovrflw_error
    imm = (str(bin(int(s[2].strip("$"))))).lstrip("0b")
    if len(imm) < 8:
        imm = "0" * (7 - len(imm)) + imm
        x = f"{ins[s[0]]}0{reg[s[1]]}{imm}"
        return x

def convert_C(s):
    global reg
    global ins
    x = f"{ins[s[0]]}00000{reg[s[1]]}{reg[s[2]]}"
    return x

def convert_D(s):
    global reg
    global ins
    global var_dic
    x = f"{ins[s[0]]}0{reg[s[1]]}{var_dic[s[2]]}"
    return x

def convert_E(s):
    global reg
    global ins
    global label_dic
    x = f"{ins[s[0]]}0000{label_dic[s[1]]}"
    return x

def convert_F(s):
    global ins
    x = f"{ins[s[0]]}00000000000"
    return x

func_dic = {
    1: convert_A,
    2: convert_B,
    3: convert_C,
    4: convert_D,
    5: convert_E,
    6: convert_F,
}


def func_call(s):
    t = ins_type[s[0]]
    if (t==7):
        if s[2][0]=="$":
            t=2
        else:
            t=3
            ins["mov"]="00011"
    x = func_dic[t](s)
    ins["mov"]="00010"
    return x

f = open("sample.txt", "r")
data = f.readlines()
f.close()
for i in range(len(data)):
    data[i] = data[i].strip()

data = [i.split() for i in data if i != "" and i != "\n"]

var_dic = {}
count_ = 0
for i in data:
    if i[0] != "var":
        count_ += 1
for i in data:
    if i[0] == "var":
        t = bin(count_)[2:]
        t = "0" * (7 - len(t)) + t
        var_dic[i[1]] = t
        count_ += 1



label_dic = {}  # storing labels in the dictionary
label_freq={}
count_ = 0
for i in range(len(data)):
    if data[i][0][-1] == ":":
        t = bin(count_)[2:]
        t = "0" * (7 - len(t)) + t
        if data[i][0][:-1] not in label_freq:
            label_freq[data[i][0][:-1]] = 0
        label_freq[data[i][0][:-1]] +=1
        label_dic[data[i][0][:-1]] = t
        count_ += 1
    elif data[i][0] != "var":
        count_ += 1
for i in range(len(data)):
    if data[i][0][-1] == ":":
        data[i] = data[i][1:]


f = open("stdout.txt", "w")
if ERRORS(data):
    for i in range(len(data)):
        if data[i][0] != "var":
            x = func_call(data[i])
            if i!=len(data)-1:
                f.write(x + "\n")
            else:
                f.write(x)
