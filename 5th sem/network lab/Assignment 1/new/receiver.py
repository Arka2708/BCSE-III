import socket
from error_detection import *

def BinaryToString(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def receive_from_socket():
    host = '127.0.0.1'  # Localhost IP address
    port = 12345  # Choose the same port used by the sender
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(10)
    print("Receiver: Waiting for the Sender to connect...")
    received_data = []
    while True:
        conn, addr = server_socket.accept()
        print("Receiver: Connection established with Sender at", addr)
        while True:
            data = conn.recv(4096)
            if(data.decode()=="END"):
                conn.close()
                return received_data
            print('Message received:', data.decode())
            conn.send("ok".encode())  # Send an acknowledgment back to the sender
            received_data.append(data.decode())

def store_received_data(received_data):
   output_file="output.txt"
   with open(output_file, 'w') as file:
        for item in received_data:
            file.write(f'{item}\n')

if __name__ == "__main__":
    print("Enter your error detection method as selected in sender site")
    print("1. Use CRC")
    print("2. Use Checksum")
    choice=int(input("Enter your choice: "))
    print("\n")
    #Receive the codewords over the socket
    received_data = receive_from_socket()

    if choice==2:
        error= CheckSum.decode(received_data, len(received_data[0]))
        if error:
            print("Complement is not zero.", end=' ')
            print("ERROR DETECTED")
        else:
            print("Complement is zero.", end=' ')
            print("NO ERROR DETECTED")
        received_data=received_data[:-1]

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

        received_data,num=CRC.decode(received_data, poly)
        if num>0:
            print(str(num) + "ERROR DETECTED in CRC\n")
        else:
            print("NO ERROR DETECTED in CRC\n")

    print("\n*******************Received DataWords************************\n")
    print(received_data)
    # Store the received binary sequences in another folder
    store_received_data(received_data)