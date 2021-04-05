import math as mt
import numpy as np
from PIL import Image


def Encode(src, dest, message='abc'):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    print(array)
    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1
    total_pixels = array.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    print(message)
    print(b_message)
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index = 0
        for p in range(total_pixels):
            for q in range(m, n):
                if index < req_pixels:
                    array[p][q] = int(format(array[p][q],'08b')[:7] + b_message[index], 2)
                    index += 1
        array = array.reshape(height, width, n)
        print(array)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


def primeNum(num, lis):
    if not lis:
        return lis.append(num)
    for i in range(len(lis)):
        if num % lis[i] == 0:
            return lis
    for i in range(lis[i], mt.floor(mt.sqrt(num)), 2):
        if num % lis[i] == 0:
            return lis
    return lis.append(num)


def insertMes(pic, mess):
    lis = []
    for i in range(2, len(pic), 1):
        primeNum(i, lis)
    for i in range(len(mess)):
        return "aaa"


if __name__ == '__main__':
    lis = [2]
    Encode('/Users/quanan/Desktop/nice.jpeg', '/Users/quanan/Desktop/njce.jpeg', 'abc')
    #
    # if not lis:
    #     print("provjp")
