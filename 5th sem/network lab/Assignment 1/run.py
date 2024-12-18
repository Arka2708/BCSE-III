from sender import Sender
from receiver import Receiver
from error_injection import injectRandomError, injectSpecificError
import random

# Function to generate random sequence of 0s and 1s and store it in a file
def generateRandomInput(length, filename):
    with open(filename, "w") as fileout:
        for i in range(length):
            fileout.write(str(random.randint(0, 1)))
    # Optionally, print the generated binary data
    with open(filename, "r") as filein:
        data = filein.read()
        print("Generated Binary Data:")
        print(data)

def case1(sender):
    puterror = True
    print("Error is detected by CRC & Checksum schemes.")
    print("-------------- Checksum ------------------------------------")
    type = 1
    s = sender
    s.createFrames("input.txt", type)
    s.displayFrames(type)
    if puterror:
        s.codeword = injectRandomError(s.codeword)
    r = Receiver(s)
    r.checkError(1)
    r.displayFrames(type)

    print("-------------- Cyclic Redundancy Check ---------------------")
    type = 2
    poly = input("Enter Generator Polynomial: ")
    s = sender
    s.createFrames("input.txt", type, poly)
    s.displayFrames(type)
    if puterror:
        s.codeword = injectRandomError(s.codeword)
    r = Receiver(s)
    r.checkError(2, poly)
    r.displayFrames(type)

    print("------------------------------------------------------------\n")

def case2(sender):
    print("--------------------------- CASE 2 -------------------------")
    print("Error is detected by checksum but not by CRC.")
    print("-------------- Checksum ------------------------------------")
    type = 1
    s = sender
    s.createFrames("input.txt", type)
    s.displayFrames(type)
    zeropos = []
    onepos = [[5]]
    s.codeword = injectSpecificError(s.codeword, zeropos, onepos)
    r = Receiver(s)
    r.checkError(type)
    r.displayFrames(type)
    print("-------------- Cyclic Redundancy Check ---------------------")
    type = 2
    poly = "1001"
    print("Generator Polynomial:", poly)
    s = sender
    s.createFrames("input.txt", type, poly)
    s.displayFrames(type)
    s.codeword = injectSpecificError(s.codeword, zeropos, onepos)
    r = Receiver(s)
    r.checkError(type, poly)
    r.displayFrames(type)
    print("------------------------------------------------------------\n")


def case3(sender):
    puterror = True
    print("--------------------------- CASE 3 -------------------------")
    print("Error is detected by CRC but not by Checksum.")
    print("-------------- Cyclic Redundancy Check ---------------------")
    type = 2
    poly = "100"
    print("Generator Polynomial:", poly)
    s = sender
    s.createFrames("input.txt", type, poly)
    s.displayFrames(type)
    zeropos = []
    onepos = [[5]]
    s.codeword = injectSpecificError(s.codeword, zeropos, onepos)
    r = Receiver(s)
    r.checkError(type, poly)
    r.displayFrames(type)

    print("-------------- Checksum ------------------------------------")
    type = 1
    s = sender
    s.createFrames("input.txt", type)
    s.displayFrames(type)
    if puterror:
        s.codeword = injectRandomError(s.codeword)
    r = Receiver(s)
    r.checkError(type)
    r.displayFrames(type)

def main(case):
    if case == 1:
        size = int(input("Enter length of the dataword: "))
        generateRandomInput(size * 4, "input.txt")
        s = Sender(size)
        case1(s)  # Call case1 function passing the sender object

    elif case == 2:
        size = 8
        s = Sender(size)
        case2(s)  # Call case2 function passing the sender object

    elif case == 3:
        size = 6
        s = Sender(size)
        case3(s)  # Call case3 function passing the sender object

    else:
        print("You entered an invalid choice.")

if __name__ == "__main__":
    print("------------------------------------------------------------")
    print("1. Error is detected by both schemes.")
    print("2. Error is detected by checksum but not by CRC.")
    print("3. Error is detected by CRC but not by Checksum.")
    case = int(input("Enter Case Number : "))
    main(case)