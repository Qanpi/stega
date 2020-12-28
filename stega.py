import numpy as np
from PIL import Image

import struct
import ntpath

#ENCODING ----------------------------------------------------------------------------------------------

class Encoder:

    def _compose_header(self, mtype, size):
        if mtype == "|T": header = np.array([124, 84, *struct.pack("I", size), 0, 0]) #[124, 84] is ascii for '|T' which signifies that this message is text
        else:             header = np.array([124, 73, *struct.pack("HHH", *size)   ]) #[124, 73] is ascii for '|I' which signifies that this message is an image
        return header.astype(np.uint8)

    def parse_message(self, path, ci=(0,1)): #ci stands for channel id aka which channel to raad binary from, if the message is an image
        ext = ntpath.splitext(path)[-1]
        if   ext == ".txt":         
            file_content = open(path, mode="rb").read()        
            message = np.asarray(struct.unpack("B" * len(file_content), file_content))
            header = self._compose_header("|T", message.size)
        elif ext in [".png", ".jpg", ".jpeg"]: 
            message = np.asarray(Image.open(path))[:,:, ci[0]:ci[1]]
            header = self._compose_header("|I", message.shape)
        else: raise TypeError("Unsupported file extension.")

        print(header)
        message = np.concatenate([header, message], axis=None)
        return message

    def convert_msg_to_binary(self, msg, n=8):
        """Convert a message (array of n-bit ints) into an array of binary data"""
        msg = np.repeat(msg, n)

        iterator = np.tile(np.arange(n), msg.size // n)
        mask = np.left_shift(1, iterator)

        bit = np.bitwise_and(msg, mask)
        binary = np.right_shift(bit, iterator)
        return binary.astype(np.dtype("u" + str(n//8)))

    def _inject_bits(self, x1, x2):
        x1 = np.bitwise_and(x1, 254)   
        return np.bitwise_or(x1, x2)

    def insert_binary(self, img, binary, ci=(0,1)):
        """Insert binary data into the least significant bit of a color channel value"""
        copy = np.copy(img)
        channel = copy[:,:, ci[0]:ci[1]] 
        binary = np.resize(binary, channel.shape) #if the binary array is not big enough, it will loop over

        output = self._inject_bits(channel, binary)
        copy[:,:, ci[0]:ci[1]] = output
        return copy   

#DECODING ----------------------------------------------------------------------------------------------

class Decoder:

    def _scrape_bits(self, x1):
        return np.bitwise_and(x1, 1) #return only the least significant bit

    def extract_binary(self, img, ci=(0,1)):
        """Extract binary data from the least significant bit of a color channel value"""
        channel = img[:,:, ci[0]:ci[1]]
        return self._scrape_bits(channel)

    def _parse_header(self, header): 
        header = header.astype(np.uint8)
        mtype = "".join([chr(i) for i in header[:2]])

        if mtype=="|T":   shape = struct.unpack("I", header[2:6])
        elif mtype=="|I": shape = struct.unpack("H" * 3, header[2:])
        else: raise ValueError("Incorrect header format or header missing.")
        return mtype, shape

    def convert_binary_to_arr(self, binary, n=8, all=False): #all stands for whether u want all (even repetitive) data from the image, or just the original size
        """Convert an array of binary data into a message"""
        groups = binary.size // n
        binary = np.resize(binary, (groups, n))

        iterator = np.tile(np.arange(n, dtype=np.dtype("u" + str(n//8))), (groups, 1))
        binary = np.left_shift(binary, iterator)

        binary = np.bitwise_or.reduce(binary, axis=1)

        header  = binary[:8]
        t, shape = self._parse_header(header)
        size = np.multiply.reduce(shape)

        message = binary[8:size+8]
        if not all and binary.size > size: return np.resize(message, shape)
        elif t == "|I": 
            rows = binary.size // shape[1] // shape[2] 
            return np.resize(message, (rows, shape[1], shape[2])), ".png"
        elif t == "|T": 
            wraps = binary.size // (size+8) + 1
            return np.resize(message, binary.size - wraps * 8), ".txt"

def write_file(msg, path, ext):  
    if ext == ".txt": open(path + ".txt", "wb").write(struct.pack("B" * msg.size, *msg.ravel()))
    elif ext in [".png", ".jpeg", ".jpg"]: 
        img = Image.fromarray(msg)
        img.save(path + "_output" + ".png", optimize=True, compress_level=9)
    else: raise TypeError("Unsupported file extension")

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=(0,1)):
    a = x[:,:, ci[0]:ci[1]]
    b = y[:,:, ci[0]:ci[1]]
    return (a - b) 


# TODO

# better OOP
# less overhead for using the headers
# support for exe files



