import numpy as np
from cv2 import cv2

import struct
import ntpath

#ENCODING ----------------------------------------------------------------------------------------------

def read_message(path, ci=(0,1)):
    ext = ntpath.splitext(path)[-1]
    
    if   ext == ".txt":         
        file_content = open(path, mode="rb").read()        
        message = struct.unpack("B" * len(file_content), file_content)
    elif ext in [".png", ".jpg", ".jpeg"]: message = cv2.imread(path)[:,:, ci[0]:ci[1]]
    else: raise TypeError("Unsupported file extension.")

    return message

def convert_msg_to_binary(msg):
    """Convert a message (array of 8-bit ints) into an array of binary data"""
    msg = np.repeat(msg, 8)

    iterator = np.tile(np.arange(8, dtype=np.uint8), msg.size // 8)
    mask = np.left_shift(1, iterator)

    bit = np.bitwise_and(msg, mask)
    binary = np.right_shift(bit, iterator)
    return binary

def _inject_bits(x1, x2):
    x1 = np.bitwise_and(x1, 254)       
    return np.bitwise_or(x1, x2)

def insert_binary(img, binary, ci=(0,1)):
    """Insert binary data into the least significant bit of a color channel value"""
    copy = np.copy(img)
    channel = copy[:,:, ci[0]:ci[1]] #ci stands for channel id aka which channel to insert binary into (first channel by default)
    
    binary = np.resize(binary, channel.shape) #if the binary array is not big enough, it will loop over

    output = _inject_bits(channel, binary)
    copy[:,:, ci[0]:ci[1]] = output
    return copy 
        

#DECODING ----------------------------------------------------------------------------------------------

def _scrape_bits(x1):
    return np.bitwise_and(x1, 1) #return only the least significant bit

def extract_binary(img, ci=(0,1)):
    """Extract binary data from the least significant bit of a color channel value"""
    channel = img[:,:, ci[0]:ci[1]]
    return _scrape_bits(channel)

def convert_binary_to_msg(binary):
    """Convert an array of binary data into a message"""
    groups = binary.size // 8
    binary = np.resize(binary, (groups, 8))

    iterator = np.tile(np.arange(8, dtype=np.uint8), (groups, 1))

    binary = np.left_shift(binary, iterator)
    message = np.bitwise_or.reduce(binary, axis=1)

    return message

def write_message(msg, path):
    ext = ntpath.splitext(path)[-1]
    if ext == ".txt": open(path, "wb").write(struct.pack("B" * msg.size, *msg.flatten()))
    elif ext in [".png", ".jpeg", ".jpg"]: cv2.imwrite(path, msg)

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=(0,1)):
    a = x[:,:, ci[0]:ci[1]]
    b = y[:,:, ci[0]:ci[1]]
    print(a-b)
    return (a - b) 





