import numpy as np
from egcd import egcd
import math

# Converts Plain Text to Numberical Array of size 1*n (ie: 1 row and n columns)
def lettonum(string):
    numarray = []
    i=0
    for letter in string:
        if(letter.isupper()==True):
            number = ord(letter)-65
        if(letter.islower()==True):
            number = ord(letter)-97
        numarray.append(number)
    return(numarray)

# Converts Numberical Array to Plain Text of size 1*n (ie: 1 row and n columns)
def numtolet(arr):
    string = []
    i=0
    for num in arr:
        alph = chr(ord('a')+num)
        string.append(alph)
    return(string)

# Takes Modulus (%26) with each element in the Matrix to convert to Alphabets easily later
def modmat(arr):
    ctext = []
    for row in arr:
        arr = []
        for element in row:
            element = element%26
            arr.append(element)
        ctext.append(arr)
    ciphertext = np.array(ctext)
    return(ciphertext)

# Inverse of Matrix and Modulo Inverse of the Determinant value being calculated
def matinv(matrix,modulus=26):
    det = int(np.round(np.linalg.det(matrix)))
    # print(det)
    det_inv = egcd(det, modulus)[1] % modulus
    # print(det_inv)
    matrix_modulus_inv = (det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus)
    return(matrix_modulus_inv)

# Reading in the Unknown Cipher Text from the User
cipher_unknown = input('Enter the Unknown Cipher Text: ')

# Reading in the Known Cipher Text from the User
cipher_known = input('Enter the Known Cipher Text: ')

# Reading in the Plain Text from the User
plain_text = input('Enter the Plain Text: ')

# Calling the function to convert strings to numeric array
cipher_unknown = lettonum(cipher_unknown)
cipher_known = lettonum(cipher_known)
plain_text = lettonum(plain_text)

# Stores the size of the Orignal Message
cipher_unknown_size = len(cipher_unknown)
cipher_known_size = len(cipher_known)
plain_text_size = len(plain_text)
# print(cipher_unknown_size)
# print(cipher_known_size)
# print(plain_text_size)

# Converting the all input arrays to Numpy Array for easy Matrix Multiplication
cipher_unknown = np.array(cipher_unknown)
cipher_known = np.array(cipher_known)
plain_text = np.array(plain_text)

# For finding the number of columns in the new Plain Text Matrix (This new matrix is being formed on the dimensions of the Key Martix for easy matrix multiplication with it) (No of Columns in Key Matrix = No of Rows in new Plain Text Matrix)
size_matrix = int(math.sqrt(plain_text_size))

# Reshapes the Plain Text Matrix of order 1*n to order col*C which is needed for matrix multipliation with Key Matrix
# Not Directly made to C,col because of the way the reshape matrix creates the matrix will not match the desired shape of the martix keeded for the Plain Text to be multiplied into Key Matrix 
cipher_unknown = cipher_unknown.reshape(int(cipher_unknown_size/size_matrix), size_matrix)
cipher_known = cipher_known.reshape(size_matrix, size_matrix)
plain_text = plain_text.reshape(size_matrix, size_matrix)
# print(cipher_unknown)
# print(cipher_known)
# print(plain_text)

# Transpose of Matrix to make the matrix of shape/order C*col
cipher_unknown = cipher_unknown.transpose()
cipher_known = cipher_known.transpose()
plain_text = plain_text.transpose()
# print(cipher_unknown)
# print(cipher_known)
# print(plain_text)

# Inverse of Matrix X being returned and stored into inverse
inverse = matinv(plain_text)

# Dot product of Key and Plain Text Matrix to give the reultant cipher text
key = cipher_known.dot(inverse)
print(key)

# Taking the Modulus of each element in the Matrix to associate with a letter
key = modmat(key)
print(key)

gcd_arr=[]
for row in key:
    for element in row:
        gcd_arr.append(element)
# print(gcd_arr)

gcd_factor = int(np.gcd.reduce(gcd_arr))
# print(gcd_factor)

if(gcd_factor!=1):
    key=key/gcd_factor

key_reduced = []
for row in key:
    gcd_arr=[]
    for element in row:
        gcd_arr.append(int(element))
    key_reduced.append(gcd_arr)
key_reduced = np.array(key_reduced)
print(key_reduced)

# Inverse of Matrix X being returned and stored into inverse
inverse = matinv(key_reduced)
print(inverse)

# Dot product of Key and Plain Text Matrix to give the reultant cipher text
unknown_plain_text = inverse.dot(cipher_unknown)

# Taking the Modulus of each element in the Matrix to associate with a letter
unknown_plain_text = modmat(unknown_plain_text)
print(unknown_plain_text)

# For Matrix Manuplation to easily convert back to alphabets in the correct order 
unknown_plain_text = unknown_plain_text.transpose()
numele = unknown_plain_text.size
temparr = unknown_plain_text.reshape(1, numele)

# Converting the Matrix back to the Alphabets for easy understanding of the cipher text
transarr=temparr[0]
unknown_plain_text = numtolet(transarr)
print(unknown_plain_text)

# vzgbxouvcdqzqngoko
# dqzqngoko
# howareyou
