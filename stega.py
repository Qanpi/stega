import numpy as np
from cv2 import cv2

import struct
import ntpath

#ENCODING ----------------------------------------------------------------------------------------------

def _compose_header(mtype, size):
    if mtype == "|T": header = np.array([124, 84, *struct.pack("I", size), 0, 0]) #[124, 84] is ascii for '|T' which signifies that this message is text
    else:             header = np.array([124, 73, *struct.pack("HHH", *size)   ]) #[124, 73] is ascii for '|I' which signifies that this message is an image
    return header.astype(np.uint8)

def read_message(path, ci=(0,1)): #ci stands for channel id aka which channel to insert binary into (first channel by default)
    ext = ntpath.splitext(path)[-1]
    if   ext == ".txt":         
        file_content = open(path, mode="rb").read()        
        message = struct.unpack("B" * len(file_content), file_content)
        message = np.asarray(message, dtype=np.uint8)

        header = _compose_header("|T", len(message))
    elif ext in [".png", ".jpg", ".jpeg"]: 
        message = cv2.imread(path)[:,:, ci[0]:ci[1]]
        header = _compose_header("|I", message.shape)
    else: raise TypeError("Unsupported file extension.")

    message = np.concatenate([header, message], axis=None)
    return message

def convert_arr_to_binary(msg):
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
    channel = copy[:,:, ci[0]:ci[1]] 
    
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

def _parse_header(header): 
    mtype = "".join([chr(i) for i in header[:2]])
    if mtype=="|T": size = struct.unpack("I", header[2:6])
    else:           
        size = struct.unpack("H" * 3, header[2:])
    return mtype, size

def convert_binary_to_arr(binary, all=False): #all stands for whether u want all (even repetitive) data from the image, or just the original size
    """Convert an array of binary data into a message"""
    groups = binary.size // 8
    binary = np.ravel(binary)

    iterator = np.tile(np.arange(8, dtype=np.uint8), groups)
    binary = np.left_shift(binary, iterator)

    binary = np.resize(binary, (groups, 8))
    binary = np.bitwise_or.reduce(binary, axis=1)

    header = binary[:8]
    message = binary[8:]
    t, size = _parse_header(header)

    if not all: return np.resize(message, size)
    elif t == "|I": 
        rows = message.size // size[1] // size[2]
        return np.resize(message, (rows, size[1], size[2]))
    else: return message

def write_message(msg, path):
    ext = ntpath.splitext(path)[-1]
    if ext == ".txt": open(path, "wb").write(struct.pack("B" * msg.size, *msg.flatten()))
    elif ext in [".png", ".jpeg", ".jpg"]: cv2.imwrite(path, msg)
    else: raise TypeError("Unsupported file extension")

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=(0,1)):
    a = x[:,:, ci[0]:ci[1]]
    b = y[:,:, ci[0]:ci[1]]

    return (a - b) 





