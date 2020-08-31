from cv2 import cv2
import numpy as np

#ENCODING ----------------------------------------------------------------------------------------------

def encode_message(msg):
    bits = np.full(len(msg) * 8, 0)

    for i in range(0, bits.size, 8):        
        o = ord(msg[i//8])

        binary = bin(o)[2:]
        binary = binary.zfill(8)
        bits[i:i+8] = list(binary)
    return bits

def inject_bits(i, b):
        output = (i & ~1) | b
        return output

inject_bits = np.vectorize(inject_bits) #vectorizing for better performance

#DECODING ----------------------------------------------------------------------------------------------

def scrape_bits(byte):
    mask = 1
    return byte & mask #return only a certain bit that is overlapped by the mask

scrape_bits = np.vectorize(scrape_bits) #vectorizing for better performance
    
def decode_message(bits):
    bits = bits.flatten() #flatten the array to prevent from errors due to multiple dimensions

    message = ""
    for i in range(0, bits.size, 8):
        byte = bits[i:i+8]
        byte = "".join(str(b) for b in byte) #convert an array of 8 bits [0,1,1,0, ...] into a string "0110..."
        ch = chr(int(byte, 2)) #get the character represented by the binary 

        message += ch

    return message





