import math as mt
import numpy as np
from PIL import Image

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

    alpha = mt.ceil(mt.sqrt(prime))
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
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1
    total_pixels = array.size // n

    # Extracting prime number and alpha value
    message += 'END.'
    b_message = ''.join([format(ord(i), '08b') for i in message])
    req_pixels = len(b_message)
    alpha, prime = getAlphaAndPrime(req_pixels)

    # Encoding prime and alpha at the end of the image
    key = str(prime) + ',' + str(alpha) + '#'
    b_key = ''.join([format(ord(i), '08b') for i in key])
    index = 0
    for p in range(total_pixels)[::-1]:
        if index < len(b_key):
            array[p][m] = int(format(array[p][m], '08b')[:7] + b_key[index], 2)
            index += 1

    # Encoding message to the image
    pixels_list = getRandomQuadraticResidues(prime, alpha)
    if req_pixels > total_pixels:
        print('ERROR: Need larger file size')
    else:
        index = 0
        for p in pixels_list:
            if index < req_pixels:
                array[p][m] = int(format(array[p][m], '08b')[:7] + b_message[index], 2)
                index += 1
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest, format='png')
        print('Successfully encoded message!')


def Decode(src):
    """
    This function takes:
    - src: source directory of the cover image
    And print the message from the image if found any.
    """

    # Loading the image
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1

    total_pixels = array.size // n

    # Extracting key and alpha
    prime = 0
    alpha = 0
    hidden_key_bits = ''
    hidden_key = ''
    bit_counter = 0
    for p in range(total_pixels)[::-1]:
        hidden_key_bits += (bin(array[p][m])[2:][-1])
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

    for p in pixels_list:
        hidden_bits += (bin(array[p][m])[2:][-1])
        
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
    # Create an image for demo
    img = Image.new("RGB", (128, 128), "#232323")
    img.save('./pic.png')

    # Encrypt message
    Encode('./labrador.png', './labrador_encoded.png', 'TranNguyenHuan.18521394_NguyenGiaHuy.1852405_OnQuanAn.1852221')

    # Decrypt message
    Decode('./labrador_encoded.png')