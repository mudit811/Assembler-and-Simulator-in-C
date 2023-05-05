reg={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
ins={"add":"0000","sub":"0001"}

var_dec_perm, var_dec_error, input_ovrflw_error, imm_ovrflw_error=1,0,0,0

#add filler bits to each type

def convert_A(s):
   global reg
   global ins
   x= f"{ins[s[0]]}{reg[s[1]]}{reg[s[2]]}{reg[s[3]]}"
   return(x)

def convert_B(s):
    global reg
    global ins
    global imm_ovrflw_error
    imm=(str(bin(int(s[2].strip("$"))))).strip("0b")
    if len(imm)<8:
        imm="0"*(7-len(imm))+imm
        x=f"{ins[s[0]]}{reg(s[1])}{imm}"
        return(x)
    else:
        imm_ovrflw_error=1
        return("Overflow Error: Imm Value Exceeds 7 bits")

def convert_C(s):
    global reg
    global ins
    x= f"{ins[s[0]]}{reg[s[1]]}{reg[s[2]]}"

def convert_D(s):   #incomplete        #memory address allocation to variables not done yet
    global reg
    global ins

def convert_D(s):   #incomplete        #memory address allocation to variables not done yet
    global reg
    global ins


stdin=open("stdin.txt", "r")
ass_int=stdin.readlines()
var_lst=[]
num_int=len(ass_int)
i=0

if num_int>128:
    intovrflw_error=1

while i<num_int:
    if ass_int[i]=='\n':
        x=ass_int.pop(i)
        num_int-=1
    else:
        ass_int[i]=ass_int[i].strip("\n")
        ass_int[i]=ass_int[i].split()
        if ass_int[i][0]=="var":
            if var_dec_perm==0:
                print("Variable Declaration error")
                var_dec_error=0
                break
            else:
                x=ass_int.pop(i)
                var_lst.append(x)
                i-=1
                num_int-=1
        else:
            var_dec_perm=0
        i+=1


print(ass_int)
print(var_lst)
print(num_int)
