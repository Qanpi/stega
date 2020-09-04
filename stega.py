from cv2 import cv2
import numpy as np

import timeit as tt
#ENCODING ----------------------------------------------------------------------------------------------

def msg_to_binary(msg):
    """Converts a text message into an array of binary data"""
    binary = np.array([[ord(ch)] * 8 for ch in msg], dtype=np.uint8) #numpy array of arrays containing ord() of character 8 times

    iterator = np.resize(np.arange(8, dtype=np.uint8), binary.shape)
    mask = np.left_shift(1, iterator)

    bit = np.bitwise_and(binary, mask)
    output = np.right_shift(bit, iterator)
    
    return output

def inject_bits(x1, x2):
        x1 = np.bitwise_and(x1, 254)       
        return np.bitwise_or(x1, x2)

def insert_binary(img, binary, ci=0):
    channel = img[:,:, ci] #ci stands for channel id aka which channel to insert binary into (first channel by default)
    
    if binary.shape != channel.shape:
        binary = np.resize(binary, channel.shape) #if the binary array is not big enough, it will loop over

    output = inject_bits(channel, binary)
    img[:,:, ci] = output.astype(np.uint8) #uint8 since the data is in the range of 0-255
    return img 
        

#DECODING ----------------------------------------------------------------------------------------------

def scrape_bits(x1):
    return np.bitwise_and(x1, 1) #return only a the least significant bit

def extract_binary(img, ci=0):
    channel = img[:,:, ci]

    return scrape_bits(channel)

def binary_to_msg(binary):
    groups = binary.size // 8
    binary = np.reshape(binary, (groups, 8))

    iterator = np.resize(np.arange(8, dtype=np.uint8), binary.shape)

    binary = np.left_shift(binary, iterator)
    output = []
    
    for i in range(len(binary)):
        ch = chr(np.bitwise_or.reduce(binary[i]))
        output.append(ch) 

    return "".join(output)

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=0):
    x = x[:,:, ci]
    y = y[:,:, ci]

    return (x - y) * 255 #multiplied by 255 to exaggerate the difference





