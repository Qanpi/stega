from cv2 import cv2
import numpy as np

import stega as st
import timeit as tt

#Prerequisites
text = open("messages/test.txt").read()
img = cv2.imread("images/img.png")

e_binary = st.encode_message(text)
e_result = st.put_binary(img, e_binary)

d_binary = st.get_binary(e_result)
d_result = st.decode_message(d_binary)

with open("output/decoded.txt", "w") as output_txt:
    output_txt.write(d_result)



