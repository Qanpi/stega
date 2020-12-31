import numpy as np
from PIL import Image

import struct
import os.path
import ntpath

#ENCODING ----------------------------------------------------------------------------------------------
class Message:
    def __init__(self, data, t):
        self.data = data
        self.type = t

        if self.type: self.gen_header()
    
    @classmethod
    def fromtextfile(cls, path):
        """Open a text file and convert it to a numpy array of integer values"""
        text = open(path, mode="rb").read()        
        data = np.asarray(struct.unpack("B" * len(text), text))
        return cls(data, "|T")
    
    @classmethod
    def fromimagefile(cls, path, c1=0, c2=1):
        """Open an image file and convert certain channel of the image to a numpy array of integer values"""
        data = np.asarray(Image.open(path))[:,:,c1:c2]
        return cls(data, "|I")

    @classmethod
    def frombinary(cls, binary, n=8):
        return cls(binary, None)

    def gen_header(self):
        """Append a header to the message which will represent the type and size of the message (useful for decoding)"""
        #First two values represent the type of the message in ascii.
        #The following value(s) signigy the size of the message (text or image)
        if self.type == "|T": header = np.array([124, 84, *struct.pack("I", self.data.size), 0, 0]) 
        elif self.type == "|I": header = np.array([124, 73, *struct.pack("HHH", *self.data.shape)]) 

        self.data = np.concatenate([header.astype(np.uint8), self.data], axis=None)

    def parse_header(self, binary):
        header = binary[:8].astype(np.uint8)
        mtype = "".join([chr(i) for i in header[:2]])

        if mtype == "|T": shape = struct.unpack("I", header[2:6])
        elif mtype == "|I": shape = struct.unpack("H" * 3, header[2:])
        else: raise ValueError("Incorrect header format or header missing.")
        return mtype, shape

    def to_binary(self, n=8):
        """Convert the data array with integer values to binary data"""
        temp = np.repeat(self.data, 8) #repeated 8 times for use with the iterator

        #Binary operations to extract each bit from the data individually
        iterator = np.tile(np.arange(n), temp.size // n)
        mask = np.left_shift(1, iterator)
        bits = np.bitwise_and(temp, mask)
        binary = np.right_shift(bits, iterator)

        return binary.astype(np.dtype("u" + str(n//8)))

    def decode(self, n=8, all=False):
        """Convert an array of extracted binary data into the original message"""
        temp = np.resize(self.data, (-1, n))

        #Binary operations to reduce the array of binary to decimal values
        bitrange = np.arange(n, dtype=np.dtype("u" + str(n//8)))
        iterator = np.tile(bitrange, (temp.shape[0], 1))
        temp = np.left_shift(temp, iterator)
        temp = np.bitwise_or.reduce(temp, axis=1)

        #Parsing the header to determine the size and type of the message
        self.type, shape = self.parse_header(temp)
        size = np.multiply.reduce(shape)

        data = temp[8:size+8]

        #Logic for retrieving a certain size of the message (all or not)
        if not all and temp.size > size: self.data = np.resize(data, shape)
        elif self.type == "|I": 
            rows = temp.size // shape[1] // shape[2] 
            if shape[2] == 1: self.data = np.resize(data, (rows, shape[1])) #the Image library demands a strictly 2D array if there is only one channel
            else: self.data = np.resize(data, (rows, shape[1], shape[2]))
        elif self.type == "|T": 
            wraps = size // (size+8) + 1
            self.data = np.resize(data, size - wraps * 8)

    def save(self, path, name="message"):
        if self.type == "|T": 
            text = struct.pack("B" * self.data.size, *self.data.ravel())
            open(path + ".txt", "wb").write(text)
        elif self.type == "|I": 
            img = Image.fromarray(self.data)
            img.save(path + name + "_decoded" + ".png", optimize=True, compress_level=9)

class Host: 
    def __init__(self, img):
        self.image = img

    @classmethod
    def fromimagefile(cls, path):
        """Open an image from a certain path as a numpy array of integer values"""
        return cls(np.asarray(Image.open(path)))

    def inject_binary(self, binary, c1=0, c2=1):
        """Insert binary data into the least significant bits of certain image channels"""
        copy = np.copy(self.image)
        channels = copy[:,:, c1:c2] 

        binary = np.resize(binary, channels.shape) #if the binary array is not big enough, it will loop/wrap over

        #Binary operations to modify the lsbs of the image based on the binary data of the message
        channels = np.bitwise_and(channels, 254)
        output = np.bitwise_or(channels, binary)

        copy[:,:, c1:c2] = output
        self.image = copy

    def extract_binary(self, c1=0, c2=1):
        """Extract binary data from the least significant bits of certain image channels"""
        channels = self.image[:,:, c1:c2]
        return np.bitwise_and(channels, 1)

    def save(self, path, name="host"):
        """Save a this image to a certain path with minimum size"""
        img = Image.fromarray(self.image)
        img.save(path + name + "_encoded" + ".png", optimize=True, compress_level=9)

# TODO

# support for exe files



