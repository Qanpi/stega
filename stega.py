from cv2 import cv2
import numpy as np

import timeit as tt
#ENCODING ----------------------------------------------------------------------------------------------

def encode_message(msg, size=None):
    """Converts a text message into an array of binary data"""
    size = size if size else len(msg) * 8
    bits = np.full(size, 0)

    #Skipping over 8 elements for better performance
    for i in range(0, bits.size, 8):        
        o = ord(msg[i//8])

        #Get binary and embed it into the list
        byte = bin(o)[2:]
        byte = byte.zfill(8)
        bits[i:i+8] = list(byte)
    return bits

def inject_bits(i, b):
        output = (i & ~1) | b
        return output

inject_bits = np.vectorize(inject_bits) #vectorizing for better performance

def put_binary(img, binary, ci=0):
    channel = img[:,:, ci] #ci stands for channel id aka which channel to insert binary into (first channel by default)
    
    if binary.shape != channel.shape:
        binary = np.resize(binary, channel.shape) #if the binary array is not big enough, it will loop over

    output = inject_bits(channel, binary)
    img[:,:, ci] = output.astype(np.uint8) #uint8 used cuz otherwise cv2 starts complaining about some depth stuff
    return img 
        

#DECODING ----------------------------------------------------------------------------------------------

def scrape_bits(b):
    return b & 1 #return only a the least significant bit

scrape_bits = np.vectorize(scrape_bits) #vectorizing for better performance

def get_binary(img, ci=0):
    channel = img[:,:, ci]

    return scrape_bits(channel)
    
def decode_message(binary):
    binary = binary.flatten() #flatten the array to prevent from errors due to multiple dimensions

    message = ""
    for i in range(0, binary.size, 8):
        byte = binary[i:i+8]
        byte = "".join(str(b) for b in byte) #convert an array of 8 bits [0,1,1,0, ...] into a string "0110..."
        ch = chr(int(byte, 2)) #get the character represented by the binary 

        message += ch
    return message

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=0):
    x = x[:,:, ci]
    y = y[:,:, ci]

    return (x - y) * 255 #multiplied by 255 to exaggerate the difference





