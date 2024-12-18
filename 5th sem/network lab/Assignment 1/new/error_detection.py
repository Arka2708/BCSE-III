from math import remainder
from pickle import FALSE
from calculator import *
import random

def inject_error(dataword,size):
    # Simulate error injection by randomly flipping a bit
    index = random.randint(0,size)
    bit = dataword[index]
    dataword = dataword[:index] + str(1 - int(bit)) + dataword[index+1:]
    return dataword

class CheckSum:  
    @staticmethod
    def encode(frames, dataWordFrameSize:int):
        # Iterate over the frames to calculate the checksum
        tmp = frames[0]
        for frame in frames[1:]:
           tmp = addBinaryStringUsingOnesComplement(tmp, frame)

        # Complement and get checksum
        checksum = complementOfBinaryString(tmp)
        print("Checksum for Sender site:", checksum)

        #  Inject some errors and append the checksum to each dataword
        l = random.randint(0, len(frames)-1)
        frames[l]=inject_error(frames[l],dataWordFrameSize)
        frames.append(checksum)
        return frames

    @staticmethod
    def decode(frames, dataWordFrameSize:int):
        errorFound = False
        # Iterate over the frames to calculate the checksum and verify 
        tmp = frames[0]
        for frame in frames[1:]:
           tmp = addBinaryStringUsingOnesComplement(tmp, frame)
            
        # Complement and get checksum
        checksum = complementOfBinaryString(tmp)
        print("Checksum for Receiver site:", checksum)
        if checksum == "0"*dataWordFrameSize:
            errorFound = False
        else:
            errorFound = True
        return errorFound

class CRC:
    @staticmethod
    def encode(frames, divisor: str):
        output = []
        for i in range(len(frames)):
            codeword = CRC.encodeData(frames[i], divisor)
            output.append(codeword)

        l = random.randint(0, len(frames) - 1)
        output[l] = inject_error(output[l], len(output[0]))
        return output

    @staticmethod
    def encodeData(data, key):
        l_key = len(key)
        # Appends n-1 zeroes at the end of data
        appended_data = data + '0' * (l_key - 1)
        remainder = divisionCRC(appended_data, key)
        print("Reamainder: "+remainder)
        # Append remainder in the original data
        codeword = data + remainder
        return codeword

    @staticmethod
    def decode(frames, divisor:str):
        datawords = []
        num=0
        for i in range(len(frames)):
            dataword, error = CRC.decodeData(frames[i], divisor)
            datawords.append(dataword)
            if error:
                num += 1
        return datawords,num

    @staticmethod
    def decodeData(data, key):
        remainder = divisionCRC(data, key)
        if all(bit == '0' for bit in remainder):
            print("Remainder is " + remainder + "-->NO ERROR")
            return data[:-(len(key)-1)], False
        else:
            print("Remainder is " + remainder + "-->ERROR DETECTED")
            return data[:-(len(key)-1)], True