fin=open("stdin.txt", "r")
bin_in=fin.readlines()
for i in range(len(bin_in)):
    if i!=len(bin_in)-1:
        bin_in[i]=bin_in[i][:-1]
reg_dic={"R0":0,"R1":0,"R2":0,"R3":0,"R4":0,"R5":0,"R6":0,"FLAGS":"0000000000000000"}
mem=["0000000000000000"]*128
pc=0
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
binary_ins={}
for i in ins:
    binary_ins[ins[i]]=i
#op functions
def add(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1]+reg_dic[sr2]

def sub(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1]-reg_dic[sr2]

def mul(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1]*reg_dic[sr2]

def xor(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1]^reg_dic[sr2]

def orfunc(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1] | reg_dic[sr2]

def andfunc(s):
    global reg_dic
    dr=f"R{int(s[7:10])}"
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr1] & reg_dic[sr2]

def mov(s):
    global reg_dic
    dr=f"R{int(s[6:9])}"
    imm= int(s[9:16], 2)
    reg_dic[dr]=imm

def mov_(s):
    global reg_dic
    dr=f"R{int(s[10:13])}"
    sr=f"R{int(s[13:16])}"
    reg_dic[dr]=reg_dic[sr]

def divide(s):
    global reg_dic
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    if (reg_dic[sr2]==0):
        reg_dic["FLAGS"]=list(reg_dic["FLAGS"])
        reg_dic["FLAGS"][-4]="1"
        reg_dic["FLAGS"]="".join(reg_dic["FLAGS"])
        reg_dic["R0"]=0
        reg_dic["R1"]=0
    else:
        q=reg_dic[sr1]//reg_dic[sr2]
        r=reg_dic[sr1]%reg_dic[sr2]
        reg_dic["R0"]=q
        reg_dic["R1"]=r

def notfunc(s):
    global reg_dic
    dr=f"R{int(s[10:13])}"
    sr=f"R{int(s[13:16])}"
    reg_dic[dr]=~reg_dic[sr]

def cmp(s):
    global reg_dic
    sr1=f"R{int(s[10:13])}"
    sr2=f"R{int(s[13:16])}"
    if (reg_dic[sr1]>reg_dic[sr2]):
        x=2
    elif (reg_dic[sr1]<reg_dic[sr2]):
        x=3
    elif (reg_dic[sr1]==reg_dic[sr2]):
        x=1
    reg_dic["FLAGS"]=list(reg_dic["FLAGS"])
    reg_dic["FLAGS"][-x]="1"
    reg_dic["FLAGS"]="".join(reg_dic["FLAGS"])

def st(s):
    global reg_dic
    sr=f"R{int(s[6:9])}"
    i=f"R{int(s[9:16])}"
    i=int(i, 2)
    val=reg_dic[sr]
    val=bin(val)[2:]
    val=val.zfill(16)
    mem[i]=val

def ld(s):
    global reg_dic
    dr=f"R{int(s[6:9])}"
    i=f"R{int(s[9:16])}"
    i=int(i, 2)
    val=mem[i]
    val=int(val, 2)
    reg_dic[dr]=val

def jmp(s):
    global reg_dic, pc
    i=f"R{int(s[9:16])}"
    i=int(i, 2)
    pc=i

def jlt(s):
    global reg_dic, pc
    if (reg_dic["FLAGS"][13]==1):
        i=f"R{int(s[9:16])}"
        i=int(i, 2)
        pc=i

def jgt(s):
    global reg_dic, pc
    if (reg_dic["FLAGS"][14]==1):
        i=f"R{int(s[9:16])}"
        i=int(i, 2)
        pc=i

def je(s):
    global reg_dic, pc
    if (reg_dic["FLAGS"][15]==1):
        i=f"R{int(s[9:16])}"
        i=int(i, 2)
        pc=i


for i in range(len(bin_in)):
    mem[i]=bin_in[i]
while(pc<128 and pc<len(bin_in)):
    opcode=mem[pc][:5]
count_=0
