import math as mt
import numpy as np
from PIL import Image


def primeNum(num, lis):
    """

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


def random_index(num, prime, temp):
    # size = 100
    # prime > 2*num
    lst = []
    for i in range(prime // 2):
        lst.append((i + temp) ** 2 % prime)
    return lst[0:-temp+1]

# def lis
def getAlpha(len, lis):
    i = 0
    while 2 * len > lis[i]:
        i = i + 1
    pri = lis[i]
    alpha = mt.ceil(mt.sqrt(pri))
    prime = (len + alpha) * 2
    for i in lis:
        if prime < i:
            prime = i
            break
    return alpha, prime


def Encode(src, dest, message):
    """
    This function takes
    - src: source directory of the cover image
    - dest: destination directory of the decoded image
    - message: message needs to be hidden
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
    # message += "$t3g0"

    # Extracting prime number and alpha value
    # ...
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    lis = []
    if primeNum(2, []):
        lis.append(2)
    for i in range(3, 3 * req_pixels, 2):
        if primeNum(i, lis):  # lis = list of prime < 3*req_pixels
            lis.append(i)
    alpha, prime = getAlpha(req_pixels, lis)
    # Encoding prime and alpha at the end of the image
    key = prime.__str__() + ',' + alpha.__str__() + '#'
    print(key)
    b_key = ''.join([format(ord(i), "08b") for i in key])
    index = 0
    for p in range(total_pixels)[::-1]:
        if index < len(b_key):
            array[p][m] = int(format(array[p][m], '08b')[:7] + b_key[index], 2)
            index += 1

    pixels_list = random_index(req_pixels, prime, alpha)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index = 0
        for p in pixels_list:
            if index < req_pixels:
                array[p][m] = int(format(array[p][m], '08b')[:7] + b_message[index], 2)
                index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest, format='png')

        print("Image Encoded Successfully")


def Decode(src):
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
        print('Cannot extract prime number key and alpha')
        return

    # Extract message
    hidden_bits = ""
    pixels_list = random_index(64, prime, alpha)

    for p in pixels_list:
        hidden_bits += (bin(array[p][m])[2:][-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
    print(hidden_bits)
    message = ''
    for i in range(len(hidden_bits)):
        # if message[-5:] == '$t3g0':
        #     break
        # else:
        message += chr(int(hidden_bits[i], 2))
    # if '$t3g0' in message:
    print("Hidden Message:", message)
    # else:
    #     print("No Hidden Message Found")


if __name__ == '__main__':
    # Create a white image
    img = Image.new("RGB", (128, 128), "#232323")
    img.save('./pic.png')

    # Encrypt message
    Encode('./conchohuan.jpg', './conchohuan_encoded.png', 'TranNguyenHuan.18521394_NguyenGiaHuy.1852405_OnQuanAn.1852221')

    # Decrypt message
    Decode('./conchohuan_encoded.png')
