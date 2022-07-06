import sys
input_function1 = {'ADD': '10000', 'SUB': '10001', 'MUL': '10110', 'OR': '11011', 'XOR': '11010', 'AND': '11100'}
input_function2 = {'MOVI': '10010', 'MOVR': '10011', 'LD': '10100', 'ST': '10101', 'DIV': '10111', 'LS': '11001', 'RS': '11000', 'NOT': '11101', 'CMP': '11110'}
input_function3 = {'JMP': '11111', 'JLT': '01100', 'JGT': '01101', 'JE': '01111'}
all_function = {'JMP': '11111', 'JLT': '01100', 'JGT': '01101', 'JE': '01111', 'MOVI': '10010', 'MOVR': '10011', 'LD': '10100', 'ST': '10101', 'DIV': '10111', 'LS': '11001', 'RS': '11000', 'NOT': '11101', 'CMP': '11110', 'ADD': '10000', 'SUB': '10001', 'MUL': '10110', 'OR': '11011', 'XOR': '11010', 'AND': '11100'}
register_value = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011', 'R4': '100', 'R5': '101', 'R6': '110'}
HLT = '01010'
FLAGS = '111'

function_stucture = {'A' : {'opcode' : 5, 'unused' : 2, 'reg1' : 3, 'reg2' : 3, 'reg3' : 3},
'B' : {'opcode' : 5, 'reg1': 3, 'imm' : 8},
"C" : {'opcode' : 5, 'unused' : 5, 'reg1' : 3, 'reg2' : 3},
'D' : {'opcode' : 5, "reg1" : 3, 'mem' : 8},
"E" : {'opcode' : 5, 'unused' : 3, 'mem' : 8}}
maximum_number_stored = 255

# A = {'ADD': '10000', 'SUB': '10001', 'MUL': '10110', 'OR': '11011', 'XOR': '11010', 'AND': '11100'}
# B = {'MOVI': '10010', 'LS': '11001', 'RS': '11000'}   
# C = {'MOVR': '10011', 'DIV': '10111', 'NOT': '11101', 'CMP': '11110'}
# D = {'LD': '10100', 'ST': '10101'}
# E = {'JMP': '11111', 'JLT': '01100', 'JGT': '01101', 'JE': '01111'}

input_instruction = []
number_of_line = 0
try:
    for i in sys.stdin:
        i = i.strip().upper().split()
        if i != []:
            input_instruction.append(i)
except:
    pass

var = []
label = {}
result = []
universal_flag = True

def errorformat(error, n):
    print(f"ERROR {error} in line number {n}")

def label_check(input_instruction, line_num):
    if input_instruction[line_num][0][-1] != ":":
        return False
    if input_instruction[line_num][0][0].isdigit() == False:
        label[input_instruction[line_num][0][:-1]] = bin(line_num).removeprefix("0b")
        input_instruction[line_num].pop(0)
    else:
        return True
    if(len(input_instruction[line_num]) < 1):
        return True
    else:
        label_check(input_instruction, line_num)

line_number = len(input_instruction)
tmp = 0
for i in range(line_number):
    tmp += 1
    if label_check(input_instruction, i):
        errorformat("label is not defined correctly", tmp)
        universal_flag = False
        break

if input_instruction[-1] == ["HLT"]:
    input_instruction.pop()
else:
    print("hlt not being used as the last instruction")
    universal_flag = False

flag = True
tmp = 0
while flag and universal_flag:
    tmp += 1
    if len(input_instruction) and input_instruction[0][0] == "VAR":
        if (len(input_instruction[0]) == 2) and input_instruction[0][1][0].isdigit() == False and input_instruction[0][1].isalnum():
            line_number -= 1
            var.append(input_instruction[0][1])
            input_instruction.pop(0)
        else:
            errorformat("var is not defined", tmp)
            universal_flag = False
            flag = False
    else:
        flag = False

if line_number > maximum_number_stored + 1:
    print(f"length of code is exceed {maximum_number_stored}")
    universal_flag = False

var_location = {}
tmp = line_number
for i in var:
    tmp += 1
    var_location[i] = bin(tmp).removeprefix('0b')

def length_fixer(strig, num):
    return f"{(num - len(strig)) * '0'}{strig}"

def func_checker(function, lis):
    if function in lis:
        return True
    return False

tmp = 0
for i in input_instruction:
    tmp += 1
    if i[0] == "VAR":
        errorformat("var is used in middle", tmp)
    elif len(i) == 2 and func_checker(i[0], input_function3):
        if i[1] in label:
            result.append(f"{all_function[i[0]]}000{length_fixer(label[i[1]], function_stucture['E']['mem'])}")
        elif i[1].isdigit() and int(i[1], 2) <= maximum_number_stored:
            result.append(f"{all_function[i[0]]}000{length_fixer(i[1], function_stucture['E']['mem'])}")
        else:
            errorformat("use of undefined label", tmp)
            universal_flag = False
            break
    elif len(i) == 4 and func_checker(i[0], input_function1):
        for j in i[1:]:
            if j not in register_value:
                universal_flag = False
                errorformat("invalid register is used", tmp)
                break
        if universal_flag:
            result.append(f"{all_function[i[0]]}00{register_value[i[1]]}{register_value[i[2]]}{register_value[i[3]]}")
    elif i[0] == 'MOV':
        if i[1] in register_value:
            if i[-1][0] == '$':
                if i[-1][1:].isdigit() == True and int(i[-1][1:]) <= maximum_number_stored:
                    result.append(f"{all_function['MOVI']}{register_value[i[1]]}{length_fixer(bin(int(i[-1][1:]))[2:], 8)}")
                else:
                    errorformat("invalid number is used", tmp)
                    universal_flag = False
                    break
            elif i[-1] in register_value:
                result.append(f"{all_function['MOVR']}00000{register_value[i[1]]}{register_value[i[-1]]}")
            elif i[-1] == 'FLAGS':
                result.append(f"{all_function['MOVR']}00000{register_value[i[1]]}{FLAGS}")
            else:
                universal_flag = False
                errorformat("illegal use of register", tmp)
                break
        else:
            universal_flag = False
            errorformat("invalid use of register", tmp)
            break
    elif len(i) == 3 and func_checker(i[0], input_function2):
        if i[1] in register_value:
            if i[-1][0] == '$':
                if int(i[-1][1:]) <= maximum_number_stored and i[-1][1:].isdigit():
                    result.append(f"{all_function[i[0]]}{register_value[i[1]]}{length_fixer(bin(int(i[2][1:])).removeprefix('0b'), function_stucture['B']['imm'])}")
                else:
                    errorformat("value is invalid", tmp)
                    universal_flag = False
                    break     
            elif i[-1] in register_value:
                result.append(f"{all_function[i[0]]}00000{register_value[i[1]]}{register_value[i[-1]]}")
            elif i[-1] in var_location:
                result.append(f"{all_function[i[0]]}{register_value[i[1]]}{length_fixer(var_location[i[-1]], function_stucture['D']['mem'])}")
            elif i[-1].isdigit() and int(i[-1][:], 2) <=maximum_number_stored:
                result.append(f"{all_function[i[0]]}{register_value[i[1]]}{length_fixer(i[2], function_stucture['D']['mem'])}")
            else:
                errorformat("invalid register is used", tmp)
                universal_flag = False
                break
        else:
            errorformat("invalid register is used", tmp)
            universal_flag = False
            break
    else:
        errorformat("invalid function is used", tmp)
        universal_flag = False
        break
result.append('0101000000000000')
if universal_flag:
    for i in result:
        print(i)
