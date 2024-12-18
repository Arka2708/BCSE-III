import socket
import pickle  
class Receiver:
	#Initialize all the data members of class
	def __init__(self, s):
		self.codeword = s.codeword
		self.dataSize = s.dataSize
		self.sentchecksum = s.checksum
		self.sum = ""
		self.addchecksum = ""
		self.complement = ""
		self.data = [] 
		# Function to decode and check for error in codewords
	def checkError(self, type, poly=""):
		if type == 1:
			self.sum = self.calculateSum()
			result = self.add(self.sum, self.sentchecksum)
			while len(result) > self.dataSize:
				t1 = result[:len(result) - self.dataSize]
				t2 = result[len(result) - self.dataSize:]
				result = self.add(t1, t2)
			self.addchecksum = result
			# finding complement and checking error
			error = False
			for ch in self.addchecksum:
				if ch == '0':
					self.complement += '1'
					error = True
				else:
					self.complement += '0'
			if error:
				print("Complement is not zero.", end=' ')
				print("ERROR DETECTED")
			else:
				print("Complement is zero.", end=' ')
				print("NO ERROR DETECTED")
			return self.extractDatawords(type)

		elif type == 2:
			error_detected = []
			for i in range(len(self.codeword)):
				remainder = self.divide(self.codeword[i], poly)
				error = False
				for j in range(len(remainder)):
					if remainder[j] == '1':
						error = True
				print("Remainder:", remainder, end=' ')
				if error:
					error_detected.append(True)
					print("ERROR DETECTED")
				else:
					error_detected.append(False)
					print("NO ERROR DETECTED")
			return self.extractDatawords(type, error_detected)

	def extractDatawords(self, type, error_detected=[]):
		datawords = []
		if type == 1:
			if not error_detected:  # If error_detected list is empty, there were no errors detected
				datawords = self.codeword.copy()  # Use self.codeword instead of self.data
			else:
				for i in range(len(self.codeword)):
					if not error_detected[i]:  # Exclude dataword if error is detected
						datawords.append(self.codeword[i])
		elif type == 2:
			# Similar to type 1, check if error_detected list is empty, if not, exclude datawords with errors
			if not error_detected:
				datawords = self.codeword.copy()
			else:
				for i in range(len(self.codeword)):
					if not error_detected[i]:
						datawords.append(self.codeword[i])
		return datawords


	#Function to display the received codewords
	def displayFrames(self, type):
		print("Codewords received by receiver:")
		print(self.codeword)
		if type == 3:
			print(self.sum, " - sum")
			print(self.addchecksum, " - sum+checksum")
			print(self.complement, " - complement")	
		for i in range(len(self.codeword)):
			self.codeword[i] = self.codeword[i][:self.dataSize]
		print("Extracting datawords from codewords:")
		print(self.codeword)
		print()
	
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
		result = self.codeword[0]
		for i in range(1,len(self.codeword)):
			result = self.add(result, self.codeword[i])
			while len(result) > self.dataSize:
				t1 = result[:len(result)-self.dataSize]
				t2 = result[len(result)-self.dataSize:]
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
	#Helper function to divide two binary sequence
	def divide(self, dividend, divisor):
		xorlen = len(divisor)
		temp = dividend[:xorlen]
		while len(dividend) > xorlen:
			if temp[0]=='1':
				temp=self.xor(divisor,temp)+dividend[xorlen]
			else:
				temp=self.xor('0'*xorlen,temp)+dividend[xorlen]
			xorlen += 1
		if temp[0]=='1':
			temp=self.xor(divisor,temp)
		else:
			temp=self.xor('0'*xorlen,temp)
		return temp

def receiveCodewords(self):
        host = '127.0.0.1'  # Localhost IP address
        port = 12345  # Choose the same port used by the sender

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen()

            print("Receiver: Waiting for the Sender to connect...")
            conn, addr = server_socket.accept()

            with conn:
                print("Receiver: Connection established with Sender at", addr)
                serialized_sender = conn.recv(4096)
                sender = pickle.loads(serialized_sender)
                self.checkError(1)  # Call the error checking function
