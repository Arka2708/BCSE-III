import socket
import pickle
from error_injection import injectRandomError, injectSpecificError
class Sender:
	#Initialize all the data members of class
	def __init__(self, size):
		self.codeword = []
		self.dataSize = size
		self.checksum = ""
    # Function to generate codewords to be sent
	def createFrames(self, filename, type, poly=""):
		fileinput = open(filename, "r")
		packet = fileinput.readline()
		fileinput.close()
		tempword = ""
		if type == 1:
			for i in range(len(packet)):
				if i > 0 and i % self.dataSize == 0:
					self.codeword.append(tempword)
					tempword = ""
				tempword += packet[i]
			self.codeword.append(tempword)

			# Calculate the size of the codeword based on the dataword size
			num_redundant_bits = 8 - self.dataSize  # Adjust this value based on your requirement
			for i in range(len(self.codeword)):
				self.codeword[i] = self.codeword[i].zfill(self.dataSize + num_redundant_bits)

			summ = self.calculateSum()
			for i in range(len(summ)):
				if summ[i] == '0':
					self.checksum += '1'
				else:
					self.checksum += '0'
		elif type == 2:
			# Modify the size of the dataword based on your requirement
			tempsize = 5

			for i in range(len(packet)):
				if i > 0 and i % tempsize == 0:
					tempword += '0' * (len(poly) - 1)
					remainder = self.divide(tempword, poly)
					remainder = remainder[len(remainder) - (len(poly) - 1):]
					tempword = tempword[:tempsize]
					tempword += remainder
					# Adjust the size of the codeword based on the dataword size and polynomial size
					tempword = tempword.zfill(tempsize + len(poly) - 1)
					self.codeword.append(tempword)
					tempword = ""
				tempword += packet[i]

			tempword += '0' * (len(poly) - 1)
			remainder = self.divide(tempword, poly)
			remainder = remainder[len(remainder) - (len(poly) - 1):]
			tempword = tempword[:tempsize]
			tempword += remainder
			# Adjust the size of the codeword based on the dataword size and polynomial size
			tempword = tempword.zfill(tempsize + len(poly) - 1)
			self.codeword.append(tempword)

	#Function to display the sent codewords
	def displayFrames(self, type):
		datawords = []
		for x in self.codeword:
			datawords.append(x[:self.dataSize])
		print("Datawords to be sent:")
		print(datawords)
		print("Codewords sent by sender:")
		print(self.codeword)
		if type == 1:
			print(self.checksum, " - checksum")
		print("\n")
	
	#Helper function to add two binary sequence
	def add(self, a, b):
		result = ""
		s = 0
		i = len(a)-1
		j = len(b)-1
		while i>=0 or j>=0 or s==1:
			if i>=0:
				s+=int(a[i])
			if j>=0:
				s+=int(b[j])
			result = str(s%2) + result
			s //= 2 
			i-=1
			j-=1
		return result
	
	#Helper function to calculate sum of all codewords
	def calculateSum(self):
		if not self.codeword:  # Check if the codeword list is empty
			return ""
		result = self.codeword[0]
		for i in range(1, len(self.codeword)):
			result = self.add(result, self.codeword[i])
			while len(result) > self.dataSize:
				t1 = result[:len(result) - self.dataSize]
				t2 = result[len(result) - self.dataSize:]
				result = self.add(t1, t2)
		return result

	#Helper function to XOR two binary sequence
	def xor(self, a, b):
		result = ""
		for i in range(1, len(b)):
			if a[i]==b[i]:
				result += '0'
			else:
				result += '1'
		return result

 # Helper function to divide two binary sequences
def divide(self, dividend, divisor):
        xorlen = len(divisor)
        temp = dividend[:xorlen]

        while len(dividend) >= xorlen:
            if temp[0] == '1':
                temp = self.xor(divisor, temp) + dividend[xorlen:]
            else:
                temp = self.xor('0' * xorlen, temp) + dividend[xorlen:]
            xorlen += 1

        if temp[0] == '1':
            temp = self.xor(divisor, temp)
        else:
            temp = self.xor('0' * xorlen, temp)

        return temp

def sendCodewords(self):
        host = '127.0.0.1'  # Localhost IP address
        port = 12345  # Choose any available port

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            serialized_sender = pickle.dumps(self)
            client_socket.sendall(serialized_sender)
            print("Data sent to the Receiver.")