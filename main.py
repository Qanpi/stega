from cv2 import cv2
import numpy as np

import spython

#Initialize prerequisites
text = open("test.txt").read() * 6480
img = cv2.imread("images/img.png", cv2.IMREAD_GRAYSCALE)

if __name__ == "__main__":
    lsb = spython.LSB(img)

    lsb.generate_bits(text)

    output = lsb.v_inject_bits()
    cv2.imshow("test", output)
    cv2.waitKey()
