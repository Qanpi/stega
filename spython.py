from cv2 import cv2
import numpy as np

class LSB:
    def __init__(self, img):
        self.img = img

        self.bits = np.full(img.shape, 0)
        self.v_inject_bits = np.vectorize(self.inject_bits)

    def generate_bits(self, msg):
        for i, ch  in enumerate(msg):
            o = ord(ch)
            for j in range(8):
                index = i * j + j
                if index >= self.img.size:
                    break
                bit = (o & (1 << j)) >> j
                self.bits.itemset(index, bit)
        np.reshape(self.bits, self.img.shape)

    def inject_bits(self):
        output = (self.img & ~1) | self.bits
        return output.astype(np.uint8)




