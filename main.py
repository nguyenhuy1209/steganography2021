import math as mt
import numpy as np
from PIL import Image

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

def Encode(src, dest, message='abc'):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1
    total_pixels = array.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
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
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")

def Decode(src):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
        m = 0
    elif img.mode == 'RGBA':
        n = 4
        m = 1
    total_pixels = array.size//n

    message = ''
    word = ''
    print(array)
    # for p in range(total_pixels):
    #     for q in range(m, n):
    #         print(format(array[p][q],'08b'))
            # bit = (format(array[p][q],'08b')[-1])
    
    # print(message)

# if __name__ == '__main__':
#     # Create a white image
#     img = Image.new("RGB", (128, 128), "#000000")
#     img.save('./pic.png')

#     # Encrypt message
#     Encode('./pic.jpg', './pic_encoded.jpg', 'Huy')

#     # Decrypt message
#     Decode('./pic_encoded.jpg')

def random(num, prime, temp):
    # size = 100
    # prime > 2*num
    lst = []
    for i in range(num):
        lst.append((i+temp)**2%prime)
    
    return lst

print(random(10, 31, 5))

"""
15, 263 
"""

def decode(temp, prime):
    out = []
    for i in range(0, 10):
        out.append((i+temp)**2%prime)
    
    return out

print(decode(5, 31))