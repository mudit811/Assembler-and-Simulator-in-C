stdin=open("stdin.txt", "r")
ass_int=stdin.readlines()
var_lst=[]
num_int=len(ass_int)
i=0
var_dec_perm, input_ovrflw_error=1,0
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
