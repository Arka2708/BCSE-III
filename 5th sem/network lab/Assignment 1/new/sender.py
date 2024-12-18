import random
import socket
import time
from error_detection import *

def generate_random_input(length, filename):
    with open(filename, "w") as fileout:
        for i in range(length):
            fileout.write(str(random.randint(0, 1)))
    # Optionally, print the generated binary data
    with open(filename, "r") as filein:
        data = filein.read()
        print("Generated Binary Data:")
        print(data)
    return data

def send_through_socket(codewords):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_address, server_port))
    try:
        print("Connection established")
        for codeword in codewords:
            s.send(codeword.encode())
            print("Sender: Codeword sent to Receiver.")
            time.sleep(0.1)  # Add a short delay to allow the receiver to process the data
        s.send("END".encode())  # Send the termination signal
    finally:
        print('Closing socket')
        s.close()

if __name__ == "__main__":
    server_address = "127.0.0.1"
    server_port = 12345

    size = int(input("Enter length of bit stream: "))
    #binary_data = generate_random_input(size, "input.txt")
    with open("input.txt", 'r') as file:
            binary_data = file.read()
    frameSize = input("Enter no of bits in each data frame of dataword [default : 8]: ")
    frameSize =  8 if frameSize == '' else int(frameSize)
    print("Enter your error detection method as selected in sender site")
    print("1. Use CRC")
    print("2. Use Checksum")
    choice=int(input("Enter your choice: "))
    if(len(binary_data)%frameSize!=0):
        l = len(binary_data)%frameSize
        binary_data += "0" * (frameSize - l)
    frames = buildFrames(binary_data, frameSize)
    print("**************************INPUT********************************")
    print(frames)
    print("\n")
    if choice==2:
        codewords = CheckSum.encode(frames, frameSize)
        print("-----------------------Codewords to be send------------------------")
        print(codewords)
    elif choice==1:
        print("Enter the polynomial you want to use for CRC calculation")
        print("1. CRC-8 ")
        print("2. CRC-10 ")
        print("3. CRC-16")
        print("4. CRC-32")
        p=int(input("Enter your choice: "))
        poly=""
        if p==1:
           poly="111010101"
        elif p==2:
           poly="11000110011"
        elif p==3:
           poly="11000000000000101"
        elif p==4:
           poly="100000100110000010001110110110111"
        else:
            print("Enter correct choice!!!!!!!!")
        codewords = CRC.encode(frames, poly)
        print("-----------------------Codewords to be send------------------------")
        print(codewords)

    # Step 6: Send the 16-bit words of the list one by one to the receiver
    send_through_socket(codewords)
    
