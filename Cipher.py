import numpy as np
from egcd import egcd

caps=[]

# Converts Plain Text to Numberical Array of size 1*n (ie: 1 row and n columns)
def lettonum(string):
    numarray=[]
    i=0
    for letter in string:
        if(letter.isupper()==True):
            number = ord(letter)-65
            caps.append(i)
            i=i+1
        if(letter.islower()==True):
            number = ord(letter)-97
            i=i+1
        numarray.append(number)
    return(numarray)

# Converts Numberical Array to Plain Text of size 1*n (ie: 1 row and n columns)
def numtolet(arr):
    string=[]
    i=0
    for num in arr:
        if i in caps:
            alph = chr(ord('A')+num)
            i=i+1
        else:
            alph = chr(ord('a')+num)
            i=i+1
        string.append(alph)
    return(string)

# Takes Modulus (%26) with each element in the Matrix to convert to Alphabets easily later
def modmat(arr):
    ctext=[]
    for row in arr:
        arr=[]
        for element in row:
            element=element%26
            arr.append(element)
        ctext.append(arr)
    ciphertext=np.array(ctext)
    return(ciphertext)

# Inverse of Matrix and Modulo Inverse of the Determinant value being calculated
def matinv(matrix,modulus=26):
    det = int(np.round(np.linalg.det(matrix)))
    det_inv = egcd(det, modulus)[1] % modulus
    matrix_modulus_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus)
    return(matrix_modulus_inv)

# Reading in the Plain Text from the User
pt = input('Enter the Plain Text: ')

# Calling the function to convert string to numeric array
temparr=lettonum(pt)

# Stores the size of the Orignal Message
size=len(temparr)

# Reading in the Key Matrix from the User where R is no of rows and C is no of Columns
R = int(input("Enter the number of rows in Key: ")) 
C = int(input("Enter the number of columns in Key: ")) 
matrix = [] 
print("Enter the entries Row Wise:") 
for i in range(R):
	a =[]
	for j in range(C):
		a.append(int(input())) 
	matrix.append(a) 

# Converting the Key to Numpy Array for easy Matrix Multiplication
key=np.array(matrix)    
print(key)

# Finding the length of the Numeric Array
num=len(temparr)

# Finding how many padded elements need to be added to Plain Text to carry out Matrix Multiplication with Key Matrix
extra=num%C
reqno=C-extra

# For Handeling the exception when the existing Plain Text Matrix dimensions can be multiplied to Key Matrix
if(reqno==C):
    reqno=0

# Padding the Plain Text with 25 (ie. letter Z) so that matrix multiplication can take place with Key Matrix
for i in range (0,reqno):
    temparr.append(25)

# Converting the temparr to Numpy Array for easy Matrix Multiplication
ptext=np.array(temparr)

# For finding the number of columns in the new Plain Text Matrix (This new matrix is being formed on the dimensions of the Key Martix for easy matrix multiplication with it) (No of Columns in Key Matrix = No of Rows in new Plain Text Matrix)
col=int(len(temparr)/C)

# Reshapes the Plain Text Matrix of order 1*n to order col*C which is needed for matrix multipliation with Key Matrix
# Not Directly made to C,col because of the way the reshape matrix creates the matrix will not match the desired shape of the martix keeded for the Plain Text to be multiplied into Key Matrix 
plaintext = ptext.reshape(col, C)
print(plaintext)

# Transpose of Matrix to make the matrix of shape/order C*col
plaintext=plaintext.transpose()
print(plaintext)

# Dot product of Key and Plain Text Matrix to give the reultant cipher text
Encrypted=key.dot(plaintext)
print(Encrypted)

# Taking the Modulus of each element in the Matrix to associate with a letter
ctext=modmat(Encrypted)
ciphertext = ctext

# For Matrix Manuplation to easily convert back to alphabets in the correct order 
ciphertext = ciphertext.transpose()
numele=ciphertext.size
temparr = ciphertext.reshape(1, numele)
print(temparr)

# Converting the Matrix back to the Alphabets for easy understanding of the cipher text
transarr=temparr[0]
encryptedtext=numtolet(transarr)
print(encryptedtext)

# Inverse of Matrix X being returned and stored into inverse
inverse=matinv(key)
print(inverse)

# Multiplying the inverse with the cipher text to get back the plain text
Decrypted=inverse.dot(ctext)

# Taking the Modulus of each element in the Matrix to associate with a letter
etext=modmat(Decrypted)
encrypttext=etext

# For Matrix Manuplation to easily convert back to alphabets in the correct order 
encrypttext=encrypttext.transpose()
numele=encrypttext.size
temparr = encrypttext.reshape(1, numele)
print(temparr)

# Converting the Matrix back to the Alphabets for easy understanding of the plain text
transarr=temparr[0]
encryptedtext=numtolet(transarr)
print(encryptedtext)


# Inverse of Matrix X being returned and stored into inverse
inverse=matinv(plaintext)

# Multiplying the inverse with the cipher text to get back the plain text
KeyMatrix=ctext.dot(inverse)
# print(KeyMatrix)

# Taking the Modulus of each element in the Matrix
KeyMatrix=modmat(KeyMatrix)
print(KeyMatrix)

gcd_arr=[]
for row in KeyMatrix:
    for element in row:
        gcd_arr.append(element)
# print(gcd_arr)

gcd_factor = int(np.gcd.reduce(gcd_arr))
# print(gcd_factor)

if(gcd_factor!=1):
    KeyMatrix=KeyMatrix/gcd_factor

key_reduced = []
for row in KeyMatrix:
    gcd_arr=[]
    for element in row:
        gcd_arr.append(int(element))
    key_reduced.append(gcd_arr)
key_reduced = np.array(key_reduced)
print(key_reduced)
