from matplotlib import pyplot
from time import asctime as gettime
import sys

input_function1 = {'10000': 'ADD', '10001': 'SUB', '10110': 'MUL', '11011': 'OR', '11010': 'XOR', '11100': 'AND', "00000": 'ADDF', '00001': 'SUBF'}
typeBfunction = {'10010': 'MOVI', '11001': 'LS', '11000': 'RS', '00010': 'MOVF'}
typeCfunction = {'10011': 'MOVR', '10111': 'DIV', '11101': 'NOT', '11110': 'CMP'}
typeDfunction = {'10100': 'LD', '10101': 'ST'}
input_function3 = {'11111': 'JMP', '01100': 'JLT', '01101': 'JGT', '01111': 'JE'}
all_function =  {'11111': 'JMP', '01100': 'JLT', '01101': 'JGT', '01111': 'JE', '10010': 'MOVI', '10011': 'MOVR', '10100': 'LD', '10101': 'ST', '10111': 'DIV', '11001': 'LS', '11000': 'RS', '11101': 'NOT', '11110': 'CMP', '10000': 'ADD', '10001': 'SUB', '10110': 'MUL', '11011': 'OR', '11010': 'XOR', '11100': 'AND'}
register_address = {'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3', '100': 'R4', '101': 'R5', '110': 'R6'}
register_value = ["0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000", "0000000000000000"]
HLT = "0101000000000000"
flagRegisterValue = {'V': 0, 'G': 0, 'L': 0, 'E': 0}

function_stucture = {"A" : {'opcode' : 5, 'unused' : 2, 'reg1' : 3, 'reg2' : 3, 'reg3' : 3},
"B" : {'opcode' : 5, 'reg1': 3, 'imm' : 8},
"C" : {'opcode' : 5, 'unused' : 5, 'reg1' : 3, 'reg2' : 3},
"D" : {'opcode' : 5, "reg1" : 3, 'mem' : 8},
"E" : {'opcode' : 5, 'unused' : 3, 'mem' : 8}}
maximum_number_stored = 255
clock_cycle = []
clockcycle = 0
memory_address = []

input_instruction = []
number_of_line = 0
try:
    for i in sys.stdin:
        i = i.strip()
        if i != []:
            number_of_line += 1
            input_instruction.append(i)
except:
    pass

for i in range(number_of_line, 256):
    input_instruction.append("0000000000000000")

def lengthbitfixer(argument, a):
    return f"{'0' * (a - len(argument))}{argument}"

def printformat():
    flag16bit = f"{'0' * 12}{flagRegisterValue['V']}{flagRegisterValue['L']}{flagRegisterValue['G']}{flagRegisterValue['E']}"
    print(lengthbitfixer(bin(PC)[2:], 8), register_value[0], register_value[1], register_value[2], register_value[3], register_value[4], register_value[5], register_value[6], flag16bit)

def flagreset():
    for i in flagRegisterValue:
        flagRegisterValue[i] = 0

def decimaltocustomIEEE(immediate):
    if 0.125 <= immediate <= 31.5:
        integral = int(immediate)
        answer = bin(integral)[2:]
        exponent = len(answer) - 1
        precision = 6
        tmp = ''
        fractal = immediate - integral
        if answer[0] == '0':
            answer = answer[1:]
            digit = 0
            while digit == 0:
                if exponent == -3:
                    return False
                exponent -= 1
                fractal *= 2
                digit = int(fractal)
            answer += '1'
            fractal -= 1
        precision = precision - len(answer)
        while precision > 0:
            fractal *= 2
            digit = int(fractal)
            tmp += str(digit)
            precision -= 1
            fractal -= digit
        exponent = bin(exponent + 3)[2:]
        tmp = '0' * (3 - len(exponent)) + exponent + answer[1:] + str(tmp)
        return tmp
    else:
        return False

def customIEEEtodecimal(binary):
    exponent = int(binary[:3], 2) - 3
    mantissa = binary[3:]
    number = 1
    j = -1
    for i in mantissa:
        number += (2 ** j) * int(i)
        j -= 1
    number *= 2 ** exponent
    return number

def typeAinstructionfunction(function, register):
    reg1 = register_value[int(register[:3], 2)][-8]
    reg2 = register_value[int(register[3:6], 2)][-8]
    if function == 'ADDF':
        tmp = customIEEEtodecimal(reg1) + customIEEEtodecimal(reg2)
        temp = decimaltocustomIEEE(tmp)
        if temp == False:
            flagRegisterValue['V'] = 1
            register_value[int(register[6:], 2)] = '0' * 16
        else:
            register_value[int(register[6:], 2)] = ('0' * 8) + temp
        return
    elif function == 'SUBF':
        tmp = customIEEEtodecimal(reg1) - customIEEEtodecimal(reg2)
        temp = decimaltocustomIEEE(tmp)
        if temp == False:
            flagRegisterValue["V"] = 1
            register_value[int(register[6:], 2)] = "0" * 16
        else:
            register_value[int(register[6:], 2)] = ('0' * 8) + temp
        return
    reg1 = int(register_value[int(register[:3], 2)], 2)
    reg2 = int(register_value[int(register[3:6], 2)], 2)
    if function == "ADD":
        tmp = reg1 + reg2
    elif function == "SUB":
        tmp = reg1 - reg2
    elif function == "MUL":
        tmp = reg1 * reg2
    elif function == "OR":
        tmp = reg1 | reg2
    elif function == "XOR":
        tmp = reg1 ^ reg2
    elif function == "AND":
        tmp = reg1 & reg2
    if tmp < 0:
        tmp = 0
        flagRegisterValue['V'] = 1
    elif tmp > 255:
        tmp = 255
        flagRegisterValue['V'] = 1
    register_value[int(register[6:], 2)] = lengthbitfixer(bin(tmp)[2:], 16)

def typeBinstructionfunction(function, value):
    if function == 'MOVI' or function == 'MOVF':
        register_value[int(value[:3], 2)] = lengthbitfixer(value[3:], 16)
    elif function == 'LS':
        register_value[int(value[:3], 2)] = lengthbitfixer(bin(int(register_value(value[:3]), 2) << int(value[3:], 2))[2:][-16:], 16)
    elif function == 'RS':
        register_value[int(value[:3], 2)] = lengthbitfixer(bin(int(register_value(value[:3]), 2) >> int(value[3:], 2))[2:][-16:], 16)


def typeCinstructionfunction(function, value):
    reg1 = int(value[:3], 2)
    reg2 = int(value[3:], 2)
    if function == 'MOVR':
        register_value[reg2] = register_value[reg1]
    elif function == 'DIV':
        register_value[1] = lengthbitfixer(bin(register_value[reg1] % register_value[reg2]), 16)
        register_value[0] = lengthbitfixer(bin(register_value[reg1] // register_value[reg2]), 16)
    elif function == 'NOT':
        register_value[reg2] = ''.join('1' if i == '0' else '0' for i in register_value[reg1])
    elif function == 'CMP':
        if int(register_value[reg1], 2) == int(register_value[reg2], 2):
            flagRegisterValue['E'] = 1
        elif int(register_value[reg1], 2) > int(register_value[reg2], 2):
            flagRegisterValue['G'] = 1
        else:
            flagRegisterValue['L'] = 1

def typeDinstructionfunction(function, value):
    memmory = int(value[3:], 2)
    clock_cycle.append(PC)
    memory_address.append(memmory)
    if function == 'LD':
        register_value[int(value[:3], 2)] = input_instruction[memmory]
    elif function == 'ST':
        input_instruction[memmory] = register_value[int(value[:3], 2)]

def typeEinstructionfunction(function, address):
    memmory = int(address, 2)
    memory_address.append(memmory)
    clock_cycle.append(PC)
    nextpointer = PC + 1
    if function == "JMP":
        nextpointer = memmory
    elif function == "JLT":
        if flagRegisterValue['L'] == 1:
            nextpointer = memmory
    elif function == "JGT":
        if flagRegisterValue['G'] == 1:
            nextpointer = memmory
    elif function == "JE":
        if flagRegisterValue['E'] == 1:
            nextpointer = memmory
    return nextpointer

PC = 0
instruction = input_instruction[0]
recursion = 0
while (instruction != HLT):
    clock_cycle.append(clockcycle)
    memory_address.append(PC)
    nextpointer = PC + 1
    opcode = instruction[:5]
    if opcode in input_function3:
        nextpointer = typeEinstructionfunction(all_function[opcode], instruction[8:])
    flagreset()
    if opcode in input_function1:
        typeAinstructionfunction(all_function[opcode], instruction[7:])
    elif opcode in typeBfunction:
        typeBinstructionfunction(all_function[opcode], instruction[5:])
    elif opcode in typeCfunction:
        typeCinstructionfunction(all_function[opcode], instruction[10:])
    elif opcode in typeDfunction:
        typeDinstructionfunction(all_function[opcode], instruction[5:])
    printformat()
    PC += 1
    if nextpointer != PC:
        PC = nextpointer
    if recursion > 999:
        print(f"maximum recursion depth exceeded[line exceed {recursion}]")
        break
    instruction = input_instruction[PC]
    clockcycle += 1
    recursion += 1

printformat()
clock_cycle.append(clockcycle)
memory_address.append(PC)
for i in input_instruction:
    print(i)
print()
pyplot.scatter(clock_cycle, memory_address)
pyplot.xlabel("clock cycle")
pyplot.ylabel("memory address")
pyplot.savefig(f"{gettime()}")
pyplot.close()
