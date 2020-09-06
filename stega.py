import numpy as np

#ENCODING ----------------------------------------------------------------------------------------------

def msg_to_binary(msg):
    """Converts a text message into an array of binary data"""
    binary = np.array([ord(ch) for ch in msg], dtype=np.uint8) #numpy array of arrays containing ord() of one character 8 times
    binary = np.repeat(binary, 8)

    iterator = np.tile(np.arange(8, dtype=np.uint8), binary.size // 8)
    mask = np.left_shift(1, iterator)

    bit = np.bitwise_and(binary, mask)
    output = np.right_shift(bit, iterator)
    return output

def inject_bits(x1, x2):
    x1 = np.bitwise_and(x1, 254)       
    return np.bitwise_or(x1, x2)

def insert_binary(img, binary, ci=0):
    """Inserts binary data into the least significant bit of a color channel value"""
    channel = img[:,:, ci] #ci stands for channel id aka which channel to insert binary into (first channel by default)
    
    binary = np.resize(binary, channel.shape) #if the binary array is not big enough, it will loop over

    output = inject_bits(channel, binary)
    img[:,:, ci] = output
    return img 
        

#DECODING ----------------------------------------------------------------------------------------------

def scrape_bits(x1):
    return np.bitwise_and(x1, 1) #return only the least significant bit

def extract_binary(img, ci=0):
    """Extracts binary data from the least significant bit of a color channel value"""
    channel = img[:,:, ci]
    return scrape_bits(channel)

def binary_to_msg(binary):
    """Converts an array of binary data into a text message"""
    groups = binary.size // 8
    binary = np.reshape(binary, (groups, 8))

    iterator = np.tile(np.arange(8, dtype=np.uint8), (groups, 1))

    binary = np.left_shift(binary, iterator)
    unic = np.bitwise_or.reduce(binary, axis=1)

    output = [chr(c) for c in unic]
    message = "".join(output)
    return message

#OTHER ----------------------------------------------------------------------------------------------

def difference(x, y, ci=0):
    x = x[:,:, ci]
    y = y[:,:, ci]
    return (x - y) * 255 #multiplied by 255 to exaggerate the difference





