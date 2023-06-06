fin = open("hard/test5", "r")
bin_in = fin.readlines()
for i in range(len(bin_in)):
    #if i != len(bin_in) - 1:
        bin_in[i] = bin_in[i][:-1]
reg_dic = {
    "R0": 0,
    "R1": 0,
    "R2": 0,
    "R3": 0,
    "R4": 0,
    "R5": 0,
    "R6": 0,
    "FLAGS": "0000000000000000",
}
mem = ["0000000000000000"] * 128
pc = 0
ins = {
    "add": "00000",
    "sub": "00001",
    "mov": "00010",
    "ld": "00100",
    "st": "00101",
    "mul": "00110",
    "div": "00111",
    "rs": "01000",
    "ls": "01001",
    "xor": "01010",
    "or": "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "11100",
    "jgt": "11101",
    "je": "11111",
    "hlt": "11010",
}
binary_ins = {}
for i in ins:
    binary_ins[ins[i]] = i


# op functions
def add(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] + reg_dic[sr2]
    if (reg_dic[dr]>2**16):
        reg_dic["FLAGS"]=list(reg_dic["FLAGS"])
        reg_dic["FLAGS"][-4]="1"
        reg_dic["FLAGS"]="".join(reg_dic["FLAGS"])
        reg_dic[dr]=0



def sub(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] - reg_dic[sr2]
    if (reg_dic[sr2]>reg_dic[sr1]):
        reg_dic[dr]=0
        reg_dic["FLAGS"]=list(reg_dic["FLAGS"])
        reg_dic["FLAGS"][-4]="1"
        reg_dic["FLAGS"]="".join(reg_dic["FLAGS"])
    else:
        reg_dic[dr]=reg_dic[sr1]-reg_dic[sr2]


def mul(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] * reg_dic[sr2]
    if (reg_dic[dr]>2**16):
        reg_dic["FLAGS"]=list(reg_dic["FLAGS"])
        reg_dic["FLAGS"][-4]="1"
        reg_dic["FLAGS"]="".join(reg_dic["FLAGS"])
        reg_dic[dr]=0


def xor(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] ^ reg_dic[sr2]


def orfunc(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] | reg_dic[sr2]


def andfunc(s):
    global reg_dic
    dr = f"R{int(s[7:10],2)}"
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    reg_dic[dr] = reg_dic[sr1] & reg_dic[sr2]


def mov(s):
    global reg_dic
    dr = f"R{int(s[6:9],2)}"
    imm = int(s[9:16], 2)
    reg_dic[dr] = imm


def mov_(s):
    global reg_dic
    dr=f"R{int(s[10:13],2)}"
    sr=f"R{int(s[13:16],2)}"
    if (sr=="R7"):
        sr="FLAGS"
        reg_dic[dr]=int(reg_dic[sr], 2)
    else:
        reg_dic[dr]=reg_dic[sr]


def divide(s):
    global reg_dic
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    if reg_dic[sr2] == 0:
        reg_dic["FLAGS"] = list(reg_dic["FLAGS"])
        reg_dic["FLAGS"][-4] = "1"
        reg_dic["FLAGS"] = "".join(reg_dic["FLAGS"])
        reg_dic["R0"] = 0
        reg_dic["R1"] = 0
    else:
        q = reg_dic[sr1] // reg_dic[sr2]
        r = reg_dic[sr1] % reg_dic[sr2]
        reg_dic["R0"] = q
        reg_dic["R1"] = r


def notfunc(s):
    global reg_dic
    dr = f"R{int(s[10:13],2)}"
    sr = f"R{int(s[13:16]),2}"
    reg_dic[dr] = ~reg_dic[sr]


def cmp(s):
    global reg_dic
    sr1 = f"R{int(s[10:13],2)}"
    sr2 = f"R{int(s[13:16],2)}"
    if reg_dic[sr1] > reg_dic[sr2]:
        x = 2
    elif reg_dic[sr1] < reg_dic[sr2]:
        x = 3
    elif reg_dic[sr1] == reg_dic[sr2]:
        x = 1
    reg_dic["FLAGS"] = list(reg_dic["FLAGS"])
    reg_dic["FLAGS"][-x] = "1"
    reg_dic["FLAGS"] = "".join(reg_dic["FLAGS"])


def st(s):
    global reg_dic
    sr = f"R{int(s[6:9],2)}"
    i = int(s[9:16],2)
    val = reg_dic[sr]
    val = bin(val)[2:]
    val = val.zfill(16)
    mem[i] = val


def ld(s):
    global reg_dic
    dr = f"R{int(s[6:9],2)}"
    i = int(s[9:16],2)
    val = mem[i]
    val = int(val, 2)
    reg_dic[dr] = val


def jmp(s):
    global reg_dic, pc
    i = int(s[9:16],2)
    pc = i


def jlt(s):
    global reg_dic, pc
    if reg_dic["FLAGS"][13] == "1":
        i = int(s[9:16],2)
        pc = i


def jgt(s):
    global reg_dic, pc
    if reg_dic["FLAGS"][14] == "1":
        i = int(s[9:16],2)
        pc = i


def je(s):
    global reg_dic, pc
    if reg_dic["FLAGS"][15] == "1":
        i = int(s[9:16],2)
        pc = i

def ls(s):
    global reg_dic,pc
    dr = f"R{int(s[6:9],2)}"
    imm = int(s[9:16], 2)
    v=reg_dic[dr]
    b_val = bin(v)[2:].zfill(16)
    b_ret = ['0']*16
    for i in range(16):
        if i + imm < 16:
            b_ret[i] = b_val[i + imm]
    b_ret="".join(b_ret)
    reg_dic[dr] = int(b_ret,2)

def rs(s):
    global reg_dic,pc
    dr = f"R{int(s[6:9],2)}"
    imm = int(s[9:16], 2)
    v=reg_dic[dr]
    b_val = bin(v)[2:].zfill(16)
    b_ret = ['0']*16
    for i in range(16):
        if i<imm:
            b_ret[i]="0"
        else:
            b_ret[i] = b_val[i-imm]
    b_ret="".join(b_ret)
    reg_dic[dr] = int(b_ret,2)



opc = {
    "00000": add,
    "00001": sub,
    "00010": mov,
    "00011": mov_,
    "00100": ld,
    "00101": st,
    "00110": mul,
    "00111": divide,
    "01000": rs,
    "01001": ls,
    "01010": xor,
    "01011": orfunc,
    "01100": andfunc,
    "01101": notfunc,
    "01110": cmp,
    "01111": jmp,
    "11100": jlt,
    "11101": jgt,
    "11111": je,
    "11010": "hlt",
}
def pc_dump(pc,f):
    bin_pc=bin(pc)[2:].zfill(7)
    f.write(bin_pc+"        ")
def rf_dump(reg,f):
    r0=bin(reg["R0"])[2:].zfill(16)
    r1=bin(reg["R1"])[2:].zfill(16)
    r2=bin(reg["R2"])[2:].zfill(16)
    r3=bin(reg["R3"])[2:].zfill(16)
    r4=bin(reg["R4"])[2:].zfill(16)
    r5=bin(reg["R5"])[2:].zfill(16)
    r6=bin(reg["R6"])[2:].zfill(16)
    flag=reg["FLAGS"]
    f.write(f"{r0} {r1} {r2} {r3} {r4} {r5} {r6} {flag}\n")
def memory_dump(mem):
    for i in range(len(mem)):
        f.write(f"{mem[i]}")
        if (i!=len(mem)-1):
            f.write("\n")
for i in range(len(bin_in)):
    mem[i] = bin_in[i]
f=open("stdout.txt","w")
print (len(bin_in))
while pc < 128 and pc < len(bin_in):
    pc_orginal=pc
    opcode = mem[pc][:5]
    pc_dump(pc_orginal,f)
    if opc[opcode]!="hlt":
        opc[opcode](mem[pc])
    rf_dump(reg_dic,f)
    if pc==pc_orginal:
        pc+=1
    if opc[opcode]=="hlt":
        break
memory_dump(mem)
f.close()
count_ = 0
