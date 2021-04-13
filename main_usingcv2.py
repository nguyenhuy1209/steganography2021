# Python program to demonstrate
# image steganography using OpenCV
  
import math as mt
import cv2
import numpy as np
import random
  
def primeNum(num, lis):
    """
    This function takes:
    - num: a number to be checked if it is a prime number or not.
    - lst: a list of known prime number, for convenience.
    Returns:
    - True: if the input number is a prime number, False if otherwise
    """

    if not lis:
        return True
    for i in range(len(lis)):
        if num % lis[i] == 0:
            return False
    for i in range(len(lis), mt.floor(mt.sqrt(num)), 2):
        if num % i == 0:
            return False
    return True

def getRandomQuadraticResidues(prime, alpha):
    """
    This function takes:
    - prime: the prime number
    - alpha: the alpha number
    Returns:
    - a list of quadratic residues.
    """

    lst = []
    for i in range(prime // 2):
        lst.append((i + alpha) ** 2 % prime)
    
    return lst[0:-alpha+1]

def getAlphaAndPrime(mess_length):
    """
    This function takes:
    - mess_length: the length of the message needed to find out the appropriate prime, alpha number.
    Returns:
    - alpha: the appropriate alpha number for the message length.
    - prime: the appropriate prime number for the message length.
    """
    prime_list = []
    prime = 0
    alpha = 0

    prime_list.append(2)

    for i in range(3, 3 * mess_length, 2):
        if primeNum(i, prime_list):  # lis = list of prime < 3*req_pixels
            prime_list.append(i)

    for num in prime_list:
        if 2 * mess_length <= num:
            prime = num
            break

    alpha = mt.ceil(np.sqrt(prime))
    prime = (mess_length + alpha) * 2

    for num in prime_list:
        if prime < num:
            prime = num
            break

    return alpha, prime

def Encode(src, dest, message):
    """
    This function takes:
    - src: source directory of the cover image
    - dest: destination directory of the decoded image
    - message: message needs to be hidden
    And encode the message to the new outputed image in PNG format.
    """

    # Loading the image
    img = cv2.imread(src)
    rows, cols, channel = img.shape
    total_pixels = img.shape[0] * img.shape[1]
    # Extracting prime number and alpha value
    message += 'END.'
    b_message = ''.join([format(ord(i), '08b') for i in message])
    req_pixels = len(b_message)
    alpha, prime = getAlphaAndPrime(req_pixels)

    # Encoding prime and alpha at the end of the image
    key = str(prime) + ',' + str(alpha) + '#'
    b_key = ''.join([format(ord(i), '08b') for i in key])
    index = 0
    for i in range(rows)[::-1]:
        for j in range(cols)[::-1]:
            if index < len(b_key):
                img[i][j][0] = int(format(img[i][j][0], '08b')[:7] + b_key[index], 2)
                index += 1

    # Encoding message to the image
    pixels_list = getRandomQuadraticResidues(prime, alpha)
    pixels_list = [(index//cols, index%cols) for index in pixels_list]
    if req_pixels > total_pixels:
        print('ERROR: Need larger file size')
    else:
        index = 0
        for p in pixels_list:
            i, j = p
            if index < req_pixels:
                if format(img[i][j][0], '08b')[7] == 1 and b_message[index] == 0:
                    if img[i][j][1] < 255:
                        img[i][j][1] += 1
                    elif img[i][j][2] < 255:
                        img[i][j][2] += 1
                if format(img[i][j][0], '08b')[7] == 0 and b_message[index] == 1:
                    if img[i][j][1] > 0:
                        img[i][j][1] -= 1
                    elif img[i][j][2] > 0:
                        img[i][j][2] -= 1
                img[i][j][0] = int(format(img[i][j][0], '08b')[:7] + b_message[index], 2)
                index += 1
        cv2.imwrite(dest, img)
        print('Successfully encoded message!')
        print('Encoded image is stored as:', dest)

def Decode(src):
    """
    This function takes:
    - src: source directory of the cover image
    And print the message from the image if found any.
    """

    # Loading the image
    img = cv2.imread(src)
    rows, cols, channel = img.shape

    # Extracting key and alpha
    prime = 0
    alpha = 0
    hidden_key_bits = ''
    hidden_key = ''
    bit_counter = 0
    for i in range(rows)[::-1]:
        for j in range(cols)[::-1]:
            hidden_key_bits += (bin(img[i][j][0])[2:][-1])
            bit_counter += 1
            if bit_counter == 8:
                letter = chr(int(hidden_key_bits[-8:], 2))
                hidden_key += letter
                if letter == '#':
                    break
                bit_counter = 0
    hidden_key = hidden_key[:-1].split(',')
    if len(hidden_key) == 2:
        prime = int(hidden_key[0])
        alpha = int(hidden_key[1])
    else:
        print('Cannot extract prime number key and alpha.')
        return

    # Extract message
    hidden_bits = ""
    pixels_list = getRandomQuadraticResidues(prime, alpha)
    pixels_list = [(index//cols, index%cols) for index in pixels_list]
    for p in pixels_list:
        i, j = p
        hidden_bits += (bin(img[i][j][0])[2:][-1])
        
    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]
    message = ''
    for i in range(len(hidden_bits)):
        if message[-4:] == 'END.':
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if 'END.' in message:
        print(f'Hidden Message: {message[:-4]}')
    else:
        print('No hidden message found!')


if __name__ == '__main__':

    print('1. Encode')
    print('2. Decode')
    prompt = input('Do you want to encode or decode? ')
    if prompt == '1':
        print('Please type in the cover image:')
        src = input()
        print('Please type in the message:')
        mess = input()
        filename = src.split('.')[0]
        dest = filename + '_encoded.png'
        Encode(src, dest, mess)
    elif prompt == '2':
        print('Please type in the image you wish to decode:')
        src = input()
        Decode(src)
    else:
        print('Invalid option.')

    # # Encrypt message
    # Encode('./cat.jpg', './cat_encoded.png', 'TranNguyenHuan-NguyenGiaHuy-OnQuanAn')

    # # Decrypt message
    # Decode('./cat_encoded.png')

    # img1 = cv2.imread('cat.png')
    # # print(img1)
    # print(img1.shape)
    # print(img1[-1][-1])
    # print(img1[-1][-2])
    # img1[-1][-1][1] -= 64
    # img1[-1][-2][1] += 64
    # print(img1[-1][-1])
    # print(img1[-1][-2])
    # print(img1.shape)
    # cv2.imwrite('cat_encoded.png', img1)