def buildFrames(input, frameSize):
    output = []
    for i in range(0, len(input), frameSize):
        output.append(input[i:i+frameSize])
    return output

def addBinaryStringUsingOnesComplement(a, b):
    max_len = max(len(a), len(b))
    a = a.zfill(max_len)
    b = b.zfill(max_len)
    result = ''
    carry = 0
    # Traverse the string
    for i in range(max_len - 1, -1, -1):
        r = carry
        r += 1 if a[i] == '1' else 0
        r += 1 if b[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        # Compute the carry.
        carry = 0 if r < 2 else 1
    if carry != 0:
        result = addBinaryStringUsingOnesComplement(result, '1')
    return result.zfill(max_len)

def complementOfBinaryString(input:str):
    input = list(input)
    for i in range(len(input)):
        if input[i] == '0':
            input[i] = '1'
        else:
            input[i] = '0'
    return ''.join(input)

def xor(a, b):
    # Initialize result
    result = []
    # Traverse all bits, if bits are same, then XOR is 0, else 1
    for i in range( len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)

def divisionCRC(dividend: str, divisor: str):
    # Number of bits to be XORed at a time.
    pick = len(divisor)

    while pick <= len(dividend):
        if dividend[0] == '1':
            tmp = xor(divisor, dividend[0:pick]) 
        else:
            tmp = xor('0' * pick, dividend[0:pick])
        if pick == len(dividend):
            return tmp[1:]
        dividend = tmp[1:] + dividend[pick:]


